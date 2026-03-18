import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from endee import Endee
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from multiple possible locations
_this_dir = Path(__file__).resolve().parent
_project_dir = _this_dir.parent
load_dotenv(_this_dir / ".env")           # debugbot/api/.env
load_dotenv(_project_dir / ".env")        # debugbot/.env

app = FastAPI(title="DebugBot API", description="Semantic Search & RAG for Runtime Errors")

# CORS - allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models and clients on startup
print("Loading Embedding Model...")
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

print("Connecting to Endee Vector Database...")
endee_client = Endee()

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    llm_model = genai.GenerativeModel('gemini-2.0-flash')
    print(f"✅ Gemini configured (key: ...{GEMINI_API_KEY[-6:]})")
else:
    print("⚠️  WARNING: GEMINI_API_KEY not found.")
    llm_model = None


class SearchRequest(BaseModel):
    error_string: str
    language: str
    top_k: int = 5

class RAGRequest(BaseModel):
    error_string: str
    language: str
    retrieved_contexts: List[dict]


# ── Serve static frontend ──
_static_dir = _project_dir / "website"
if _static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

@app.get("/")
async def serve_landing():
    f = _static_dir / "index.html"
    if f.exists():
        return FileResponse(str(f))
    return {"message": "DebugBot API is running. Place website files in debugbot/website/"}

@app.get("/debug")
async def serve_debug():
    f = _static_dir / "debug.html"
    if f.exists():
        return FileResponse(str(f))
    return {"message": "Debug page not found."}

@app.get("/report")
async def serve_report():
    f = _static_dir / "report.html"
    if f.exists():
        return FileResponse(str(f))
    return {"message": "Report page not found."}


@app.post("/search")
async def semantic_search(request: SearchRequest):
    try:
        print(f"Embedding query: {request.error_string}")
        embedding = embed_model.encode([request.error_string])[0].tolist()
        index = endee_client.get_index("debugbot_errors")
        
        # Determine filter
        query_filter = None
        if request.language.lower() != 'all':
            lang_map = {"python": "Python", "java": "Java", "javascript": "JavaScript"}
            db_lang = lang_map.get(request.language.lower(), request.language)
            query_filter = [{"language": {"$eq": db_lang}}]
            print(f"Applying filter: {query_filter}")

        raw_results = index.query(
            vector=embedding, 
            top_k=request.top_k, 
            filter=query_filter
        )

        filtered_results = []
        for res in raw_results:
            meta = res.get('meta', {}) if isinstance(res, dict) else res.get('meta', {})
            filtered_results.append({
                "id": res.get('id', ''),
                "score": res.get('similarity', 0.0),
                "error": meta.get('error', ''),
                "solution": meta.get('solution', ''),
                "context": meta.get('context', ''),
                "language": meta.get('language', '')
            })

        return {"results": filtered_results}
    except Exception as e:
        print(f"Error in search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rag")
