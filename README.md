# TickTok

**Ứng dụng Android quản lý công việc và thời gian tập trung.**

TickTok kết hợp danh sách việc cần làm, lịch, sự kiện và bộ đếm Pomodoro trong cùng một ứng dụng. Người dùng có thể tổ chức công việc theo danh mục, theo dõi thời hạn, đặt lời nhắc và xem thống kê thời gian tập trung của mình.

Dự án được viết bằng **Java**, sử dụng giao diện **XML**, **Firebase Authentication** để xác thực và **Cloud Firestore** để lưu dữ liệu theo tài khoản.

## Tài liệu phân tích nghiệp vụ

[Bộ tài liệu BA](docs/ba/README.md) gồm BRD, SRS, User Stories & Acceptance Criteria, Business Rules, Use Case Diagram, đặc tả use case và các quy trình BPMN. Nội dung mô tả hiện trạng theo mã nguồn; sơ đồ có bản xem SVG và file nguồn chỉnh sửa.

## Tính năng

| Nhóm chức năng | Nội dung |
| --- | --- |
| Tài khoản | Đăng ký, đăng nhập bằng email hoặc tên tài khoản và mật khẩu; đăng nhập Google; đổi mật khẩu cho tài khoản dùng mật khẩu; đăng xuất. |
| Tổng quan công việc | Xem số lượng và danh sách việc hôm nay, ngày mai, quá hạn và đã hoàn thành hôm nay. |
| Danh mục | Thêm, sửa, xóa danh mục; chọn biểu tượng và kéo để sắp xếp thứ tự. |
| Công việc | Thêm, sửa, xóa, đánh dấu hoàn thành; nhập tiêu đề và mô tả; chọn ngày đến hạn, mức ưu tiên và thời điểm nhắc; kéo để sắp xếp trong danh mục. |
| Nhập bằng giọng nói | Nhận nội dung tiếng Việt thông qua dịch vụ nhận dạng giọng nói trên thiết bị. |
| Tìm kiếm | Tìm công việc theo tiêu đề và mô tả; mở danh mục chứa kết quả và làm nổi bật công việc được chọn. |
| Lịch và Eisenhower | Xem công việc theo ngày trong lịch tháng; xem ma trận Eisenhower phân nhóm theo mức ưu tiên. |
| Sự kiện | Tạo sự kiện với biểu tượng, ngày diễn ra và số ngày còn lại; nhắc lúc 08:00 vào ngày trước sự kiện và ngày diễn ra. |
| Pomodoro | Mặc định 25 phút tập trung và 5 phút nghỉ; tùy chỉnh thời lượng từ 5–90 phút; chọn công việc, tạm dừng, tiếp tục, đặt lại và lưu lịch sử tập trung. |
| Thống kê tập trung | Xem số phiên và thời gian tập trung hôm nay, tuần này; biểu đồ phân bổ thời gian theo tên công việc; chia sẻ thống kê bằng văn bản. |
| Cài đặt | Chọn giao diện sáng, tối hoặc theo hệ thống; quản lý mật khẩu và phiên đăng nhập. |

## Công nghệ và cấu hình

Các phiên bản dưới đây phản ánh cấu hình đang có trong mã nguồn.

| Thành phần | Cấu hình |
| --- | --- |
| Ngôn ngữ ứng dụng | Java 11 |
| Giao diện | XML, AndroidX, Material Components, RecyclerView, ConstraintLayout |
| Android tối thiểu | Android 7.0 — API 24 |
| Android SDK | `compileSdk` 36.1, `targetSdk` 36 |
| Công cụ build | Gradle Wrapper 9.4.1, Android Gradle Plugin 9.2.1, Kotlin DSL |
| JVM cho Gradle daemon | JDK 21, khai báo trong `gradle/gradle-daemon-jvm.properties` |
| Firebase | Authentication, Cloud Firestore, Analytics; Firebase BoM 34.11.0 |
| Đăng nhập Google | Google Play services Auth 21.2.0 |
| Biểu đồ | MPAndroidChart 3.1.0 |
| Nhắc lịch | AlarmManager, PendingIntent, BroadcastReceiver, NotificationCompat |
| Cài đặt cục bộ | SharedPreferences |

## Cấu trúc mã nguồn

```text
TickTok/
├── app/                  # Mã nguồn và tài nguyên Android
├── docs/
│   ├── ba/               # Yêu cầu, use case, BPMN và truy vết
│   └── reference/        # Sơ đồ và tư liệu gốc
├── scripts/              # Công cụ tái tạo sơ đồ
├── gradle/               # Gradle Wrapper và cấu hình phiên bản
├── build.gradle.kts
├── settings.gradle.kts
├── gradle.properties
├── gradlew
├── gradlew.bat
└── README.md
```

