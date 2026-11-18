# User Stories & Acceptance Criteria — TickTok

Phiên bản 1.0 · Ngày lập: 18/11/2026 · Cơ sở: các luồng đã xuất hiện trong mã nguồn.

## 1. Quy ước

User stories mô tả nhu cầu và kết quả mong đợi của người dùng. Mức ưu tiên đề xuất: **P1** — chức năng cốt lõi; **P2** — chức năng hỗ trợ; **P3** — tùy chỉnh cá nhân. Mức ưu tiên độc lập với trạng thái hoàn thành.

AC dùng Given/When/Then; mã AC duy nhất được tạo từ mã story và số thứ tự, ví dụ `AC-TASK-01-1` thuộc `US-TASK-01`. Trạng thái kiểm thử các AC: **chưa thực thi**. Callback “lưu thành công” nghĩa là thao tác Firebase tương ứng được báo thành công; không suy ra có SLA mạng, tính đồng bộ tức thời mọi thiết bị hoặc quyền server đã được kiểm chứng.

`Liên kết` chỉ ra mã yêu cầu SRS, use case và business rules tương ứng. Đọc [Business Rules](BUSINESS_RULES.md) để xem điều kiện chính xác, bằng chứng và các giới hạn; [SRS](SRS.md) mô tả giao diện/dữ liệu; [đặc tả use case](../use-cases/SPECIFICATIONS.md) mô tả các luồng chính chi tiết hơn.

## 2. Tài khoản

### US-AUTH-01 — Đăng ký tài khoản · P1

Là người dùng mới, tôi muốn tạo tài khoản để lưu công việc và lịch sử tập trung theo tài khoản của mình.

Liên kết: FR-AUTH-01; UC-01; BR-AUTH-01, BR-AUTH-02, BR-AUTH-07.

- **AC-AUTH-01-1:** Given tài khoản hoặc một trong hai ô mật khẩu rỗng sau trim, When nhấn đăng ký, Then app thông báo thiếu thông tin và không gửi yêu cầu tạo account.
- **AC-AUTH-01-2:** Given username `Abc_1` và hai mật khẩu giống nhau, dài ít nhất 6 ký tự sau trim, When đăng ký, Then app gửi email nội bộ `abc_1@ticktok.user` tới Firebase; chỉ mở màn chính sau khi tạo account thành công và callback cập nhật profile kết thúc.
- **AC-AUTH-01-3:** Given username không khớp định dạng, mật khẩu xác nhận khác hoặc mật khẩu ngắn hơn 6 ký tự, When nhấn đăng ký, Then app chặn và báo lỗi tương ứng.
- **AC-AUTH-01-4:** Given input vượt kiểm tra cục bộ nhưng Firebase từ chối tạo account, When có callback lỗi, Then app bật lại nút đăng ký và hiện thông báo; không điều hướng thành công.

### US-AUTH-02 — Đăng nhập bằng tài khoản và mật khẩu · P1

Là người đã có tài khoản, tôi muốn đăng nhập để sử dụng dữ liệu của mình.

Liên kết: FR-AUTH-02; UC-02; BR-AUTH-01, BR-AUTH-03, BR-AUTH-07.

- **AC-AUTH-02-1:** Given thông tin nhập hợp lệ, When nhấn đăng nhập, Then tài khoản được trim/ánh xạ, mật khẩu được trim và gửi Firebase; nút đăng nhập mật khẩu và Google bị vô hiệu hóa trong lúc chờ.
- **AC-AUTH-02-2:** Given Firebase xác thực thành công, When callback kết thúc, Then mở MainActivity và đóng màn Login; nếu thất bại thì giữ màn Login, hiển thị lỗi và bật lại nút.
- **AC-AUTH-02-3:** Given đã có Firebase current user, When mở LoginActivity, Then app chuyển thẳng sang màn chính. Given không có current user, When MainActivity resume, Then app chuyển về Login và xóa task stack màn chính.

### US-AUTH-03 — Đăng nhập Google · P1

Là người dùng có tài khoản Google, tôi muốn dùng tài khoản đó để vào ứng dụng.

Liên kết: FR-AUTH-03; UC-03; BR-AUTH-04.

- **AC-AUTH-03-1:** Given Web Client ID hợp lệ, When chọn Google và nhận Google account có ID token, Then app tạo Google credential, xác thực Firebase và mở màn chính nếu Firebase báo thành công.
- **AC-AUTH-03-2:** Given thiếu cấu hình Web Client ID, When chọn Google, Then app báo chưa cấu hình và không khởi động xác thực Google.
- **AC-AUTH-03-3:** Given người dùng hủy, không có dữ liệu trả về, token thiếu hoặc SDK/Firebase báo lỗi, When callback được xử lý, Then app giữ màn đăng nhập, thông báo lỗi và bật lại nút; không xem đây là phiên đăng nhập thành công.

