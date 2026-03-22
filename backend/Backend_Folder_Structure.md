# File Tree: backend

**Root Path:** `legal-doc-analysis-project\backend`

```
├── 📁 app
│   ├── 📁 api
│   │   ├── 📁 endpoints
│   │   │   ├── 🐍 __init__.py
│   │   │   ├── 🐍 analysis.py
│   │   │   ├── 🐍 classify.py
│   │   │   ├── 🐍 graph.py
│   │   │   └── 🐍 upload.py
│   │   └── 🐍 api_router.py
│   ├── 📁 core
│   │   └── 🐍 __init__.py
│   ├── 📁 db
│   │   └── 🐍 __init__.py
│   ├── 📁 ml
│   │   ├── 📁 model
│   │   │   └── 📁 lawformer_final_model
│   │   │       ├── ⚙️ config.json
│   │   │       ├── 📄 model.safetensors
│   │   │       ├── ⚙️ tokenizer.json
│   │   │       ├── ⚙️ tokenizer_config.json
│   │   │       └── ⚙️ training_args.bin
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 lawformer_handler.py
│   │   └── 🐍 preprocessing.py
│   ├── 📁 schemas
│   │   ├── 🐍 __init__.py
│   │   └── 🐍 analysis_result.py
│   ├── 📁 services
│   │   ├── 🐍 __init__.py
│   │   ├── 🐍 classifier_service.py
│   │   ├── 🐍 clause_segmenter.py
│   │   ├── 🐍 domain_router.py
│   │   ├── 🐍 fsm_matcher.py
│   │   ├── 🐍 fuzzy_detector.py
│   │   ├── 🐍 network_service.py
│   │   ├── 🐍 ocr_service.py
│   │   └── 🐍 term_selector.py
│   ├── 🐍 __init__.py
│   └── 🐍 main.py
├── 📁 tests
│   └── 🐍 __init__.py
├── 📁 uploads_storage
│   ├── 📕 Contract_Law_Document.pdf
│   ├── 📕 Criminal_Law_Document.pdf
│   ├── 📕 Drillbit report.pdf
│   ├── 📕 Education_Law_Document.pdf
│   ├── 📕 Empty_Document.pdf
│   ├── 📕 Legal_NLP_Paper.pdf
│   └── 📕 Resonance_2026.pdf
├── ⚙️ .gitignore
├── 📝 backend_folder.md
├── 📄 requirements.dev.txt
└── 📄 requirements.txt
```
---