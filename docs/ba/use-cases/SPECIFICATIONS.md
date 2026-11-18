# Đặc tả các use case quan trọng — TickTok

Phiên bản: **1.0** · Ngày cập nhật: **18/11/2026**. Tài liệu đặc tả luồng xử lý của các use case trọng tâm trong TickTok.

Mã UC theo [danh mục và sơ đồ use case](README.md). Mã FR theo [SRS](../requirements/SRS.md), mã BR theo [Business Rules](../requirements/BUSINESS_RULES.md). “Ghi thành công” là callback thành công của thao tác Firestore/Firebase; không bao gồm cam kết alarm chắc chắn phát hoặc giao dịch nhiều bước đã nguyên tử.

## UC-02 — Đăng nhập bằng tài khoản và mật khẩu

| Thuộc tính | Nội dung |
| --- | --- |
| Mục tiêu | Xác thực người dùng để truy cập dữ liệu của UID tương ứng. |
| Tác nhân chính | Người chưa đăng nhập. |
| Tác nhân hỗ trợ | Firebase Authentication. |
| Trigger | Chọn nút Đăng nhập tại LoginActivity. |
| Tiền điều kiện | Form Login đã mở; Firebase project và provider Email/Password đã cấu hình. Luồng thành công giả định Firebase nhận và xử lý được yêu cầu. |
| Dữ liệu | Account input, password. |
| Liên kết | FR-AUTH-02, FR-AUTH-06; BR-AUTH-01, BR-AUTH-03, BR-AUTH-06. |

### Luồng chính

1. Người dùng nhập account input và password, bấm Đăng nhập.
2. Hệ thống ẩn bàn phím, trim đầu/cuối hai chuỗi và kiểm tra không trống.
3. Hệ thống ánh xạ username hợp lệ thành email nội bộ; với email thì chuyển chữ thường.
4. Hệ thống vô hiệu hóa nút đăng nhập thường và Google, gửi email đã ánh xạ và password đến Firebase Authentication.
5. Firebase trả kết quả thành công; hệ thống kết thúc loading, mở MainActivity và đóng LoginActivity.
6. MainActivity kiểm tra current user trong onResume, tải dữ liệu theo UID. Cleanup theo ngày có thể chạy tại đây theo FR-CLEAN-01.

### Luồng thay thế và ngoại lệ

| Mã | Điểm rẽ | Xử lý và điểm kết thúc/quay lại |
| --- | --- | --- |
| A1 | Mở Login khi đã có Firebase current user | Bỏ qua form, mở MainActivity và đóng Login. Không gọi đăng nhập lại. |
| A2 | Người dùng chọn Đăng ký | Mở RegisterActivity, thực hiện UC-01. |
| A3 | Người dùng chọn Quên mật khẩu | Hiện hướng dẫn liên hệ quản trị viên; đóng hộp thoại để quay lại form. Không gửi email khôi phục. |
| A4 | Người dùng chọn Google | Thực hiện UC-03 riêng; không đi tiếp bước 3–5 của luồng email/password. |
| E1 | Bước 2: một chuỗi trống sau trim | Báo thiếu thông tin, không gọi Firebase; quay lại nhập liệu. |
| E2 | Bước 3: username sai regex | Báo tài khoản không hợp lệ; không gửi yêu cầu. Chuỗi có @ được giao cho Firebase quyết định hợp lệ. |
| E3 | Bước 4: xác thực/mạng/Firebase thất bại | Bật lại các nút, hiện thông báo từ exception hoặc thông báo mặc định; giữ màn Login để sửa và thử lại. Không khẳng định mọi nguyên nhân lỗi đều được phân loại riêng. |

**Hậu điều kiện thành công:** Firebase có current user, người dùng ở MainActivity. **Hậu điều kiện thất bại:** vẫn ở form; không tạo dữ liệu nghiệp vụ mới. Password được trim trong code hiện tại, do đó khoảng trắng đầu/cuối không được giữ nguyên như một phần mật khẩu.

**Nguồn:** [LoginActivity](../../../app/src/main/java/com/example/ticktok/activity/LoginActivity.java) — `onCreate`, `loginUser`, `showContactAdminDialog`; [AuthAccountMapper](../../../app/src/main/java/com/example/ticktok/util/AuthAccountMapper.java).

