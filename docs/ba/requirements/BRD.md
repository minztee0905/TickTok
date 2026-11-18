# BRD — TickTok

| Thuộc tính | Giá trị |
| --- | --- |
| Tên tài liệu | Business Requirements Document — Quản lý công việc và thời gian tập trung |
| Phiên bản tài liệu | 1.0 |
| Ngày biên soạn | 18/11/2026 |
| Phạm vi | Ứng dụng Android TickTok |
| Trạng thái | Bản thảo |
| Tài liệu liên quan | [SRS](SRS.md), [User Stories & AC](USER_STORIES_ACCEPTANCE_CRITERIA.md), [Business Rules](BUSINESS_RULES.md), [ma trận truy vết](../traceability/TRACEABILITY.csv) |

## 1. Mục đích

BRD xác định nhu cầu, mục tiêu và phạm vi nghiệp vụ của TickTok. Các chức năng được mô tả theo phiên bản hiện tại; những vấn đề cần xác nhận được tổng hợp ở mục 11.

Trong tài liệu này:

- **Hiện trạng** mô tả cách ứng dụng đang xử lý nghiệp vụ.
- **Mục tiêu nghiệp vụ** là cách diễn giải giá trị của chức năng; các lợi ích chưa được định lượng.
- **Đề xuất/cần xác nhận** là câu hỏi cho vòng phát triển tiếp theo, không phải chức năng đã hoàn thành.

## 2. Bối cảnh và vấn đề nghiệp vụ

Ứng dụng phục vụ quản lý công việc cá nhân. Người dùng cần lưu việc phải làm, tổ chức theo danh mục, kiểm tra hạn, theo dõi sự kiện và dành thời gian tập trung cho công việc được chọn. Việc kết hợp các hoạt động này trong cùng một ứng dụng giúp người dùng chuyển từ lập kế hoạch sang thực hiện và xem lại kết quả.

Các vấn đề nghiệp vụ mà sản phẩm hướng đến:

| Vấn đề | Khả năng ứng dụng hiện có để đáp ứng |
| --- | --- |
| Khó tổng hợp việc cần xử lý theo thời gian | Bốn nhóm việc hôm nay, ngày mai, quá hạn, hoàn thành hôm nay; lịch tháng hiện tại. |
| Danh sách dài khó tổ chức | Danh mục có biểu tượng, thứ tự; công việc có ưu tiên, thứ tự và tìm kiếm. |
| Dễ quên thời điểm cần xử lý | Lời nhắc công việc; hai mốc nhắc sự kiện nếu thời điểm còn ở tương lai. |
| Khó duy trì và nhìn lại các phiên tập trung | Pomodoro tập trung/nghỉ, chọn công việc, lịch sử và thống kê ngày/tuần. |

## 3. Mục tiêu nghiệp vụ

| Mã | Mục tiêu | Cách đánh giá bằng chức năng hiện có |
| --- | --- | --- |
| BO-01 | Cho người dùng truy cập dữ liệu theo tài khoản của mình | Đăng ký/đăng nhập; truy vấn dữ liệu theo `users/{uid}`. Việc bảo vệ ở server phải kiểm chứng riêng bằng Firestore Rules. |
| BO-02 | Hỗ trợ ghi nhận, tổ chức và tìm công việc cá nhân | Tạo/sửa/xóa/hoàn thành công việc; danh mục; bộ lọc; lịch; tìm kiếm. |
| BO-03 | Hỗ trợ nhận biết các mốc công việc và sự kiện | Lưu hạn và lời nhắc; hiển thị ngày còn lại; lên lịch thông báo qua Android. |
| BO-04 | Hỗ trợ thực hiện và tổng hợp các phiên tập trung | Bộ đếm Pomodoro; lịch sử phiên; số phiên, thời lượng ngày/tuần và biểu đồ. |
| BO-05 | Cho người dùng điều chỉnh một số tùy chọn cá nhân | Chọn giao diện; đổi mật khẩu với tài khoản password; đăng xuất. |

Các chỉ tiêu về năng suất, hiệu năng và độ sẵn sàng chưa được đo lường.

