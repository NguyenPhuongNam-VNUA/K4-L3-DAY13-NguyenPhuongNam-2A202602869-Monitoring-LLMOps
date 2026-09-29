import os
from dotenv import load_dotenv
from langfuse import get_client
import httpx

load_dotenv()

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    client = get_client()

    print("\n=== Step 1: Verify prompt v1 (baseline) and v2 (candidate) ===")
    p_baseline = client.get_prompt("day13-chat", label="baseline", cache_ttl_seconds=0)
    print(f"Prompt with label 'baseline': Version {p_baseline.version}, text: {repr(p_baseline.prompt[:40])}...")
    
    p_candidate = client.get_prompt("day13-chat", label="candidate", cache_ttl_seconds=0)
    print(f"Prompt with label 'candidate': Version {p_candidate.version}, text: {repr(p_candidate.prompt[:40])}...")

    p_prod = client.get_prompt("day13-chat", label="production", cache_ttl_seconds=0)
    print(f"Prompt with label 'production': Version {p_prod.version}")

    print("\n=== Step 2: Send request with current production (v1) ===")
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as http_client:
        r1 = http_client.post(
            "/chat",
            json={
                "user_id": "student-01",
                "session_id": "session-v1",
                "feature": "qa",
                "message": "Testing prompt version 1",
            },
        )
        print("Response v1 status:", r1.status_code, "CID:", r1.headers.get("x-request-id"))

    print("\n=== Step 3: Promote production to Version 2 ===")
    client.update_prompt(
        name="day13-chat",
        version=2,
        new_labels=["production"],
    )
    p_prod_v2 = client.get_prompt("day13-chat", label="production", cache_ttl_seconds=0)
    print(f"Prompt with label 'production' after promotion: Version {p_prod_v2.version}")

    with httpx.Client(base_url=BASE_URL, timeout=30.0) as http_client:
        r2 = http_client.post(
            "/chat",
            json={
                "user_id": "student-01",
                "session_id": "session-v2-promoted",
                "feature": "qa",
                "message": "Testing prompt version 2 promoted",
            },
        )
        print("Response v2 status:", r2.status_code, "CID:", r2.headers.get("x-request-id"))

    print("\n=== Step 4: Rollback production to Version 1 ===")
    client.update_prompt(
        name="day13-chat",
        version=1,
        new_labels=["production"],
    )
    p_prod_rollback = client.get_prompt("day13-chat", label="production", cache_ttl_seconds=0)
    print(f"Prompt with label 'production' after rollback: Version {p_prod_rollback.version}")

    with httpx.Client(base_url=BASE_URL, timeout=30.0) as http_client:
        r3 = http_client.post(
            "/chat",
            json={
                "user_id": "student-01",
                "session_id": "session-v1-rollback",
                "feature": "qa",
                "message": "Testing prompt rollback to version 1",
            },
        )
        print("Response rollback status:", r3.status_code, "CID:", r3.headers.get("x-request-id"))

    print("\nPrompt flow completed successfully!")

if __name__ == "__main__":
    test_flow()
