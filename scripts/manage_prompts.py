import os
from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()

def main():
    client = get_client()
    print("Connecting to Langfuse at:", os.getenv("LANGFUSE_BASE_URL"))
    
    # Prompt contract:
    # Feature={{feature}}
    # Docs={{docs}}
    # Question={{message}}
    
    prompt_v1_text = "Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}"
    prompt_v2_text = "Feature={{feature}}\nDocs={{docs}}\nQuestion={{message}}\nPlease provide a concise and accurate response."
    
    print("\n--- 1. Creating Prompt v1 (labels: ['baseline', 'production']) ---")
    p1 = client.create_prompt(
        name="day13-chat",
        type="text",
        prompt=prompt_v1_text,
        labels=["baseline", "production"],
        config={"temperature": 0.7, "model": "claude-sonnet-4-5"}
    )
    print(f"Created Prompt v1: name={p1.name}, version={p1.version}, labels={p1.labels}")

    print("\n--- 2. Creating Prompt v2 (labels: ['candidate']) ---")
    p2 = client.create_prompt(
        name="day13-chat",
        type="text",
        prompt=prompt_v2_text,
        labels=["candidate"],
        config={"temperature": 0.7, "model": "claude-sonnet-4-5"}
    )
    print(f"Created Prompt v2: name={p2.name}, version={p2.version}, labels={p2.labels}")

    print("\nPrompts initialized successfully!")

if __name__ == "__main__":
    main()
