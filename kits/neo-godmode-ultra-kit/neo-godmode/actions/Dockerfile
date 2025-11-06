FROM python:3.11-slim
WORKDIR /app
COPY actions/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY actions /app/actions
ENV PYTHONUNBUFFERED=1
ENV NEO_DB_PATH=/data/neo_store.sqlite3
VOLUME ["/data", "/deliverables"]
CMD ["uvicorn", "actions.app:app", "--host", "0.0.0.0", "--port", "8080"]