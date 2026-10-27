# Build context is the repo root: docker build -f services/api/Dockerfile .
FROM python:3.12-slim
RUN pip install --no-cache-dir uv
WORKDIR /app
COPY services/api ./services/api
COPY fixtures ./fixtures
COPY runs ./runs
RUN cd services/api && uv sync --no-dev --frozen
ENV PATH="/app/services/api/.venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn", "searchlab.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