## UC-05 — Tạo công việc và đặt nhắc tùy chọn

| Thuộc tính | Nội dung |
| --- | --- |
| Mục tiêu | Tạo task có tiêu đề, ngày hạn, mức ưu tiên và lời nhắc tùy chọn. |
| Tác nhân chính | Người đã đăng nhập. |
| Tác nhân hỗ trợ | Firestore; dịch vụ nhận dạng giọng nói; Android permission/alarm/notification services. |
| Trigger | Bấm nút + tại màn cho phép thêm task. |
| Tiền điều kiện | Current user tồn tại; bottom sheet chưa mở trùng tag; luồng chính giả định ghi Firestore thành công. |
| Dữ liệu | Raw text; categoryId theo màn đang chọn (có thể null); dueDate; priority 0..3; reminderTime tùy chọn. |
| Liên kết | FR-TASK-01, FR-TASK-06; BR-TASK-01..05, BR-TASK-08..09. |

### Luồng chính

1. Hệ thống mở AddTaskBottomSheetFragment; nếu đang ở Calendar thì điền sẵn ngày đang chọn, nếu ở danh mục thì truyền categoryId.
2. Người dùng nhập dòng đầu làm tiêu đề; nếu có mô tả, nhập các dòng tiếp theo.
3. Người dùng tùy chọn ngày hạn, ưu tiên, ngày/giờ nhắc. Mặc định ưu tiên 0; ngày hạn không chọn thì là hôm nay.
4. Người dùng gửi. Hệ thống trim toàn bộ input, kiểm tra không trống, tách title/description, chuẩn hóa ngày hạn về 00:00.
5. Hệ thống kiểm tra reminder. Reminder phải lớn hơn now và nhỏ hơn đầu ngày sau ngày hạn; giá trị không hợp lệ được xóa về 0 và báo cho người dùng, rồi tiếp tục tạo task.
6. Hệ thống lấy collection users/{uid}/tasks, tạo task chưa hoàn thành, completedAt null, order bằng giây Unix hiện tại và ghi document mới.
7. Sau callback ghi thành công, cập nhật createdAt bằng server timestamp; lấy document ID. Nếu reminder còn trong tương lai, yêu cầu quyền thông báo khi cần và gọi ReminderManager.
8. ReminderManager hủy lịch cùng taskId và đặt lịch mới nếu hợp lệ; dùng exact alarm khi được phép, nếu không thì dùng lịch không chính xác.
9. Hệ thống thông báo thêm thành công, đóng bottom sheet. Màn đang lắng nghe dữ liệu cập nhật danh sách nếu task thuộc phạm vi của màn đó.

### Luồng thay thế và ngoại lệ

| Mã | Điểm rẽ | Xử lý và điểm kết thúc/quay lại |
| --- | --- | --- |
| A1 | Bước 2: chọn micro khi input trống | UC-18: kiểm tra dịch vụ và quyền RECORD_AUDIO, mở nhận dạng tiếng Việt; lấy kết quả đầu tiên để điền input. Nếu có nội dung khi callback trả về thì nối bằng dòng mới. Sau đó tiếp tục bước 3. |
| A2 | Bước 3: không chọn reminder | Lưu reminderTime=0; không đặt alarm mới. |
| A3 | Bước 3/5: chọn reminder sai ngày hạn hoặc không còn ở tương lai | Xóa reminder, hiện toast; task vẫn tiếp tục được lưu. Đây không phải lỗi chặn tạo task. |
| A4 | Tạo từ Welcome/bộ lọc/lịch không gắn danh mục | categoryId có thể null; task có thể hiện ở lịch/bộ lọc nhưng không có danh mục để mở từ kết quả search. |
| E1 | Bước 4: input trống sau trim | Báo cần nhập nội dung; không ghi Firestore; giữ form. |
| E2 | Bước 6: không có current user/collection | Báo cần đăng nhập; không ghi dữ liệu. |
| E3 | Bước 6: add thất bại | Hiện lỗi từ callback; không thông báo thêm thành công; form còn để thử lại. Không có cơ chế idempotency ngăn tạo trùng khi gửi nhiều lần hoặc retry một yêu cầu không rõ kết quả. |
| E4 | Bước 7/8: người dùng từ chối quyền thông báo | Task vẫn tồn tại; receiver không hiển thị thông báo khi thiếu quyền trên Android 13+. Yêu cầu quyền và thiết lập lịch không được xử lý thành một giao dịch chặn lưu task. |
| E5 | Bước 7: lệnh cập nhật createdAt riêng gặp lỗi | Code không có xử lý lỗi riêng của lệnh này; không suy ra add task đã rollback. |
| E6 | A1: không có nhận dạng, hủy hoặc từ chối micro | Không tạo task từ voice; có thể nhập bằng bàn phím và tiếp tục. |