### US-AUTH-04 — Đổi mật khẩu và xem hướng dẫn khi quên · P2

Là người dùng tài khoản mật khẩu, tôi muốn đổi mật khẩu hoặc biết cách liên hệ hỗ trợ khi không nhớ mật khẩu.

Liên kết: FR-AUTH-04, FR-AUTH-06; UC-16, UC-02; BR-AUTH-05, BR-AUTH-06.

- **AC-AUTH-04-1:** Given current user có provider `password`, When mở cài đặt, Then có mục đổi mật khẩu; user chỉ có Google provider không thấy mục này.
- **AC-AUTH-04-2:** Given mật khẩu mới dưới 6 ký tự sau trim, When xác nhận cập nhật, Then không gọi updatePassword và báo quá ngắn. Với mật khẩu đủ dài, Firebase quyết định thành công/thất bại và app thông báo tương ứng.
- **AC-AUTH-04-3:** Given đang ở Login, When chọn quên mật khẩu, Then app mở hướng dẫn liên hệ quản trị viên; không gửi email reset hoặc tạo mã OTP.

### US-AUTH-05 — Đăng xuất · P1

Là người đang đăng nhập, tôi muốn kết thúc phiên trước khi rời ứng dụng hoặc chuyển tài khoản.

Liên kết: FR-AUTH-05; UC-17; BR-AUTH-06.

- **AC-AUTH-05-1:** Given đang mở cài đặt, When chọn đăng xuất rồi hủy xác nhận, Then phiên Firebase hiện tại được giữ.
- **AC-AUTH-05-2:** Given xác nhận đăng xuất, When app gọi signOut, Then mở Login với task stack được xóa; nút Back không đưa trở lại phiên màn chính cũ.
- **AC-AUTH-05-3:** Given đã có alarm tương lai và SessionStore chứa trạng thái Pomodoro trong cùng tiến trình, When `performLogout` chạy, Then hàm gọi Firebase signOut và điều hướng Login nhưng không gọi hủy alarm hoặc đặt lại SessionStore; các giá trị static của SessionStore không bị luồng logout thay đổi. Kiểm tra bằng cách đối chiếu lời gọi trong source hoặc quan sát state trước/sau bằng debugger.

## 3. Danh mục và công việc

### US-CAT-01 — Tạo và chỉnh sửa danh mục · P1

Là người dùng, tôi muốn đặt tên và biểu tượng danh mục để tổ chức công việc theo nhóm.

Liên kết: FR-CAT-01, FR-CAT-02; UC-04; BR-CAT-01, BR-CAT-02, BR-CAT-03.

- **AC-CAT-01-1:** Given tên rỗng sau trim, When lưu danh mục mới hoặc sửa, Then chặn lưu và báo lỗi. Icon rỗng được thay bằng `≡`.
- **AC-CAT-01-2:** Given tên hợp lệ và tạo mới thành công, When danh sách được tải lại, Then danh mục mới có order 1, các order cũ được tăng trong batch, Welcome vẫn đứng đầu menu.
- **AC-CAT-01-3:** Given một danh mục người dùng có ID hợp lệ, When đổi tên/icon và lưu thành công, Then cập nhật chính document đó; nếu đang chọn danh mục này thì tiêu đề màn hình được cập nhật.
- **AC-CAT-01-4:** Given thao tác ghi Firebase bị từ chối, When có callback lỗi, Then giữ màn thêm/sửa và báo lỗi để có thể thử lại; không thông báo lưu thành công.

### US-CAT-03 — Xóa danh mục cùng các công việc · P1

Là người dùng, tôi muốn xóa nhóm công việc không cần giữ để thu gọn danh sách.

Liên kết: FR-CAT-03; UC-04; BR-CAT-03, BR-CAT-04.

- **AC-CAT-03-1:** Given chọn xóa danh mục rồi hủy hộp thoại, When hộp thoại đóng, Then không xóa task hay danh mục; Welcome không có menu xóa.
- **AC-CAT-03-2:** Given xác nhận và mọi bước Firebase thành công, When các task có categoryId tương ứng đã được xóa theo batch, Then document danh mục được xóa; nếu đó là danh mục đang mở thì chuyển về tổng quan.
- **AC-CAT-03-3:** Given ít nhất một batch xóa task đã commit và bước sau thất bại, When callback lỗi được nhận, Then báo xóa thất bại, các task trong batch đã commit vẫn bị xóa và luồng không thực hiện rollback hay gọi hủy alarm từng task.

