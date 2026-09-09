FROM python:3.13-slim

WORKDIR /app

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

CMD ["python", "main.py"]
