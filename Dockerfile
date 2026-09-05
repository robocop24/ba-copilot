FROM python:3.13-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY BA_Copilot_V3/requirements.txt BA_Copilot_V3/
COPY BA_MCP_Server/requirements.txt BA_MCP_Server/
RUN pip install --no-cache-dir \
    -r BA_Copilot_V3/requirements.txt \
    -r BA_MCP_Server/requirements.txt

# langchain is imported by analyzer_agent/estimation_agent (create_agent) but
# not yet declared in requirements.txt. Kept as a separate step so the heavy
# torch install above stays cached.
RUN pip install --no-cache-dir langchain==1.3.14

# Copy only the folders the app needs at runtime
COPY BA_Copilot_V3 BA_Copilot_V3
COPY BA_MCP_Server BA_MCP_Server
COPY observability observability
COPY guardrails guardrails
COPY evaluation_v3 evaluation_v3

WORKDIR /app/BA_Copilot_V3

CMD ["python", "main.py"]