### US-CAT-04 — Sắp xếp các danh sách cá nhân · P2

Là người dùng, tôi muốn kéo sắp xếp danh mục và công việc để đặt thứ tự theo cách làm việc của mình.

Liên kết: FR-CAT-04, FR-TASK-05; UC-04, UC-09; BR-CAT-03, BR-CAT-05, BR-TASK-08.

- **AC-CAT-04-1:** Given menu có Welcome và các danh mục người dùng, When kéo danh mục khác qua vị trí Welcome hoặc kéo Welcome, Then thao tác đó không được chấp nhận.
- **AC-CAT-04-2:** Given kéo một danh mục người dùng đến vị trí hợp lệ, When thả và lưu thành công, Then các danh mục người dùng được đánh lại order 1..n và giữ thứ tự sau tải lại.
- **AC-CAT-04-3:** Given danh sách task trong một danh mục, When kéo/thả và lưu thành công, Then app lưu order mới theo batch tối đa 450; khi query cập nhật, task chưa hoàn thành vẫn đứng trước task đã hoàn thành.

### US-TASK-01 — Tạo và sửa công việc có lịch nhắc · P1

Là người dùng, tôi muốn nhập việc cần làm, ngày đến hạn và lời nhắc để theo dõi công việc của mình.

Liên kết: FR-TASK-01, FR-TASK-02; UC-05, UC-06; BR-TASK-01, BR-TASK-02, BR-TASK-03, BR-TASK-04, BR-TASK-05.

- **AC-TASK-01-1:** Given nội dung rỗng sau trim, When gửi, Then app yêu cầu nhập nội dung và không lưu. Given `Đọc sách\nChương 1`, When lưu thành công, Then title là `Đọc sách`, description là `Chương 1`.
- **AC-TASK-01-2:** Given chưa chọn ngày, When lưu, Then dueDate là đầu ngày hôm nay theo thiết bị. Given tạo từ màn lịch, When mở form, Then ngày đang chọn được điền sẵn; tạo ngoài danh mục có thể lưu categoryId null.
- **AC-TASK-01-3:** Given chọn priority cao/vừa/thấp/không ưu tiên, When lưu, Then lưu lần lượt 3/2/1/0; mặc định 0. Task mới có trạng thái chưa hoàn thành và order dựa trên giây hiện tại.
- **AC-TASK-01-4:** Given reminder không ở tương lai hoặc từ đầu ngày sau hạn trở đi, When lưu, Then app thông báo, đặt reminderTime về 0 và vẫn lưu task. Reminder tương lai trong giới hạn được gửi lên lịch sau khi ghi task thành công.
- **AC-TASK-01-5:** Given mở sửa một task có ID, When lưu thành công, Then cập nhật title/description/priority/dueDate/categoryId/reminderTime trên document hiện có và thay/hủy alarm tương ứng; không tạo task mới. Nếu ghi lỗi, app báo lỗi và không đóng sheet theo nhánh thành công.

### US-TASK-03 — Đánh dấu hoàn thành và mở lại · P1

Là người dùng, tôi muốn đánh dấu công việc đã xong hoặc mở lại để danh sách thể hiện tiến độ.

Liên kết: FR-TASK-03; UC-07; BR-TASK-06, BR-VIEW-01.

- **AC-TASK-03-1:** Given task có ID và đang chưa hoàn thành, When tick, Then app yêu cầu ghi `isCompleted=true`, `completed=true`, `completedAt=serverTimestamp` và hủy alarm của task.
- **AC-TASK-03-2:** Given task đã hoàn thành, When bỏ tick, Then yêu cầu ghi hai cờ false và completedAt null; không tự khôi phục alarm đã hủy.
- **AC-TASK-03-3:** Given đang dùng các danh sách có snapshot listener, When Firestore phản ánh trạng thái mới, Then danh sách/bộ đếm cập nhật theo tiêu chí màn hiện tại. Khi ghi lỗi, không xem việc model được tick cục bộ là bằng chứng dữ liệu đã lưu.

### US-TASK-04 — Xóa một công việc · P1

Là người dùng, tôi muốn bỏ công việc không còn cần theo dõi.

Liên kết: FR-TASK-04; UC-08; BR-TASK-07.