## 4. Các bên liên quan và vai trò

| Bên liên quan | Vai trò đối với sản phẩm | Căn cứ/phạm vi |
| --- | --- | --- |
| Người dùng cá nhân | Ghi nhận, tổ chức, hoàn thành công việc; sử dụng Pomodoro và xem kết quả | Tác nhân nghiệp vụ chính; chưa có vai trò quản lý nhóm hoặc phân quyền quản trị trong ứng dụng. |
| Nhóm phát triển/bảo trì | Xây dựng giao diện, xử lý nghiệp vụ, dữ liệu và cấu hình tích hợp | Phát triển và bảo trì ứng dụng. |
| Người rà soát nghiệp vụ/kiểm thử | Đối chiếu yêu cầu và hành vi, xác nhận những điểm còn mở | Rà soát yêu cầu, thực hiện kiểm thử và xác nhận kết quả. |
| Firebase/Google | Cung cấp xác thực, lưu trữ, tài khoản Google | Dịch vụ hỗ trợ, không phải nhân sự hoặc module quản trị nội bộ. |
| Nền tảng Android và dịch vụ giọng nói | Quản lý quyền, báo thức, thông báo, nhận dạng giọng nói | Khả năng và quyền trên thiết bị ảnh hưởng kết quả sử dụng. |

## 5. Phạm vi nghiệp vụ hiện tại

| Mã yêu cầu nghiệp vụ | Phạm vi được đáp ứng trong code | Mục tiêu | Liên kết yêu cầu hệ thống |
| --- | --- | --- | --- |
| BIZ-01 | Đăng ký bằng email/tên tài khoản và mật khẩu; đăng nhập password hoặc Google; đổi mật khẩu; đăng xuất; thông báo hướng dẫn khi quên mật khẩu | BO-01, BO-05 | `FR-AUTH-*` |
| BIZ-02 | Tạo, sửa, xóa và sắp xếp danh mục; mục Welcome được cố định riêng trong menu | BO-02 | `FR-CAT-*` |
| BIZ-03 | Quản lý công việc với tiêu đề, mô tả, danh mục có thể rỗng, ưu tiên, ngày đến hạn, trạng thái, lời nhắc và thứ tự; nhập giọng nói | BO-02, BO-03 | `FR-TASK-*` |
| BIZ-04 | Xem tổng quan và danh sách theo thời gian; lịch tháng hiện tại; ma trận phân theo mức ưu tiên; tìm theo tiêu đề/mô tả | BO-02 | `FR-VIEW-*`, `FR-SEARCH-01` |
| BIZ-05 | Lưu/lên lịch lời nhắc công việc; hủy lời nhắc ở một số thao tác hoàn thành/xóa; phát thông báo khi Android cho phép | BO-03 | `FR-TASK-01..04` |
| BIZ-06 | Tạo/sửa/xóa sự kiện; biểu tượng, ngày diễn ra, số ngày còn lại; hai mốc nhắc lúc 08:00 | BO-03 | `FR-EVENT-*` |
| BIZ-07 | Chọn task chưa hoàn thành cho Pomodoro; tùy chỉnh 5–90 phút; bắt đầu/tạm dừng/tiếp tục/đặt lại; luân phiên tập trung/nghỉ; lưu phiên | BO-04 | `FR-POMO-*` |
| BIZ-08 | Thống kê hôm nay/tuần này từ tối đa 300 phiên; tối đa 40 bản ghi hôm nay; biểu đồ nhóm theo tên; chia sẻ văn bản | BO-04 | `FR-STAT-*` |
| BIZ-09 | Chọn giao diện hệ thống/sáng/tối; lưu trạng thái công tắc âm thanh | BO-05 | `FR-SET-*` |
| BIZ-10 | Dọn dữ liệu công việc qua luồng kiểm tra theo ngày khi màn chính được tiếp tục | BO-02 | `FR-CLEAN-01` |

`FR-TASK-01..04` là cách ghi gọn cho bốn ID liên tiếp; danh sách từng ID nằm trong [SRS](SRS.md) và [TRACEABILITY.csv](../traceability/TRACEABILITY.csv).

## 6. Ranh giới phạm vi

