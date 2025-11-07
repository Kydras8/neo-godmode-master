FROM python:3.11-slim
WORKDIR /app
COPY jwks/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY jwks /app/jwks
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn","jwks.app:app","--host","0.0.0.0","--port","8081"]