- **AC-TASK-04-1:** Given chọn menu xóa task, When hủy xác nhận, Then không gửi lệnh xóa.
- **AC-TASK-04-2:** Given xác nhận xóa task có ID hợp lệ, When Firebase báo xóa thành công, Then hủy reminder task, báo thành công và listener loại task khỏi danh sách.
- **AC-TASK-04-3:** Given Firebase báo lỗi xóa, When callback được xử lý, Then app thông báo thất bại; không coi task đã được xóa thành công.

### US-TASK-06 — Nhập nội dung bằng tiếng nói · P2

Là người dùng, tôi muốn đọc nội dung tiếng Việt để nhập task nhanh hơn.

Liên kết: FR-TASK-06; UC-18, UC-05; BR-TASK-09.

- **AC-TASK-06-1:** Given có dịch vụ nhận dạng và đã có quyền micro, When bấm microphone, Then mở nhận dạng với ngôn ngữ vi-VN và lấy kết quả đầu tiên; không tự gửi task.
- **AC-TASK-06-2:** Given chưa cấp micro, When bấm microphone, Then xin quyền; đồng ý thì tiếp tục nhận dạng, từ chối thì thông báo và không thay nội dung.
- **AC-TASK-06-3:** Given nhận được kết quả không rỗng, When ô nhập đang trống, Then điền kết quả; nếu ô đã có chữ thì nối bằng dòng mới. Không có dịch vụ/hủy/không có kết quả không tạo task.

## 4. Xem và tìm kiếm

### US-VIEW-01 — Tổng quan và bộ lọc theo ngày · P1

Là người dùng, tôi muốn thấy việc hôm nay, ngày mai, quá hạn và đã hoàn thành hôm nay để chọn việc cần xử lý.

Liên kết: FR-VIEW-01, FR-VIEW-02; UC-09; BR-VIEW-01.

- **AC-VIEW-01-1:** Given dữ liệu ngày đến hạn đã chuẩn hóa, When tải tổng quan, Then đếm các task chưa hoàn thành đúng ngày hôm nay/ngày mai hoặc quá hạn; task đã hoàn thành chỉ thuộc số hoàn thành hôm nay nếu completedAt nằm trong khoảng ngày đó.
- **AC-VIEW-01-2:** Given bấm một thẻ tổng quan, When danh sách mở, Then dùng đúng cùng tiêu chí với số đếm; hôm nay/ngày mai sắp theo order, quá hạn theo dueDate tăng, hoàn thành hôm nay theo completedAt giảm.
- **AC-VIEW-01-3:** Given không có task phù hợp, When snapshot được xử lý, Then danh sách trống có trạng thái hướng dẫn; không hiển thị task sai điều kiện để lấp danh sách.

### US-VIEW-03 — Xem lịch và ma trận ưu tiên · P2

Là người dùng, tôi muốn xem lịch theo ngày hoặc nhóm ưu tiên để chọn cách quan sát công việc phù hợp.

Liên kết: FR-VIEW-03, FR-VIEW-04; UC-09; BR-VIEW-02, BR-VIEW-03.

- **AC-VIEW-03-1:** Given mở lịch, When tạo lưới tháng, Then có 42 ô với tuần bắt đầu Chủ nhật, tháng hiện tại và ngày hôm nay được chọn; ngày có task được đánh dấu chấm.
- **AC-VIEW-03-2:** Given chọn một ngày, When query trả về, Then liệt kê task có dueDate trong khoảng từ đầu ngày tới trước đầu ngày cộng 24 giờ, gồm cả task đã hoàn thành; task chưa hoàn thành đứng trước.
- **AC-VIEW-03-3:** Given chuyển tab Eisenhower, When phân nhóm, Then bỏ task đã hoàn thành; priority 3/2/1 vào Q1/Q2/Q3, còn lại Q4. Deadline không tự thay đổi nhóm.

### US-SEARCH-01 — Tìm và mở công việc · P2

Là người dùng, tôi muốn tìm theo tiêu đề hoặc mô tả và chuyển tới công việc tương ứng.

Liên kết: FR-SEARCH-01; UC-10; BR-SEARCH-01, BR-SEARCH-02.

- **AC-SEARCH-01-1:** Given query trống sau chuẩn hóa, When bộ lọc chạy, Then ẩn kết quả và hiển thị hướng dẫn. Query có nội dung được tìm contains trên title và description đã NFD/bỏ combining marks/chuyển chữ thường/trim.
- **AC-SEARCH-01-2:** Given có kết quả đã và chưa hoàn thành, When hiển thị, Then chưa hoàn thành đứng trước, tiếp đến dueDate tăng (`null` sau), rồi order; không có kết quả thì hiện thông báo không tìm thấy.
- **AC-SEARCH-01-3:** Given chọn kết quả có categoryId, When điều hướng, Then mở danh mục, cuộn tới task và highlight khoảng 1.200 ms; với categoryId rỗng không có điều hướng này.
- **AC-SEARCH-01-4:** Given task có title `đi học` và description rỗng, When tìm `di hoc`, Then task đó không khớp vì phép chuẩn hóa giữ nguyên chữ `đ`; nội dung event không được đưa vào tập dữ liệu tìm kiếm.

