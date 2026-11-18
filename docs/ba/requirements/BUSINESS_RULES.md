# Business Rules — TickTok

Phiên bản 1.0 · Ngày lập: 18/11/2026 · Phạm vi: mã nguồn hiện có.

## 1. Cách đọc

Tài liệu quy định điều kiện dữ liệu và cách xử lý nghiệp vụ của phiên bản TickTok hiện tại. Mỗi quy tắc gồm điều kiện, kết quả và vị trí đối chiếu trong mã nguồn. Các vấn đề cần làm rõ được tập hợp ở mục 12.

Các mã `BR-*` dùng để truy vết từ [SRS](SRS.md), [User Stories & Acceptance Criteria](USER_STORIES_ACCEPTANCE_CRITERIA.md) và [đặc tả use case](../use-cases/SPECIFICATIONS.md). Quyền sở hữu dữ liệu ở đây mô tả đường dẫn do client chọn; chưa thể xác nhận quyền truy cập phía server khi dự án không kèm rules triển khai.

## 2. Tài khoản — AUTH

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-AUTH-01 | Chuỗi tài khoản được `trim`. Nếu có `@`, chuyển chữ thường và gửi Firebase; nếu không có `@`, phải khớp `^[a-zA-Z0-9._-]{3,30}$`. | Username hợp lệ được chuyển thành `<username chữ thường>@ticktok.user`; app không tự kiểm tra cú pháp email đầy đủ trước Firebase. | [A1], `toAuthEmail` |
| BR-AUTH-02 | Đăng ký yêu cầu tài khoản, mật khẩu, xác nhận mật khẩu đều khác rỗng sau `trim`; hai mật khẩu phải bằng nhau và dài ít nhất 6 ký tự. | Vi phạm chặn yêu cầu tạo tài khoản và thông báo lỗi. Khi tạo Firebase account thành công, app cập nhật display name rồi điều hướng màn chính; kết quả cập nhật profile không được kiểm tra trước khi báo đăng ký thành công. | [A2], `registerUser` |
| BR-AUTH-03 | Đăng nhập mật khẩu kiểm tra trường rỗng, ánh xạ tài khoản rồi gọi Firebase. | Chỉ khi Firebase báo thành công mới mở màn chính. Khi đang xác thực, các nút đăng nhập bị vô hiệu hóa. Nếu đã có Firebase user lúc mở màn login thì bỏ qua form. | [A3], `loginUser`, `setAuthLoading`, `onCreate` |
| BR-AUTH-04 | Google Sign-In cần `default_web_client_id` khác rỗng và khác `YOUR_WEB_CLIENT_ID`, Google account và ID token hợp lệ. | Thiếu cấu hình, dữ liệu trả về hoặc token thì báo lỗi; credential hợp lệ được gửi Firebase để xác thực. | [A3], `startGoogleSignIn`, `firebaseAuthWithGoogle` |
| BR-AUTH-05 | Mục đổi mật khẩu hiển thị cho user có provider `password`; mật khẩu mới được `trim` và dài ít nhất 6 ký tự. | App gọi `updatePassword`; lỗi trả về được diễn đạt thành yêu cầu đăng nhập lại. Chưa có màn re-authentication riêng. | [A4], `onCreate`, `showChangePasswordDialog` |
| BR-AUTH-06 | Đăng xuất có bước xác nhận. Chọn đồng ý gọi Firebase `signOut` rồi xóa task stack và mở Login. Quên mật khẩu mở hộp thoại liên hệ quản trị viên. | Chưa có luồng gửi email reset mật khẩu; đăng xuất không gọi hủy tất cả alarm hoặc xóa `PomodoroFragment.SessionStore`. | [A4], `confirmLogout`, `performLogout`; [A3], `showContactAdminDialog` |
| BR-AUTH-07 | Collection dữ liệu nghiệp vụ được resolve theo current UID dưới `users/{uid}`; không có UID thì helper trả `null`. | Nhiều màn chặn thao tác hoặc hiện dữ liệu trống khi chưa đăng nhập. `MainActivity.onResume` đưa người dùng về Login nếu mất user. Đây không phải bằng chứng Firestore Rules đã được triển khai. | [A5]; [M1], `onResume` |

