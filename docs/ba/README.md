# Bộ tài liệu phân tích nghiệp vụ — TickTok

**Phiên bản:** 1.0 · **Ngày:** 18/11/2026 · **Ngôn ngữ:** Tiếng Việt.

Tài liệu nghiệp vụ và đặc tả chức năng của ứng dụng Android TickTok.

**Trạng thái:** Bản thảo, chưa nghiệm thu. Các đề xuất mở rộng được ghi riêng với chức năng hiện tại.

## 1. Danh mục tài liệu

```text
ba/
├── README.md
├── requirements/
│   ├── BRD.md
│   ├── SRS.md
│   ├── USER_STORIES_ACCEPTANCE_CRITERIA.md
│   └── BUSINESS_RULES.md
├── use-cases/
│   ├── README.md
│   ├── SPECIFICATIONS.md
│   ├── diagram.puml
│   └── diagram.svg
├── bpmn/
│   ├── README.md
│   ├── 01-create-task/
│   ├── 02-focus-completion/
│   └── 03-event-reminders/
└── traceability/
    └── TRACEABILITY.csv
```

Mỗi thư mục quy trình BPMN chứa `diagram.bpmn` để chỉnh sửa và `diagram.svg` để xem. Script sinh sơ đồ nằm tại [scripts/generate_diagrams.py](../../scripts/generate_diagrams.py).

| Thứ tự | Tài liệu | Nội dung |
| --- | --- | --- |
| 1 | [BRD](requirements/BRD.md) | Bối cảnh, mục tiêu nghiệp vụ, các bên liên quan, phạm vi, lợi ích kỳ vọng và câu hỏi cần xác nhận. |
| 2 | [SRS](requirements/SRS.md) | Yêu cầu chức năng, giao diện, dữ liệu, ràng buộc kỹ thuật và giới hạn triển khai. |
| 3 | [User Stories & Acceptance Criteria](requirements/USER_STORIES_ACCEPTANCE_CRITERIA.md) | Nhu cầu từ góc nhìn người dùng và kịch bản Given/When/Then để đối chiếu. |
| 4 | [Business Rules](requirements/BUSINESS_RULES.md) | Quy tắc dữ liệu, điều kiện hợp lệ, tính toán, chuyển trạng thái và ngoại lệ trong code. |
| 5 | [Use Case Diagram](use-cases/README.md) | Sơ đồ UML, tác nhân, ranh giới hệ thống, danh mục use case và file nguồn PlantUML. |
| 6 | [Đặc tả Use Case](use-cases/SPECIFICATIONS.md) | Sáu use case quan trọng: đăng nhập, tạo task, hoàn thành task, sự kiện, Pomodoro và thống kê. |
| 7 | [BPMN](bpmn/README.md) | Ba quy trình: tạo task kèm lời nhắc, hoàn tất phiên Pomodoro, tạo/cập nhật sự kiện và lời nhắc. Có bản SVG và file BPMN 2.0 để chỉnh sửa. |
| Bổ sung | [Ma trận truy vết](traceability/TRACEABILITY.csv) | Nối từng FR với mục tiêu, yêu cầu nghiệp vụ, story/AC, business rule, use case, BPMN và mã nguồn. |

Nên đọc BRD → SRS → Business Rules → User Stories/AC → Use Case → BPMN. Khi kiểm tra một chức năng cụ thể, dùng ma trận truy vết để tìm các tài liệu liên quan.

## 2. Quy ước đọc

| Nhãn | Ý nghĩa |
| --- | --- |
| Chức năng hiện tại | Mô tả chức năng và cách xử lý của phiên bản hiện tại. |
| Giới hạn / điểm cần xác nhận | Mã nguồn có hành vi cần làm rõ hoặc chưa đáp ứng kỳ vọng thường gặp; không tự diễn giải thành tính năng hoàn chỉnh. |
| Đề xuất / mục tiêu | Nội dung cho vòng phát triển, kiểm thử hoặc thảo luận sau; không phải kết quả đã đạt. |

Mức ưu tiên của stories phục vụ lập kế hoạch. Kết quả thực hiện AC được ghi riêng trong báo cáo kiểm thử.

## 3. Hệ thống mã định danh

| Tiền tố | Đối tượng | Ví dụ |
| --- | --- | --- |
| `BO-*` | Mục tiêu nghiệp vụ trong BRD | `BO-04` — hỗ trợ tập trung và tổng hợp phiên |
| `BIZ-*` | Yêu cầu nghiệp vụ trong BRD | `BIZ-07` — Pomodoro |
| `FR-NHÓM-NN` | Yêu cầu chức năng trong SRS | `FR-TASK-01` — tạo công việc |
| `US-NHÓM-NN` | User story | `US-TASK-01` |
| `AC-*` | Tiêu chí chấp nhận trong từng story | Xem quy ước cụ thể trong tài liệu stories |
| `BR-NHÓM-NN` | Business rule | `BR-POMO-01` |
| `UC-NN` | Use case | `UC-05` — tạo công việc |

Các nhóm chức năng dùng chung: `AUTH`, `CAT`, `TASK`, `VIEW`, `SEARCH`, `EVENT`, `POMO`, `STAT`, `SET`, `CLEAN`. Một story có thể liên quan nhiều FR; một FR có thể liên quan nhiều quy tắc và AC. `UC-04`, `UC-09`, `UC-11`, `UC-12`, `UC-15` là các mục gom những mục tiêu liên quan để sơ đồ tổng quan vẫn đọc được; đặc tả chi tiết chỉ ra luồng được chọn.