## 5. Sự kiện

### US-EVENT-01 — Quản lý và xem đếm ngày sự kiện · P2

Là người dùng, tôi muốn ghi các mốc sự kiện và biết còn bao nhiêu ngày để chuẩn bị.

Liên kết: FR-EVENT-01, FR-EVENT-02, FR-EVENT-03, FR-EVENT-04; UC-11; BR-EVENT-01, BR-EVENT-02, BR-EVENT-04.

- **AC-EVENT-01-1:** Given chưa chọn ngày hoặc đang lưu, When mở form, Then nút lưu bị vô hiệu hóa. Given đã có ngày nhưng tên rỗng, When lưu, Then thông báo thiếu tên và không ghi.
- **AC-EVENT-01-2:** Given tên/ngày hợp lệ, When lưu mới thành công, Then tạo event với icon đã chọn hoặc `●`, targetDate ở đầu ngày và load danh sách tăng theo targetDate; ngày quá khứ không bị form chặn.
- **AC-EVENT-01-3:** Given event đã có, When sửa và lưu thành công, Then cập nhật document hiện có và đặt lại alarm; khi xác nhận xóa thành công thì hủy alarm và loại event khỏi danh sách; hủy xác nhận không xóa.
- **AC-EVENT-01-4:** Given event được bind vào danh sách, When tính chênh ngày theo múi giờ thiết bị, Then hiển thị `Còn n ngày`, `Hôm nay`, `Trễ n ngày` hoặc `--` nếu không có ngày.

Ghi chú hiện trạng: adapter chỉ tính countdown khi bind; chưa có timer riêng để refresh countdown lúc nửa đêm.

### US-EVENT-05 — Nhận lời nhắc sự kiện · P2

Là người dùng, tôi muốn được nhắc trước và trong ngày sự kiện để nhớ mốc cần chuẩn bị.

Liên kết: FR-EVENT-05; UC-11; BR-EVENT-03, BR-TASK-05.

- **AC-EVENT-05-1:** Given event có ID và ngày hợp lệ, When đặt reminder, Then tính mốc 08:00 ngày trước và 08:00 ngày diễn ra theo thiết bị, hủy lịch cũ rồi chỉ đặt những mốc còn ở tương lai.
- **AC-EVENT-05-2:** Given sự kiện hôm nay và đã qua 08:00, When app đặt lại lịch, Then cả hai mốc đều bị bỏ qua; không tự chuyển sang một giờ khác.
- **AC-EVENT-05-3:** Given alarm tới thời điểm và quyền notification đã được cấp, When receiver xử lý, Then tạo notification với nội dung phù hợp loại trước ngày/trong ngày; không có quyền thì receiver bỏ qua hiển thị. Thiếu quyền exact alarm dùng lịch không chính xác.

## 6. Pomodoro

### US-POMO-01 — Chọn task để tập trung · P1

Là người dùng, tôi muốn gắn tên công việc vào phiên tập trung để nhận biết lịch sử của mình.

Liên kết: FR-POMO-01; UC-12; BR-POMO-02, BR-POMO-05.

- **AC-POMO-01-1:** Given mở picker task, When dữ liệu được nhận, Then chỉ liệt kê task chưa hoàn thành có title không rỗng, ưu tiên cao trước, gần đầu hôm nay trước, rồi dueDate và tên để phân định.
- **AC-POMO-01-2:** Given chọn một task, When picker đóng, Then tên được dùng làm nhãn lựa chọn; không có task phù hợp thì thông báo danh sách trống.
- **AC-POMO-01-3:** Given chưa chọn task, When bấm Start, Then vẫn cho bắt đầu; nếu sau đó lưu focus thì dùng tên mặc định Pomodoro. Lịch sử chỉ lưu tên, không có taskId.

### US-POMO-02 — Chọn thời lượng phiên · P1

Là người dùng, tôi muốn điều chỉnh thời lượng để phù hợp với một lần tập trung hoặc nghỉ.

Liên kết: FR-POMO-02; UC-12; BR-POMO-01.

