# Công cụ tài liệu

[generate_diagrams.py](generate_diagrams.py) tái tạo sơ đồ UML và ba BPMN từ mô hình trong script, chỉ dùng thư viện chuẩn Python.

Chạy từ thư mục gốc repository:

```bash
python3 scripts/generate_diagrams.py
```

Đầu ra:

- `docs/ba/use-cases/diagram.puml` và `diagram.svg`.
- `docs/ba/bpmn/01-create-task/diagram.bpmn` và `diagram.svg`.
- `docs/ba/bpmn/02-focus-completion/diagram.bpmn` và `diagram.svg`.
- `docs/ba/bpmn/03-event-reminders/diagram.bpmn` và `diagram.svg`.

Đường dẫn được xác định theo vị trí script. Nếu chỉnh sơ đồ bằng công cụ ngoài, cần cập nhật mô hình trong script hoặc giữ riêng bản chỉnh trước khi tái tạo, vì script sẽ ghi đè đầu ra.
