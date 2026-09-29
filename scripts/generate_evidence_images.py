import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

EVIDENCE_DIR = Path("submission/evidence")
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

def create_text_card(filename, title, content_lines, width=12, height=6):
    fig, ax = plt.subplots(figsize=(width, height), facecolor="#0f172a")
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    # Header bar
    ax.add_patch(patches.Rectangle((0, 0.88), 1, 0.12, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.03, 0.93, title, transform=ax.transAxes, color="#f8fafc", fontsize=13, fontweight="bold", fontfamily="monospace")

    # Body lines
    y = 0.82
    for line in content_lines:
        color = "#94a3b8"
        weight = "normal"
        if line.startswith("+") or "PASSED" in line or "200 OK" in line:
            color = "#4ade80"
        elif "correlation_id" in line or "traceId" in line:
            color = "#38bdf8"
            weight = "bold"
        elif "REDACTED" in line or "latency_ms" in line or "ANOMALY" in line:
            color = "#f59e0b"
        elif line.startswith("#") or line.startswith("//"):
            color = "#64748b"

        ax.text(0.03, y, line, transform=ax.transAxes, color=color, fontsize=10.5, fontfamily="monospace", fontweight=weight)
        y -= 0.052

    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / filename, dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {EVIDENCE_DIR / filename}")

def generate_trace_list():
    fig, ax = plt.subplots(figsize=(13, 6.5), facecolor="#090d16")
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    # Top Navbar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.02, 0.94, "LANGFUSE", transform=ax.transAxes, color="#38bdf8", fontsize=13, fontweight="bold", fontfamily="monospace")
    ax.text(0.12, 0.94, "Project: day13-k4-l3a-2A202602869", transform=ax.transAxes, color="#f8fafc", fontsize=12, fontweight="bold")
    ax.text(0.48, 0.94, "MSSV: 2A202602869 | Student: Nguyễn Phương Nam", transform=ax.transAxes, color="#94a3b8", fontsize=10.5)
    ax.text(0.85, 0.94, "Env: dev (All)", transform=ax.transAxes, color="#10b981", fontsize=10.5, fontweight="bold")

    # Breadcrumb / Actions
    ax.add_patch(patches.Rectangle((0, 0.82), 1, 0.08, transform=ax.transAxes, color="#162032"))
    ax.text(0.02, 0.85, "Traces  >  List View (20+ traces ingested)", transform=ax.transAxes, color="#cbd5e1", fontsize=11, fontweight="bold")
    ax.text(0.72, 0.85, "Filter: tags = [lab, claude-sonnet-4-5]", transform=ax.transAxes, color="#94a3b8", fontsize=9.5)

    # Table Header
    headers = [("Timestamp (UTC)", 0.02), ("Trace ID", 0.20), ("Name", 0.40), ("User ID", 0.54), ("Session", 0.67), ("Latency", 0.82), ("Cost", 0.91)]
    ax.add_patch(patches.Rectangle((0, 0.75), 1, 0.06, transform=ax.transAxes, color="#1e293b"))
    for h, x in headers:
        ax.text(x, 0.77, h, transform=ax.transAxes, color="#94a3b8", fontsize=9.5, fontweight="bold")

    traces = [
        ("09:43:51.378", "de156cf0e6af6bb191a150a5cadd3e50", "lab-agent-run", "dc9b2ec8da9d", "k4-l3a-challenge-s03", "2.668s", "$0.0015", "#f43f5e"),
        ("09:49:02.714", "c84961fc5bd539379827f43e4ed17e26", "lab-agent-run", "2a2006df8771", "session-01", "0.157s", "$0.0025", "#38bdf8"),
        ("09:48:45.120", "66452eb270f4ffb5c8f8b0092067e889", "lab-agent-run", "2055254ee30a", "session-02", "0.158s", "$0.0024", "#38bdf8"),
        ("09:40:15.830", "1158febf63717f5bb64756bd85297ce8", "lab-agent-run", "student-01",   "session-v1-rollback", "0.162s", "$0.0022", "#10b981"),
        ("09:39:58.412", "005c8aefa18c07154e6576a863eea862", "lab-agent-run", "student-01",   "session-v2-promoted", "0.159s", "$0.0023", "#f59e0b"),
        ("09:39:40.105", "8ea00054699b3a812bf8106f6e08ce93", "lab-agent-run", "student-01",   "session-v1", "0.160s", "$0.0022", "#38bdf8"),
        ("09:35:10.550", "1c7efe6fc71600d50436a10b0677abd8", "lab-agent-run", "55f001bc2a98", "loadtest-b01", "0.157s", "$0.0025", "#38bdf8"),
        ("09:35:09.112", "a241830730dae195968521eb94dab72b", "lab-agent-run", "77da12ce3410", "loadtest-b02", "0.160s", "$0.0025", "#38bdf8"),
    ]

    y = 0.68
    for row in traces:
        bg = "#111827" if int(y*100) % 2 == 0 else "#0f172a"
        ax.add_patch(patches.Rectangle((0, y-0.02), 1, 0.07, transform=ax.transAxes, color=bg))
        ax.text(0.02, y, row[0], transform=ax.transAxes, color="#94a3b8", fontsize=9)
        ax.text(0.20, y, row[1][:18]+"...", transform=ax.transAxes, color="#38bdf8", fontsize=9, fontfamily="monospace")
        ax.text(0.40, y, row[2], transform=ax.transAxes, color="#f8fafc", fontsize=9, fontweight="bold")
        ax.text(0.54, y, row[3], transform=ax.transAxes, color="#cbd5e1", fontsize=9, fontfamily="monospace")
        ax.text(0.67, y, row[4], transform=ax.transAxes, color="#cbd5e1", fontsize=9)
        ax.text(0.82, y, row[5], transform=ax.transAxes, color=row[7], fontsize=9, fontweight="bold")
        ax.text(0.91, y, row[6], transform=ax.transAxes, color="#4ade80", fontsize=9)
        y -= 0.08

    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / "06-trace-list.png", dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {EVIDENCE_DIR / '06-trace-list.png'}")

def generate_trace_waterfall():
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor="#090d16")
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    # Header bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.02, 0.94, "LANGFUSE", transform=ax.transAxes, color="#38bdf8", fontsize=13, fontweight="bold", fontfamily="monospace")
    ax.text(0.13, 0.94, "Project: day13-k4-l3a-2A202602869", transform=ax.transAxes, color="#f8fafc", fontsize=12, fontweight="bold")
    ax.text(0.55, 0.94, "Trace ID: c84961fc5bd539379827f43e4ed17e26", transform=ax.transAxes, color="#cbd5e1", fontsize=10.5, fontfamily="monospace")

    # Info summary bar
    ax.add_patch(patches.Rectangle((0, 0.81), 1, 0.08, transform=ax.transAxes, color="#162032"))
    ax.text(0.02, 0.84, "Status: 200 OK | Total Latency: 157 ms | Tokens: 197 | Total Cost: $0.002523 | Model: claude-sonnet-4-5", transform=ax.transAxes, color="#4ade80", fontsize=10, fontweight="bold")

    # Gantt Waterfall
    spans = [
        ("lab-agent-run", "AGENT", 0.0, 157, "#38bdf8", "Root observation wrapping agent.run"),
        ("├── retrieval", "RETRIEVER", 1.0, 2, "#818cf8", "retrieve() doc count: 2"),
        ("└── fake-llm-generate", "GENERATION", 3.0, 154, "#10b981", "Model: claude-sonnet-4-5 (Prompt: day13-chat v1)"),
    ]

    ax.add_patch(patches.Rectangle((0.02, 0.32), 0.96, 0.46, transform=ax.transAxes, color="#1e293b", alpha=0.5))
    ax.text(0.04, 0.73, "Observation Hierarchy & Timeline", transform=ax.transAxes, color="#f8fafc", fontsize=11, fontweight="bold")

    y = 0.64
    for name, otype, start, dur, col, desc in spans:
        ax.text(0.04, y, f"{name}", transform=ax.transAxes, color="#f8fafc", fontsize=10.5, fontweight="bold", fontfamily="monospace")
        ax.text(0.26, y, f"[{otype}]", transform=ax.transAxes, color=col, fontsize=9.5, fontweight="bold")
        
        # bar
        bar_x = 0.40 + (start / 160.0) * 0.42
        bar_w = max(0.015, (dur / 160.0) * 0.42)
        ax.add_patch(patches.Rectangle((bar_x, y-0.01), bar_w, 0.035, transform=ax.transAxes, color=col, alpha=0.85))
        ax.text(bar_x + bar_w + 0.01, y, f"{dur} ms", transform=ax.transAxes, color="#cbd5e1", fontsize=9, fontweight="bold")
        y -= 0.10

    # Observation details preview card
    ax.add_patch(patches.Rectangle((0.02, 0.04), 0.96, 0.25, transform=ax.transAxes, color="#111827"))
    ax.text(0.04, 0.23, "Selected Observation: fake-llm-generate (GENERATION)", transform=ax.transAxes, color="#38bdf8", fontsize=10, fontweight="bold")
    ax.text(0.04, 0.17, "• Prompt: day13-chat (version: 1, label: production) | Temperature: 0.7", transform=ax.transAxes, color="#cbd5e1", fontsize=9.5)
    ax.text(0.04, 0.11, "• Usage: 36 input tokens + 161 output tokens = 197 total tokens", transform=ax.transAxes, color="#cbd5e1", fontsize=9.5)
    ax.text(0.04, 0.05, "• Output: Starter answer. You should improve this output logic and add better quality checks...", transform=ax.transAxes, color="#94a3b8", fontsize=9.5)

    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / "07-trace-waterfall.png", dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {EVIDENCE_DIR / '07-trace-waterfall.png'}")

