# LegalDoc AI: Intelligent Document Analysis Framework

An engineering-inspired NLP framework designed to classify, analyze, and visualize scope-limited legal documents. This project leverages **Lawformer** (Legal-BERT) for semantic understanding and **Graph Theory** for information density optimization.



## 🚀 Key Engineering Pillars

### 1. Vector Space Model (VSM) Classifier
Documents are numerically represented in a high-dimensional space. The system calculates the **Cosine Proximity** between the document vector and domain centroids (Criminal, Contract, Education) to perform automated classification.

### 2. Graph Centrality Word Clouds
Unlike standard frequency-based clouds, our system builds a **Co-occurrence Graph** of legal terms. **Degree Centrality** is used to identify semantically "influential" terms, which are then passed to our visualization engine.

### 3. Greedy Knapsack Selection
To manage "Information Density," the system treats terms as items in a Knapsack problem. It selects the most "valuable" terms (highest centrality) that fit within a limited visual "budget," preventing UI clutter.

## 🛠️ Tech Stack
- **Backend:** FastAPI (Python), PyMuPDF, NetworkX, PyTorch, Lawformer (Transformers)
- **Frontend:** React 19, Vite, Material UI, Zustand, React-TagCloud

## ⚙️ Local Setup

### Backend
1. `cd backend`
2. `python -m venv venv`
3. `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install --legacy-peer-deps`
3. `npm run dev`

## 📊 Methodology Reference
This implementation follows the research methodology outlined in:
*Tanishq Shinde, Mansi Jangle, Nilakshi Sonawane, Vaishnavi Madavi, Sarang Joshi  et al. "Intelligent Legal Document Analysis using NLP," Pune Institute of Computer Technology.*