## 3. Danh mục — CAT

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-CAT-01 | Tên danh mục sau `trim` không được rỗng; icon rỗng được thay bằng `≡`. Khi sửa, ID cũng không được rỗng. | Dữ liệu không hợp lệ bị từ chối. Không có kiểm tra tên duy nhất hoặc độ dài tên trong repository. | [C1], `addCategory`, `updateCategory` |
| BR-CAT-02 | Tạo danh mục mới đọc toàn bộ danh mục, tăng `order` hiện tại lên 1 và đặt danh mục mới `order=1` trong một write batch. | Danh mục mới nằm đầu danh sách người dùng. `order` thiếu/không đọc được được xem là `Integer.MAX_VALUE`; trường hợp này không tăng thêm. Không dùng transaction để khóa lần đọc khi có nhiều client. | [C2], `runInsertAndShiftBatch` |
| BR-CAT-03 | Welcome là mục menu tổng quan với ID `__welcome__`, được tạo cục bộ và đặt ở vị trí đầu. | Không có thao tác sửa/xóa qua menu action; không kéo Welcome hoặc kéo danh mục khác qua vị trí Welcome. | [M1], `createWelcomeDrawerCategory`, `onCategoryLongPressed`, `setupDrawerMenu`; [C3] |
| BR-CAT-04 | Xóa danh mục cần xác nhận; app xóa các task có `categoryId` tương ứng theo batch tối đa 450 rồi mới xóa document danh mục. | Xóa task và danh mục không nằm trong một transaction chung. Nếu bước sau lỗi có thể còn danh mục nhưng một phần/toàn bộ task đã bị xóa. Luồng này không gọi hủy alarm của từng task. | [M1], `deleteCategory`, `deleteTasksForCategory`, `deleteTasksInBatches` |
| BR-CAT-05 | Sau kéo thả, danh mục người dùng được đánh lại `order=1..n`, bỏ qua Welcome rồi lưu batch. | Danh sách load được sắp tăng dần theo `order`; không có quy tắc duy nhất cho tên hoặc tự tạo các danh mục mẫu. | [M1], `persistMenuCategoryOrder`; [C1], `getCategories` |

