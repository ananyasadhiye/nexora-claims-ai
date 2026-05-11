# NEXORA · Claims Intelligence AI
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2e37d6c9-e4c2-4925-8bf6-aac99ec92e29" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1415f4f6-b4b4-4a28-842e-0127441b99ff" />


Ultra-premium cyberpunk Streamlit dashboard for AI-powered insurance claims processing.

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Structure

```
jarvis-claims/
├── app.py              # Main Streamlit app (JARVIS dashboard)
├── jarvis_theme.py     # Full JARVIS CSS theme & animations
├── extractor.py        # AI field extraction (OpenRouter / GPT-4o-mini)
├── validator.py        # Policy validation & inconsistency detection
├── router.py           # Claim routing rules engine
├── explainer.py        # Human-readable reasoning generator
├── db.py               # SQLite claims database
├── ai_chat.py          # AI chat interface
├── agents.py           # Multi-agent orchestration (Gemini)
├── gpt_agent.py        # GPT fraud investigation agent
├── voice_agent.py      # Voice recognition agent
├── claims.db           # SQLite database
├── requirements.txt
└── sample_docs/
    └── sample1.txt     # Sample FNOL document
```

## Pages

- **Dashboard** — Hero KPIs, FNOL intake, decision output, throughput chart, live pipeline
- **Claims** — Full FNOL processing with AI extraction & routing
- **Fraud Radar** — Hotspot map, risk distribution, radar charts
- **Pipeline** — Searchable/filterable claims table
- **AI Console** — Direct chat with the claims AI agent
- **Settings** — Model config, thresholds, system preferences

## Secrets (.streamlit/secrets.toml)

```toml
OPENROUTER_API_KEY = "your-key-here"
GEMINI_API_KEY     = "your-gemini-key-here"
```
