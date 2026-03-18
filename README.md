<div align="center">

  <img src="Results/background.png" width="100%" alt="ErrorLens AI Banner" style="border-radius:12px; margin-bottom: 20px;" />

  <h2>ErrorLens AI</h2>
  <p><b>Semantic Debugging Powered by Vector Search & Retrieval-Augmented Generation</b></p>
  <p>Intelligent Error Understanding | Instant Fix Generation | Developer Productivity</p>

  <p>
    <a href="https://github.com/ashokkumarboya93" target="_blank"><img src="https://img.shields.io/badge/Developer-Ashok_Kumar_Boya-333333?style=for-the-badge&logo=github" alt="Developer" /></a>
    <a href="https://drive.google.com/file/d/1LPUb81Rom5XfHx5-Pli8BuophFw1UkZb/view?usp=drive_link" target="_blank"><img src="https://img.shields.io/badge/Live_Demo-Active-6C5CE7?style=for-the-badge&logo=google-drive" alt="Live Demo" /></a>
    <img src="https://img.shields.io/badge/Vector_DB-Endee-00B894?style=for-the-badge" alt="Endee" />
    <img src="https://img.shields.io/badge/AI_Engine-Gemini-FDCB6E?style=for-the-badge" alt="Gemini" />
  </p>

</div>

---

### [ Developer Introduction ]

**Ashok Kumar Boya**  
*Full Stack Developer & AI Integration Engineer*  

I am dedicated to engineering intelligent, highly scalable AI systems that accurately bridge the gap between sophisticated machine learning models and highly interactive, performant user interfaces.

<p>
  <a href="https://github.com/ashokkumarboya93" target="_blank"><img src="https://img.shields.io/badge/Github-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="https://www.linkedin.com/in/ashok-kumar-boya" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://ashok-kumar-portfolio.onrender.com" target="_blank"><img src="https://img.shields.io/badge/Portfolio-059669?style=flat-square&logo=internet-explorer&logoColor=white" alt="Portfolio" /></a>
</p>

---

### [ Project Overview & Evaluation Criteria ]

This framework was designed strictly following the Endee evaluation parameters which requested candidates to:   
> *"Demonstrate a practical use case such as semantic search, RAG (Retrieval Augmented Generation), recommendations, agentic AI workflows, or similar AI applications"*

**ErrorLens AI directly fulfills this requirement by establishing a production-grade Semantic Search and RAG pipeline.** By migrating away from rigid keyword matching, this project utilizes high-dimensional semantic vector mathematics mapped natively inside the Endee Vector Database to parse, understand, and automatically resolve complex software anomalies instantly.

---

### [ Live Application & Video Walkthrough ]

Please proceed to the live demonstration video detailing the complete vector traversal process, UI generation, and LLM formatting.

**🔗 [Click Here to View the Live Video Demonstration (Google Drive)](https://drive.google.com/file/d/1LPUb81Rom5XfHx5-Pli8BuophFw1UkZb/view?usp=drive_link)**

<div align="center">
  <p><i>Alternatively, view the raw 1080p MP4 attached inside this repository below:</i></p>
  <video src="https://github.com/ashokkumarboya93/endee/raw/master/Results/ErrorLense_ai.mp4" controls="controls" width="85%" style="border-radius:12px;"></video>
  <br>
  <a href="https://github.com/ashokkumarboya93/endee/raw/master/Results/ErrorLense_ai.mp4">Download Raw MP4 directly</a>
</div>

---

### [ About Project Work & Core Concepts ]

The core foundation behind ErrorLens AI relies entirely on isolating factual data retrieval from Gen-AI generation.

**The Semantic Vector Concept**  
Traditional traceback mapping fails because an error throwing *"Property is missing"* and *"Object is Null"* share zero string similarities. By compressing debugging texts into 384-dimensional numerical arrays (Sentence Embedding), identical *meaning* is captured regardless of specific vocabulary.

**The Workflow execution**  
The dataset is pre-populated into Endee's HNSW infrastructure. Upon user query, a localized cosine-similarity search returns exact historical occurrences. This context acts as the undeniable "Truth", heavily restraining the Google Gemini LLM via RAG prompting to only construct fixes explicitly verified by historical parameters.

---

### [ System Architecture & Infrastructure ]

The design intentionally isolates computational vectors from the static visual interface. This architecture demonstrates high competency regarding micro-service decoupling—providing a comprehensively structured application that simplifies candidate evaluation by operating efficiently and predictably.

<div align="center">
  <img src="Results/S_A.png" width="85%" alt="Complete System Architecture Engine" style="border-radius:12px; margin-top:20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
</div>

---

### [ Debug Results Portfolio ]

<div align="center">
  <img src="Results/Res1.png" width="85%" style="margin-bottom:15px; border-radius:12px;" />
  <img src="Results/res4.png" width="85%" style="margin-bottom:15px; border-radius:12px;" />
  <img src="Results/res5.png" width="85%" style="margin-bottom:15px; border-radius:12px;" />
  <img src="Results/res6.png" width="85%" style="margin-bottom:15px; border-radius:12px;" />
  <img src="Results/res8.png" width="85%" style="margin-bottom:15px; border-radius:12px;" />
</div>

---

### [ Quick Setup & Reproducibility ]

To audit the repository implementation natively inside localized Docker and Python virtualization domains:

```bash
# 1. Clone the master repository branch
git clone https://github.com/ashokkumarboya93/endee.git
cd endee

# 2. Spin up the underlying Endee Database isolated Server
docker compose up -d

# 3. Formulate the local Python logic workspace
cd debugbot
python -m venv venv
pip install -r requirements.txt

# 4. Integrate your active LLM authentication token
# Add .env file exclusively inside debugbot/api/ (.env content: GEMINI_API_KEY=your_key)

# 5. Populate Endee mappings using the 700+ vectors
python -m ingest.loader

# 6. Boot the Application engine binding on localhost:8000
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

---

### [ Acknowledgement to Endee.io ]

This system was engineered exclusively for the Endee.io evaluation pipeline. Utilizing the Endee Vector Database provided the crucial foundation for the application's semantic execution speed. Its raw edge performance, transparent HNSW indexing formatting, and highly reliable SDK enabled an extraordinarily robust pipeline required for this RAG infrastructure. 

We sincerely thank the Endee engineering team for providing such an incredible vector infrastructure to the machine learning community, and for granting this opportunity to showcase high-level AI integrations.