**Hậu điều kiện thành công:** Có document task mới theo UID; alarm là tác dụng phụ có điều kiện. **Hậu điều kiện thất bại:** lỗi validation chưa tạo document; lỗi sau add có thể để lại document đã lưu. Các trường khác nhau không được ghi/đặt lịch trong một transaction tổng thể.

**Nguồn:** [MainActivity](../../../app/src/main/java/com/example/ticktok/activity/MainActivity.java) — `openAddTaskBottomSheet`; [AddTaskBottomSheetFragment](../../../app/src/main/java/com/example/ticktok/fragment/AddTaskBottomSheetFragment.java) — `handleSendTask`, `addNewTaskWithNextOrder`, `startVoiceInput`; [ReminderManager](../../../app/src/main/java/com/example/ticktok/reminder/ReminderManager.java).

## UC-07 — Đánh dấu hoàn thành hoặc mở lại công việc

| Thuộc tính | Nội dung |
| --- | --- |
| Mục tiêu | Cập nhật trạng thái hoàn thành của một task. |
| Tác nhân chính | Người đã đăng nhập. |
| Tác nhân hỗ trợ | Firestore, Android AlarmManager. |
| Trigger | Chọn/bỏ chọn checkbox ở danh mục, bộ lọc, search, lịch hoặc ma trận. |
| Tiền điều kiện | Task được hiển thị, có ID hợp lệ; current user tồn tại để lấy collection. |
| Liên kết | FR-TASK-03; BR-TASK-06; liên quan FR-CLEAN-01, BR-CLEAN-01..03. |

### Luồng chính: đánh dấu hoàn thành

1. Người dùng chọn checkbox task chưa hoàn thành.
2. Adapter cập nhật model cục bộ thành completed và điều chỉnh cách hiển thị.
3. Handler kiểm tra ID, gọi hủy reminder của task.
4. Handler lấy collection theo UID, gửi update đồng thời `isCompleted=true`, `completed=true`, `completedAt=serverTimestamp()`.
5. Snapshot của màn cập nhật danh sách/bộ đếm khi có dữ liệu: task có thể đổi vị trí hoặc không còn thuộc bộ lọc chưa hoàn thành.

### Luồng thay thế và ngoại lệ

| Mã | Điểm rẽ | Xử lý và điểm kết thúc/quay lại |
| --- | --- | --- |
| A1 | Bước 1: bỏ chọn task đã hoàn thành | Adapter đổi model thành chưa hoàn thành; ghi hai cờ false và completedAt=null. Không tự đặt lại reminder đã hủy. |
| E1 | Bước 3: ID trống | Handler dừng, không gửi update. Adapter có thể đã đổi trạng thái cục bộ. |
| E2 | Bước 4: không có current user | Handler không ghi. Màn danh mục báo cần đăng nhập, một số màn khác chỉ return. Không có rollback chung cho adapter hoặc alarm đã hủy. |
| E3 | Bước 4: Firestore update thất bại | Màn danh mục/search có failure toast; bộ lọc/lịch không có xử lý failure tương đương. Không có rollback UI/alarm thống nhất. Cần nạp lại để đối chiếu trạng thái backend. |

**Hậu điều kiện thành công:** Hai trường trạng thái và completedAt được ghi theo thao tác. **Hậu điều kiện thất bại:** Không được khẳng định UI, backend và alarm đồng bộ; reminder có thể đã bị hủy trước khi backend báo lỗi. Đây là khác biệt hiện tại cần ghi nhận khi kiểm thử, không phải chính sách nghiệp vụ mong muốn.