[Mục lục tài liệu](docs/README.md) · [Hướng dẫn công cụ tài liệu](scripts/README.md).

Chi tiết module Android:

```text
app/
├── build.gradle.kts
├── google-services.json
└── src/
    ├── main/
    │   ├── AndroidManifest.xml
    │   ├── java/com/example/ticktok/
    │   │   ├── TickTokApplication.java   # Áp dụng giao diện khi khởi động
    │   │   ├── activity/                # Đăng nhập, màn chính, cài đặt, thống kê
    │   │   ├── fragment/                # Công việc, danh mục, lịch, sự kiện, Pomodoro
    │   │   ├── adapter/                 # Hiển thị danh sách và lịch
    │   │   ├── model/                   # Task, Category, Event, PomodoroSession, FocusRecord
    │   │   ├── repository/              # Repository và DataSource cho danh mục
    │   │   ├── reminder/                # Đặt lịch và hiển thị thông báo
    │   │   └── util/                    # Ánh xạ tài khoản, đường dẫn Firestore
    │   └── res/                         # Layout, biểu tượng, màu sắc và chuỗi giao diện
    ├── test/                            # Kiểm thử JUnit mẫu
    └── androidTest/                     # Kiểm thử trên thiết bị mẫu
```

[MainActivity](app/src/main/java/com/example/ticktok/activity/MainActivity.java) điều phối điều hướng, menu danh mục và nút thêm nội dung. Logic màn hình chủ yếu nằm trong Activity/Fragment; các màn công việc, sự kiện và Pomodoro truy cập Firestore trực tiếp. Phần danh mục tách thành `CategoryRepositoryContract`, `CategoryRepository`, `CategoryDataSource` và `FirestoreCategoryDataSource`.

## Cài đặt và chạy

### 1. Chuẩn bị môi trường

- Android Studio hỗ trợ Android Gradle Plugin 9.2.1.
- JDK 21 cho Gradle daemon. Cấu hình biên dịch mã Java của ứng dụng vẫn là Java 11.
- Android SDK Platform 36.1 và các SDK Tools cần thiết, cài qua SDK Manager.
- Thiết bị hoặc máy ảo chạy Android 7.0 trở lên; để thử đăng nhập Google, sử dụng thiết bị có Google Play services.
- Kết nối mạng để tải Gradle, thư viện từ Google Maven, Maven Central, JitPack và sử dụng Firebase.

Mở thư mục chứa `settings.gradle.kts` bằng Android Studio. Các bước tiếp theo thiết lập Firebase trước khi build ứng dụng.

### 2. Cấu hình Firebase

1. Tạo hoặc chọn một Firebase project và đăng ký ứng dụng Android có package name **`com.example.ticktok`**, khớp với `applicationId` trong `app/build.gradle.kts`.
2. Trong Firebase Authentication, bật nhà cung cấp **Email/Password** và **Google**.
3. Thêm SHA-1 của chứng chỉ ký ứng dụng vào cấu hình Android app trong Firebase. Có thể lấy thông tin chứng chỉ debug từ thư mục gốc dự án:

   ```bash
   ./gradlew :app:signingReport
   ```

4. Tải `google-services.json` sau khi đã bật Google Sign-In và đặt tại **`app/google-services.json`**. Thư mục dự án hiện có tệp này; thay bằng cấu hình Firebase của bạn nếu dùng backend riêng.
5. Tạo cơ sở dữ liệu Cloud Firestore mặc định và cấu hình quyền truy cập cho dữ liệu theo UID như phần bên dưới.

