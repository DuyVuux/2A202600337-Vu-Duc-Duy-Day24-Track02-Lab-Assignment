# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [x] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: dpo@medviet.vn

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | 🚧 In Progress | Infra Team |
| Audit logging | Structured JSON logging (Python logging + ELK Stack). Mỗi API request log: user, resource, action, timestamp, IP. Retention 1 năm. | ✅ Done | Platform Team |
| Breach detection | Prometheus alerting rules: failed_auth > 10/min triggers PagerDuty. Grafana dashboard real-time. WAF rate-limiting. | ✅ Done | Security Team |

## F. Technical Solutions Details
- **Audit logging**: Structured JSON logging (Python logging + ELK Stack). Mỗi API request log: user, resource, action, timestamp, IP. Retention 1 năm.
- **Breach detection**: Prometheus alerting rules: failed_auth > 10/min triggers PagerDuty. Grafana dashboard real-time. WAF rate-limiting.
