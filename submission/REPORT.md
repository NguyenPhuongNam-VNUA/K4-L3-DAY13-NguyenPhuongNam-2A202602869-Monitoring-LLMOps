# Báo cáo cá nhân — K4-L3A Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Nguyễn Phương Nam
- **MSSV:** 2A202602869
- **Lớp:** K4-L3A
- **Repository URL:** https://github.com/NguyenPhuongNam-VNUA/K4-L3-DAY13-NguyenPhuongNam-2A202602869-Monitoring-LLMOps
- **Commit SHA cuối:** 
- **Challenge ID:** 
- **Tên project Langfuse cá nhân:** `day13-k4-l3a-2A202602869`

## 2. Evidence index

Điền đúng đường dẫn tới evidence thực tế. Có thể đổi tên hoặc dùng nhiều ảnh nếu cần.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | `evidence/01-pytest.png` |
| Log validator | `evidence/02-log-validator.png` |
| Dashboard validator | `evidence/03-dashboard-validator.png` |
| Structured log | `evidence/04-structured-log.png` |
| PII redaction | `evidence/05-pii-redaction.png` |
| Trace list | `evidence/06-trace-list.png` |
| Trace waterfall | `evidence/07-trace-waterfall.png` |
| Trace metadata | `evidence/08-trace-metadata.png` |
| Prompt versions | `evidence/09-prompt-versions.png` |
| Prompt rollback | `evidence/10-prompt-rollback.png` |
| Dashboard runtime | `evidence/11-dashboard-overview.png` |
| Incident metric | `evidence/12-incident-metric.png` |
| Incident log | `evidence/13-incident-log.png` |
| Incident trace | `evidence/14-incident-trace.png` |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | 30/100 | 100/100 | Đạt điểm tuyệt đối; đầy đủ schema, correlation_id, context enrichment và PII scrubbing |
| `validate_dashboard.py` | 6/6 panel | 6/6 panel | Hợp lệ 100% contract cấu hình 6 panel |
| `pytest` | 22 passed / 22 | 24 passed / 24 | 100% unit tests passed (bổ sung test CCCD và Credit Card) |
| Số traces hợp lệ | 10 | 20+ | Đầy đủ quan hệ cha-con (root agent, retriever, generation) trên Langfuse |
| Số PII leak | 0 | 0 | Scrubbing triệt để email, phone, CCCD, credit card |
| Latency P95 / TTFT P95 | 864.0ms / 55.0ms | 164.0ms / 55.0ms | Đo được qua load test và endpoint /metrics |
| Retrieval success rate | 100% | 100% | 100% request retrieval thành công |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** Trong `CorrelationIdMiddleware` (`app/middleware.py`), gọi `clear_contextvars()` ở đầu mỗi request để cô lập context. Đọc header `x-request-id`, nếu thiếu thì sinh mới theo format `req-<8-char-hex>` (`f"req-{uuid.uuid4().hex[:8]}"`). Bind ID vào contextvars của structlog, gán vào `request.state.correlation_id`, và trả về client qua 2 header `x-request-id` và `x-response-time-ms`. Đồng thời truyền ID này vào `agent.run` để liên kết đồng bộ sang metadata của Langfuse trace.
- **Các metadata được ghi vào structured log:** Các trường toàn cục (`ts`, `level`, `service`, `event`), các trường context request (`correlation_id`, `user_id_hash` từ sha256, `session_id`, `feature`, `model`, `env`), và các trường đo lường hiệu năng/kết quả (`latency_ms`, `ttft_ms`, `tokens_in`, `tokens_out`, `cost_usd`, `quality_score`, `tool_name`, `tool_success`, `payload`).
- **Cách bảo đảm PII được scrub trước khi ghi:** Sử dụng các regex pattern trong `app/pii.py` cho email, số điện thoại VN, CCCD (12 chữ số) và thẻ tín dụng (16 chữ số). Cấu hình processor `scrub_event` trong chuỗi xử lý của structlog (`app/logging_config.py`) nằm ngay trước file writer (`JsonlFileProcessor`) và JSON renderer, thực hiện quét và thay thế PII đệ quy trên toàn bộ dữ liệu log trước khi ghi xuống đĩa hoặc in ra console.
- **Cách kiểm chứng kết quả:** Chạy `python scripts/validate_logs.py` đạt điểm tuyệt đối **100/100** (pass cả 4 tiêu chí JSON schema, correlation ID propagation, context enrichment, và PII scrubbing). Chạy `pytest` pass **24/24 tests** bao gồm cả test PII cho email, số điện thoại, CCCD và thẻ tín dụng. Sample log trong `data/logs.jsonl` không còn rò rỉ PII nguyên văn.

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** Sử dụng API key pair cá nhân (`pk-lf-...`, `sk-lf-...`) trong `.env` trỏ tới project Langfuse `day13-k4-l3a-2A202602869`. Mọi trace đều mang environment `dev`, tags `["lab", feature, "claude-sonnet-4-5"]`, `user_id` đã được băm SHA-256 an toàn (12 ký tự) và `session_id` riêng biệt.
- **Cấu trúc root/retrieval/generation observations:**
  - **Root:** `lab-agent-run` (type `AGENT`) bao bọc toàn bộ luồng xử lý agent, gắn context `propagate_attributes`.
  - **Child 1:** `retrieval` (type `RETRIEVER`) đo bước tra cứu tài liệu `retrieve()`, nhận query preview đã sanitize, trả ra document count và doc previews.
  - **Child 2:** `fake-llm-generate` (type `GENERATION`) đo bước gọi LLM, liên kết với `prompt.managed_prompt`, lưu model `claude-sonnet-4-5`, `usage_details` (input/output tokens) và `cost_details` (USD).
  - Cấu trúc cây quan hệ cha-con hiển thị rõ ràng trên waterfall trace, giúp cô lập ngay lập tức bước gây chậm trễ (do retrieval hay do LLM).