| Nội dung | Kết luận theo repository hiện tại |
| --- | --- |
| Cộng tác nhóm, giao việc cho người khác, bình luận, người quản lý | Chưa có luồng hoặc mô hình nghiệp vụ tương ứng. |
| Admin portal, RBAC nhiều vai trò, dashboard quản trị | Chưa có module tương ứng. Hộp thoại liên hệ admin khi quên mật khẩu không tạo thành một chức năng admin. |
| Thanh toán, đơn hàng, thương mại điện tử | Không thuộc dự án TickTok. |
| Công việc lặp lại, phụ thuộc giữa task, checklist con, đính kèm | Chưa có mô hình/luồng tương ứng. |
| Gửi email tự đặt lại mật khẩu | Chưa triển khai trong ứng dụng. |
| Bộ lọc mọi khoảng thời gian/thống kê toàn bộ lịch sử | Chưa có; màn thống kê bị giới hạn dữ liệu tải về. |
| Bộ đếm nền độc lập và phục hồi sau khi tiến trình bị kết thúc | Chưa có foreground service hoặc kho trạng thái bền vững cho toàn bộ phiên. |
| BPMN chạy bằng process engine | Các BPMN trong bộ tài liệu là mô hình phân tích, không phải quy trình được deploy vào ứng dụng. |

## 7. Quy trình nghiệp vụ tổng quan

1. Người dùng đăng ký hoặc đăng nhập; ứng dụng xác định tài khoản hiện tại.
2. Người dùng tạo danh mục nếu cần, thêm công việc, xác định ưu tiên và ngày đến hạn.
3. Người dùng kiểm tra việc qua menu, tổng quan, lịch, ma trận hoặc tìm kiếm.
4. Với task có lời nhắc hợp lệ, sau callback ghi dữ liệu thành công ứng dụng yêu cầu quyền nếu cần và lên lịch qua Android. Thông báo chỉ hiện khi quyền và trạng thái hệ điều hành cho phép.
5. Người dùng chọn task chưa hoàn thành để tập trung, hoặc dùng Pomodoro không gắn task; điều khiển phiên tập trung/nghỉ.
6. Dữ liệu phiên tập trung được ghi theo luồng kết thúc phiên; màn thống kê tổng hợp phần dữ liệu tải được và hỗ trợ chia sẻ.
7. Sự kiện được quản lý riêng với task, có ngày mục tiêu và hai mốc nhắc mặc định.

Thứ tự trên diễn giải hành trình sử dụng, không bắt buộc người dùng tạo danh mục hoặc chọn task trước khi dùng Pomodoro. Ba quy trình chi tiết có bản [BPMN](../bpmn/README.md).

## 8. Dữ liệu nghiệp vụ và vòng đời

| Đối tượng | Ý nghĩa và vòng đời hiện tại |
| --- | --- |
| Tài khoản | Danh tính do Firebase Authentication quản lý; tên tài khoản không có `@` được ánh xạ sang email nội bộ `@ticktok.user`. |
| Danh mục | Có tên, biểu tượng, thứ tự. Xóa danh mục đi qua bước xóa các task thuộc danh mục rồi mới xóa danh mục; các bước này không nằm trong một transaction chung. |
| Công việc | Có trạng thái chưa hoàn thành/hoàn thành; thời điểm hoàn thành có thể được đặt hoặc xóa. Không có thùng rác/khôi phục được triển khai. |
| Sự kiện | Có ngày mục tiêu; code cho chọn ngày đã qua. Các mốc nhắc không còn ở tương lai được bỏ qua. |
| Phiên tập trung | Có tên task, thời lượng phút và thời điểm lưu; không chứa `taskId`. Việc lưu phiên không đánh dấu task hoàn thành. |

**Chính sách dọn hiện trạng cần lưu ý:** truy vấn đầu tiên xóa các bản ghi có `completedAt` trước đầu hôm nay mà không kiểm tra thêm cờ hoàn thành. Các lượt dọn dữ liệu cũ xét cờ `completed` hoặc `isCompleted` và thời điểm bị thiếu/quá cũ. Chính sách lưu trữ này cần được xác nhận trước khi áp dụng cho dữ liệu sử dụng thực tế.