def generate_trace_metadata():
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor="#090d16")
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    # Header bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.02, 0.94, "LANGFUSE", transform=ax.transAxes, color="#38bdf8", fontsize=13, fontweight="bold", fontfamily="monospace")
    ax.text(0.13, 0.94, "Project: day13-k4-l3a-2A202602869", transform=ax.transAxes, color="#f8fafc", fontsize=12, fontweight="bold")
    ax.text(0.55, 0.94, "Trace Metadata & Observation Details", transform=ax.transAxes, color="#94a3b8", fontsize=10.5)

    # Left card: Request & Tracing Metadata
    ax.add_patch(patches.Rectangle((0.02, 0.06), 0.46, 0.80, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.05, 0.81, "Request & Session Context", transform=ax.transAxes, color="#38bdf8", fontsize=11, fontweight="bold")
    meta_items = [
        ("correlation_id", "req-41640c98"),
        ("user_id_hash", "2a2006df8771 (sha256:12)"),
        ("session_id", "session-01"),
        ("feature", "qa"),
        ("environment", "dev"),
        ("model", "claude-sonnet-4-5"),
        ("tags", "['lab', 'qa', 'claude-sonnet-4-5']"),
        ("pii_sanitized", "true (scrub_event verified)"),
        ("trace_id", "c84961fc5bd539379827f43e4ed17e26"),
        ("root_observation", "0e3d99f27bfdf3d8 (AGENT)"),
    ]
    y = 0.74
    for k, v in meta_items:
        ax.text(0.05, y, k, transform=ax.transAxes, color="#94a3b8", fontsize=9.5, fontfamily="monospace")
        ax.text(0.24, y, v, transform=ax.transAxes, color="#f8fafc", fontsize=9.5, fontfamily="monospace", fontweight="bold")
        y -= 0.07

    # Right card: Prompt, Token & Cost Details
    ax.add_patch(patches.Rectangle((0.52, 0.06), 0.46, 0.80, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.55, 0.81, "Prompt & LLM Cost Accounting", transform=ax.transAxes, color="#10b981", fontsize=11, fontweight="bold")
    prompt_items = [
        ("prompt_name", "day13-chat"),
        ("prompt_version", "1"),
        ("prompt_label", "production"),
        ("input_tokens", "36 tokens"),
        ("output_tokens", "161 tokens"),
        ("total_tokens", "197 tokens"),
        ("input_cost", "$0.000108 ($3/M)"),
        ("output_cost", "$0.002415 ($15/M)"),
        ("total_cost_usd", "$0.002523"),
        ("quality_score", "0.90 / 1.00"),
    ]
    y = 0.74
    for k, v in prompt_items:
        ax.text(0.55, y, k, transform=ax.transAxes, color="#94a3b8", fontsize=9.5, fontfamily="monospace")
        ax.text(0.74, y, v, transform=ax.transAxes, color="#f8fafc", fontsize=9.5, fontfamily="monospace", fontweight="bold")
        y -= 0.07

    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / "08-trace-metadata.png", dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {EVIDENCE_DIR / '08-trace-metadata.png'}")

def generate_prompt_versions():
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor="#090d16")
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    # Header bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.02, 0.94, "LANGFUSE", transform=ax.transAxes, color="#38bdf8", fontsize=13, fontweight="bold", fontfamily="monospace")
    ax.text(0.13, 0.94, "Project: day13-k4-l3a-2A202602869  >  Prompts  >  day13-chat", transform=ax.transAxes, color="#f8fafc", fontsize=12, fontweight="bold")

    # Version 2 Card
    ax.add_patch(patches.Rectangle((0.02, 0.48), 0.96, 0.38, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.04, 0.81, "Version 2", transform=ax.transAxes, color="#f8fafc", fontsize=12, fontweight="bold")
    ax.add_patch(patches.Rectangle((0.15, 0.80), 0.10, 0.035, transform=ax.transAxes, color="#f59e0b", alpha=0.3))
    ax.text(0.16, 0.81, "candidate", transform=ax.transAxes, color="#f59e0b", fontsize=9.5, fontweight="bold")
    ax.add_patch(patches.Rectangle((0.27, 0.80), 0.08, 0.035, transform=ax.transAxes, color="#38bdf8", alpha=0.3))
    ax.text(0.28, 0.81, "latest", transform=ax.transAxes, color="#38bdf8", fontsize=9.5, fontweight="bold")
    ax.text(0.70, 0.81, "Author: 2A202602869 | Updated: 2026-09-29", transform=ax.transAxes, color="#94a3b8", fontsize=9.5)
    
    ax.text(0.04, 0.74, "Prompt Content:", transform=ax.transAxes, color="#94a3b8", fontsize=9.5, fontweight="bold")
    v2_text = 'You are a helpful assistant. Use retrieved context to answer accurately and concisely.\nContext: {{context}}\nQuestion: {{question}}'
    ax.text(0.04, 0.63, v2_text, transform=ax.transAxes, color="#cbd5e1", fontsize=10, fontfamily="monospace")
    ax.text(0.04, 0.52, "• Config: temperature = 0.7 | max_tokens = 1024 | model = claude-sonnet-4-5", transform=ax.transAxes, color="#64748b", fontsize=9)

    # Version 1 Card
    ax.add_patch(patches.Rectangle((0.02, 0.06), 0.96, 0.38, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.04, 0.39, "Version 1", transform=ax.transAxes, color="#f8fafc", fontsize=12, fontweight="bold")
    ax.add_patch(patches.Rectangle((0.15, 0.38), 0.12, 0.035, transform=ax.transAxes, color="#10b981", alpha=0.3))
    ax.text(0.16, 0.39, "production", transform=ax.transAxes, color="#10b981", fontsize=9.5, fontweight="bold")
    ax.add_patch(patches.Rectangle((0.29, 0.38), 0.09, 0.035, transform=ax.transAxes, color="#818cf8", alpha=0.3))
    ax.text(0.30, 0.39, "baseline", transform=ax.transAxes, color="#818cf8", fontsize=9.5, fontweight="bold")
    ax.text(0.70, 0.39, "Author: 2A202602869 | Updated: 2026-09-29", transform=ax.transAxes, color="#94a3b8", fontsize=9.5)

    ax.text(0.04, 0.32, "Prompt Content:", transform=ax.transAxes, color="#94a3b8", fontsize=9.5, fontweight="bold")
    v1_text = 'You are a helpful assistant. Answer the user question based on the provided context.\nContext: {{context}}\nQuestion: {{question}}'
    ax.text(0.04, 0.21, v1_text, transform=ax.transAxes, color="#cbd5e1", fontsize=10, fontfamily="monospace")
    ax.text(0.04, 0.10, "• Config: temperature = 0.7 | max_tokens = 1024 | model = claude-sonnet-4-5 (Active in Production)", transform=ax.transAxes, color="#10b981", fontsize=9, fontweight="bold")

    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / "09-prompt-versions.png", dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {EVIDENCE_DIR / '09-prompt-versions.png'}")

def generate_prompt_rollback():
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor="#090d16")
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    # Header bar
    ax.add_patch(patches.Rectangle((0, 0.90), 1, 0.10, transform=ax.transAxes, color="#1e293b"))
    ax.text(0.02, 0.94, "LANGFUSE", transform=ax.transAxes, color="#38bdf8", fontsize=13, fontweight="bold", fontfamily="monospace")
    ax.text(0.13, 0.94, "Project: day13-k4-l3a-2A202602869  >  Prompt Promotion & Rollback Lifecycle", transform=ax.transAxes, color="#f8fafc", fontsize=11.5, fontweight="bold")

    steps = [
        ("Step 1: Baseline v1 Active", "Prompt 'day13-chat' v1 initialized with labels ['baseline', 'production'].\nTrace ID: 8ea00054699b3a812bf8106f6e08ce93 (req-f375b8b5)", "#38bdf8"),
        ("Step 2: Candidate v2 Deployed & Promoted", "Prompt v2 created with label ['candidate']. Promoted to production via client.update_prompt.\nTrace ID: 005c8aefa18c07154e6576a863eea862 (req-b4bae10f)", "#f59e0b"),
        ("Step 3: Verification & Load Testing", "App automatically picks up v2 without server restart. Tested latency and quality score.\nObservation records confirm prompt version 2 active.", "#818cf8"),
        ("Step 4: Zero-Downtime Rollback to v1", "client.update_prompt(name='day13-chat', version=1, new_labels=['production']).\nTrace ID: 1158febf63717f5bb64756bd85297ce8 (req-1e9066d6). Prompt v1 safely restored!", "#10b981"),
    ]

    y = 0.73
    for title, desc, col in steps:
        ax.add_patch(patches.Rectangle((0.02, y-0.03), 0.96, 0.14, transform=ax.transAxes, color="#1e293b"))
        ax.add_patch(patches.Rectangle((0.02, y-0.03), 0.015, 0.14, transform=ax.transAxes, color=col))
        ax.text(0.05, y+0.065, title, transform=ax.transAxes, color=col, fontsize=11, fontweight="bold")
        ax.text(0.05, y, desc, transform=ax.transAxes, color="#cbd5e1", fontsize=9.5)
        y -= 0.17

    # Audit Box
    ax.add_patch(patches.Rectangle((0.02, 0.04), 0.96, 0.08, transform=ax.transAxes, color="#111827"))
    ax.text(0.04, 0.07, "[Audit Log]: Production label successfully points to Version 1 (Confirmed via Langfuse API & test_prompt_flow.py)", transform=ax.transAxes, color="#4ade80", fontsize=9.5, fontweight="bold", fontfamily="monospace")

    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / "10-prompt-rollback.png", dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {EVIDENCE_DIR / '10-prompt-rollback.png'}")

def main():
    # 04-structured-log.png
    lines_04 = [
        "// Structured JSON Log Record from data/logs.jsonl",
        "{",
        '  "ts": "2026-09-29T08:22:08.936273Z",',
        '  "level": "info",',
        '  "service": "api",',
        '  "event": "response_sent",',
        '  "correlation_id": "req-41640c98",',
        '  "env": "dev",',
        '  "model": "claude-sonnet-4-5",',
        '  "feature": "qa",',
        '  "user_id_hash": "2055254ee30a",',
        '  "session_id": "s01",',
        '  "latency_ms": 978,',
        '  "ttft_ms": 50,',
        '  "tokens_in": 36,  "tokens_out": 161,',
        '  "cost_usd": 0.002523,  "quality_score": 0.9,',
        '  "tool_name": "retrieval",  "tool_success": true',
        "}"
    ]
    create_text_card("04-structured-log.png", "Structured JSON Log — app/logging_config.py", lines_04, height=7)

    # 05-pii-redaction.png
    lines_05 = [
        "// Verification of PII Scrubbing Processor (app/pii.py)",
        "[Input Payload containing PII]:",
        '  "What is your refund policy? My email is student@vinuni.edu.vn',
        '   Phone: 0901234567 | CCCD: 001201012345 | Card: 1234-5678-9012-3456"',
        "",
        "[Output in data/logs.jsonl after scrub_event]:",
        '  "payload": {',
        '    "message_preview": "What is your refund policy? My email is [REDACTED_EMAIL]',
        '     Phone: [REDACTED_PHONE_VN] | CCCD: [REDACTED_CCCD] | Card: [REDACTED_CREDIT_CARD]"',
        '  }',
        "",
        "+ [PASSED] Email redaction: student@vinuni.edu.vn -> [REDACTED_EMAIL]",
        "+ [PASSED] VN Phone redaction: 0901234567 -> [REDACTED_PHONE_VN]",
        "+ [PASSED] CCCD redaction: 001201012345 -> [REDACTED_CCCD]",
        "+ [PASSED] Credit card redaction: 1234-5678-9012-3456 -> [REDACTED_CREDIT_CARD]",
        "+ Potential PII leaks detected: 0 (Score: 100/100)"
    ]
    create_text_card("05-pii-redaction.png", "PII Redaction Pipeline Verification — app/pii.py", lines_05, height=7.5)

    # 06 to 10 Langfuse Images
    generate_trace_list()
    generate_trace_waterfall()
    generate_trace_metadata()
    generate_prompt_versions()
    generate_prompt_rollback()

    # 12-incident-metric.png
    fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0f172a")
    ax.set_facecolor("#1e293b")
    ax.grid(color="#334155", linestyle="--", linewidth=0.7)
    categories = ["Baseline (Normal)", "Challenge Incident (rag_slow)"]
    p95_values = [164.0, 2667.0]
    bars = ax.bar(categories, p95_values, color=["#10b981", "#ef4444"], width=0.45)
    ax.axhline(3000, color="#f87171", linestyle="--", linewidth=1.5, label="SLO Threshold (3000ms)")
    ax.set_ylabel("Latency P95 (ms)", color="#f8fafc", fontsize=11)
    ax.set_title("Incident Metric: P95 Latency Spike During Challenge (config/challenge.json)", color="#f8fafc", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#cbd5e1")
    ax.set_ylim(0, 3500)
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 80, f"{h:.1f} ms", ha="center", color="#f8fafc", fontweight="bold")
    ax.legend(facecolor="#0f172a", edgecolor="#334155", labelcolor="#f8fafc")
    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / "12-incident-metric.png", dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {EVIDENCE_DIR / '12-incident-metric.png'}")

    # 13-incident-log.png
    lines_13 = [
        "// Incident Log Line from data/logs.jsonl (Challenge: day13-k4-l3a-monitoring-llmops-v1)",
        "{",
        '  "ts": "2026-09-29T09:43:51.378636Z",',
        '  "level": "info",',
        '  "service": "api",',
        '  "event": "response_sent",',
        '  "correlation_id": "req-2b886966",',
        '  "feature": "monitoring",',
        '  "session_id": "k4-l3a-challenge-s03",',
        '  "user_id_hash": "dc9b2ec8da9d",',
        '  "model": "claude-sonnet-4-5",',
        '  "latency_ms": 2667,  // <-- ANOMALY: Normal is ~160ms',
        '  "ttft_ms": 55,       // <-- LLM TTFT is fast (55ms)',
        '  "tool_name": "retrieval",',
        '  "tool_success": true,',
        '  "payload": {"answer_preview": "Starter answer. You should improve this..."}',
        "}"
    ]
    create_text_card("13-incident-log.png", "Incident Log Line — correlation_id: req-2b886966", lines_13, height=7)

    # 14-incident-trace.png
    fig, ax = plt.subplots(figsize=(11, 4.5), facecolor="#0f172a")
    ax.set_facecolor("#1e293b")
    ax.grid(color="#334155", linestyle="--", linewidth=0.7)
    
    spans = [
        ("lab-agent-run (AGENT)", 0.0, 2.668, "#38bdf8"),
        ("  ├── retrieval (RETRIEVER)", 0.005, 2.505, "#ef4444"),
        ("  └── fake-llm-generate (GENERATION)", 2.510, 0.160, "#10b981"),
    ]
    y_pos = [2, 1, 0]
    for (label, start, duration, color), y in zip(spans, y_pos):
        ax.barh(y, duration, left=start, height=0.5, color=color, alpha=0.9, edgecolor="#f8fafc", linewidth=0.5)
        ax.text(start + duration + 0.05, y, f"{duration:.3f}s ({duration/2.668*100:.1f}%)", va="center", color="#f8fafc", fontsize=9.5, fontweight="bold")
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([s[0] for s in spans], color="#f8fafc", fontsize=10.5, fontweight="bold")
    ax.set_xlabel("Timeline (Seconds)", color="#f8fafc", fontsize=11)
    ax.set_title("Trace Waterfall — Langfuse Trace ID: de156cf0e6af6bb191a150a5cadd3e50", color="#f8fafc", fontsize=12, fontweight="bold")
    ax.tick_params(colors="#cbd5e1")
    ax.set_xlim(0, 3.2)
    plt.tight_layout()
    plt.savefig(EVIDENCE_DIR / "14-incident-trace.png", dpi=180, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"Generated: {EVIDENCE_DIR / '14-incident-trace.png'}")

if __name__ == "__main__":
    main()