- **Cách nối trace với log:** Sử dụng chung mã định danh `correlation_id` (format `req-<8-hex>`). Middleware gán `correlation_id` vào structured log trong `data/logs.jsonl` đồng thời truyền vào metadata của trace trên Langfuse (`metadata={"correlation_id": correlation_id}`).
- **Prompt name:** `day13-chat`
- **Version/label baseline:** Version 1 (gắn nhãn `baseline` và `production`).
- **Version/label candidate:** Version 2 (gắn nhãn `candidate`).
- **Trace ID của mỗi version:**
  - Version 1 (Baseline / Production ban đầu): `8ea00054699b3a812bf8106f6e08ce93` (Correlation ID: `req-f375b8b5`)
  - Version 2 (Candidate / Promoted to Production): `005c8aefa18c07154e6576a863eea862` (Correlation ID: `req-b4bae10f`)
  - Version 1 (Sau khi Rollback Production về v1): `1158febf63717f5bb64756bd85297ce8` (Correlation ID: `req-1e9066d6`)
- **Cách promote và rollback `production`:**
  - *Promote:* Gán nhãn `production` sang Version 2 thông qua `client.update_prompt(name="day13-chat", version=2, new_labels=["production"])` (hoặc chuyển nhãn trên Langfuse UI).
  - *Rollback:* Chuyển nhãn `production` quay trở lại Version 1 thông qua `client.update_prompt(name="day13-chat", version=1, new_labels=["production"])`. Ứng dụng tự động tải lại prompt Version 1 mà không cần sửa code hoặc khởi động lại dịch vụ.

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:** Dựng đúng 6 panel theo cấu hình chuẩn `config/dashboard.yaml` (cửa sổ 60 phút):
  1. *Latency percentiles and TTFT:* Hiển thị P50, P95, P99 và TTFT P95 kèm đường ngưỡng SLO 3000ms.
  2. *Request traffic:* Số lượng request tích lũy và tốc độ request kèm ngưỡng tối thiểu 1 req/phút.
  3. *Error rate and retrieval success:* Tỷ lệ lỗi (%) kèm ngưỡng tối đa 2% và tỷ lệ retrieval thành công (%) kèm ngưỡng tối thiểu 90%.
  4. *Cost over time:* Chi phí tích lũy (USD) kèm đường ngưỡng ngân sách $2.50.
  5. *Input and output tokens:* Phân bổ token đầu vào/đầu ra kèm ngưỡng 50,000 tokens.
  6. *Quality proxy:* Điểm chất lượng trung bình kèm đường ngưỡng SLO tối thiểu 0.75.
- **SLO và lý do chọn:**
  - Tên SLO: `fast_successful_requests` với mục tiêu **99.5%** trong chu kỳ 28 ngày (`window: 28d`).
  - SLI: Tỷ lệ request trả về thành công có độ trễ $\le$ 3000ms trên tổng số request nhận được.
  - Lý do: Đối chiếu với kết quả baseline thực tế (Latency P95 = 864ms, runtime bình thường ~160ms, error rate 0%), ngưỡng 3000ms đủ rộng cho các biến động thông thường nhưng đủ nhạy để phát hiện sự cố nghẽn mạng (tail latency) hoặc lỗi vector search.
- **Cách tính error budget:**
  - $\text{Error Budget} = 100\% - 99.5\% = 0.5\%$.
  - Trong chu kỳ 28 ngày với giả định 10,000 requests, hệ thống chỉ cho phép tối đa 50 requests bị lỗi (HTTP 500) hoặc có độ trễ $> 3000\text{ms}$.
- **Ba alert và runbook tương ứng:**
  1. `high_latency_p95`: Severity warning, điều kiện `latency_p95 > 3000` trong `5m`, kênh Slack `#alerts-ai-latency`, runbook tại `docs/alerts.md#alert-1`.
  2. `high_error_rate`: Severity critical, điều kiện `error_rate_pct > 2` trong `2m`, kênh Slack `#alerts-ai-critical`, runbook tại `docs/alerts.md#alert-2`.
  3. `quality_or_retrieval_degraded`: Severity warning, điều kiện `quality_score_avg < 0.75 or retrieval_success_rate < 90` trong `5m`, kênh Slack `#alerts-ai-quality`, runbook tại `docs/alerts.md#alert-3`.

## 7. Điều tra challenge

- **Challenge ID:**
- **Khoảng thời gian điều tra:**
- **Triệu chứng từ metrics:**
- **Log line và correlation ID liên quan:**
- **Trace ID và span gây ảnh hưởng:**
- **Root cause:**
- **Fix action:**
- **Preventive measure:**

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:**
- **Một lỗi/blocker đã gặp:**
- **Cách tìm nguyên nhân và xử lý:**
- **Cách hiểu luồng Metrics → Logs → Traces:**
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:**
- **Điều quan trọng nhất đã học:**
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:**

## 9. Checklist trước khi nộp

- [ ] Kết quả và evidence thuộc commit SHA cuối.
- [ ] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [ ] Incident evidence nối đúng metric → log → trace.
- [ ] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [ ] Repository chạy lại được theo README.
- [ ] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [ ] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