async def rag_explanation(request: RAGRequest):
    """Generate a structured JSON debug report using RAG."""
    context_str = ""
    references = []
    for i, ctx in enumerate(request.retrieved_contexts):
        context_str += f"\n--- Known Error {i+1} ---\n"
        context_str += f"Similar Error: {ctx.get('error')}\n"
        context_str += f"Context: {ctx.get('context')}\n"
        context_str += f"Solution: {ctx.get('solution')}\n"
        references.append({
            "error": ctx.get("error", ""),
            "solution": ctx.get("solution", ""),
            "language": ctx.get("language", ""),
            "score": ctx.get("score", 0)
        })

    # Build the structured report
    if llm_model:
        try:
            prompt = f"""You are a Senior Software Engineer debugging assistant.
The user encountered this {request.language} error:
USER ERROR: "{request.error_string}"

Similar known errors from our semantic database:
{context_str}

Return a valid JSON object (no markdown, no code fences) with EXACTLY these keys:
{{
  "error_title": "Short descriptive title of the error",
  "language": "{request.language}",
  "confidence_score": "HIGH or MEDIUM or LOW based on match quality",
  "root_cause": "Clear, concise explanation of why this error occurs (2-3 sentences)",
  "description": "Detailed explanation in simple terms (4-6 sentences). Explain what happens technically.",
  "solution": "Step-by-step fix instructions as a numbered list string",
  "example_code": "Realistic {request.language} buggy code that causes this error. Must be valid {request.language} syntax.",
  "fixed_code": "The corrected {request.language} code. Must be valid {request.language} syntax.",
  "visual_explanation": "A conceptual text explanation of what goes wrong. Use ASCII diagram style if possible. Example: for IndexError show array[0,1,2] and arrow pointing to index 5 which is out of bounds.",
  "prevention_tips": ["Tip 1", "Tip 2", "Tip 3"],
  "summary": "One-line summary of the fix",
  "highlighted_keywords": ["keyword1", "keyword2", "keyword3"],
  "reference_links": [
    {{"title": "Official Documentation Title", "url": "https://exact-real-url-to-docs"}},
    {{"title": "Stack Overflow Solution", "url": "https://stackoverflow.com/questions/relevant-id"}},
    {{"title": "Tutorial or Guide Title", "url": "https://real-tutorial-url"}}
  ]
}}

RULES FOR reference_links:
- Provide 2-4 REAL, EXISTING URLs that are relevant to this specific error
- For Python errors use docs.python.org, for Java use docs.oracle.com, for JS use developer.mozilla.org
- Include at least one Stack Overflow link if applicable
- URLs must be real and accurate

RULES FOR code:
- example_code and fixed_code must be valid {request.language} code
- Include comments explaining the key lines

IMPORTANT: Return ONLY the JSON object. No markdown. No code fences. No extra text."""

            response = llm_model.generate_content(prompt)
            raw = response.text.strip()
            # Clean up potential markdown code fences
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3].strip()
            if raw.startswith("json"):
                raw = raw[4:].strip()

            import json
            report = json.loads(raw)
            report["references"] = references
            report["language"] = request.language
            return {"report": report, "source": "gemini"}
        except Exception as e:
            print(f"Gemini error, falling back: {e}")

    # Fallback: build DETAILED report from retrieved contexts
    best = request.retrieved_contexts[0] if request.retrieved_contexts else {}
    lang = request.language.lower()
    error_str = request.error_string

    # Generate language-specific code samples
    code_samples = _generate_code_samples(error_str, lang, best)

    # Generate reference links based on language
    ref_links = _generate_reference_links(error_str, lang)

    # Extract keywords from error
    keywords = [w for w in error_str.replace(":", "").replace("'", "").split() if len(w) > 3][:5]

    # Build detailed descriptions
    context_info = best.get("context", "")
    solution_info = best.get("solution", "")

    root_cause = context_info if context_info else f"This error occurs when the program encounters an unexpected condition during execution. The '{error_str}' error is a common {lang} runtime error that indicates a logical flaw in the code."
    root_cause += f" This type of error typically arises from incorrect assumptions about data state, missing validation checks, or improper handling of edge cases in the application logic."

    description = f"The error '{error_str}' was analyzed using semantic search against our database of known error patterns. "
    description += f"We found {len(request.retrieved_contexts)} similar patterns that match your error signature. "
    if context_info:
        description += f"Based on our analysis: {context_info} "
    description += f"This is a {lang.title()} runtime error that developers frequently encounter. Understanding the root cause and applying the correct fix pattern is essential for maintaining robust, production-ready code. "
    description += "The error can manifest in different scenarios depending on the input data and execution flow of your application."

    solution_text = solution_info if solution_info else "Review your code logic and add proper error handling."
    solution_text += f"\n\nStep-by-step fix:\n1. Identify the exact line causing the error from the stack trace\n2. Add proper validation and boundary checks before the problematic operation\n3. Implement error handling using try-catch (or try-except in Python) blocks\n4. Test with edge cases including empty inputs, null values, and boundary conditions\n5. Add logging to capture the state when the error occurs for future debugging"

    visual = f"Error Flow Visualization:\n\n"
    visual += f"  [Your Code] --> [Operation: {error_str[:40]}]\n"
    visual += f"       |\n"
    visual += f"       v\n"
    visual += f"  [Runtime Check] --> FAIL --> [Exception Thrown]\n"
    visual += f"       |\n"
    visual += f"       v\n"
    visual += f"  [Apply Fix] --> [Validated Operation] --> SUCCESS\n\n"
    visual += f"  Matched {len(request.retrieved_contexts)} similar patterns in Endee vector database."

    fallback_report = {
        "error_title": error_str[:80],
        "language": request.language,
        "confidence_score": "MEDIUM",
        "root_cause": root_cause,
        "description": description,
        "solution": solution_text,
        "example_code": code_samples["wrong"],
        "fixed_code": code_samples["fixed"],
        "visual_explanation": visual,
        "prevention_tips": [
            "Always validate input data before processing — check for null, empty, and out-of-range values",
            "Implement comprehensive error handling with try-catch/except blocks around risky operations",
            "Write unit tests that cover edge cases, boundary conditions, and invalid inputs",
            "Use type annotations and static analysis tools to catch errors before runtime",
            "Add detailed logging to help diagnose issues quickly in production environments"
        ],
        "summary": solution_info[:120] if solution_info else f"Fix the {error_str[:50]} error by adding proper validation and error handling.",
        "highlighted_keywords": keywords,
        "reference_links": ref_links,
        "references": references
    }
    return {"report": fallback_report, "source": "fallback"}