- **AC-POMO-02-1:** Given chưa tùy chỉnh, When mở Pomodoro, Then focus mặc định 25 phút, break 5 phút; picker có preset 5/15/25/45/90 và ô nhập phút nguyên.
- **AC-POMO-02-2:** Given nhập 4, 91 hoặc nội dung không đọc được thành số nguyên, When áp dụng, Then không chấp nhận thời lượng; 5 và 90 là hai biên hợp lệ.
- **AC-POMO-02-3:** Given timer đang chạy, When xác nhận đổi thời lượng, Then dừng timer và ở paused với toàn bộ thời lượng mới; hủy xác nhận không áp dụng. Đổi trong focus cập nhật thời lượng focus dùng lần sau, đổi trong break không đổi giá trị focus đó.

### US-POMO-03 — Điều khiển và luân phiên tập trung/nghỉ · P1

Là người dùng, tôi muốn bắt đầu, tạm dừng và tiếp tục phiên, sau đó chuyển giữa tập trung và nghỉ.

Liên kết: FR-POMO-03, FR-POMO-04; UC-12; BR-POMO-03, BR-POMO-04.

- **AC-POMO-03-1:** Given timer ở trạng thái chưa chạy, When Start, Then bắt đầu đếm xuống; khi đang running thì Pause giữ remainingMillis, khi paused thì Resume đếm từ phần còn lại.
- **AC-POMO-03-2:** Given phiên đang hoạt động, When Reset, Then hủy timer, trở về focus với selectedFocusDuration và trạng thái chưa chạy; không lưu một phiên chỉ do Reset.
- **AC-POMO-03-3:** Given focus về 0 qua callback timer, When hoàn tất phiên, Then phát âm/rung, yêu cầu lưu history, tự bắt đầu break 5 phút. Break về 0 thì tự bắt đầu focus với thời lượng đã chọn và không lưu break.
- **AC-POMO-03-4:** Given đang ở break và chọn Complete, When xử lý, Then thông báo Complete chỉ áp dụng focus và reset; không thêm session break vào history.

### US-POMO-05 — Lưu lịch sử focus · P1

Là người dùng, tôi muốn phiên tập trung xuất hiện trong thống kê để xem lại hoạt động.

Liên kết: FR-POMO-05; UC-12, UC-13; BR-POMO-05.

- **AC-POMO-05-1:** Given focus hoàn tất tự động và có UID, When gửi lưu, Then payload chứa userId, taskName, duration theo phút từ totalMillis và timestamp hiện tại; không đổi trạng thái hoàn thành của task.
- **AC-POMO-05-2:** Given focus được đặt 25 phút và mới chạy 1 phút, When chọn Complete thủ công rồi Firebase lưu thành công, Then history hiện tại ghi 25 phút, không phải 1 phút thực tế.
- **AC-POMO-05-3:** Given Complete thủ công, When callback lưu thành công hoặc lỗi, Then reset timer; lỗi lưu có thông báo và không có retry nghiệp vụ tự động. Given lưu tự động lỗi, Then không chặn việc chuyển sang break.

### US-POMO-06 — Quay lại bộ đếm trong cùng tiến trình · P2

Là người dùng, tôi muốn quay lại màn Pomodoro và tiếp tục quan sát trạng thái còn được giữ trong ứng dụng.

Liên kết: FR-POMO-06; UC-12; BR-POMO-06.

- **AC-POMO-06-1:** Given rời màn làm view bị hủy nhưng tiến trình vẫn tồn tại, When mở lại bằng SessionStore đang running có elapsedRealtime hợp lệ, Then đối chiếu đồng hồ để tính mode và thời gian còn lại, sau đó tạo lại CountDownTimer.
- **AC-POMO-06-2:** Given trong lúc không có view, thời điểm kết thúc focus đã bị vượt qua, When reconcile chạy, Then có thể chuyển mode/thời gian nhưng không tự ghi bù history cho phiên đã bị vượt.
- **AC-POMO-06-3:** Given ứng dụng được mở trong tiến trình mới và Pomodoro không nhận savedInstanceState để khôi phục, When tạo màn Pomodoro, Then SessionStore static khởi tạo lại ở FOCUS, thời lượng và thời gian còn lại 25 phút, chưa running/paused và chưa chọn task.

Ghi chú hiện trạng: AC thứ ba chỉ áp dụng khởi động mới không có Bundle khôi phục. Ứng dụng chưa có foreground service hoặc cơ chế lưu SessionStore bền vững bảo đảm bộ đếm liên tục qua process death.

## 7. Thống kê và cài đặt

### US-STAT-01 — Xem số liệu hôm nay và tuần này · P1

