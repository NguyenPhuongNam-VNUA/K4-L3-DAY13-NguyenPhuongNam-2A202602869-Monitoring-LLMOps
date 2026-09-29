import json
from pathlib import Path
from datetime import datetime, timezone
import matplotlib.pyplot as plt
import numpy as np

LOG_PATH = Path("data/logs.jsonl")
EVIDENCE_PATH = Path("submission/evidence/11-dashboard-overview.png")

def main():
    if not LOG_PATH.exists():
        print(f"Error: {LOG_PATH} not found.")
        return

    records = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    response_events = [r for r in records if r.get("event") == "response_sent"]
    request_events = [r for r in records if r.get("event") == "request_received"]
    failed_events = [r for r in records if r.get("event") == "request_failed"]

    # 1. Latency & TTFT
    latencies = [r.get("latency_ms", 0) for r in response_events if "latency_ms" in r]
    ttfts = [r.get("ttft_ms", 0) for r in response_events if "ttft_ms" in r]
    
    p50 = float(np.percentile(latencies, 50)) if latencies else 0.0
    p95 = float(np.percentile(latencies, 95)) if latencies else 0.0
    p99 = float(np.percentile(latencies, 99)) if latencies else 0.0
    ttft_p95 = float(np.percentile(ttfts, 95)) if ttfts else 0.0

    # 2. Traffic
    total_requests = len(request_events)

    # 3. Errors & Retrieval
    total_received = len(request_events)
    total_failed = len(failed_events)
    error_rate_pct = (total_failed / total_received * 100) if total_received else 0.0
    
    retrieval_responses = [r for r in response_events if r.get("tool_name") == "retrieval"]
    retrieval_successes = [r for r in retrieval_responses if r.get("tool_success") is True]
    retrieval_success_pct = (len(retrieval_successes) / len(retrieval_responses) * 100) if retrieval_responses else 100.0

    # 4. Cost
    costs = [r.get("cost_usd", 0.0) for r in response_events]
    total_cost = sum(costs)

    # 5. Tokens
    tokens_in = sum(r.get("tokens_in", 0) for r in response_events)
    tokens_out = sum(r.get("tokens_out", 0) for r in response_events)
    total_tokens = tokens_in + tokens_out

    # 6. Quality
    qualities = [r.get("quality_score", 0.0) for r in response_events if "quality_score" in r]
    avg_quality = float(np.mean(qualities)) if qualities else 0.0

    print("--- Calculated Dashboard Metrics (Last 60 mins) ---")
    print(f"Latency P50: {p50:.1f}ms | P95: {p95:.1f}ms | P99: {p99:.1f}ms | TTFT P95: {ttft_p95:.1f}ms (SLO <= 3000ms)")
    print(f"Traffic: {total_requests} requests")
    print(f"Error Rate: {error_rate_pct:.1f}% (SLO <= 2%) | Retrieval Success: {retrieval_success_pct:.1f}% (SLO >= 90%)")
    print(f"Total Cost: ${total_cost:.4f} USD (SLO <= $2.5)")
    print(f"Tokens In: {tokens_in} | Tokens Out: {tokens_out} | Total: {total_tokens} (SLO <= 50000)")
    print(f"Avg Quality Score: {avg_quality:.2f} (SLO >= 0.75)")

    # Plotting 6-Panel Dashboard
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle("K4-L3A Day 13 Monitoring & LLMOps — Runtime Dashboard (Last 60 Minutes)", fontsize=16, fontweight="bold")

    # Panel 1: Latency & TTFT
    ax1 = axes[0, 0]
    bars1 = ax1.bar(["P50", "P95", "P99", "TTFT P95"], [p50, p95, p99, ttft_p95], color=["#3b82f6", "#2563eb", "#1d4ed8", "#60a5fa"])
    ax1.axhline(3000, color="red", linestyle="--", linewidth=1.5, label="SLO Threshold (3000ms)")
    ax1.set_title("1. Latency percentiles and TTFT (ms)", fontweight="bold")
    ax1.set_ylabel("Latency (ms)")
    ax1.legend(loc="upper left")
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, yval + 10, f"{yval:.1f}", ha="center", va="bottom", fontsize=9)
    ax1.set_ylim(0, max(3500, p99 * 1.3))

    # Panel 2: Request Traffic
    ax2 = axes[0, 1]
    req_indices = list(range(1, len(response_events) + 1))
    ax2.plot(req_indices, req_indices, marker="o", color="#10b981", linewidth=2, label="Cumulative Requests")
    ax2.axhline(1, color="red", linestyle="--", linewidth=1.5, label="Min Traffic Threshold (1 req/m)")
    ax2.set_title("2. Request traffic (Total Requests)", fontweight="bold")
    ax2.set_xlabel("Request Sequence")
    ax2.set_ylabel("Count")
    ax2.legend(loc="upper left")

    # Panel 3: Error rate and retrieval success
    ax3 = axes[0, 2]
    bars3 = ax3.bar(["Error Rate (%)", "Retrieval Success (%)"], [error_rate_pct, retrieval_success_pct], color=["#ef4444", "#10b981"])
    ax3.axhline(2, color="red", linestyle="--", linewidth=1.5, label="Max Error Rate (2%)")
    ax3.axhline(90, color="orange", linestyle=":", linewidth=1.5, label="Min Retrieval Target (90%)")
    ax3.set_title("3. Error rate and retrieval success (%)", fontweight="bold")
    ax3.set_ylabel("Percent (%)")
    ax3.set_ylim(0, 115)
    ax3.legend(loc="upper right")
    for bar in bars3:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval:.1f}%", ha="center", va="bottom", fontsize=9)

    # Panel 4: Cost over time
    ax4 = axes[1, 0]
    cum_costs = np.cumsum(costs) if costs else [0]
    ax4.plot(range(1, len(cum_costs) + 1), cum_costs, color="#f59e0b", marker="s", linewidth=2, label="Cumulative Cost ($)")
    ax4.axhline(2.5, color="red", linestyle="--", linewidth=1.5, label="Daily Budget ($2.50)")
    ax4.set_title("4. Cost over time (USD)", fontweight="bold")
    ax4.set_xlabel("Request Sequence")
    ax4.set_ylabel("Cost ($)")
    ax4.set_ylim(0, 3.0)
    ax4.legend(loc="upper left")

    # Panel 5: Input and output tokens
    ax5 = axes[1, 1]
    bars5 = ax5.bar(["Input Tokens", "Output Tokens", "Total Tokens"], [tokens_in, tokens_out, total_tokens], color=["#8b5cf6", "#a855f7", "#6366f1"])
    ax5.axhline(50000, color="red", linestyle="--", linewidth=1.5, label="Token Threshold (50k)")
    ax5.set_title("5. Input and output tokens", fontweight="bold")
    ax5.set_ylabel("Token Count")
    ax5.legend(loc="upper left")
    for bar in bars5:
        yval = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2, yval + 30, f"{int(yval)}", ha="center", va="bottom", fontsize=9)
    ax5.set_ylim(0, max(55000, total_tokens * 1.3))

    # Panel 6: Quality proxy
    ax6 = axes[1, 2]
    if qualities:
        ax6.plot(range(1, len(qualities) + 1), qualities, marker="o", color="#06b6d4", linewidth=1.5, label="Sample Quality Score")
    ax6.axhline(0.75, color="red", linestyle="--", linewidth=1.5, label="Min Quality SLO (0.75)")
    ax6.axhline(avg_quality, color="#0891b2", linestyle="-.", linewidth=1.5, label=f"Mean Quality ({avg_quality:.2f})")
    ax6.set_title("6. Quality proxy (0.0 to 1.0)", fontweight="bold")
    ax6.set_xlabel("Request Sequence")
    ax6.set_ylabel("Score")
    ax6.set_ylim(0, 1.1)
    ax6.legend(loc="lower left")

    plt.tight_layout()
    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(EVIDENCE_PATH, dpi=180)
    print(f"\n[OK] Saved runtime dashboard image to: {EVIDENCE_PATH}")

if __name__ == "__main__":
    main()