## 4. Công việc — TASK

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-TASK-01 | Toàn bộ nội dung nhập được `trim` và không được rỗng. Dòng đầu là title; phần sau dấu xuống dòng đầu là description được `trim`. | Nội dung rỗng không lưu. Không có kiểm tra title duy nhất hoặc giới hạn độ dài ở tầng màn hình. | [T1], `handleSendTask`, `extractTitle`, `extractDescription` |
| BR-TASK-02 | Khi lưu, ngày đã chọn được chuẩn hóa về 00:00:00.000 của múi giờ thiết bị; chưa chọn ngày thì dùng đầu ngày hôm nay. | Task có thể không gắn danh mục (`categoryId=null`) khi tạo từ tổng quan/lịch/filter. Tạo từ lịch điền trước ngày đang chọn. Không có kiểm tra cấm ngày quá khứ. | [T1], `handleSendTask`, `normalizeToStartOfDay`; [M1], `openAddTaskBottomSheet` |
| BR-TASK-03 | Menu ưu tiên cung cấp 4 giá trị: 3=cao, 2=vừa, 1=thấp, 0=không ưu tiên; mặc định 0. | Đây là miền giá trị do UI cung cấp, không phải ràng buộc server. Không có hai thuộc tính quan trọng/khẩn cấp độc lập. | [T1], `showPriorityMenu`; [V3], `partitionAndRenderEisenhower` |
| BR-TASK-04 | Gọi `now` là thời điểm lưu, `D` là đầu ngày đến hạn; reminder hợp lệ phải `reminderTime > now` và `< D + 86.400.000 ms`. | Reminder trong quá khứ hoặc từ đầu ngày sau hạn trở đi bị đưa về `0` và thông báo; task vẫn được lưu. Đổi ngày đến hạn/chọn reminder cũng kiểm tra giới hạn cuối ngày. Có thể nhắc trước ngày đến hạn. | [T1], `handleSendTask`, `validateReminderAgainstDueDate` |
| BR-TASK-05 | Chỉ lịch nhắc có ID task hợp lệ và thời điểm tương lai mới được lên lịch. Alarm cũ cùng task được hủy/thay thế. | Android 12+ không cho exact alarm thì dùng alarm không chính xác. Android 13+ cần `POST_NOTIFICATIONS` để receiver hiển thị. Lưu task thành công không đồng nghĩa notification đã được cấp quyền hay phát đúng giây. | [R1], `setReminder`, `ensureNotificationPermission`; [R3], `showTaskReminder` |
| BR-TASK-06 | Khi tick/bỏ tick, ghi cả `isCompleted` và `completed`; tick dùng server timestamp cho `completedAt`, bỏ tick đặt `completedAt=null`. | Tick hủy reminder; bỏ tick không tự đặt lại reminder. Adapter cập nhật model trước khi Firestore hoàn tất nên UI có thể tạm khác dữ liệu khi ghi lỗi. | [T2], `onTaskCheckedChanged`; [T3], `onBindViewHolder`; cùng luồng ở [V2], [V3], [S1] |
| BR-TASK-07 | Xóa một task qua menu phải xác nhận, có ID hợp lệ và document được xóa thành công. | Sau callback xóa thành công, app hủy alarm task. Khác với xóa hàng loạt theo danh mục/dọn ngày. | [T2], `confirmDeleteTask`, `deleteTask` |
| BR-TASK-08 | Task mới dùng `order=(int)(currentTimeMillis/1000)`; khi kéo trong danh mục, app đánh lại thứ tự 1..n và lưu mỗi batch tối đa 450. | Danh mục hiển thị task chưa hoàn thành trước, rồi tăng theo order. Thứ tự kéo không làm mất quy tắc gom task đã hoàn thành xuống sau. | [T1], `addNewTaskWithNextOrder`; [T2], `persistTaskOrder`, `startTaskListener` |
| BR-TASK-09 | Nhập giọng nói cần thiết bị có dịch vụ nhận dạng và quyền `RECORD_AUDIO`; ngôn ngữ yêu cầu là `vi-VN`, lấy kết quả đầu tiên. | Ô đang trống thì thay nội dung; ô có chữ thì nối kết quả bằng dòng mới. Không có kết quả/hủy/từ chối quyền thì không thêm task tự động. | [T1], `onCreate`, `onMicrophoneClicked`, `startVoiceInput` |

## 5. Xem và tìm kiếm — VIEW / SEARCH

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-VIEW-01 | Gọi `T` là đầu ngày hôm nay, `N=T+86.400.000`. Việc hôm nay: chưa hoàn thành và `dueDate==T`; ngày mai: chưa hoàn thành và `dueDate==N`; quá hạn: chưa hoàn thành và `0<dueDate<T`; hoàn thành hôm nay: đã hoàn thành và `T<=completedAt<N`. | Ngày đến hạn trong dữ liệu cũ không đúng 00:00 sẽ không khớp bộ lọc hôm nay/ngày mai. Số đếm tổng quan dùng cùng quy tắc. Bộ lọc quá hạn tăng theo ngày đến hạn; hoàn thành hôm nay giảm theo completedAt; hôm nay/ngày mai tăng theo order. | [V1], `computeAndUpdateCounts`; [V2], `filterTasks`, `sortFiltered` |
| BR-VIEW-02 | Lịch có 42 ô, tuần bắt đầu Chủ nhật; tạo danh sách ngày của tháng hiện tại. Chọn ngày truy vấn `dayStart<=dueDate<dayStart+86.400.000`. | Danh sách ngày có cả task đã hoàn thành; dấu chấm đánh dấu ngày có task trong tháng. Chưa thấy điều khiển chuyển tháng trong code. | [V3], `daysInMonthList`, `startTaskListener`, `startMonthTaskMarkerListener` |
| BR-VIEW-03 | Ma trận chỉ nhận task chưa hoàn thành; priority 3→Q1, 2→Q2, 1→Q3, các giá trị khác→Q4. | Không suy luận khẩn cấp theo deadline; không phải thuật toán đánh giá hai trục độc lập. | [V3], `partitionAndRenderEisenhower` |
| BR-SEARCH-01 | Query và chuỗi `title + khoảng trắng + description` được chuẩn hóa NFD, bỏ combining marks, chuyển chữ thường và `trim`; so sánh `contains`. | Query rỗng hiển thị hướng dẫn và không liệt kê task. Chữ `đ` không được chuyển thành `d`, nên `di` không được đảm bảo khớp `đi`. Không tìm nội dung event. | [S1], `normalizeForSearch`, `applyFilter` |
| BR-SEARCH-02 | Kết quả gồm task đã và chưa hoàn thành, xếp chưa hoàn thành trước, ngày đến hạn tăng dần (`null` sau cùng), rồi order. | Chọn kết quả có categoryId mở danh mục, cuộn và highlight khoảng 1.200 ms. Với categoryId rỗng thì thao tác chọn không điều hướng. | [S1], `startTaskListener`, `onTaskClicked`; [T2], `maybeScrollToHighlightedTask` |

