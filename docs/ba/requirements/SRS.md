# SRS — Đặc tả yêu cầu phần mềm TickTok

| Thuộc tính | Giá trị |
| --- | --- |
| Phiên bản tài liệu | 1.0 |
| Ngày đối chiếu | 18/11/2026 |
| Phạm vi | Ứng dụng Android trong repository hiện tại |
| Tài liệu tham chiếu | Mã Java, layout XML, cấu hình Gradle và manifest |
| Trạng thái | Bản thảo; phục vụ rà soát và kiểm thử |

## 1. Mục đích và cách đọc

SRS mô tả đầu vào, xử lý và đầu ra của các chức năng trong TickTok. Từ “hệ thống” chỉ ứng dụng TickTok và các điểm tích hợp được nêu rõ. Những giới hạn hoặc sai lệch hiện tại được ghi riêng, không xem là mục tiêu nghiệp vụ đã được chấp thuận.

Đọc cùng [BRD](BRD.md), [User Stories và Acceptance Criteria](USER_STORIES_ACCEPTANCE_CRITERIA.md), [Business Rules](BUSINESS_RULES.md), [sơ đồ use case](../use-cases/README.md) và [đặc tả use case](../use-cases/SPECIFICATIONS.md). Mã FR là định danh yêu cầu phần mềm; mã BR là định danh quy tắc dùng chung.

## 2. Bối cảnh và tác nhân

| Tác nhân/thành phần | Trách nhiệm trong phạm vi hiện tại |
| --- | --- |
| Người chưa đăng nhập | Đăng ký; đăng nhập bằng tài khoản/mật khẩu hoặc Google; mở hướng dẫn quên mật khẩu. |
| Người đã đăng nhập | Quản lý dữ liệu cá nhân, tập trung, xem/chia sẻ thống kê và cài đặt. Chưa có phân vai cộng tác viên/quản trị viên trong ứng dụng. |
| Firebase Authentication | Tạo tài khoản, xác thực và cập nhật mật khẩu; cung cấp UID cho đường dẫn dữ liệu. |
| Cloud Firestore | Đọc/ghi danh mục, công việc, sự kiện, phiên Pomodoro và cung cấp snapshot listener. |
| Google Sign-In | Trả ID token để trao đổi với Firebase Authentication. |
| Dịch vụ Android | Nhận dạng giọng nói, quyền micro/thông báo, lịch báo thức, phát thông báo và bảng chọn chia sẻ. |

Ứng dụng dùng Java/XML, `minSdk=24`, `targetSdk=36`, `compileSdk=36.1`; Firestore được gọi từ Activity/Fragment và DataSource danh mục. Không có máy chủ nghiệp vụ riêng, API cộng tác nhóm hoặc foreground service Pomodoro trong repository. Cấu hình cụ thể: [app/build.gradle.kts](../../../app/build.gradle.kts), [AndroidManifest.xml](../../../app/src/main/AndroidManifest.xml).

## 3. Yêu cầu chức năng

### 3.1. Tài khoản