Khi quay về MainActivity ngày sau, cleanup có thể xóa task có completedAt trước hôm nay; dữ liệu legacy thiếu timestamp được xét riêng. Không có lịch sử hoàn thành dài hạn hay thùng rác task.

**Nguồn:** [TaskAdapter](../../../app/src/main/java/com/example/ticktok/adapter/TaskAdapter.java), [EisenhowerTaskAdapter](../../../app/src/main/java/com/example/ticktok/adapter/EisenhowerTaskAdapter.java); handler `onTaskCheckedChanged` ở [CategoryFragment](../../../app/src/main/java/com/example/ticktok/fragment/CategoryFragment.java), [TaskFilterFragment](../../../app/src/main/java/com/example/ticktok/fragment/TaskFilterFragment.java), [CalendarFragment](../../../app/src/main/java/com/example/ticktok/fragment/CalendarFragment.java), [SearchFragment](../../../app/src/main/java/com/example/ticktok/fragment/SearchFragment.java).

## UC-11 — Tạo/cập nhật sự kiện và đặt hai lịch nhắc

| Thuộc tính | Nội dung |
| --- | --- |
| Mục tiêu | Theo dõi một mốc ngày và nhận nhắc khi các mốc nhắc còn trong tương lai. |
| Tác nhân chính | Người đã đăng nhập. |
| Tác nhân hỗ trợ | Firestore; Android permission/alarm/notification services. |
| Trigger | Bấm + ở màn sự kiện, hoặc chọn Sửa từ menu nhấn giữ sự kiện. |
| Tiền điều kiện | Current user tồn tại; sự kiện có ID hợp lệ trong nhánh sửa. |
| Dữ liệu | Title, icon, targetDate (00:00 địa phương). |
| Liên kết | FR-EVENT-01..05; BR-EVENT-01..04. |

### Luồng chính: tạo sự kiện

1. Hệ thống mở form thêm sự kiện, chưa chọn ngày nên nút Lưu bị vô hiệu hóa.
2. Người dùng nhập tên, chọn biểu tượng và ngày diễn ra. Hệ thống chuẩn hóa ngày về 00:00, hiện nhãn ngày và bật Lưu.
3. Người dùng lưu; hệ thống kiểm tra tên sau trim không trống, targetDate>0; icon trống dùng `●`.
4. Hệ thống bật trạng thái đang lưu, vô hiệu hóa Lưu và ghi document Event mới vào collection users/{uid}/events.
5. Khi add thành công, lấy ID, cập nhật createdAt server timestamp và yêu cầu quyền thông báo khi cần.
6. EventReminderManager hủy lịch cũ cùng eventId; tính hai mốc 08:00 ngày trước và 08:00 ngày diễn ra; chỉ đặt những mốc lớn hơn now.
7. Hệ thống báo thành công, đóng form. Listener hiển thị sự kiện theo targetDate tăng và tính countdown.

### Luồng thay thế và ngoại lệ

| Mã | Điểm rẽ | Xử lý và điểm kết thúc/quay lại |
| --- | --- | --- |
| A1 | Trigger sửa | Điền sẵn title/icon/date; cập nhật ba trường trên cùng document, rồi đặt lại các lịch; không tạo sự kiện mới. |
| A2 | Bước 2: chọn ngày quá khứ | Vẫn được lưu nếu targetDate>0. Countdown có thể là Trễ N ngày; mốc nhắc đã qua bị bỏ qua. |
| A3 | Menu sự kiện: Xóa | Xác nhận, xóa document. Khi xóa thành công, hủy hai reminder, cập nhật danh sách; hủy xác nhận thì giữ nguyên. |
| E1 | Bước 3: tên trống | Hiện hướng dẫn nhập tên, không ghi; form vẫn mở. |
| E2 | Bước 1/3: chưa chọn ngày | Nút Lưu không khả dụng; guard trong handler cũng dừng nếu selectedTargetDate<=0. |
| E3 | Bước 4: không có collection hoặc ID nhánh sửa không hợp lệ | Báo lỗi/đăng nhập, kết thúc trạng thái đang lưu, không gửi ghi hợp lệ. |
| E4 | Bước 4: ghi thất bại | Bật lại khả năng lưu theo ngày đang chọn, hiện lỗi, giữ form. |
| E5 | Bước 5/6: thiếu quyền thông báo hoặc AlarmManager | Sự kiện vẫn được lưu; việc nhận thông báo không được bảo đảm. Exact alarm không được phép thì dùng lịch không chính xác. |