## 6. Sự kiện — EVENT

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-EVENT-01 | Sự kiện cần tên khác rỗng sau `trim` và ngày được chọn (`targetDate>0`). Icon rỗng dùng `●`; ngày chọn lưu ở đầu ngày theo thiết bị. | Nút lưu chỉ bật khi có ngày và không đang lưu; nếu tên rỗng thì báo lỗi khi nhấn. Không cấm ngày quá khứ hoặc trùng tên. | [E1], `handleSaveAction`, `updateSaveEnabledState`, `showDatePicker` |
| BR-EVENT-02 | Countdown là chênh lệch chỉ số ngày địa phương giữa targetDate và hiện tại. | Dương: “Còn n ngày”; bằng 0: “Hôm nay”; âm: “Trễ n ngày”; thiếu ngày: `--`. Sự kiện load theo targetDate tăng dần; không có lịch refresh countdown riêng ở adapter. | [E2], `calculateDaysRemaining`, `toLocalDayIndex`, `formatCountdown`; [E3], `startEventListener` |
| BR-EVENT-03 | Có tối đa hai alarm: 08:00 ngày trước sự kiện và 08:00 ngày diễn ra, tính bằng Calendar theo múi giờ thiết bị. | Mỗi lần đặt thay alarm cũ; chỉ thời điểm `>now` được đặt. Event hôm nay sau 08:00 không có alarm tương lai cho hai mốc này. Không exact alarm thì dùng inexact; hiển thị notification vẫn cần quyền. | [R2], `setEventReminders`, `buildReminderAtMillis`, `scheduleIfFuture`; [R3] |
| BR-EVENT-04 | Sửa thành công cập nhật title/icon/date rồi đặt lại hai alarm; xóa cần xác nhận, xóa document thành công rồi hủy alarm. | Listener danh sách cũng đặt lại alarm cho các event đã load. Callback chỉ tiếp tục phần UI/lên lịch khi fragment còn attached. | [E1], `handleSaveAction`; [E3], `deleteEvent`, `startEventListener` |