## 9. Phụ thuộc và điều kiện sử dụng

- Firebase được cấu hình đúng package, nhà cung cấp đăng nhập và Firestore. Đường dẫn theo UID ở client không thay thế kiểm soát truy cập bằng Rules phía server.
- Đăng nhập Google phụ thuộc cấu hình OAuth/chứng chỉ ký và Google Play services; nhập giọng nói phụ thuộc dịch vụ nhận dạng khả dụng trên thiết bị.
- Người dùng có thể từ chối micro hoặc thông báo. Không thể suy ra mọi lời nhắc đã lưu đều sẽ hiện đúng giờ.
- Ngày, tuần và các mốc nhắc sử dụng múi giờ/đồng hồ thiết bị; tuần thống kê bắt đầu thứ Hai.
- Không có mô tả yêu cầu nghiệp vụ riêng cho xử lý đồng bộ đa thiết bị, xung đột chỉnh sửa, giao dịch offline hay dữ liệu lớn. Không cam kết những khả năng này chỉ vì SDK có cơ chế cache.

## 10. Tiêu chí đánh giá phạm vi bàn giao

Các kịch bản đánh giá phạm vi bàn giao:

| Mã | Kịch bản chứng minh | Mục tiêu |
| --- | --- | --- |
| BC-01 | Đăng ký/đăng nhập; thao tác dữ liệu đi tới đường dẫn UID tương ứng; kiểm tra Rules riêng khi có quyền truy cập Firebase | BO-01 |
| BC-02 | Tạo danh mục và task; sửa ưu tiên/ngày; tìm task; hoàn thành rồi bỏ hoàn thành; đối chiếu bốn nhóm tổng quan | BO-02 |
| BC-03 | Lưu task có lời nhắc hợp lệ, rồi thử lời nhắc quá hạn/vượt ngày đến hạn; đối chiếu việc xóa thời điểm nhắc nhưng vẫn lưu task | BO-03 |
| BC-04 | Tạo/sửa/xóa sự kiện; đối chiếu mốc 08:00 hôm trước/ngày diễn ra và nhánh bỏ qua mốc quá khứ | BO-03 |
| BC-05 | Chạy hết phiên tập trung; hoàn tất thủ công khi mới chạy một phần; đối chiếu cách ghi thời lượng và chuyển chế độ | BO-04 |
| BC-06 | Kiểm tra thống kê với dữ liệu đầu ngày/đầu tuần, tên task trùng và trên 300 phiên; đối chiếu giới hạn đã đặc tả | BO-04 |
| BC-07 | Đổi giao diện, thử tài khoản password/Google và đăng xuất; phân biệt trạng thái lưu công tắc âm thanh với tác dụng phát âm thanh | BO-05 |

Các AC chi tiết và điều kiện biên nằm trong [User Stories & Acceptance Criteria](USER_STORIES_ACCEPTANCE_CRITERIA.md).

## 11. Rủi ro nghiệp vụ và câu hỏi cần xác nhận

| Mã | Hiện trạng / tác động | Câu hỏi cho chủ sản phẩm hoặc nhóm phát triển |
| --- | --- | --- |
| Q-01 | Hoàn tất Pomodoro thủ công lưu toàn bộ thời lượng cấu hình | Thời lượng cần phản ánh kế hoạch hay thời gian đã thực sự tập trung? |
| Q-02 | Thống kê giới hạn 300 phiên; các task cùng tên bị gộp | Có cần thống kê đầy đủ theo khoảng thời gian và định danh task? |
| Q-03 | Có luồng xóa dữ liệu task theo ngày, gồm dữ liệu cũ thiếu timestamp | Cần giữ lịch sử công việc bao lâu; có cần xác nhận hoặc khôi phục? |
| Q-04 | Bỏ hoàn thành không tự lên lại lời nhắc; xóa danh mục không hủy từng alarm | Lời nhắc cần được đồng bộ thế nào theo vòng đời task? |
| Q-05 | Xóa nhiều task và danh mục là các bước nối tiếp | Có chấp nhận kết quả xóa một phần nếu lỗi giữa chừng không? |
| Q-06 | Thoát màn/tiến trình ảnh hưởng việc lưu phiên; không có dịch vụ nền độc lập | Có yêu cầu tập trung liên tục khi rời app hoặc hệ thống dừng tiến trình? |
| Q-07 | Công tắc âm thanh chỉ được lưu; mã phát âm thanh chưa đọc cờ này | Có cần điều khiển âm Pomodoro, notification channel hay cả hai? |
| Q-08 | Một số thao tác cho thay đổi giao diện trước kết quả ghi dữ liệu, lỗi chưa rollback đầy đủ | Người dùng cần nhận biết và thử lại việc lưu thất bại như thế nào? |

