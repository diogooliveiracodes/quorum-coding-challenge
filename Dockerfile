FROM python:3.12-slim

WORKDIR /app

# stdlib only — no pip install needed
COPY src/ ./src/
COPY data/ ./data/

RUN mkdir -p /app/output

CMD ["python", "-m", "src.main"]