**Hậu điều kiện thành công:** Event tồn tại/cập nhật, danh sách theo dõi được; có 0–2 lịch mới tùy mốc thời gian và khả năng thiết bị. Tính countdown là hiển thị lúc bind dữ liệu; chưa có bộ hẹn tự refresh sự kiện tại nửa đêm như màn thống kê.

**Nguồn:** [AddEventBottomSheetFragment](../../../app/src/main/java/com/example/ticktok/fragment/AddEventBottomSheetFragment.java) — `handleSaveAction`, `updateSaveEnabledState`; [EventFragment](../../../app/src/main/java/com/example/ticktok/fragment/EventFragment.java); [EventAdapter](../../../app/src/main/java/com/example/ticktok/adapter/EventAdapter.java); [EventReminderManager](../../../app/src/main/java/com/example/ticktok/reminder/EventReminderManager.java).

## UC-12 — Thực hiện phiên Pomodoro và lưu lịch sử tập trung

| Thuộc tính | Nội dung |
| --- | --- |
| Mục tiêu | Chạy bộ đếm tập trung/nghỉ và ghi phiên tập trung. |
| Tác nhân chính | Người sử dụng Pomodoro; lưu lịch sử yêu cầu Firebase current user. |
| Tác nhân hỗ trợ | Firestore; đồng hồ, âm thanh và rung Android. |
| Trigger | Mở Pomodoro và chọn Bắt đầu. |
| Tiền điều kiện | Fragment có view; chưa chạy/chưa pause để dùng Start. Luồng ghi thành công giả định current user và Firestore phản hồi. |
| Dữ liệu | Mode FOCUS/BREAK; selectedFocusDurationMillis; totalMillis; remainingMillis; selectedTaskId/title; cờ running/paused. |
| Liên kết | FR-POMO-01..06; BR-POMO-01..06. |

### Luồng chính: hết phiên tập trung tự nhiên

1. Hệ thống hiện 25:00 ở mode FOCUS nếu chưa có trạng thái khôi phục; người dùng tùy chọn task chưa hoàn thành hoặc giữ tên mặc định Pomodoro.
2. Người dùng tùy chọn thời lượng phút nguyên trong 5–90; hệ thống đặt totalMillis và remainingMillis theo lựa chọn.
3. Người dùng chọn Start; hệ thống đặt running=true, paused=false, ghi mốc kết thúc elapsedRealtime và chạy CountDownTimer.
4. Mỗi tick cập nhật thời gian còn lại, tiến độ và trạng thái nút; đồng bộ SessionStore.
5. Khi timer về 0, hệ thống phát âm/rung khoảng một giây, gọi lưu lịch sử nếu đang FOCUS.
6. Payload gồm UID, tên task đang chọn hoặc Pomodoro, `duration=max(1,totalMillis/60000)` và timestamp theo giờ thiết bị. Ghi bất đồng bộ vào users/{uid}/pomodoro.
7. Không chờ callback ghi, hệ thống chuyển sang BREAK 5 phút và tự Start. Hết BREAK thì chuyển FOCUS theo selectedFocusDurationMillis và tự Start; không ghi lịch sử cho BREAK.
8. Callback ghi thành công có thể báo đã lưu; thất bại có thể báo lỗi. Chu kỳ timer ở bước 7 tiếp tục độc lập.

### Luồng thay thế và ngoại lệ