## 7. Pomodoro — POMO

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-POMO-01 | Mặc định focus 25 phút, break 5 phút. Picker nhận số phút nguyên trong [5,90], gồm preset 5/15/25/45/90. | Đổi thời lượng khi đang chạy cần xác nhận và đưa về paused với toàn bộ thời lượng mới; không giữ phần đã chạy. Đổi trong focus cập nhật focus mặc định lần sau; đổi trong break không đổi selectedFocusDuration. | [P1], hằng số, `handleApplyDurationClick`, `applyDurationMillis` |
| BR-POMO-02 | Picker task chỉ nhận task chưa hoàn thành có title không rỗng. | Xếp priority giảm dần, khoảng cách tuyệt đối từ dueDate tới đầu hôm nay tăng dần, dueDate tăng dần, tên không phân biệt hoa thường. Không bắt buộc chọn task để start; lịch sử dùng tên mặc định nếu chưa chọn. | [P1], `showTaskPickerDialog`, `sortTasksForPicker`, `savePomodoroHistory` |
| BR-POMO-03 | Start chỉ xử lý khi chưa running/paused; pause chỉ khi running; resume chỉ khi paused. Reset hủy timer, về focus, nạp selectedFocusDuration và trạng thái chưa chạy. | Chọn Complete ở focus đang chạy hoặc paused sẽ lưu; chọn ở break không lưu lịch sử, thông báo chỉ hoàn thành focus và reset. | [P1], `handleStartButtonClick`, `handlePauseButtonClick`, `handleResumeButtonClick`, `handleResetButtonClick`, `handleCompleteButtonClick` |
| BR-POMO-04 | Khi callback timer về 0 ở focus, app yêu cầu lưu lịch sử rồi chuyển break 5 phút và tự start. Khi break về 0, chuyển focus theo selectedFocusDuration và tự start. | Không cần người dùng bấm start lại giữa các phiên. Âm/rung phát khi timer hoàn tất; ghi Firestore lỗi không ngăn chuyển phiên. | [P1], `startTimer`, `onSessionCompleted`, `playTimerFinishedAlert` |
| BR-POMO-05 | Lịch sử chỉ lưu focus, có UID; payload gồm `userId`, tên task tại thời điểm gọi lưu, `duration=max(1,totalMillis/60000)`, `timestamp=currentTimeMillis`. | Complete thủ công cũng dùng toàn bộ thời lượng cài đặt, không trừ remainingMillis. Không lưu taskId, không đánh dấu task hoàn thành và không lưu break. Sau Complete thủ công, cả callback lưu thành công/lỗi đều reset. Không có retry nghiệp vụ riêng. | [P1], `savePomodoroHistoryAndReset`, `savePomodoroHistory` |
| BR-POMO-06 | View bị hủy thì CountDownTimer bị cancel. State được chép vào SessionStore static; quay lại trong cùng tiến trình có thể đối chiếu elapsedRealtime để nhảy qua các mốc focus/break. | Hàm reconcile chỉ tính lại mode/thời gian; không ghi bù các phiên focus đã vượt mốc trong lúc view không tồn tại. Không có foreground service hoặc lưu SessionStore bền vững qua process death; không coi Bundle restore là cam kết liên tục tuyệt đối. | [P1], `onDestroyView`, `restoreFromSessionStore`, `reconcileRunningStateWithClock`, `onSaveInstanceState` |

## 8. Thống kê — STAT

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-STAT-01 | Lấy tối đa 300 document theo timestamp giảm dần. Hôm nay từ đầu ngày đến `now`; tuần từ 00:00 thứ Hai đến `now`, theo múi giờ thiết bị. | Mỗi session trong khoảng cộng 1 vào số phiên; phút cộng `max(0,duration)`. Tổng tuần có thể thiếu nếu trong tuần có hơn 300 phiên. Giờ hôm nay hiển thị 1 chữ số thập phân; thời lượng tuần dạng `h` và `m`. | [F1], `loadPomodoroData`, `handlePomodoroSnapshot`, `getStartOfWeekMillis` |
| BR-STAT-02 | Biểu đồ chỉ dùng phiên hôm nay, gộp theo taskName đã trim; tên rỗng/null thay `(Không rõ)`; chỉ vẽ phần tổng phút lớn hơn 0. | Task khác ID nhưng cùng tên vẫn chung phần biểu đồ. Session duration âm/0 vẫn có thể được đếm nhưng không tạo lát có giá trị dương. Không có dữ liệu hợp lệ thì xóa chart. | [F1], `loadChartData` |
| BR-STAT-03 | Danh sách focus record chỉ lấy tối đa 40 phiên hôm nay theo thứ tự query mới trước. | Hiển thị tên, thời gian, số phút và nhãn TẬP TRUNG; không có phân trang hay bộ lọc lịch sử các ngày trước. | [F1], `handlePomodoroSnapshot`, `mapSessionToRecord` |
| BR-STAT-04 | Share lấy trực tiếp 4 giá trị đang hiển thị trên màn hình, tạo ACTION_SEND loại `text/plain`. | Chia sẻ văn bản hôm nay/tuần này qua chooser Android; không xuất ảnh, PDF hoặc toàn bộ dữ liệu lịch sử. Không có ứng dụng nhận thì báo lỗi. | [F1], `shareCurrentStatistics` |
| BR-STAT-05 | Khi resume qua ngày mới hoặc Handler tới nửa đêm khi màn đang active, app tính lại số liệu từ snapshot gần nhất; chưa có snapshot thì load. | Timer midnight gỡ khi pause; listener Firestore gỡ khi stop và tạo lại khi start. Refresh ngày không phải lịch dọn task của MainActivity. | [F1], lifecycle, `scheduleNextMidnightRefresh` |

