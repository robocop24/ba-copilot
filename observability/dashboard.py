import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
METRICS_DIR = BASE_DIR/"metrics"


def load_metrics(file_name):
    
    file_path = METRICS_DIR/file_name
    
    if not file_path.exists():
        return {}
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return {}
            return json.loads(content)
    except (json.JSONDecodeError, OSError):
        return {}
    
    
def main():
    
    v3_metrics = load_metrics("v3_metrics.json")
    
    mcp_metrics = load_metrics("mcp_metrics.json")
    
    print("\n=== BA COPILOT DASHBOARD ===\n")
    
    print("V3 Metrics")
    print("-"*30)
    
    for key, value in v3_metrics.items():
        print(f"{key}: {value}")
        
    print()
    
    print("MCP Metrics")
    print("-"*30)
        
    for key, value in mcp_metrics.items():
        print(f"{key}: {value}")
            

if __name__ == "__main__":
    main()