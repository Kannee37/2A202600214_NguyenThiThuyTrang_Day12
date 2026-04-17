# TravelBuddy

TravelBuddy là trợ lý du lịch dùng LangGraph + Gemini, hỗ trợ:
- Tìm chuyến bay
- Tìm khách sạn
- Tính ngân sách
- Guardrails cơ bản: auth, rate limit, cost guard

## 1. Cấu trúc project

```text
your-repo/
├── app/
├── utils/
├── tools.py
├── ui.py
├── system_prompt.txt
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .dockerignore
├── .gitignore
├── railway.toml
└── README.md