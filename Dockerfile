FROM python:3.13-slim

# Flush stdout immediately — Docker pipes stdout, so Python would otherwise
# block-buffer it and workflow logs would appear in delayed bursts.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# CPU-only torch first — no GPU in the container, and the CPU wheel is ~250 MB
# vs ~2.5 GB for the CUDA build. Installed before the requirements so the main
# pip install skips torch entirely.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Install dependencies first (better layer caching)
COPY BA_Copilot_V3/requirements.txt BA_Copilot_V3/
COPY BA_MCP_Server/requirements.txt BA_MCP_Server/
RUN pip install --no-cache-dir \
    -r BA_Copilot_V3/requirements.txt \
    -r BA_MCP_Server/requirements.txt

# Copy only the folders the app needs at runtime
COPY BA_Copilot_V3 BA_Copilot_V3
COPY BA_MCP_Server BA_MCP_Server
COPY observability observability
COPY guardrails guardrails
COPY evaluation_v3 evaluation_v3

WORKDIR /app/BA_Copilot_V3

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]