| Mã | Điểm rẽ | Xử lý và điểm kết thúc/quay lại |
| --- | --- | --- |
| A1 | Bước 3/4: Pause rồi Resume | Hủy timer, giữ remainingMillis và paused=true; Resume tạo timer mới theo remainingMillis. |
| A2 | Bước 4: bấm Hoàn thành khi FOCUS đang chạy/pause | Dừng timer, gọi lưu theo **toàn bộ totalMillis**, không tính thời gian đã trôi. Callback thành công hoặc thất bại đều reset về FOCUS/thời lượng đã chọn, không tự chuyển nghỉ. Ví dụ cấu hình 25 phút, bấm sau 2 phút thì duration ghi là 25. |
| A3 | Bước 4: Reset | Hủy timer, đặt FOCUS, running=false, paused=false, remaining=selectedFocusDuration; không lưu phiên đang làm. |
| A4 | Bước 4: áp dụng thời lượng mới lúc chạy | Hiện xác nhận; đồng ý thì pause và đặt lại cả total/remaining bằng giá trị mới, vẫn paused. Hủy xác nhận không thay đổi timer. Nếu sửa ở mode nghỉ, thời lượng nghỉ tự động lần sau vẫn 5 phút. |
| A5 | Trong lúc chạy: đổi task đang chọn | Picker không khóa theo trạng thái chạy; các lần lưu sau dùng tên mới hiện hành. Không lưu ảnh chụp task tại lúc Start và không lưu taskId trong lịch sử. |
| A6 | View bị hủy rồi mở lại cùng tiến trình | Hủy CountDownTimer ở onDestroyView; lấy lại SessionStore, tính mode/thời gian theo elapsedRealtime. Các khoảng FOCUS đã đi qua lúc view vắng mặt không được ghi bù lịch sử. |
| E1 | Bước 2: không phải số nguyên hoặc ngoài 5–90 | Báo lỗi/đề nghị chọn thời lượng; không áp dụng. |
| E2 | Bước 6: không có UID | Auto-save bỏ qua; nhánh Complete thủ công thông báo nếu còn context và reset. Không tạo document. |
| E3 | A2 khi đang BREAK | Thông báo chỉ hoàn thành tập trung, reset; không lưu lịch sử nghỉ. |
| E4 | Bước 6: Firestore lỗi | Báo lỗi nếu còn context. Auto-cycle không rollback; Complete thủ công vẫn reset. Không có hàng đợi nghiệp vụ/idempotency do ứng dụng tự quản lý để chắc chắn tránh mất/trùng phiên. |
| E5 | A6: tiến trình bị kết thúc hoặc thay đổi tài khoản | SessionStore không phải lưu trữ bền vững/theo UID; không bảo đảm tiếp tục đầy đủ bộ đếm hoặc dữ liệu đang chọn. Đây là giới hạn, không phải luồng khôi phục thành công đã triển khai. |

**Hậu điều kiện thành công:** Có lịch sử FOCUS nếu callback ghi thành công; timer chuyển mode tự động hoặc reset tùy cách kết thúc. “Hoàn thành Pomodoro” không đổi checkbox hoàn thành task. **Hậu điều kiện lỗi:** timer có thể vẫn tiếp tục hoặc đã reset dù lịch sử chưa được ghi.

**Nguồn:** [PomodoroFragment](../../../app/src/main/java/com/example/ticktok/fragment/PomodoroFragment.java) — `handleCompleteButtonClick`, `startTimer`, `onSessionCompleted`, `savePomodoroHistory`, `applyDurationMillis`, `reconcileRunningStateWithClock`.

## UC-13 — Xem thống kê tập trung

| Thuộc tính | Nội dung |
| --- | --- |
| Mục tiêu | Xem số phiên/thời gian hôm nay, tuần này và phân bổ theo công việc. |
| Tác nhân chính | Người đã đăng nhập. |
| Tác nhân hỗ trợ | Firestore, đồng hồ/múi giờ thiết bị; Android chooser trong nhánh chia sẻ. |
| Trigger | Bấm biểu tượng lịch sử ở Pomodoro để mở FocusStatisticsActivity. |
| Tiền điều kiện | Current user tồn tại; các document dùng duration phút, timestamp mili giây như model hiện tại. |
| Liên kết | FR-STAT-01..05; BR-STAT-01..05. Chia sẻ là UC-14. |

### Luồng chính