## 9. Cài đặt — SET

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-SET-01 | Giao diện lưu cục bộ bằng SharedPreferences: 0=theo hệ thống, 1=sáng, 2=tối; ứng dụng áp dụng lại khi khởi động. | AppCompatDelegate nhận mode tương ứng. Một số layout/chart vẫn hardcode màu; chưa đủ căn cứ nói mọi thành phần đã hỗ trợ sáng/tối hoàn chỉnh. | [A4], `showThemeDialog`; [SET1], `mapToNightMode` |
| BR-SET-02 | Switch âm thanh đọc/ghi `sound_notifications_enabled`, mặc định `true`. | Chưa thấy phần phát chuông Pomodoro hoặc tạo notification đọc preference này; AC chỉ xác nhận lưu và khôi phục switch, không cam kết tắt được mọi âm. | [A4], `setupSoundNotificationSwitch`; [P1], `playAlarmSoundOnce`; [R3] |

## 10. Dọn công việc — CLEAN

| Mã | Điều kiện / quy tắc hiện tại | Kết quả và giới hạn | Căn cứ |
| --- | --- | --- | --- |
| BR-CLEAN-01 | `MainActivity.onResume` kiểm tra UID và ngày thiết bị; nếu preference ngày dọn gần nhất của UID khác hôm nay thì bắt đầu dọn. | Không phải job nền hay Handler chạy đúng 00:00. Sau toàn bộ chuỗi callback thành công mới lưu ngày đã dọn; lỗi có thể làm lần resume sau thử lại. | [M1], `maybeRunDailyCompletedTaskCleanup` |
| BR-CLEAN-02 | Truy vấn đầu tiên chọn `completedAt < đầu hôm nay`, orderBy completedAt, mỗi lần tối đa 450; xóa rồi lặp đến hết. | **Không kiểm tra completed/isCompleted trong truy vấn hoặc vòng xóa này**: mọi document thỏa completedAt đều bị xóa, kể cả cờ hoàn thành không nhất quán. Không gọi hủy alarm của từng task trong bước này. | [M1], `deleteCompletedTasksBefore` |
| BR-CLEAN-03 | Bước tiếp theo lần lượt query `completed==true` rồi `isCompleted==true`, mỗi query limit 450; trong tập trả về, xóa bản ghi có completedAt null hoặc trước hôm nay. | Nếu 450 kết quả đầu đều không cần xóa, hàm kết thúc nhánh đó mà không phân trang để tìm bản ghi phía sau. Vì vậy không bảo đảm dọn mọi legacy record trong một lần. | [M1], `purgeCompletedTasksWithoutTimestamp` |

## 11. Bảng biên quan trọng để kiểm tra lại

Dữ liệu kiểm tra các giá trị biên:

| Trường hợp | Kết quả hiện trạng cần kiểm tra | Quy tắc |
| --- | --- | --- |
| Username `Abc_1` / `ab` / `abc xyz` | Chuỗi đầu thành `abc_1@ticktok.user`; hai chuỗi sau bị chặn. | BR-AUTH-01 |
| Mật khẩu đăng ký sau trim có 5 / 6 ký tự | 5 bị chặn; 6 qua kiểm tra độ dài, còn phụ thuộc xác thực Firebase. | BR-AUTH-02 |
| Reminder bằng now / bằng D+86.400.000 / ít hơn mốc cuối 1 ms và vẫn ở tương lai | Hai trường hợp đầu bị xóa; trường hợp cuối được giữ. | BR-TASK-04 |
| Bỏ tick task đã hủy alarm trước đó | Cờ và completedAt được đổi; không tự khôi phục alarm. | BR-TASK-06 |
| Complete focus 25 phút sau khi mới chạy 1 phút | Gửi lịch sử duration=25 nếu lưu thành công. | BR-POMO-05 |
| Thời lượng 4 / 5 / 90 / 91 phút | 4 và 91 bị chặn; 5 và 90 được chấp nhận. | BR-POMO-01 |
| Có 301 phiên trong tuần | Thống kê chỉ tính 300 bản ghi query trả về. | BR-STAT-01 |
| Nhiều task cùng tên | Biểu đồ gộp chung, không dựa vào taskId. | BR-STAT-02 |
| 450 legacy kết quả đầu đều hoàn thành hôm nay, có legacy thiếu timestamp ở phía sau | Nhánh legacy có thể kết thúc trước khi tới bản ghi phía sau. | BR-CLEAN-03 |

