Codigo inicio CloudFlared: \n


  cloudflared tunnel --protocol http2 --url http://localhost:8000 \n

  
Codigo inicio FastApi: \n


  uvicorn IA:app --host 0.0.0.0 --port 8000 --reload
