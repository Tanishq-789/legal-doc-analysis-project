# File Tree: legal-doc-analysis-project

**Root Path:** `legal-doc-analysis-project`

```
├── 📁 Sample files
│   ├── 📕 Contract_Law_Document.pdf
│   ├── 📕 Criminal_Law_Document.pdf
│   ├── 📕 Education_Law_Document.pdf
│   └── 📕 Empty_Document.pdf
├── 📁 backend
│   ├── 📁 app
│   │   ├── 📁 api
│   │   │   ├── 📁 endpoints
│   │   │   │   ├── 🐍 __init__.py
│   │   │   │   ├── 🐍 analysis.py
│   │   │   │   ├── 🐍 classify.py
│   │   │   │   ├── 🐍 graph.py
│   │   │   │   └── 🐍 upload.py
│   │   │   └── 🐍 api_router.py
│   │   ├── 📁 core
│   │   │   └── 🐍 __init__.py
│   │   ├── 📁 db
│   │   │   └── 🐍 __init__.py
│   │   ├── 📁 ml
│   │   │   ├── 📁 model
│   │   │   │   └── 📁 lawformer_final_model
│   │   │   │       ├── ⚙️ config.json
│   │   │   │       ├── 📄 model.safetensors
│   │   │   │       ├── ⚙️ tokenizer.json
│   │   │   │       ├── ⚙️ tokenizer_config.json
│   │   │   │       └── ⚙️ training_args.bin
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 lawformer_handler.py
│   │   │   └── 🐍 preprocessing.py
│   │   ├── 📁 schemas
│   │   │   ├── 🐍 __init__.py
│   │   │   └── 🐍 analysis_result.py
│   │   ├── 📁 services
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 classifier_service.py
│   │   │   ├── 🐍 clause_segmenter.py
│   │   │   ├── 🐍 domain_router.py
│   │   │   ├── 🐍 fsm_matcher.py
│   │   │   ├── 🐍 fuzzy_detector.py
│   │   │   ├── 🐍 network_service.py
│   │   │   ├── 🐍 ocr_service.py
│   │   │   └── 🐍 term_selector.py
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 main.py
│   ├── 📁 tests
│   │   └── 🐍 __init__.py
│   ├── 📁 uploads_storage  
│   ├── ⚙️ .gitignore
│   ├── 📝 Backend_Folder_Structure.md
│   ├── 📄 requirements.dev.txt
│   └── 📄 requirements.txt
├── 📁 frontend
│   ├── 📁 public
│   │   └── 🖼️ vite.svg
│   ├── 📁 src
│   │   ├── 📁 api
│   │   │   ├── 📄 client.js
│   │   │   └── 📄 documentApi.js
│   │   ├── 📁 assets
│   │   ├── 📁 components
│   │   │   └── 📄 FileUploadDemo.jsx
│   │   ├── 📁 features
│   │   │   ├── 📁 dashboard
│   │   │   ├── 📁 risk-analysis
│   │   │   │   ├── 📄 RiskHighlighter.jsx
│   │   │   │   └── 📄 RiskView.jsx
│   │   │   ├── 📁 structural-map
│   │   │   │   └── 📄 LegalGraphView.jsx
│   │   │   ├── 📁 upload
│   │   │   │   └── 📄 DocumentUpload.jsx
│   │   │   ├── 📁 visualization
│   │   │   │   ├── 📄 ProceduralFlowView.jsx
│   │   │   │   └── 📄 WordCloudView.jsx
│   │   │   └── 📁 visualizations
│   │   ├── 📁 hooks
│   │   ├── 📁 store
│   │   │   └── 📄 useDocStore.js
│   │   ├── 📁 theme
│   │   ├── 📁 utils
│   │   │   ├── 📄 flowTransformer.jsx
│   │   │   └── 📄 graphTransformer.js
│   │   ├── 🎨 App.css
│   │   ├── 📄 App.jsx
│   │   ├── 🎨 index.css
│   │   └── 📄 main.jsx
│   ├── ⚙️ .gitignore
│   ├── ⚙️ .npmrc
│   ├── 📝 Frontend_Folder_Structure.md
│   ├── 📝 README.md
│   ├── 📄 eslint.config.js
│   ├── 🌐 index.html
│   ├── ⚙️ package-dev.json
│   ├── ⚙️ package-lock.json
│   ├── ⚙️ package.json
│   └── 📄 vite.config.js
├── ⚙️ .gitattributes
├── ⚙️ .gitignore
├── ⚙️ Criminal_law_clauses.json
├── 📄 LICENSE
└── 📝 README.md
```
---