## 12. Điểm cần làm rõ khi nâng cấp

Các vấn đề cần thống nhất trước khi nâng cấp:

1. Ý nghĩa “phút tập trung” khi Complete thủ công đang là thời lượng dự kiến; cần thống nhất nếu muốn đổi sang thời gian thực tế.
2. Chính sách xóa task hằng ngày đang làm mất lịch sử task và không hủy alarm hàng loạt; bước đầu chỉ dựa completedAt.
3. Tìm kiếm không chuyển `đ` sang `d`; tìm event chưa có.
4. Ma trận phân nhóm theo priority; chưa tính hai trục quan trọng/khẩn cấp từ dữ liệu độc lập.
5. Bỏ tick không đặt lại alarm; chỉnh một task đã hoàn thành vẫn có thể đi qua luồng sửa và đặt reminder vì task tạm dùng để lên lịch không mang cờ completed.
6. SessionStore không được xóa theo logout/UID; không xem nó là dữ liệu bền vững hoặc được cách ly theo tài khoản.
7. Sound switch mới lưu preference; quyền notification và exact alarm phụ thuộc thiết bị. Manifest chưa khai báo receiver khôi phục lịch sau reboot.
8. Quy tắc phía Firestore, giới hạn dữ liệu nhập, đồng thời đa thiết bị và xử lý lỗi không đồng nhất cần kiểm chứng riêng; client path theo UID không thay thế kiểm soát truy cập phía server.

## 13. Chỉ mục bằng chứng

[A1]: ../../../app/src/main/java/com/example/ticktok/util/AuthAccountMapper.java
[A2]: ../../../app/src/main/java/com/example/ticktok/activity/RegisterActivity.java
[A3]: ../../../app/src/main/java/com/example/ticktok/activity/LoginActivity.java
[A4]: ../../../app/src/main/java/com/example/ticktok/activity/SettingsActivity.java
[A5]: ../../../app/src/main/java/com/example/ticktok/util/UserFirestorePaths.java
[C1]: ../../../app/src/main/java/com/example/ticktok/repository/CategoryRepository.java
[C2]: ../../../app/src/main/java/com/example/ticktok/repository/FirestoreCategoryDataSource.java
[C3]: ../../../app/src/main/java/com/example/ticktok/adapter/MenuCategoryAdapter.java
[M1]: ../../../app/src/main/java/com/example/ticktok/activity/MainActivity.java
[T1]: ../../../app/src/main/java/com/example/ticktok/fragment/AddTaskBottomSheetFragment.java
[T2]: ../../../app/src/main/java/com/example/ticktok/fragment/CategoryFragment.java
[T3]: ../../../app/src/main/java/com/example/ticktok/adapter/TaskAdapter.java
[V1]: ../../../app/src/main/java/com/example/ticktok/fragment/WelcomeFragment.java
[V2]: ../../../app/src/main/java/com/example/ticktok/fragment/TaskFilterFragment.java
[V3]: ../../../app/src/main/java/com/example/ticktok/fragment/CalendarFragment.java
[S1]: ../../../app/src/main/java/com/example/ticktok/fragment/SearchFragment.java
[E1]: ../../../app/src/main/java/com/example/ticktok/fragment/AddEventBottomSheetFragment.java
[E2]: ../../../app/src/main/java/com/example/ticktok/adapter/EventAdapter.java
[E3]: ../../../app/src/main/java/com/example/ticktok/fragment/EventFragment.java
[P1]: ../../../app/src/main/java/com/example/ticktok/fragment/PomodoroFragment.java
[F1]: ../../../app/src/main/java/com/example/ticktok/activity/FocusStatisticsActivity.java
[R1]: ../../../app/src/main/java/com/example/ticktok/reminder/ReminderManager.java
[R2]: ../../../app/src/main/java/com/example/ticktok/reminder/EventReminderManager.java
[R3]: ../../../app/src/main/java/com/example/ticktok/reminder/NotificationReceiver.java
[SET1]: ../../../app/src/main/java/com/example/ticktok/TickTokApplication.java

Các link trên trỏ đến file nguồn trong repository; tên phương thức trong mỗi hàng xác định vị trí kiểm tra khi số dòng thay đổi.
