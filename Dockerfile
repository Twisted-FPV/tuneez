FROM python:3.12-slim
WORKDIR /app
COPY app/backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app/app
WORKDIR /app/app/backend
ENV PYTHONPATH=/app/app/backend
EXPOSE 8000
CMD ["uvicorn","tuneez.api.main:app","--host","0.0.0.0","--port","8000"]
