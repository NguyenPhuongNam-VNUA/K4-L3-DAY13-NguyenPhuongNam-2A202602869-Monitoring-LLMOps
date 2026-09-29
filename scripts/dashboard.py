import json
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="K4-L3A LLMOps Dashboard", layout="wide")

st.title("📊 K4-L3A Day 13 Monitoring & LLMOps Dashboard")
st.caption("Runtime Observability Dashboard (Contract: config/dashboard.yaml — 60m window)")

LOG_PATH = Path("data/logs.jsonl")

if not LOG_PATH.exists():
    st.error(f"Log file {LOG_PATH} not found.")
    st.stop()

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

# Calculations
latencies = [r.get("latency_ms", 0) for r in response_events if "latency_ms" in r]
ttfts = [r.get("ttft_ms", 0) for r in response_events if "ttft_ms" in r]
p50 = float(np.percentile(latencies, 50)) if latencies else 0.0
p95 = float(np.percentile(latencies, 95)) if latencies else 0.0
p99 = float(np.percentile(latencies, 99)) if latencies else 0.0
ttft_p95 = float(np.percentile(ttfts, 95)) if ttfts else 0.0

total_requests = len(request_events)
total_failed = len(failed_events)
error_rate = (total_failed / total_requests * 100) if total_requests else 0.0

retrieval_responses = [r for r in response_events if r.get("tool_name") == "retrieval"]
retrieval_successes = [r for r in retrieval_responses if r.get("tool_success") is True]
retrieval_rate = (len(retrieval_successes) / len(retrieval_responses) * 100) if retrieval_responses else 100.0

total_cost = sum(r.get("cost_usd", 0.0) for r in response_events)
tokens_in = sum(r.get("tokens_in", 0) for r in response_events)
tokens_out = sum(r.get("tokens_out", 0) for r in response_events)
total_tokens = tokens_in + tokens_out

qualities = [r.get("quality_score", 0.0) for r in response_events if "quality_score" in r]
avg_quality = float(np.mean(qualities)) if qualities else 0.0

# 6 Panels Grid
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("1. Latency & TTFT (ms)")
    st.metric("P95 Latency", f"{p95:.1f} ms", delta=f"{p95 - 3000:.1f} ms vs SLO (<=3000ms)", delta_color="inverse")
    st.write(f"- **P50:** {p50:.1f} ms\n- **P99:** {p99:.1f} ms\n- **TTFT P95:** {ttft_p95:.1f} ms")
    if latencies:
        st.line_chart(pd.DataFrame({"Latency": latencies}))

with col2:
    st.subheader("2. Request Traffic")
    st.metric("Total Traffic", f"{total_requests} reqs", delta=">= 1 req/m threshold")
    st.write(f"- Received: {len(request_events)}\n- Sent: {len(response_events)}\n- Failed: {len(failed_events)}")
    st.line_chart(pd.DataFrame({"Requests": list(range(1, len(response_events)+1))}))

with col3:
    st.subheader("3. Error Rate & Retrieval")
    st.metric("Error Rate", f"{error_rate:.1f} %", delta=f"{error_rate - 2.0:.1f}% vs Max 2%", delta_color="inverse")
    st.metric("Retrieval Success", f"{retrieval_rate:.1f} %", delta="Target >= 90%")
    st.write(f"- Failed requests: {total_failed}\n- Retrieval calls: {len(retrieval_responses)}")

st.divider()

col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("4. Cost Over Time (USD)")
    st.metric("Total Cost", f"${total_cost:.4f}", delta=f"${total_cost - 2.5:.4f} vs Budget $2.50", delta_color="inverse")
    costs = [r.get("cost_usd", 0.0) for r in response_events]
    if costs:
        st.area_chart(pd.DataFrame({"Cumulative Cost": np.cumsum(costs)}))

with col5:
    st.subheader("5. Input / Output Tokens")
    st.metric("Total Tokens", f"{total_tokens:,}", delta=f"{total_tokens - 50000:,} vs Max 50,000", delta_color="inverse")
    st.write(f"- **Tokens In:** {tokens_in:,}\n- **Tokens Out:** {tokens_out:,}")
    st.bar_chart(pd.DataFrame({"Tokens": [tokens_in, tokens_out]}, index=["Input", "Output"]))

with col6:
    st.subheader("6. Quality Proxy")
    st.metric("Mean Quality Score", f"{avg_quality:.2f}", delta=f"{avg_quality - 0.75:.2f} vs Min SLO 0.75")
    if qualities:
        st.line_chart(pd.DataFrame({"Quality Score": qualities}))