Ma trận CSV có 40 dòng FR, dùng UTF-8 có BOM để thuận tiện mở trong bảng tính. Các mã trong cùng ô ngăn cách bằng dấu `;`; các cột Source và BPMN tính từ thư mục gốc repository. Khi một story gom nhiều FR, các AC của story được truy vết chung đến từng FR đó, chưa phải phép tách riêng mỗi AC cho đúng một FR. Quy tắc đường dẫn UID `BR-AUTH-07` còn là ràng buộc dùng chung trong stories và NFR-02 của SRS. Dọn dữ liệu là tác vụ tự động khi resume, nên ô Use_cases của FR-CLEAN-01 để trống; US-CLEAN-01 liên hệ nó với bối cảnh xem công việc UC-09.

## 4. Các điểm hiện trạng quan trọng

1. Ma trận Eisenhower được phân nhóm trực tiếp theo `priority` 3/2/1/0. Không có hai trường riêng cho mức quan trọng và khẩn cấp, cũng không suy luận quadrant từ deadline.
2. Lời nhắc task ở quá khứ hoặc từ đầu ngày kế tiếp sau hạn được xóa khỏi dữ liệu nhắc; task vẫn có thể được lưu. Không mô tả thành chặn toàn bộ thao tác tạo task.
3. Hoàn tất Pomodoro thủ công lưu `totalMillis`, tức thời lượng cấu hình. Lưu lịch sử không hoàn thành task, và phiên nghỉ không được lưu thành phiên tập trung.
4. Kết thúc tự nhiên một phiên tập trung gọi lưu lịch sử bất đồng bộ rồi chuyển sang nghỉ. Việc chuyển chế độ không chờ ghi Firestore thành công.
5. Thống kê tính trên tối đa 300 phiên gần nhất, chỉ hiện tối đa 40 bản ghi hôm nay và gộp biểu đồ theo tên task. Không mô tả thành báo cáo toàn bộ lịch sử hay nhóm theo `taskId`.
6. Cơ chế dọn task chạy khi `MainActivity.onResume` kiểm tra ngày, không phải job server hay bộ hẹn giờ đúng nửa đêm. Truy vấn dọn đầu tiên dựa vào `completedAt` mà không lọc thêm cờ hoàn thành.
7. Công tắc âm thanh lưu tùy chọn nhưng bộ phát âm Pomodoro/notification chưa đọc tùy chọn này. Đổi giao diện có xử lý áp dụng qua `AppCompatDelegate`, nhưng một số màn còn màu hardcode.
8. Đường dẫn dữ liệu theo UID có trong client; repository chưa cung cấp bằng chứng Firestore Rules đang triển khai, kiểm thử bảo mật hoặc kiểm thử đa thiết bị.

## 5. Từ điển thuật ngữ

| Thuật ngữ | Cách dùng trong bộ tài liệu |
| --- | --- |
| Task / công việc | Mục việc cần làm; có thể thuộc danh mục hoặc có `categoryId = null`. |
| Category / danh mục | Nhóm tổ chức task; có tên, biểu tượng và thứ tự. |
| Event / sự kiện | Mốc ngày riêng với task, có thông tin đếm ngày còn lại. |
| Focus / tập trung | Chế độ tập trung của Pomodoro; có thể sinh bản ghi lịch sử. |
| Break / nghỉ | Chế độ nghỉ; mặc định 5 phút, không sinh bản ghi tập trung. |
| Phiên / Pomo | Một bản ghi tập trung trong collection `pomodoro`; số bản ghi không phải số task hoàn thành. |
| Snapshot listener | Cơ chế SDK thông báo thay đổi tập dữ liệu; không tự tạo cam kết độ trễ hay tính sẵn sàng. |
| Callback thành công | Nhánh xử lý thành công của thao tác SDK trong code; tài liệu không giả lập hoặc chứng nhận vận hành backend. |
| Hôm nay | Mốc ngày theo múi giờ thiết bị; một số phép tính trong source dùng hằng 24 giờ. |
| Tuần này | Từ đầu thứ Hai đến thời điểm tính thống kê, trong phần dữ liệu đã tải. |

## 6. Bảo trì tài liệu

Khi rà soát tài liệu, kiểm tra các liên kết, mã FR/US/BR/UC và sự nhất quán giữa đặc tả với sơ đồ.

Khi thay đổi nghiệp vụ, cập nhật FR, BR và AC liên quan, sau đó điều chỉnh use case/BPMN và ma trận truy vết. Cách chỉnh từng sơ đồ được mô tả trong [Use Case Diagram](use-cases/README.md) và [BPMN](bpmn/README.md).

Mã nguồn là căn cứ chính cho bản hiện trạng này. Những ảnh sơ đồ cũ trong `docs/reference/diagrams/` chỉ là tài liệu tham khảo: ví dụ ảnh use case cũ có nhãn tìm sự kiện, trong khi `SearchFragment` hiện chỉ tìm task.

## 7. Trạng thái kiểm chứng

Các liên kết tài liệu, mã tham chiếu và cấu trúc sơ đồ đã được kiểm tra. Các AC chưa được thực thi trên Android/Firebase; mô hình BPMN chưa chạy trên workflow engine.