Là người dùng, tôi muốn biết số phiên và thời lượng tập trung trong ngày/tuần để tự theo dõi hoạt động.

Liên kết: FR-STAT-01, FR-STAT-05; UC-13; BR-STAT-01, BR-STAT-05.

- **AC-STAT-01-1:** Given có UID, When mở thống kê, Then lắng nghe tối đa 300 session mới nhất theo timestamp giảm dần; tổng hôm nay tính từ đầu ngày tới now, tổng tuần từ 00:00 thứ Hai tới now theo múi giờ thiết bị.
- **AC-STAT-01-2:** Given session thuộc khoảng tính, When tổng hợp, Then số phiên tăng 1, phút cộng max(0,duration); giờ hôm nay hiển thị một số lẻ thập phân và thời lượng tuần hiển thị giờ/phút. Timestamp tương lai không được cộng.
- **AC-STAT-01-3:** Given màn thống kê đang active tới nửa đêm hoặc resume vào ngày khác, When refresh chạy, Then tính lại từ snapshot gần nhất hoặc load khi chưa có snapshot. Given có 301 session trong tuần hiện tại, tất cả trước now và mỗi session duration=1, When query 300 phiên mới nhất trả về, Then số phiên tuần là 300 và tổng phút tuần là 300.
- **AC-STAT-01-4:** Given không có current user, When load thống kê, Then báo cần đăng nhập và đóng Activity; lỗi listener báo không tải được dữ liệu, không tạo session thay thế.

### US-STAT-02 — Xem phân bổ và các phiên hôm nay · P2

Là người dùng, tôi muốn xem thời gian được phân bổ cho tên công việc nào và các phiên vừa ghi nhận.

Liên kết: FR-STAT-02, FR-STAT-03; UC-13; BR-STAT-02, BR-STAT-03.

- **AC-STAT-02-1:** Given session hôm nay có taskName giống nhau sau trim, When tổng hợp chart, Then gộp phút vào cùng một mục bất kể taskId; tên rỗng/null dùng `(Không rõ)`.
- **AC-STAT-02-2:** Given nhóm có tổng phút bằng 0 hoặc không có phiên hôm nay, When vẽ, Then không tạo lát giá trị dương cho nhóm đó; không có entry hợp lệ thì xóa chart và dùng trạng thái không có dữ liệu.
- **AC-STAT-02-3:** Given có nhiều phiên hôm nay, When hiển thị focus records, Then lấy tối đa 40 phiên mới nhất trong tập đã tải và hiển thị tên/thời gian/phút/nhãn TẬP TRUNG; không phân trang sang lịch sử hôm trước.

### US-STAT-04 — Chia sẻ thống kê · P2

Là người dùng, tôi muốn gửi nhanh số liệu đang xem qua ứng dụng khác.

Liên kết: FR-STAT-04; UC-14; BR-STAT-04.

- **AC-STAT-04-1:** Given màn thống kê có các giá trị hiện tại, When nhấn Share, Then mở Android chooser với ACTION_SEND text/plain chứa số phiên/giờ hôm nay và số phiên/thời lượng tuần đang hiển thị.
- **AC-STAT-04-2:** Given không có ứng dụng nhận hoặc không mở được chooser, When thử chia sẻ, Then báo không thể chia sẻ; không tạo file ảnh/PDF hoặc đánh dấu dữ liệu đã được người nhận xem.

### US-SET-01 — Lưu tùy chọn giao diện và switch âm thanh · P3

Là người dùng, tôi muốn lưu các lựa chọn cục bộ để lần mở ứng dụng tiếp theo dùng lại cấu hình.

Liên kết: FR-SET-01, FR-SET-02; UC-15; BR-SET-01, BR-SET-02.

- **AC-SET-01-1:** Given chọn theo hệ thống/sáng/tối, When xác nhận, Then lưu lần lượt 0/1/2, áp dụng AppCompatDelegate và recreate màn; lần Application khởi động sau đọc lại mode đã lưu.
- **AC-SET-01-2:** Given chưa có preference âm thanh, When mở cài đặt, Then switch mặc định bật. Given thay đổi switch, When mở lại cài đặt, Then trạng thái được đọc lại từ SharedPreferences.
- **AC-SET-01-3:** Given `sound_notifications_enabled=false` và Context hợp lệ, When `playTimerFinishedAlert` được gọi khi timer kết thúc, Then hàm vẫn gọi `vibrateOnce` và `playAlarmSoundOnce` mà không đọc preference âm thanh. Kiểm tra đường gọi trong source; âm thực phát còn phụ thuộc thiết bị, URI chuông và cấu hình âm lượng.