Xem [hướng dẫn thêm Firebase vào Android](https://firebase.google.com/docs/android/setup) về đăng ký ứng dụng và vị trí tệp cấu hình. Phần bật Google, khai báo SHA-1 và tải lại cấu hình OAuth được mô tả trong [hướng dẫn Google Sign-In của Firebase](https://firebase.google.com/docs/auth/android/google-signin).

`LoginActivity` sử dụng tài nguyên `default_web_client_id`, được Google Services plugin sinh từ cấu hình OAuth trong `google-services.json`. Tệp cấu hình cần chứa OAuth client loại Web để tài nguyên này được tạo khi build.

Tên tài khoản không chứa `@` được ứng dụng ánh xạ thành email nội bộ dạng `ten_tai_khoan@ticktok.user`. Tên tài khoản chấp nhận 3–30 ký tự gồm chữ cái Latin, chữ số, dấu chấm, gạch dưới và gạch ngang. Cơ chế này vẫn sử dụng nhà cung cấp Email/Password của Firebase Authentication.

### 3. Quyền truy cập Firestore

Dữ liệu được tổ chức dưới `users/{uid}`. Có thể dùng quy tắc cơ bản sau để mỗi tài khoản chỉ đọc và ghi dữ liệu thuộc UID của mình:

```text
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId}/{document=**} {
      allow read, write: if request.auth != null
                        && request.auth.uid == userId;
    }
  }
}
```

Áp dụng quy tắc trong Firebase Console. Đây là ví dụ kiểm soát quyền sở hữu dữ liệu; dự án chưa kèm tệp rules triển khai hoặc kiểm tra cấu trúc từng trường. Xem [tài liệu Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started) để thiết lập và kiểm tra quy tắc.

### 4. Build và mở ứng dụng

Trong Android Studio, đồng bộ Gradle, chọn module `app`, chọn thiết bị rồi nhấn **Run**.

Hoặc tạo APK debug từ thư mục gốc:

```bash
./gradlew :app:assembleDebug
```

Trên Windows, dùng:

```powershell
.\gradlew.bat :app:assembleDebug
```

APK được tạo tại `app/build/outputs/apk/debug/app-debug.apk`.

## Bắt đầu sử dụng

1. Đăng ký tài khoản hoặc đăng nhập bằng Google.
2. Mở menu để tạo danh mục, sau đó thêm công việc bằng nút **+**. Dòng đầu là tiêu đề; các dòng tiếp theo là mô tả. Công việc mặc định có ngày đến hạn là hôm nay nếu chưa chọn ngày khác.
3. Xem việc theo ngày ở màn tổng quan hoặc màn lịch; dùng mức ưu tiên để phân nhóm trong ma trận Eisenhower.
4. Mở Pomodoro, chọn công việc và bắt đầu tập trung. Mở biểu tượng lịch sử để xem thống kê.
5. Mở màn sự kiện để thêm các mốc cần theo dõi và chọn ngày diễn ra.

Ứng dụng yêu cầu quyền thông báo trên Android 13 trở lên khi thiết lập lời nhắc, và quyền micro khi dùng nhập giọng nói. Nếu thiết bị chưa cho phép đặt báo thức chính xác, phần nhắc lịch dùng báo thức không chính xác làm phương án thay thế.

## Tổ chức dữ liệu

```text
users/{uid}/
├── categories/{categoryId}
├── tasks/{taskId}
├── events/{eventId}
└── pomodoro/{sessionId}
```

| Collection | Dữ liệu chính |
| --- | --- |
| `categories` | Tên danh mục, biểu tượng, thứ tự hiển thị. |
| `tasks` | Tiêu đề, mô tả, danh mục, mức ưu tiên, trạng thái hoàn thành, ngày đến hạn, thời điểm nhắc và thứ tự. |
| `events` | Tên sự kiện, biểu tượng, ngày diễn ra và thời điểm tạo. |
| `pomodoro` | `userId`, `taskName`, `duration` tính bằng phút và `timestamp` tính bằng mili giây. |

Các trường `dueDate`, `reminderTime` và `targetDate` cũng dùng mili giây Unix. `createdAt` và `completedAt` dùng thời điểm Firestore. `FocusRecord` là model phục vụ hiển thị lịch sử, được chuyển đổi từ `PomodoroSession`.

## Hành vi hiện tại

- **Thống kê:** tính trên tối đa 300 phiên Pomodoro gần nhất; danh sách lịch sử hiển thị tối đa 40 phiên của hôm nay. Tuần bắt đầu vào thứ Hai theo múi giờ thiết bị. Các phiên có cùng tên công việc được gộp trong biểu đồ.
- **Dọn công việc:** khi quay lại màn chính vào ngày mới, ứng dụng dọn công việc đã hoàn thành từ các ngày trước. Bản ghi cũ được đánh dấu hoàn thành nhưng thiếu `completedAt` cũng thuộc diện dọn.
- **Bộ đếm Pomodoro:** sử dụng `CountDownTimer` và trạng thái trong tiến trình ứng dụng; chưa có foreground service để duy trì bộ đếm độc lập khi tiến trình bị hệ thống kết thúc.
- **Quên mật khẩu:** hiện mở hướng dẫn liên hệ quản trị viên; chưa có luồng gửi email đặt lại mật khẩu trong ứng dụng.

## Kiểm thử

Chạy kiểm thử đơn vị:

```bash
./gradlew :app:testDebugUnitTest
```

Chạy kiểm thử trên thiết bị hoặc máy ảo đang kết nối:

```bash
./gradlew :app:connectedDebugAndroidTest
```

Mã nguồn hiện có các kiểm thử mẫu cho phép cộng và package name của ứng dụng. Các luồng nghiệp vụ như quản lý công việc, nhắc lịch và thống kê Pomodoro chưa có bộ kiểm thử tự động riêng.
