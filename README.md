Codigo inicio CloudFlared: 
  cloudflared tunnel --protocol http2 --url http://localhost:8000
Codigo inicio FastApi:
  uvicorn IA:app --host 0.0.0.0 --port 8000 --reload