Ghi chú hiện trạng: một số màn/chart còn hardcode màu; lựa chọn AppCompat mode chưa đồng nghĩa mọi thành phần đã hiển thị đúng trong cả hai theme.

## 8. Vòng đời dữ liệu công việc

### US-CLEAN-01 — Dọn dữ liệu công việc theo ngày · P2

Là người dùng, tôi muốn hiểu cách ứng dụng tự dọn dữ liệu để biết công việc nào còn xuất hiện khi quay lại màn chính.

Liên kết: FR-CLEAN-01; UC-09; BR-CLEAN-01, BR-CLEAN-02, BR-CLEAN-03.

Dọn dữ liệu chạy tự động; ứng dụng chưa có tùy chọn bật/tắt cơ chế này.

- **AC-CLEAN-01-1:** Given MainActivity resume có UID và ngày dọn cuối của UID khác hôm nay, When bắt đầu xử lý, Then chạy chuỗi dọn; nếu cùng ngày đã hoàn tất thì bỏ qua. Không có yêu cầu job chạy nền đúng 00:00.
- **AC-CLEAN-01-2:** Given task có completedAt trước đầu hôm nay, When query đầu chạy, Then task thuộc diện xóa kể cả cờ completed/isCompleted không đồng nhất, vì query không kiểm tra hai cờ này; mỗi batch tối đa 450 rồi query lại.
- **AC-CLEAN-01-3:** Given bước legacy trả về task có completed hoặc isCompleted true và completedAt null/trước hôm nay, When lọc tập tối đa 450 kết quả, Then xóa các task đó. Nếu tập đầu không có item cần xóa thì nhánh có thể dừng, không bảo đảm quét hết các bản ghi phía sau.
- **AC-CLEAN-01-4:** Given mọi bước callback thành công, When kết thúc, Then lưu ngày đã dọn của UID; nếu một bước lỗi thì chưa ghi mốc thành công. Các hàm dọn không gọi `ReminderManager.cancelReminder` cho task bị xóa, có thể kiểm tra trực tiếp trong source.

## 9. Đối chiếu và nghiệm thu

| Nhóm story | Điểm kiểm tra nguồn chính |
| --- | --- |
| AUTH | `AuthAccountMapper.toAuthEmail`; `RegisterActivity.registerUser`; `LoginActivity.loginUser`, `firebaseAuthWithGoogle`; `SettingsActivity.showChangePasswordDialog`, `performLogout`. |
| CAT | `CategoryRepository`; `FirestoreCategoryDataSource.runInsertAndShiftBatch`; `MainActivity.deleteCategory`, `persistMenuCategoryOrder`; `MenuCategoryAdapter`. |
| TASK | `AddTaskBottomSheetFragment.handleSendTask`, `addNewTaskWithNextOrder`, voice launchers; `CategoryFragment.onTaskCheckedChanged`, `deleteTask`, `persistTaskOrder`; `ReminderManager`. |
| VIEW / SEARCH | `WelcomeFragment.computeAndUpdateCounts`; `TaskFilterFragment.filterTasks`; `CalendarFragment`; `SearchFragment.normalizeForSearch`, `applyFilter`, `onTaskClicked`. |
| EVENT | `AddEventBottomSheetFragment.handleSaveAction`; `EventAdapter`; `EventFragment`; `EventReminderManager`; `NotificationReceiver`. |
| POMO | `PomodoroFragment` handlers, `onSessionCompleted`, `savePomodoroHistory`, `reconcileRunningStateWithClock`. |
| STAT / SET / CLEAN | `FocusStatisticsActivity`; `TickTokApplication`; `SettingsActivity`; `MainActivity.maybeRunDailyCompletedTaskCleanup`, `deleteCompletedTasksBefore`, `purgeCompletedTasksWithoutTimestamp`. |

Liên kết tới từng file nguồn và diễn giải điều kiện nằm trong [chỉ mục bằng chứng của Business Rules](BUSINESS_RULES.md#13-chỉ-mục-bằng-chứng). Khi thực thi AC, cần ghi riêng thiết bị/API, múi giờ, UID/test data, quyền micro/notification/exact alarm, kết quả ghi Firebase và ảnh hoặc log làm bằng chứng. Không dùng dữ liệu thật để thử các kịch bản xóa/dọn.

Chuẩn bị dữ liệu riêng cho các tình huống lỗi Firebase, đổi ngày, kết thúc tiến trình, thay đổi quyền và số lượng bản ghi lớn. Ghi nhận kết quả Pass/Fail trong báo cáo kiểm thử.