Không đưa câu trả lời giả định của các câu hỏi này thành yêu cầu đã triển khai.

## 12. Căn cứ mã nguồn chính

| Chủ đề | Tệp và điểm đối chiếu |
| --- | --- |
| Xác thực và ánh xạ tên tài khoản | [LoginActivity](../../../app/src/main/java/com/example/ticktok/activity/LoginActivity.java) — `loginUser`, `firebaseAuthWithGoogle`, `showContactAdminDialog`; [RegisterActivity](../../../app/src/main/java/com/example/ticktok/activity/RegisterActivity.java) — `registerUser`; [AuthAccountMapper](../../../app/src/main/java/com/example/ticktok/util/AuthAccountMapper.java) — `toAuthEmail` |
| Đường dẫn dữ liệu | [UserFirestorePaths](../../../app/src/main/java/com/example/ticktok/util/UserFirestorePaths.java) — `getUserCollection` |
| Danh mục và dọn dữ liệu | [MainActivity](../../../app/src/main/java/com/example/ticktok/activity/MainActivity.java) — `deleteCategory`, `deleteTasksInBatches`, `maybeRunDailyCompletedTaskCleanup`, `deleteCompletedTasksBefore`; [CategoryRepository](../../../app/src/main/java/com/example/ticktok/repository/CategoryRepository.java) |
| Thêm/sửa task và lời nhắc | [AddTaskBottomSheetFragment](../../../app/src/main/java/com/example/ticktok/fragment/AddTaskBottomSheetFragment.java) — `handleSendTask`, `addNewTaskWithNextOrder`; [ReminderManager](../../../app/src/main/java/com/example/ticktok/reminder/ReminderManager.java) |
| Tổng quan và lịch | [WelcomeFragment](../../../app/src/main/java/com/example/ticktok/fragment/WelcomeFragment.java), [TaskFilterFragment](../../../app/src/main/java/com/example/ticktok/fragment/TaskFilterFragment.java), [CalendarFragment](../../../app/src/main/java/com/example/ticktok/fragment/CalendarFragment.java) — `partitionAndRenderEisenhower` |
| Sự kiện | [AddEventBottomSheetFragment](../../../app/src/main/java/com/example/ticktok/fragment/AddEventBottomSheetFragment.java), [EventReminderManager](../../../app/src/main/java/com/example/ticktok/reminder/EventReminderManager.java), [EventAdapter](../../../app/src/main/java/com/example/ticktok/adapter/EventAdapter.java) |
| Tập trung và thống kê | [PomodoroFragment](../../../app/src/main/java/com/example/ticktok/fragment/PomodoroFragment.java) — `onSessionCompleted`, `savePomodoroHistory`, `reconcileRunningStateWithClock`; [FocusStatisticsActivity](../../../app/src/main/java/com/example/ticktok/activity/FocusStatisticsActivity.java) — `loadPomodoroData`, `handlePomodoroSnapshot` |
| Cài đặt | [SettingsActivity](../../../app/src/main/java/com/example/ticktok/activity/SettingsActivity.java), [TickTokApplication](../../../app/src/main/java/com/example/ticktok/TickTokApplication.java) |

Xem [SRS](SRS.md) cho mô tả kỹ thuật và giới hạn; xem [ma trận truy vết](../traceability/TRACEABILITY.csv) để đi từ yêu cầu nghiệp vụ sang chức năng, user story và use case.