def _generate_code_samples(error_str: str, lang: str, best: dict) -> dict:
    """Generate realistic language-specific code samples based on the error."""
    error_lower = error_str.lower()
    solution = best.get("solution", "")

    samples = {
        "python": {
            "wrong": '# Python code that causes the error\ndef process_data(items):\n    # BUG: No validation before accessing elements\n    result = items[10]  # May throw IndexError\n    value = data["key"]  # May throw KeyError\n    return result / 0  # May throw ZeroDivisionError\n\n# Calling with invalid data\nprocess_data([1, 2, 3])',
            "fixed": '# Fixed Python code with proper error handling\ndef process_data(items):\n    try:\n        # FIXED: Validate before accessing\n        if len(items) > 10:\n            result = items[10]\n        else:\n            result = items[-1] if items else None\n\n        value = data.get("key", "default_value")\n\n        # FIXED: Check divisor before division\n        divisor = get_divisor()\n        if divisor != 0:\n            return result / divisor\n        return None\n    except (IndexError, KeyError, TypeError) as e:\n        print(f"Error processing data: {e}")\n        return None\n\nprocess_data([1, 2, 3])'
        },
        "java": {
            "wrong": '// Java code that causes the error\npublic class DataProcessor {\n    public static void main(String[] args) {\n        // BUG: No null check before method call\n        String text = null;\n        int length = text.length(); // NullPointerException!\n\n        // BUG: Array index out of bounds\n        int[] arr = {1, 2, 3};\n        int val = arr[5]; // ArrayIndexOutOfBoundsException!\n    }\n}',
            "fixed": '// Fixed Java code with proper validation\npublic class DataProcessor {\n    public static void main(String[] args) {\n        try {\n            // FIXED: Null check before usage\n            String text = getData();\n            if (text != null) {\n                int length = text.length();\n                System.out.println("Length: " + length);\n            }\n\n            // FIXED: Bounds check before access\n            int[] arr = {1, 2, 3};\n            int index = 5;\n            if (index >= 0 && index < arr.length) {\n                int val = arr[index];\n            }\n        } catch (Exception e) {\n            System.err.println("Error: " + e.getMessage());\n        }\n    }\n}'
        },
        "javascript": {
            "wrong": '// JavaScript code that causes the error\nfunction processUser(data) {\n  // BUG: No null/undefined check\n  const name = data.user.name; // TypeError: Cannot read properties\n  const items = data.list;\n  const result = items.map(x => x * 2); // TypeError if undefined\n  return result;\n}\n\nprocessUser({}); // Crashes!',
            "fixed": '// Fixed JavaScript code with proper checks\nfunction processUser(data) {\n  try {\n    // FIXED: Optional chaining and nullish coalescing\n    const name = data?.user?.name ?? "Unknown";\n    const items = data?.list ?? [];\n\n    // FIXED: Validate before array operations\n    if (Array.isArray(items)) {\n      const result = items.map(x => x * 2);\n      return result;\n    }\n    return [];\n  } catch (error) {\n    console.error("Error processing user:", error.message);\n    return [];\n  }\n}\n\nprocessUser({}); // Returns [] safely'
        }
    }

    # Default to python-style if language not found
    if lang in samples:
        return {"wrong": samples[lang]["wrong"], "fixed": samples[lang]["fixed"]}

    # Database-specific samples
    db_samples = {
        "mysql": {
            "wrong": "-- MySQL query causing the error\nSELECT * FROM users WHERE id = 5;\n-- In a transaction that may deadlock:\nSTART TRANSACTION;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\n-- Another session updates in reverse order\nUPDATE accounts SET balance = balance + 100 WHERE id = 2;\n-- DEADLOCK: Both transactions wait for each other\nCOMMIT;",
            "fixed": "-- Fixed MySQL query with proper handling\n-- Use consistent lock ordering to prevent deadlocks\nSTART TRANSACTION;\n-- Always lock rows in the same order (by ID ascending)\nSELECT * FROM accounts WHERE id IN (1, 2) FOR UPDATE;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nUPDATE accounts SET balance = balance + 100 WHERE id = 2;\nCOMMIT;\n\n-- Or use retry logic in application:\n-- try { execute_transaction(); }\n-- catch (DeadlockException) { retry(); }"
        },
        "mongodb": {
            "wrong": "// MongoDB operation causing the error\ndb.users.insertOne({\n  _id: 'user123',\n  name: 'John',\n  email: 'john@example.com'\n});\n\n// ERROR: Duplicate key error\n// _id 'user123' already exists!\ndb.users.insertOne({\n  _id: 'user123',\n  name: 'Jane',\n  email: 'jane@example.com'\n});",
            "fixed": "// Fixed MongoDB operation\n// Option 1: Use updateOne with upsert\ndb.users.updateOne(\n  { _id: 'user123' },\n  {\n    $set: {\n      name: 'Jane',\n      email: 'jane@example.com'\n    }\n  },\n  { upsert: true }\n);\n\n// Option 2: Check existence first\nconst existing = db.users.findOne({ _id: 'user123' });\nif (!existing) {\n  db.users.insertOne({ _id: 'user123', name: 'Jane' });\n}"
        },
        "redis": {
            "wrong": "# Redis commands causing the error\n# Trying to connect to a server that's not running\nimport redis\n\nclient = redis.Redis(host='localhost', port=6379)\nclient.set('key', 'value')  # ConnectionRefusedError!\n\n# Wrong type operation\nclient.set('mykey', 'hello')\nclient.lpush('mykey', 'world')  # WRONGTYPE Error!",
            "fixed": "# Fixed Redis operations with proper handling\nimport redis\nfrom redis.exceptions import ConnectionError, ResponseError\n\ntry:\n    client = redis.Redis(\n        host='localhost',\n        port=6379,\n        socket_timeout=5,\n        retry_on_timeout=True\n    )\n    client.ping()  # Test connection first\n    \n    # Check type before operations\n    key_type = client.type('mykey')\n    if key_type == b'string':\n        client.set('mykey', 'hello')\n    elif key_type == b'list':\n        client.lpush('mykey', 'world')\nexcept ConnectionError:\n    print('Redis server not available')\nexcept ResponseError as e:\n    print(f'Redis error: {e}')"
        },
        "firebase": {
            "wrong": "// Firebase operation causing the error\nconst db = firebase.firestore();\n\n// ERROR: Permission denied\ndb.collection('admin_data').doc('secret').get()\n  .then(doc => console.log(doc.data()));\n\n// ERROR: Invalid path\ndb.doc('users//profile').set({ name: 'John' });",
            "fixed": "// Fixed Firebase operations\nconst db = firebase.firestore();\n\n// Check auth state before accessing restricted data\nfirebase.auth().onAuthStateChanged(user => {\n  if (user) {\n    // User is authenticated\n    db.collection('users').doc(user.uid).get()\n      .then(doc => {\n        if (doc.exists) {\n          console.log(doc.data());\n        }\n      })\n      .catch(err => console.error('Access error:', err));\n  }\n});\n\n// Validate paths before operations\nconst userId = 'user123';\nif (userId && userId.trim()) {\n  db.doc(`users/${userId}/profile`).set({ name: 'John' });\n}"
        },
        "cassandra": {
            "wrong": "-- Cassandra query causing the error\nINSERT INTO users (id, name, email)\nVALUES (uuid(), 'John', 'john@test.com');\n\n-- ERROR: Key already exists (lightweight transaction fail)\nINSERT INTO users (id, name, email)\nVALUES (existing-uuid, 'Jane', 'jane@test.com')\nIF NOT EXISTS;  -- Returns [applied]=false",
            "fixed": "-- Fixed Cassandra operations\n-- Use IF NOT EXISTS for safe inserts\nINSERT INTO users (id, name, email)\nVALUES (uuid(), 'Jane', 'jane@test.com')\nIF NOT EXISTS;\n\n-- Or use UPDATE for upsert behavior\nUPDATE users\nSET name = 'Jane', email = 'jane@test.com'\nWHERE id = existing-uuid;\n\n-- Set appropriate consistency level\n-- CONSISTENCY LOCAL_QUORUM;\n-- Retry with lower consistency if Unavailable"
        }
    }

    if lang in db_samples:
        return {"wrong": db_samples[lang]["wrong"], "fixed": db_samples[lang]["fixed"]}

    # Generic sample
    return {
        "wrong": f"// {lang.title()} - Code causing: {error_str}\n// Error occurs due to missing validation\n// See solution for the corrected version\n\n{solution if solution else '// Review error pattern and apply fix'}",
        "fixed": f"// {lang.title()} - Corrected code\n// Added proper validation and error handling\n// Always validate inputs before operations\n\n{solution if solution else '// Apply defensive coding practices'}"
    }


