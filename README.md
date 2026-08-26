# RIVA
**RTL Verification and Intelligent Verification Assistant**

## Architecture Overview

```text
RIVA
│
├── Backend
│   └── RTL verification engine + API
│
├── Frontend
│   └── RIVA user interface
│
└── Docs
    └── Architecture and API documentation
```

### What is RIVA?
RIVA is a deterministic verification platform with grounded AI reasoning, designed to verify SystemVerilog RTL against natural-language specifications and waveform traces.

### Why it exists?
To bridge the gap between deterministic formal/simulation verification and AI-assisted debugging without risking AI hallucinations.

### What the backend does?
The Python-based backend acts as a frozen service. It parses RTL, runs static and semantic analysis (width inference, signedness), extracts specifications, traces requirements, parses VCD testbenches, logs deterministic diagnostic evidence, queries AI based *only* on that evidence, and serves this data via a FastAPI REST endpoint.

### What the frontend does?
The React-based frontend provides a professional, futuristic workstation UI. It manages editors for RTL, specifications, and testbenches, and presents detailed diagnostic, traceability, and AI results via multiple dock tabs.

### How to Run

#### Backend (FastAPI Service)
```bash
cd ~/RIVA/backend
source ~/RIVA/.venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend (React / Vite)
```bash
cd ~/RIVA/frontend
npm run dev
```

### How They Communicate
Strictly via the REST API (`POST /api/analyze`), maintaining a clean separation of concerns.

### Manual Acceptance Testing
The repository includes a manual real-code acceptance test script for end-to-end backend verification:
```bash
cd ~/RIVA/backend
source ~/RIVA/.venv/bin/activate
PYTHONPATH=. python real_riva_acceptance.py
```
This script runs 47 real SystemVerilog acceptance checks against the FastAPI engine and is intentionally excluded from automatic pytest collection (renamed from `*_test.py` to prevent `SystemExit` interference during automated unit test runs).