1. Hệ thống dựng bốn ô số liệu, danh sách và biểu đồ; gắn snapshot listener vào users/{uid}/pomodoro, order timestamp giảm, limit 300.
2. Khi có snapshot, hệ thống chuyển document thành PomodoroSession và lấy mốc đầu hôm nay, đầu tuần thứ Hai, now theo thiết bị.
3. Duyệt các phiên đã tải: phiên có timestamp trong khoảng tương ứng tới now được đếm; duration âm được tính 0 khi cộng phút.
4. Hiện số phiên/giờ hôm nay (một chữ số thập phân), số phiên/thời lượng tuần dạng giờ/phút.
5. Gộp các phiên hôm nay theo tên sau trim, cộng phút để vẽ donut; chỉ vẽ tổng phút dương. Tên null/trống được gom `(Không rõ)`.
6. Lấy tối đa 40 phiên hôm nay mới nhất để hiển thị tên, thời gian và duration label. Phiên có duration 0 vẫn có thể được đếm/hiển thị trong danh sách dù không có lát cắt biểu đồ.
7. Snapshot mới cập nhật lại. Nếu qua ngày lúc màn hoạt động hoặc khi resume sang ngày mới, tính lại từ snapshot gần nhất; nếu chưa có snapshot thì tải lại.

### Luồng thay thế và ngoại lệ

| Mã | Điểm rẽ | Xử lý và điểm kết thúc/quay lại |
| --- | --- | --- |
| A1 | Không có phiên hôm nay | Hiện số hôm nay bằng 0, danh sách trống và trạng thái biểu đồ không có dữ liệu; tuần vẫn có thể có dữ liệu. |
| A2 | Có hơn 300 phiên trong kỳ | Chỉ tính từ 300 phiên mới nhất đã tải; không truy vấn bù để tính toàn bộ tuần/ngày. |
| A3 | Người dùng chọn chia sẻ | UC-14: đọc chuỗi đang hiển thị, mở ACTION_SEND text/plain gồm hôm nay và tuần này. Không chia sẻ ảnh biểu đồ. |
| A4 | Người dùng đóng/đưa màn ra nền | Nút đóng finish; onPause hủy callback nửa đêm; onStop tháo listener. onStart gắn lại listener khi quay lại. |
| E1 | Bước 1: không có current user | Báo cần đăng nhập và finish Activity; không đọc dữ liệu UID khác. |
| E2 | Bước 1/7: listener trả lỗi | Báo không tải được dữ liệu; không chuyển sang số liệu giả. Dữ liệu đang hiển thị có thể vẫn là snapshot trước. |
| E3 | A3: không mở được chooser | Báo không có ứng dụng chia sẻ; giữ màn thống kê. |

**Hậu điều kiện thành công:** Người dùng xem số liệu từ tập snapshot giới hạn 300; dữ liệu không bị cập nhật bởi thao tác xem. Tuần dùng timestamp kết thúc/lưu phiên, không chia nhỏ phiên đi qua nửa đêm. Các task trùng tên được gộp, kể cả khi là hai task khác ID.

**Nguồn:** [FocusStatisticsActivity](../../../app/src/main/java/com/example/ticktok/activity/FocusStatisticsActivity.java) — `loadPomodoroData`, `handlePomodoroSnapshot`, `loadChartData`, `getStartOfWeekMillis`, `dayChangeRunnable`, `shareCurrentStatistics`.

## Gợi ý kiểm tra các nhánh quan trọng

Đây là danh sách chuẩn bị thực thi, không phải kết quả test:

| Use case | Tình huống đại diện |
| --- | --- |
| UC-02 | Thiếu password; username 2/3/30/31 ký tự; email không hợp lệ; lỗi Firebase; user đã đăng nhập. |
| UC-05 | Nội dung nhiều dòng; không có categoryId; reminder quá khứ hoặc đúng 00:00 ngày sau hạn; từ chối quyền; gửi lặp. |
| UC-07 | Hoàn thành rồi bỏ chọn; update thất bại sau khi hủy alarm; nạp lại để đối chiếu trạng thái. |
| UC-11 | Chưa chọn ngày; tên trống; sự kiện quá khứ; chỉnh ngày; xóa; mốc nhắc 08:00 đã qua. |
| UC-12 | Complete sớm; BREAK Complete; đổi thời lượng lúc chạy; đổi task giữa phiên; rời màn qua một chu kỳ; lỗi ghi lịch sử. |
| UC-13 | 0/40/41 bản ghi hôm nay; 300/301 trong tuần; tên trùng/rỗng; qua nửa đêm/thứ Hai; timestamp tương lai. |