def _generate_reference_links(error_str: str, lang: str) -> list:
    """Generate relevant documentation links based on language and error type."""
    error_lower = error_str.lower()
    links = []

    if lang == "python":
        links.append({"title": "Python Official Documentation — Built-in Exceptions", "url": "https://docs.python.org/3/library/exceptions.html"})
        if "index" in error_lower:
            links.append({"title": "Python Lists — Indexing and Slicing", "url": "https://docs.python.org/3/tutorial/introduction.html#lists"})
        elif "key" in error_lower:
            links.append({"title": "Python Dictionaries — Accessing Values", "url": "https://docs.python.org/3/tutorial/datastructures.html#dictionaries"})
        elif "type" in error_lower:
            links.append({"title": "Python Type System — Common Type Errors", "url": "https://docs.python.org/3/library/stdtypes.html"})
        elif "attribute" in error_lower:
            links.append({"title": "Python Objects — Attribute Access", "url": "https://docs.python.org/3/reference/datamodel.html"})
        links.append({"title": "Real Python — Exception Handling Guide", "url": "https://realpython.com/python-exceptions/"})
    elif lang == "java":
        links.append({"title": "Oracle Java Docs — Exception Handling", "url": "https://docs.oracle.com/javase/tutorial/essential/exceptions/"})
        if "null" in error_lower:
            links.append({"title": "Understanding NullPointerException in Java", "url": "https://docs.oracle.com/javase/8/docs/api/java/lang/NullPointerException.html"})
        elif "array" in error_lower or "index" in error_lower:
            links.append({"title": "Java Arrays — Index Out of Bounds", "url": "https://docs.oracle.com/javase/8/docs/api/java/lang/ArrayIndexOutOfBoundsException.html"})
        links.append({"title": "Baeldung — Java Exception Handling Best Practices", "url": "https://www.baeldung.com/java-exceptions"})
    elif lang == "javascript":
        links.append({"title": "MDN Web Docs — JavaScript Errors Reference", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors"})
        if "type" in error_lower:
            links.append({"title": "MDN — TypeError Documentation", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypeError"})
        elif "reference" in error_lower:
            links.append({"title": "MDN — ReferenceError Documentation", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ReferenceError"})
        links.append({"title": "JavaScript.info — Error Handling Guide", "url": "https://javascript.info/error-handling"})
    elif lang == "mysql":
        links.append({"title": "MySQL Error Reference — Official Documentation", "url": "https://dev.mysql.com/doc/refman/8.0/en/error-handling.html"})
        if "deadlock" in error_lower:
            links.append({"title": "MySQL — How to Minimize and Handle Deadlocks", "url": "https://dev.mysql.com/doc/refman/8.0/en/innodb-deadlocks-handling.html"})
        elif "duplicate" in error_lower:
            links.append({"title": "MySQL — INSERT ON DUPLICATE KEY UPDATE", "url": "https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html"})
        elif "syntax" in error_lower:
            links.append({"title": "MySQL — SQL Statement Syntax", "url": "https://dev.mysql.com/doc/refman/8.0/en/sql-statements.html"})
        links.append({"title": "MySQL Troubleshooting Guide", "url": "https://dev.mysql.com/doc/refman/8.0/en/problems.html"})
    elif lang == "mongodb":
        links.append({"title": "MongoDB — Error Codes Reference", "url": "https://www.mongodb.com/docs/manual/reference/error-codes/"})
        if "duplicate" in error_lower:
            links.append({"title": "MongoDB — Unique Indexes", "url": "https://www.mongodb.com/docs/manual/core/index-unique/"})
        elif "timeout" in error_lower:
            links.append({"title": "MongoDB — Connection Troubleshooting", "url": "https://www.mongodb.com/docs/manual/reference/connection-string/"})
        links.append({"title": "MongoDB University — Troubleshooting Guide", "url": "https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/"})
    elif lang == "redis":
        links.append({"title": "Redis — Command Reference", "url": "https://redis.io/commands/"})
        if "connection" in error_lower:
            links.append({"title": "Redis — Troubleshooting Connections", "url": "https://redis.io/docs/management/troubleshooting/"})
        elif "type" in error_lower or "wrong" in error_lower:
            links.append({"title": "Redis — Data Types", "url": "https://redis.io/docs/data-types/"})
        links.append({"title": "Redis — Administration Guide", "url": "https://redis.io/docs/management/"})
    elif lang == "firebase":
        links.append({"title": "Firebase — Error Handling Guide", "url": "https://firebase.google.com/docs/reference/js/firestore_"})
        links.append({"title": "Firebase — Security Rules Guide", "url": "https://firebase.google.com/docs/firestore/security/get-started"})
        links.append({"title": "Firebase — Troubleshooting Common Issues", "url": "https://firebase.google.com/support/troubleshooter"})
    elif lang == "cassandra":
        links.append({"title": "Apache Cassandra — Documentation", "url": "https://cassandra.apache.org/doc/latest/"})
        links.append({"title": "DataStax — Cassandra Error Codes", "url": "https://docs.datastax.com/en/developer/java-driver/latest/manual/core/"})
        links.append({"title": "Cassandra — Consistency Levels Guide", "url": "https://cassandra.apache.org/doc/latest/cassandra/architecture/dynamo.html"})
    else:
        links.append({"title": f"{lang.title()} Error Handling — Stack Overflow", "url": f"https://stackoverflow.com/search?q={lang}+{error_str.replace(' ', '+')[:50]}"})

    links.append({"title": f"Stack Overflow — {error_str[:50]}", "url": f"https://stackoverflow.com/search?q={error_str.replace(' ', '+')[:60]}"})
    return links
