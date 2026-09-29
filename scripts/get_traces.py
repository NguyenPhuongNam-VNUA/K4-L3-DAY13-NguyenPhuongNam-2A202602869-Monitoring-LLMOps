import os
from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

def main():
    client = get_client()
    traces = client.fetch_traces(limit=20)
    print(f"Fetched {len(traces.data)} traces from Langfuse:")
    for t in traces.data:
        cid = t.metadata.get("correlation_id", "N/A") if t.metadata else "N/A"
        prompt_ver = t.version or "N/A"
        print(f"Trace ID: {t.id} | CID: {cid} | Name: {t.name} | Version: {prompt_ver}")

if __name__ == "__main__":
    main()
