# Runbook và Đặc tả Alert Hệ thống

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ. Quy trình điều tra bám sát chuỗi: **Metrics → Logs → Traces**.

<a id="alert-1"></a>
## Alert 1: high_latency_p95

- **Tên:** high_latency_p95
- **Severity:** warning
- **Duration:** 5m
- **Kênh thông báo:** Slack (`#alerts-ai-latency`)
- **SLI/SLO liên quan:** Primary SLO `fast_successful_requests` (độ trễ $\le$ 3000ms trên 99.5% request).
- **Điều kiện và thời gian duy trì:** `latency_p95 > 3000` ms duy trì liên tục trong `5m`.
- **Ảnh hưởng tới người dùng:** Người dùng trải nghiệm độ trễ trả lời quá lâu (> 3 giây), tăng nguy cơ người dùng hủy request hoặc timeout giao diện.
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra panel **Latency percentiles and TTFT** trên Dashboard để xác định khoảng thời gian bắt đầu trễ và xem TTFT có tăng theo không.
  2. Lọc log trong `data/logs.jsonl` tìm các request có `latency_ms > 3000`, lấy ra danh sách các `correlation_id` tiêu biểu.
  3. Mở Langfuse tìm trace của các `correlation_id` đó, xem waterfall trace để xác định bước chậm nằm ở span `retrieval` (vector DB) hay `fake-llm-generate` (LLM call).
- **Mitigation tạm thời:**
  - Nếu span `retrieval` bị nghẽn (do incident `rag_slow`): gửi POST `/incidents/rag_slow/disable` hoặc chuyển fallback sang bộ nhớ đệm cache.
  - Nếu LLM quá tải: bật rate limiter tạm thời hoặc giảm kích thước input context.
- **Owner:** `@oncall-ai`

<a id="alert-2"></a>
## Alert 2: high_error_rate

- **Tên:** high_error_rate
- **Severity:** critical
- **Duration:** 2m
- **Kênh thông báo:** Slack (`#alerts-ai-critical`)
- **SLI/SLO liên quan:** Guardrail `error_rate_pct_max <= 2%` và Primary SLO `fast_successful_requests`.
- **Điều kiện và thời gian duy trì:** `error_rate_pct > 2%` duy trì liên tục trong `2m`.
- **Ảnh hưởng tới người dùng:** Người dùng nhận phản hồi lỗi HTTP 500 (`request_failed`), không nhận được câu trả lời từ AI.
- **Ba bước kiểm tra đầu tiên:**
  1. Mở panel **Error rate and retrieval success** trên Dashboard để xem `error_breakdown` phân bổ lỗi theo loại exception nào (`RuntimeError`, `Timeout`, v.v.).
  2. Tra cứu log trong `data/logs.jsonl` lọc theo `event == "request_failed"` để xem `error_type`, `detail` và `correlation_id`.
  3. Mở Langfuse đối chiếu trace theo `correlation_id` xem span con nào ném ngoại lệ và ghi nhận mã lỗi.
- **Mitigation tạm thời:**
  - Nếu do lỗi retrieval timeout (incident `tool_fail`): gửi POST `/incidents/tool_fail/disable` để vô hiệu hóa sự cố giả lập.
  - Kích hoạt cơ chế trả lời dự phòng (fallback response) cho user thay vì ném lỗi 500 chưa được bắt.
- **Owner:** `@oncall-ai`

<a id="alert-3"></a>
## Alert 3: quality_or_retrieval_degraded

- **Tên:** quality_or_retrieval_degraded
- **Severity:** warning
- **Duration:** 5m
- **Kênh thông báo:** Slack (`#alerts-ai-quality`)
- **SLI/SLO liên quan:** Guardrails `quality_score_avg_min >= 0.75` và `retrieval_success_rate_pct_min >= 90%`.
- **Điều kiện và thời gian duy trì:** `quality_score_avg < 0.75` hoặc `retrieval_success_rate < 90%` trong `5m`.
- **Ảnh hưởng tới người dùng:** Câu trả lời AI bị giảm chất lượng, thiếu căn cứ tài liệu chính xác, hoặc câu trả lời bị lặp từ/thiếu ngữ cảnh.
- **Ba bước kiểm tra đầu tiên:**
  1. Kiểm tra panel **Quality proxy** và tỷ lệ `retrieval success` trên Dashboard để phát hiện xu hướng sụt giảm chất lượng.
  2. Kiểm tra log `response_sent` xem có sự thay đổi về `prompt_version` gần đây không (ví dụ vừa promote prompt mới).
  3. Lấy trace trên Langfuse của các request có `quality_score < 0.75` để kiểm tra tài liệu `docs` được retrieve và câu trả lời sinh ra.
- **Mitigation tạm thời:**
  - Nếu chất lượng sụt giảm sau khi đổi prompt: thực hiện rollback prompt `production` về version ổn định trước đó (v1) qua Langfuse.
  - Nếu retrieval thất bại: kiểm tra kết nối tới dịch vụ vector search và nạp lại corpus dữ liệu.
- **Owner:** `@oncall-ai`