| ID | Hành vi được đặc tả | UC | Nguồn |
| --- | --- | --- | --- |
| FR-AUTH-01 | Nhận tài khoản, mật khẩu, xác nhận mật khẩu; trim đầu/cuối; chặn trống, tài khoản không hợp lệ, hai mật khẩu khác nhau, mật khẩu dưới 6 ký tự; tạo tài khoản Firebase và cập nhật display name. Sau callback cập nhật profile, chuyển màn chính, kể cả khi callback profile thất bại. | UC-01 | [SRC-AUTH](#src-auth) |
| FR-AUTH-02 | Chấp nhận email hoặc username được ánh xạ; trim mật khẩu; chặn trống/username sai trước khi gọi Firebase. Trong lúc xác thực, vô hiệu hóa hai nút đăng nhập. Thành công mở màn chính; lỗi hiển thị thông báo, cho thử lại. Có Firebase user sẵn khi mở Login thì bỏ qua form. | UC-02 | [SRC-AUTH](#src-auth) |
| FR-AUTH-03 | Dùng `default_web_client_id` để yêu cầu Google ID token, sau đó gọi `signInWithCredential`. Thiếu cấu hình, dữ liệu kết quả, tài khoản hoặc token phải báo lỗi; không có đăng nhập Google nội bộ thay thế. | UC-03 | [SRC-AUTH](#src-auth) |
| FR-AUTH-04 | Chỉ hiển thị hàng đổi mật khẩu cho user có provider `password`. Mật khẩu mới sau trim tối thiểu 6 ký tự; gọi Firebase `updatePassword`; báo thành công hoặc yêu cầu đăng nhập lại khi thất bại. Không có form nhập lại mật khẩu cũ. | UC-16 | [SRC-SET](#src-set) |
| FR-AUTH-05 | Sau xác nhận đăng xuất, gọi Firebase `signOut`, xóa task stack màn hình và mở Login. Mã hiện tại không hủy toàn bộ alarm hoặc xóa SessionStore Pomodoro khi đăng xuất. | UC-17 | [SRC-SET](#src-set) |
| FR-AUTH-06 | Khi chọn quên mật khẩu, chỉ mở hộp thoại hướng dẫn liên hệ quản trị viên; không gửi email reset password. | UC-02 | [SRC-AUTH](#src-auth) |

Username hợp lệ khớp `^[a-zA-Z0-9._-]{3,30}$`; username được chuyển chữ thường và nối `@ticktok.user`. Chuỗi có `@` được chuyển chữ thường rồi giao cho Firebase xác thực định dạng. Xem BR-AUTH-01–06.

### 3.2. Danh mục

| ID | Hành vi được đặc tả | UC | Nguồn |
| --- | --- | --- | --- |
| FR-CAT-01 | Tên sau trim bắt buộc; biểu tượng trống dùng `≡`. Thêm danh mục có `order=1`, dịch thứ tự các danh mục cũ bằng batch. Không kiểm tra trùng tên. | UC-04 | [SRC-CAT](#src-cat) |
| FR-CAT-02 | Cập nhật tên và biểu tượng của ID hợp lệ; không cập nhật `order`. Nếu sửa danh mục đang chọn, cập nhật tiêu đề màn hình qua Fragment Result. | UC-04 | [SRC-CAT](#src-cat) |
| FR-CAT-03 | Xác nhận trước khi xóa. Xóa các task có cùng `categoryId` theo batch tối đa 450, sau đó xóa danh mục. Các bước không nằm trong một transaction tổng thể; nhánh xóa hàng loạt này không hủy alarm từng task. | UC-04 | [SRC-CAT](#src-cat) |
| FR-CAT-04 | Cho kéo sắp xếp danh mục người dùng; lưu thứ tự từ 1. Mục Welcome (`__welcome__`) luôn đứng đầu, không sửa/xóa/kéo. | UC-04 | [SRC-CAT](#src-cat) |

### 3.3. Công việc

| ID | Hành vi được đặc tả | UC | Nguồn |
| --- | --- | --- | --- |
| FR-TASK-01 | Nội dung sau trim không trống; dòng đầu làm tiêu đề, phần sau xuống dòng làm mô tả. Ngày hạn mặc định hôm nay hoặc ngày đang chọn ở lịch; chuẩn hóa 00:00 theo thiết bị. `categoryId` được lấy từ màn đang chọn và có thể null. Task mới chưa hoàn thành; `order` ban đầu là số giây Unix hiện tại. | UC-05 | [SRC-TASK](#src-task) |
| FR-TASK-02 | Mở lại dữ liệu hiện có trong cùng bottom sheet; cập nhật tiêu đề, mô tả, ưu tiên, ngày hạn, categoryId và reminderTime; không đổi cờ hoàn thành trong form. Reminder quá khứ hoặc từ ngày sau hạn bị xóa về 0, có thông báo; task vẫn được lưu. Sau ghi thành công, thiết lập lại/hủy alarm theo reminder mới. | UC-06 | [SRC-TASK](#src-task) |
| FR-TASK-03 | Checkbox cập nhật cả `isCompleted` và `completed`. Khi chọn hoàn thành, ghi `completedAt` bằng server timestamp và hủy reminder; khi bỏ chọn, đặt `completedAt=null`. Bỏ chọn không tự đặt lại alarm. | UC-07 | [SRC-TASK](#src-task) |
| FR-TASK-04 | Xác nhận xóa task, xóa document và hủy reminder khi ghi thành công. | UC-08 | [SRC-TASK](#src-task) |
| FR-TASK-05 | Kéo task trong màn danh mục, lưu `order` từ 1 theo batch tối đa 450. Danh sách danh mục sắp task chưa hoàn thành trước, rồi theo `order`. | UC-09 | [SRC-TASK](#src-task) |
| FR-TASK-06 | Yêu cầu quyền micro khi cần và kiểm tra dịch vụ nhận dạng; mở `ACTION_RECOGNIZE_SPEECH` với `vi-VN`, lấy kết quả đầu tiên. Nếu input trống thì thay nội dung; nếu đã có chữ thì nối dòng mới. Nút micro hiện khi input trống, nút gửi hiện khi có nội dung. Từ chối quyền, không có dịch vụ hoặc hủy nhận dạng không tạo task. | UC-18 | [SRC-TASK](#src-task) |

Quy tắc reminder áp dụng cho cả thêm/sửa: `reminderTime > now` và `reminderTime < dueDate + 86.400.000`. Đặt giờ nhắc không bắt buộc; không có reminder thì lưu `0`. Việc lưu task thành công không đồng nghĩa thiết bị đã cho phép hiển thị thông báo. Xem BR-TASK-01–09.

### 3.4. Danh sách, lịch và tìm kiếm

| ID | Hành vi được đặc tả | UC | Nguồn |
| --- | --- | --- | --- |
| FR-VIEW-01 | Welcome đếm task hôm nay, ngày mai, quá hạn chưa hoàn thành và task hoàn thành hôm nay. Các thẻ mở danh sách lọc tương ứng. | UC-09 | [SRC-VIEW](#src-view) |
| FR-VIEW-02 | Hôm nay/ngày mai so sánh dueDate bằng mốc 00:00; quá hạn là `0 < dueDate < todayStart`; hoàn thành hôm nay cần cờ hoàn thành và completedAt trong ngày. Danh sách thường theo order; quá hạn theo ngày hạn tăng; hoàn thành hôm nay theo completedAt giảm. | UC-09 | [SRC-VIEW](#src-view) |
| FR-VIEW-03 | Hiển thị lịch tháng hiện tại dạng lưới 42 ô, tuần bắt đầu Chủ nhật; chọn ngày để đọc task có dueDate trong khoảng ngày đó, chấm đánh dấu ngày có task. Chưa có điều khiển chuyển tháng trong mã hiện tại. | UC-09 | [SRC-VIEW](#src-view) |
| FR-VIEW-04 | Ma trận Eisenhower chỉ nhận task chưa hoàn thành, chia Q1/Q2/Q3/Q4 tương ứng priority 3/2/1/0. Không tự suy ra mức khẩn cấp từ dueDate. | UC-09 | [SRC-VIEW](#src-view) |
| FR-SEARCH-01 | Tìm cục bộ trong title + description của toàn bộ task đã tải. Chuẩn hóa NFD, bỏ combining marks, chuyển thường, trim rồi kiểm tra contains. Chưa ánh xạ riêng `đ` thành `d`. Query trống hiện hướng dẫn; không khớp hiện thông báo rỗng. Thứ tự: chưa hoàn thành trước, ngày hạn tăng, rồi order. Bấm kết quả có categoryId mở danh mục và highlight khoảng 1,2 giây; task không có categoryId không điều hướng. | UC-10 | [SRC-SEARCH](#src-search) |

Các khoảng ngày ở bộ lọc/lịch dùng hằng 24 giờ, trong khi mốc đầu ngày lấy từ Calendar. Do đó chưa bảo đảm tính đúng trên ngày đổi giờ mùa hè hoặc khi múi giờ thiết bị đổi trong lúc mở màn.

### 3.5. Sự kiện và thông báo

| ID | Hành vi được đặc tả | UC | Nguồn |
| --- | --- | --- | --- |
| FR-EVENT-01 | Tên sau trim không trống; phải chọn targetDate > 0 để bật lưu; biểu tượng trống dùng `●`. Lưu ngày diễn ra ở 00:00. Không chặn ngày trong quá khứ. | UC-11 | [SRC-EVENT](#src-event) |
| FR-EVENT-02 | Nạp tên, biểu tượng và ngày cũ; ghi ba trường đã sửa; sau thành công đặt lại reminder sự kiện. Trong lúc ghi, vô hiệu hóa lưu. | UC-11 | [SRC-EVENT](#src-event) |
| FR-EVENT-03 | Nhấn giữ để mở thao tác; xác nhận xóa; khi xóa Firestore thành công, hủy cả hai reminder của sự kiện. | UC-11 | [SRC-EVENT](#src-event) |
| FR-EVENT-04 | Danh sách theo targetDate tăng; nhãn `Còn N ngày`, `Hôm nay`, `Trễ N ngày`; số ngày dựa trên chỉ số ngày địa phương, không phải số khoảng 24 giờ còn lại. | UC-11 | [SRC-EVENT](#src-event) |
| FR-EVENT-05 | Đặt hai lịch lúc 08:00 ngày trước và ngày diễn ra theo múi giờ thiết bị, chỉ đặt mốc còn trong tương lai; hủy lịch cũ trước khi thay. Cả task/event dùng exact alarm nếu được phép, nếu không dùng lịch không chính xác. Android 13+ cần quyền POST_NOTIFICATIONS để receiver phát thông báo. | UC-11 | [SRC-REM](#src-rem) |

Thông báo dùng PendingIntent mở MainActivity. Receiver có truyền taskId cho task reminder nhưng MainActivity hiện chưa đọc extra này để tự mở đúng task; không đặc tả deep link đến task/sự kiện là tính năng đã có. Manifest không khai báo receiver khôi phục alarm sau reboot.

### 3.6. Pomodoro

| ID | Hành vi được đặc tả | UC | Nguồn |
| --- | --- | --- | --- |
| FR-POMO-01 | Cho chọn task chưa hoàn thành có title không trống; sắp priority giảm, khoảng cách tuyệt đối ngày hạn tới hôm nay tăng, ngày hạn tăng rồi tên. Không bắt buộc chọn task để bắt đầu. Task có thể đổi trong khi chạy; bản ghi lưu dùng tên đang chọn ở thời điểm lưu. | UC-12 | [SRC-POMO](#src-pomo) |
| FR-POMO-02 | Mặc định tập trung 25 phút/nghỉ 5 phút; preset 5, 15, 25, 45, 90 và nhập phút nguyên 5–90. Áp dụng khi đang chạy yêu cầu xác nhận rồi tạm dừng và đặt lại toàn bộ thời lượng mới, không giữ thời gian đã trôi qua. Điều chỉnh ở mode nghỉ chỉ áp dụng lần nghỉ đó; lần nghỉ tự động kế tiếp dùng 5 phút. | UC-12 | [SRC-POMO](#src-pomo) |
| FR-POMO-03 | Start chỉ khi chưa chạy/chưa pause; Pause giữ số còn lại; Resume chạy số còn lại; Reset về mode tập trung và thời lượng tập trung đã chọn. Nút hoàn thành chỉ xử lý phiên đang chạy hoặc pause; hoàn thành ở mode nghỉ không ghi lịch sử, thông báo và reset. | UC-12 | [SRC-POMO](#src-pomo) |
| FR-POMO-04 | Timer về 0 phát rung/âm báo khoảng một giây. Hết tập trung thì gọi lưu lịch sử, chuyển nghỉ và tự chạy ngay; hết nghỉ thì chuyển tập trung và tự chạy. Lưu bất đồng bộ không chặn chuyển mode. | UC-12 | [SRC-POMO](#src-pomo) |
| FR-POMO-05 | Lưu dưới users/{uid}/pomodoro khi hết tập trung tự nhiên hoặc người dùng bấm hoàn thành tập trung. Duration là `max(1,totalMillis/60000)`, kể cả hoàn thành sớm; không phải số phút thực đã chạy. Lưu userId, tên đang chọn hoặc Pomodoro, và giờ thiết bị lúc lưu; không lưu taskId. Hoàn thành thủ công reset cả khi ghi lỗi; phiên nghỉ không lưu. | UC-12 | [SRC-POMO](#src-pomo) |
| FR-POMO-06 | Dùng Bundle và SessionStore tĩnh để khôi phục trạng thái; khi view bị hủy thì cancel CountDownTimer. Nếu quay lại cùng tiến trình, dùng elapsedRealtime để tính mode/thời gian còn lại. Đoạn bù thời gian không ghi lịch sử các phiên đã đi qua khi view vắng mặt. Không có lưu bền vững toàn bộ timer/foreground service. | UC-12 | [SRC-POMO](#src-pomo) |

### 3.7. Thống kê và cài đặt

| ID | Hành vi được đặc tả | UC | Nguồn |
| --- | --- | --- | --- |
| FR-STAT-01 | Đọc tối đa 300 document Pomodoro mới nhất theo timestamp giảm. Tính số phiên và tổng phút cho hôm nay, tuần bắt đầu thứ Hai đến hiện tại theo Calendar thiết bị; loại timestamp tương lai. Giờ hôm nay hiển thị một chữ số thập phân; tuần hiển thị giờ/phút. | UC-13 | [SRC-STAT](#src-stat) |
| FR-STAT-02 | Biểu đồ donut chỉ dùng phiên hôm nay, cộng phút không âm theo taskName sau trim; tên rỗng thành `(Không rõ)`. Mục có tổng phút 0 không tạo lát cắt. Các task cùng tên bị gộp. Không có dữ liệu thì xóa biểu đồ và hiện nhãn rỗng. | UC-13 | [SRC-STAT](#src-stat) |
| FR-STAT-03 | Hiển thị tối đa 40 phiên hôm nay theo thứ tự mới nhất, gồm tên, giờ, nhãn phút và tag TẬP TRUNG. Không có màn phân trang lịch sử trong mã hiện tại. | UC-13 | [SRC-STAT](#src-stat) |
| FR-STAT-04 | Chia sẻ chuỗi văn bản gồm số phiên/giờ hôm nay và số phiên/thời gian tuần qua ACTION_SEND, type text/plain; nếu không mở được chooser thì báo lỗi. | UC-14 | [SRC-STAT](#src-stat) |
| FR-STAT-05 | Khi mở lại qua ngày hoặc đến nửa đêm lúc Activity đang hoạt động, tính lại từ snapshot gần nhất; tháo listener khi onStop và gắn lại khi onStart; hủy callback ngày khi onPause. Nếu không có user thì thông báo và đóng màn. | UC-13 | [SRC-STAT](#src-stat) |
| FR-SET-01 | Lưu lựa chọn giao diện hệ thống/sáng/tối trong prefs_settings, gọi AppCompatDelegate; áp dụng lại lúc Application khởi động. Một số màu màn hình/biểu đồ được hardcode, nên chưa khẳng định toàn bộ giao diện thích nghi theme. | UC-15 | [SRC-SET](#src-set) |
| FR-SET-02 | Đọc/lưu switch âm thanh, mặc định bật, trong SharedPreferences. Chưa thấy Pomodoro/NotificationReceiver đọc khóa này để thực sự tắt tiếng. | UC-15 | [SRC-SET](#src-set) |
| FR-CLEAN-01 | Khi MainActivity.onResume và chưa hoàn tất cleanup trong ngày cho UID, chạy dọn: đầu tiên xóa document có completedAt trước đầu hôm nay theo batch 450 **không kiểm tra cờ hoàn thành**; tiếp tục các lượt legacy theo completed=true/isCompleted=true, xóa khi thiếu completedAt hoặc timestamp cũ. Ghi khóa ngày sau khi toàn chuỗi thành công. Lượt legacy limit 450 không phân trang qua các bản ghi được giữ lại; chưa bảo đảm dọn hết mọi dữ liệu legacy. | UC-09 | [SRC-CLEAN](#src-clean) |

## 4. Dữ liệu và quy ước lưu trữ

```text
users/{uid}/categories/{categoryId}
users/{uid}/tasks/{taskId}
users/{uid}/events/{eventId}
users/{uid}/pomodoro/{sessionId}
```

`UserFirestorePaths` lấy UID từ FirebaseAuth và trả null nếu chưa có user. Việc tổ chức đường dẫn chưa chứng minh quyền truy cập được bảo vệ ở backend: repository không kèm bản rules Firestore đang triển khai. Xem [model](../../../app/src/main/java/com/example/ticktok/model) và [UserFirestorePaths](../../../app/src/main/java/com/example/ticktok/util/UserFirestorePaths.java).

| Đối tượng/trường | Kiểu, ý nghĩa, giá trị hiện tại |
| --- | --- |
| Category.id | String document ID; `__welcome__` là mục điều hướng tổng hợp, không phải danh mục người dùng tạo. |
| Category.title/icon/order | String tên bắt buộc sau trim; String biểu tượng mặc định `≡`; int thứ tự. Không ràng buộc unique title. |
| Task.id/title/description | String ID; String tiêu đề từ dòng đầu; String mô tả từ phần còn lại, có thể rỗng. |
| Task.categoryId | String có thể null; liên kết mềm đến Category, không có foreign key do ứng dụng/database tự bảo đảm. |
| Task.priority/order | int priority 0/1/2/3; int order để hiển thị. Thời điểm tạo dùng giây Unix cho order, sắp xếp thủ công dùng 1..n. |
| Trạng thái Task | Model dùng `isCompleted()`/`setCompleted()`; thao tác checkbox ghi cả trường `completed` và `isCompleted` để tương thích dữ liệu. Không có enum workflow ngoài hoàn thành/chưa hoàn thành. |
| Task.dueDate/reminderTime | Long mili giây Unix; dueDate chuẩn hóa 00:00; reminderTime 0 nghĩa không nhắc. Model chấp nhận null từ dữ liệu cũ. |
| Task.createdAt/completedAt | Date/Firestore timestamp; createdAt bằng server timestamp, completedAt bằng server timestamp khi hoàn thành hoặc null khi mở lại. Chưa có lịch sử audit các lần chuyển trạng thái. |
| Event.id/title/icon/targetDate | String ID, tên, icon mặc định `●`; Long mili giây Unix ngày diễn ra ở 00:00. |
| Event.createdAt | Date/server timestamp. |
| PomodoroSession.id/userId/taskName | ID; UID; tên task hoặc Pomodoro. Không có taskId/categoryId để join lịch sử. |
| PomodoroSession.duration/timestamp | long phút thời lượng cấu hình; long mili giây Unix theo đồng hồ thiết bị khi gọi ghi. |
| FocusRecord | Model giao diện bất biến: title, subtitle, durationLabel, tag. Không phải collection riêng. |

Task và Event có createdAt server timestamp; một số đường tạo còn cập nhật createdAt bằng một lệnh riêng sau add. Category không có trường createdAt trong model/DataSource hiện tại. Không đặc tả hai lệnh ghi timestamp là một giao dịch nguyên tử. Các thao tác ghi và snapshot callback là bất đồng bộ; tài liệu không đặt SLA online/offline hoặc cam kết đồng bộ tức thì trên mọi thiết bị.

## 5. Giao diện ngoài và vòng đời

| Điểm tích hợp | Đầu vào/đầu ra và xử lý hiện có |
| --- | --- |
| Firebase Auth | Tài khoản/mật khẩu hoặc credential Google → FirebaseUser hoặc lỗi callback. Không có quản trị người dùng trong client. |
| Firestore | Query/get/add/update/delete/batch, snapshot listener. Các màn tháo listener theo lifecycle; lỗi thường thành toast/empty state hoặc giữ dữ liệu cũ tùy màn. |
| Nhận dạng giọng nói | Activity Result với EXTRA_RESULTS; dùng kết quả đầu tiên, tiếng Việt. Chỉ dữ liệu văn bản được thêm vào input. |
| AlarmManager | PendingIntent theo ID task hoặc cặp eventId/type; hủy rồi thay thế. Phát thông báo cần quyền; thời gian giao thực tế phụ thuộc Android. |
| Thông báo | Hai channel task_reminder/event_reminder; mở MainActivity. Không cam kết mở đúng item vì chưa xử lý intent extra ở màn đích. |
| Chia sẻ | ACTION_SEND với nội dung tổng hợp; ứng dụng nhận và việc gửi tiếp do người dùng chọn. |
| SharedPreferences | Theme, switch âm thanh và khóa ngày cleanup theo UID. SessionStore Pomodoro là trạng thái static, không phải prefs. |

## 6. Ràng buộc chất lượng và giới hạn xác minh

| ID | Ràng buộc/hành vi có bằng chứng | Mức xác minh và cách đánh giá |
| --- | --- | --- |
| NFR-01 Tương thích | Manifest/build đặt Android 7.0+; Java source/target 11. | Cần kiểm thử trên các thiết bị/API được hỗ trợ. |
| NFR-02 Phân tách tài khoản | Client xây dựng đường dẫn dưới UID hiện tại. | Cần kiểm thử Firestore Rules với truy cập chéo tài khoản. |
| NFR-03 Phản hồi giao diện | Một số thao tác có loading/disable nút; snapshot cập nhật danh sách; timer tick 1 giây. | Chưa đo độ trễ, tính sẵn sàng, khả năng chịu tải hoặc giới hạn số người dùng. Không coi chu kỳ tick là SLA cập nhật dữ liệu. |
| NFR-04 Tính nhất quán | Xóa danh mục/task nhiều batch và ghi + đặt alarm là nhiều bước độc lập. Adapter checkbox đổi model cục bộ trước phản hồi. | Chưa có rollback đồng nhất hoặc đảm bảo exactly-once khi lỗi mạng; cần kiểm thử lỗi từng bước. |
| NFR-05 Duy trì phiên | Có Bundle/SessionStore và tính bù elapsedRealtime; view bị hủy thì timer bị cancel. | Chưa bảo đảm timer/lịch sử khi process bị kill, reboot hoặc thay tài khoản. |
| NFR-06 Địa phương hóa | Nhiều nhãn tiếng Việt; ngày theo Calendar/Locale thiết bị. | Chưa có cam kết đa ngôn ngữ, kiểm thử DST, timezone change hay accessibility toàn diện. |
| NFR-07 Khả năng kiểm thử | Repository danh mục có interface/data source; test hiện hữu chỉ là ví dụ JUnit/instrumentation. | Chưa có bộ test nghiệp vụ hoặc biên bản UAT trong repository. |

Các mục tiêu chất lượng như thời gian phản hồi tối đa, tỷ lệ sẵn sàng, accessibility, số lượng người dùng, bảo toàn dữ liệu khi mất mạng cần thống nhất và đo ở vòng tiếp theo; tài liệu này không gán con số chưa được thử nghiệm.

## 7. Cách xác minh chức năng

Các tình huống kiểm tra chức năng: Dùng Firebase project thử nghiệm, dữ liệu có thể xóa và thiết bị có các trạng thái quyền khác nhau.

| Nhóm | Dữ liệu/tình huống cần kiểm tra | Kết quả cần đối chiếu |
| --- | --- | --- |
| AUTH | Username hợp lệ/sai, password 5/6 ký tự, xác nhận sai, tài khoản có sẵn, Google hủy/thiếu token. | FR-AUTH-01..06; kiểm tra thông báo và trạng thái loading. |
| TASK/CAT | Nội dung nhiều dòng; task không có danh mục; reminder=now, trước now, cuối ngày hạn và đúng đầu ngày sau; xóa danh mục chứa nhiều task. | FR-TASK-01..06, FR-CAT-01..04; kiểm tra dữ liệu và alarm riêng từng bước. |
| VIEW/SEARCH | Task hôm nay/ngày mai/quá hạn/hoàn thành; search khác hoa/dấu và `đ/d`; bốn priority. | FR-VIEW-01..04, FR-SEARCH-01; đối chiếu bộ lọc và ma trận. |
| EVENT | Chưa chọn ngày; tên trống; ngày quá khứ; sửa ngày; xóa; quyền thông báo bật/tắt. | FR-EVENT-01..05; không đòi mốc reminder quá khứ phải phát. |
| POMO | 4/5/90/91 phút; pause/resume; complete sớm; hết giờ; rời màn qua một chu kỳ; hủy tiến trình. | FR-POMO-01..06; lưu thời lượng cấu hình, xác nhận giới hạn khôi phục/lịch sử. |
| STAT | Cùng tên task; duration âm/0; timestamp tương lai; hơn 40 phiên hôm nay, hơn 300 phiên; qua Chủ nhật/thứ Hai/nửa đêm. | FR-STAT-01..05; thống kê theo tập đã tải, không coi là tổng toàn lịch sử. |
| CLEAN/SET | completedAt cũ nhưng cờ false; completed thiếu timestamp; hơn 450 dữ liệu legacy; đổi theme và switch âm thanh. | FR-CLEAN-01, FR-SET-01..02; ghi nhận sự khác nhau giữa ý định và hành vi hiện tại. |

## 8. Nguồn đối chiếu

### SRC-AUTH

[LoginActivity](../../../app/src/main/java/com/example/ticktok/activity/LoginActivity.java): `loginUser`, `startGoogleSignIn`, `firebaseAuthWithGoogle`, `showContactAdminDialog`; [RegisterActivity](../../../app/src/main/java/com/example/ticktok/activity/RegisterActivity.java): `registerUser`; [AuthAccountMapper](../../../app/src/main/java/com/example/ticktok/util/AuthAccountMapper.java).

### SRC-CAT

[CategoryRepository](../../../app/src/main/java/com/example/ticktok/repository/CategoryRepository.java); [FirestoreCategoryDataSource](../../../app/src/main/java/com/example/ticktok/repository/FirestoreCategoryDataSource.java); [MainActivity](../../../app/src/main/java/com/example/ticktok/activity/MainActivity.java): `deleteCategory`, `deleteTasksForCategory`, `deleteTasksInBatches`, `persistMenuCategoryOrder`.

### SRC-TASK

[AddTaskBottomSheetFragment](../../../app/src/main/java/com/example/ticktok/fragment/AddTaskBottomSheetFragment.java): `handleSendTask`, `addNewTaskWithNextOrder`, `extractTitle`, `extractDescription`, `validateReminderAgainstDueDate`, `startVoiceInput`; [CategoryFragment](../../../app/src/main/java/com/example/ticktok/fragment/CategoryFragment.java): `onTaskCheckedChanged`, `deleteTask`, `persistTaskOrder`; [TaskAdapter](../../../app/src/main/java/com/example/ticktok/adapter/TaskAdapter.java): `onBindViewHolder`. Các màn Search/Calendar/TaskFilter cũng có handler checkbox/xóa.

### SRC-VIEW

[WelcomeFragment](../../../app/src/main/java/com/example/ticktok/fragment/WelcomeFragment.java): `computeAndUpdateCounts`; [TaskFilterFragment](../../../app/src/main/java/com/example/ticktok/fragment/TaskFilterFragment.java): `filterTasks`, `sortFiltered`; [CalendarFragment](../../../app/src/main/java/com/example/ticktok/fragment/CalendarFragment.java): `daysInMonthList`, `startTaskListener`, `partitionAndRenderEisenhower`.

### SRC-SEARCH

[SearchFragment](../../../app/src/main/java/com/example/ticktok/fragment/SearchFragment.java): `applyFilter`, `normalizeForSearch`, `onTaskClicked`; [CategoryFragment](../../../app/src/main/java/com/example/ticktok/fragment/CategoryFragment.java): `maybeScrollToHighlightedTask`.

### SRC-EVENT

[AddEventBottomSheetFragment](../../../app/src/main/java/com/example/ticktok/fragment/AddEventBottomSheetFragment.java): `handleSaveAction`, `updateSaveEnabledState`; [EventFragment](../../../app/src/main/java/com/example/ticktok/fragment/EventFragment.java): `deleteEvent`, `startEventListener`; [EventAdapter](../../../app/src/main/java/com/example/ticktok/adapter/EventAdapter.java): `calculateDaysRemaining`, `toLocalDayIndex`.

### SRC-REM

[ReminderManager](../../../app/src/main/java/com/example/ticktok/reminder/ReminderManager.java), [EventReminderManager](../../../app/src/main/java/com/example/ticktok/reminder/EventReminderManager.java), [NotificationReceiver](../../../app/src/main/java/com/example/ticktok/reminder/NotificationReceiver.java).

### SRC-POMO

[PomodoroFragment](../../../app/src/main/java/com/example/ticktok/fragment/PomodoroFragment.java): `handleCompleteButtonClick`, `onSessionCompleted`, `savePomodoroHistory`, `applyDurationMillis`, `restoreTimerState`, `restoreFromSessionStore`, `reconcileRunningStateWithClock`, `sortTasksForPicker`.

### SRC-STAT

[FocusStatisticsActivity](../../../app/src/main/java/com/example/ticktok/activity/FocusStatisticsActivity.java): `loadPomodoroData`, `handlePomodoroSnapshot`, `getStartOfWeekMillis`, `loadChartData`, `shareCurrentStatistics`, `scheduleNextMidnightRefresh`; [FocusRecordAdapter](../../../app/src/main/java/com/example/ticktok/adapter/FocusRecordAdapter.java).

### SRC-SET

[SettingsActivity](../../../app/src/main/java/com/example/ticktok/activity/SettingsActivity.java): `showChangePasswordDialog`, `setupSoundNotificationSwitch`, `showThemeDialog`, `performLogout`; [TickTokApplication](../../../app/src/main/java/com/example/ticktok/TickTokApplication.java).

### SRC-CLEAN

[MainActivity](../../../app/src/main/java/com/example/ticktok/activity/MainActivity.java): `onResume`, `maybeRunDailyCompletedTaskCleanup`, `deleteCompletedTasksBefore`, `purgeCompletedTasksWithoutTimestamp`.
