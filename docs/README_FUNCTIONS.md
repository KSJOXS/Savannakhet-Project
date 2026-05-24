# 📘 Tài liệu Đặc tả Chức năng Hệ thống
# Ứng dụng Du lịch Thông minh Savannakhet (Savannakhet Smart Travel)

---

## 2.1.1 Đặc tả chức năng — Người dùng thông thường (User)

---

### Bảng 01 Đặc tả chức năng Đăng ký

| Mã chức năng | 01 |
|---|---|
| Tên chức năng | Đăng ký tài khoản (Register) |
| Đối tượng sử dụng | Người dùng chưa có tài khoản |
| Tiền điều kiện | Chưa có tài khoản trong hệ thống |
| Quy trình nghiệp vụ | Người dùng mở trang đăng ký → Điền tên người dùng, Email, mật khẩu, xác nhận mật khẩu và chọn sở thích → Nhấn nút "Đăng ký" |
| Kết quả | - Nếu thành công: Hệ thống tạo tài khoản mới và chuyển hướng đến trang đăng nhập<br>- Nếu thất bại: Hiển thị thông báo "Tên người dùng đã được sử dụng" hoặc "Email đã được đăng ký" |

---

### Bảng 02 Đặc tả chức năng Đăng nhập

| Mã chức năng | 02 |
|---|---|
| Tên chức năng | Đăng nhập vào hệ thống (Login) |
| Đối tượng sử dụng | Người dùng / Quản trị viên |
| Tiền điều kiện | Đã có tài khoản trong hệ thống |
| Quy trình nghiệp vụ | Người dùng mở trang đăng nhập → Điền tên người dùng và mật khẩu → Nhấn nút "Đăng nhập" |
| Kết quả | - Nếu thành công: Hệ thống tạo JWT Token, trả thông tin người dùng (role, username) và chuyển đến trang khám phá<br>- Nếu thất bại: Hiển thị thông báo "Tên người dùng hoặc mật khẩu không đúng" hoặc "Tài khoản đã bị tạm khóa" |

---

### Bảng 03 Đặc tả chức năng Quên mật khẩu

| Mã chức năng | 03 |
|---|---|
| Tên chức năng | Quên mật khẩu (Forgot Password) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Đã có tài khoản trong hệ thống |
| Quy trình nghiệp vụ | Người dùng mở trang quên mật khẩu → Nhập địa chỉ Email → Nhấn nút "Gửi liên kết đặt lại" → Hệ thống tạo Token ngẫu nhiên và gửi Email |
| Kết quả | - Nếu thành công: Hệ thống gửi liên kết đặt lại mật khẩu đến Email (luôn hiển thị thông báo thành công để bảo mật)<br>- Nếu thất bại: Hệ thống vẫn hiển thị thông báo "Gửi thành công" để tránh rò rỉ thông tin người dùng |

---

### Bảng 04 Đặc tả chức năng Đặt lại mật khẩu

| Mã chức năng | 04 |
|---|---|
| Tên chức năng | Đặt lại mật khẩu (Reset Password) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Có Token đặt lại mật khẩu chưa hết hạn |
| Quy trình nghiệp vụ | Người dùng nhấp vào liên kết trong Email → Nhập mật khẩu mới và xác nhận → Nhấn nút "Lưu mật khẩu mới" |
| Kết quả | - Nếu thành công: Hệ thống cập nhật mật khẩu mới (mã hóa bcrypt) và xóa Token, chuyển đến trang đăng nhập<br>- Nếu thất bại: Hiển thị thông báo "Token không hợp lệ hoặc đã hết hạn" |

---

### Bảng 05 Đặc tả chức năng Chỉnh sửa hồ sơ

| Mã chức năng | 05 |
|---|---|
| Tên chức năng | Chỉnh sửa hồ sơ cá nhân (Edit Profile) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập vào hệ thống |
| Quy trình nghiệp vụ | Người dùng mở trang hồ sơ → Chỉnh sửa tên, Email, mật khẩu, sở thích hoặc ảnh đại diện → Nhấn nút "Lưu" |
| Kết quả | - Nếu thành công: Hệ thống cập nhật thông tin và hiển thị hồ sơ đã được cập nhật<br>- Nếu thất bại: Hiển thị thông báo "Tên người dùng/Email đã được sử dụng" |

---

### Bảng 06 Đặc tả chức năng Khám phá địa điểm

| Mã chức năng | 06 |
|---|---|
| Tên chức năng | Tìm kiếm và xem địa điểm du lịch (Explore Places) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Không có (có thể sử dụng ngay) |
| Quy trình nghiệp vụ | Người dùng mở trang khám phá → Chọn lọc theo danh mục (thiên nhiên / nhà hàng / khách sạn v.v.) → Hệ thống tải danh sách địa điểm đã được phê duyệt |
| Kết quả | - Nếu thành công: Hiển thị danh sách địa điểm kèm hình ảnh, điểm đánh giá và danh mục<br>- Nếu thất bại: Hiển thị thông báo không tìm thấy địa điểm theo điều kiện |

---

### Bảng 07 Đặc tả chức năng Xem chi tiết địa điểm

| Mã chức năng | 07 |
|---|---|
| Tên chức năng | Xem thông tin chi tiết địa điểm (Place Detail) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Không có |
| Quy trình nghiệp vụ | Người dùng nhấp vào địa điểm từ danh sách → Hệ thống tải thông tin chi tiết và ghi nhật ký tương tác loại "xem" với trọng số 1.0 |
| Kết quả | - Nếu thành công: Hiển thị hình ảnh, mô tả, giờ mở cửa, bản đồ, đánh giá và địa điểm tương tự (AI Similar)<br>- Nếu thất bại: Hiển thị trang "Không tìm thấy địa điểm" |

---

### Bảng 08 Đặc tả chức năng Lưu địa điểm yêu thích

| Mã chức năng | 08 |
|---|---|
| Tên chức năng | Lưu / Hủy địa điểm yêu thích (Toggle Favorite) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập vào hệ thống |
| Quy trình nghiệp vụ | Người dùng nhấn biểu tượng trái tim trên trang chi tiết địa điểm → Hệ thống kiểm tra địa điểm có trong danh sách yêu thích hay không |
| Kết quả | - Nếu thêm thành công: Địa điểm được lưu vào danh sách yêu thích, biểu tượng chuyển sang màu đỏ<br>- Nếu hủy thành công: Địa điểm bị xóa khỏi danh sách yêu thích, biểu tượng chuyển sang màu xám<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy địa điểm" |

---

### Bảng 09 Đặc tả chức năng Viết đánh giá

| Mã chức năng | 09 |
|---|---|
| Tên chức năng | Viết đánh giá và chấm điểm địa điểm (Write Review) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập vào hệ thống |
| Quy trình nghiệp vụ | Người dùng mở trang viết đánh giá → Chọn địa điểm → Chấm điểm (1–5 sao) → Viết nội dung đánh giá → Tải ảnh lên (nếu có) → Nhấn nút "Gửi đánh giá" |
| Kết quả | - Nếu thành công: Lưu đánh giá và tự động tính điểm trung bình mới của địa điểm, ghi nhật ký tương tác theo số sao<br>- Nếu thất bại: Hiển thị thông báo lỗi |

---

### Bảng 10 Đặc tả chức năng Chỉnh sửa và xóa đánh giá

| Mã chức năng | 10 |
|---|---|
| Tên chức năng | Chỉnh sửa / Xóa đánh giá của mình (Edit / Delete Review) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập và là chủ sở hữu của đánh giá đó |
| Quy trình nghiệp vụ | Người dùng mở trang hồ sơ → Chọn đánh giá muốn thay đổi → Nhấn nút "Chỉnh sửa" hoặc "Xóa" → Xác nhận hành động |
| Kết quả | - Chỉnh sửa thành công: Cập nhật nội dung, điểm số, hình ảnh và tính lại điểm trung bình của địa điểm<br>- Xóa thành công: Xóa đánh giá và tính lại điểm trung bình<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy đánh giá hoặc không có quyền" |

---

### Bảng 11 Đặc tả chức năng Xem bảng tin cộng đồng

| Mã chức năng | 11 |
|---|---|
| Tên chức năng | Xem bảng tin đánh giá cộng đồng (Community Feed) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Không có |
| Quy trình nghiệp vụ | Người dùng mở trang cộng đồng → Hệ thống tải 50 bài đánh giá mới nhất cùng bình luận |
| Kết quả | - Nếu thành công: Hiển thị bài đăng kèm hình ảnh, tên người đăng, tên địa điểm và số lượt thích<br>- Nếu thất bại: Hiển thị thông báo không có bài đăng trong lúc này |

---

### Bảng 12 Đặc tả chức năng Thích bài đánh giá

| Mã chức năng | 12 |
|---|---|
| Tên chức năng | Thích / Bỏ thích bài đánh giá (Toggle Like) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập vào hệ thống |
| Quy trình nghiệp vụ | Người dùng nhấn nút thích trên bài đăng trong bảng tin → Hệ thống kiểm tra đã từng thích hay chưa |
| Kết quả | - Thích thành công: Thêm ID người dùng vào danh sách liked_by, số lượt thích tăng lên<br>- Bỏ thích thành công: Xóa ID người dùng khỏi danh sách liked_by, số lượt thích giảm xuống<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy bài đăng" |

---

### Bảng 13 Đặc tả chức năng Bình luận bài đăng

| Mã chức năng | 13 |
|---|---|
| Tên chức năng | Bình luận dưới bài đánh giá (Post Comment) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập vào hệ thống |
| Quy trình nghiệp vụ | Người dùng gõ bình luận vào ô bình luận dưới bài đăng → Nhấn nút "Gửi" |
| Kết quả | - Nếu thành công: Bình luận được lưu và hiển thị ngay dưới bài đăng<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy bài đăng" |

---

### Bảng 14 Đặc tả chức năng Lập kế hoạch du lịch bằng AI

| Mã chức năng | 14 |
|---|---|
| Tên chức năng | Tạo lịch trình du lịch tự động bằng AI (AI Trip Planner) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Không có (đăng nhập để nhận lịch trình phù hợp hơn với sở thích) |
| Quy trình nghiệp vụ | Người dùng mở trang lập kế hoạch → Chọn số ngày, ngân sách, tháng và sở thích → Nhấn nút "Tạo kế hoạch" → Hệ thống tự động chọn địa điểm theo khung giờ Sáng / Chiều / Tối |
| Kết quả | - Nếu thành công: Hiển thị lịch trình theo từng ngày với 3 địa điểm mỗi ngày không trùng lặp<br>- Nếu thất bại: Hiển thị thông báo không có đủ địa điểm |

---

### Bảng 15 Đặc tả chức năng Lưu lịch trình du lịch

| Mã chức năng | 15 |
|---|---|
| Tên chức năng | Lưu lịch trình du lịch (Save Itinerary) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập và đã tạo lịch trình |
| Quy trình nghiệp vụ | Người dùng nhấn nút "Lưu kế hoạch" → Đặt tên cho lịch trình → Xác nhận |
| Kết quả | - Nếu thành công: Lưu lịch trình vào cơ sở dữ liệu và hiển thị trong trang hồ sơ<br>- Nếu thất bại: Hiển thị thông báo lỗi |

---

### Bảng 16 Đặc tả chức năng Đổi địa điểm trong kế hoạch

| Mã chức năng | 16 |
|---|---|
| Tên chức năng | Đổi địa điểm trong lịch trình du lịch (Swap Place) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Đã có lịch trình được tạo |
| Quy trình nghiệp vụ | Người dùng nhấn nút "Đổi địa điểm" trên thẻ địa điểm → Hệ thống tìm địa điểm khác phù hợp với khung giờ và sở thích |
| Kết quả | - Nếu thành công: Hiển thị địa điểm mới phù hợp với khung giờ (Sáng/Chiều/Tối) và chưa được dùng trong kế hoạch<br>- Nếu thất bại: Hiển thị thông báo "Không có địa điểm thay thế" |

---

### Bảng 17 Đặc tả chức năng Gửi địa điểm mới

| Mã chức năng | 17 |
|---|---|
| Tên chức năng | Gửi địa điểm mới chờ phê duyệt (Submit Place) |
| Đối tượng sử dụng | Người dùng đã được cấp quyền đăng bài |
| Tiền điều kiện | Người dùng đã đăng nhập và đã được quản trị viên phê duyệt quyền đăng |
| Quy trình nghiệp vụ | Người dùng mở trang gửi địa điểm → Điền tên, mô tả, danh mục, tọa độ GPS, giờ mở cửa và tải ảnh lên → Nhấn nút "Gửi" |
| Kết quả | - Nếu thành công: Địa điểm được lưu với trạng thái "đang chờ" chờ quản trị viên xét duyệt<br>- Nếu thất bại: Hiển thị thông báo lỗi |

---

### Bảng 18 Đặc tả chức năng Yêu cầu quyền đăng bài

| Mã chức năng | 18 |
|---|---|
| Tên chức năng | Yêu cầu quyền đăng địa điểm (Request Post Permission) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập và chưa có quyền đăng bài |
| Quy trình nghiệp vụ | Người dùng mở trang hồ sơ → Nhấn nút "Yêu cầu quyền đăng địa điểm" |
| Kết quả | - Nếu thành công: Trạng thái người dùng chuyển sang "đang chờ" và chờ quản trị viên phê duyệt<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy người dùng" |

---

### Bảng 19 Đặc tả chức năng Xem địa điểm gợi ý bởi AI

| Mã chức năng | 19 |
|---|---|
| Tên chức năng | Xem địa điểm được AI gợi ý (AI Recommendations) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Người dùng đã đăng nhập và có lịch sử sử dụng trong hệ thống |
| Quy trình nghiệp vụ | Hệ thống tải mô hình AI (GNN) → Tính điểm Hybrid: 60% lọc cộng tác + 40% lọc dựa trên nội dung từ sở thích của người dùng |
| Kết quả | - Nếu thành công: Hiển thị địa điểm gợi ý kèm lý do "Vì bạn đã từng thích..." và điểm phù hợp<br>- Trường hợp Cold Start: Hiển thị thông báo "Chưa có đủ dữ liệu" và gợi ý địa điểm phổ biến thay thế |

---

### Bảng 20 Đặc tả chức năng Liên hệ

| Mã chức năng | 20 |
|---|---|
| Tên chức năng | Gửi tin nhắn liên hệ (Contact Us) |
| Đối tượng sử dụng | Người dùng thông thường |
| Tiền điều kiện | Không có |
| Quy trình nghiệp vụ | Người dùng mở trang liên hệ → Điền tên, Email, chủ đề, nội dung tin nhắn → Nhấn nút "Gửi tin nhắn" |
| Kết quả | - Nếu thành công: Lưu tin nhắn vào cơ sở dữ liệu và hiển thị thông báo xác nhận<br>- Nếu thất bại: Hiển thị thông báo lỗi |

---

## 2.1.2 Đặc tả chức năng — Quản trị viên (Admin)

---

### Bảng 21 Đặc tả chức năng Xem bảng điều khiển thống kê

| Mã chức năng | 21 |
|---|---|
| Tên chức năng | Xem bảng điều khiển thống kê hệ thống (Admin Dashboard) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Đã đăng nhập với quyền quản trị viên |
| Quy trình nghiệp vụ | Quản trị viên mở bảng điều khiển quản trị → Hệ thống truy vấn thống kê từ cơ sở dữ liệu |
| Kết quả | - Nếu thành công: Hiển thị tổng số người dùng, địa điểm, đánh giá, thống kê theo danh mục và top 5 địa điểm được đánh giá cao nhất<br>- Nếu thất bại: Hiển thị thông báo "Lỗi truy vấn cơ sở dữ liệu" |

---

### Bảng 22 Đặc tả chức năng Quản lý địa điểm

| Mã chức năng | 22 |
|---|---|
| Tên chức năng | Quản lý địa điểm du lịch (Manage Places) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Đã đăng nhập với quyền quản trị viên |
| Quy trình nghiệp vụ | Quản trị viên mở trang quản lý địa điểm → Chọn thêm / chỉnh sửa / xóa địa điểm → Điền thông tin và xác nhận |
| Kết quả | - Thêm thành công: Địa điểm mới với trạng thái "đã duyệt" hiển thị ngay lập tức<br>- Chỉnh sửa thành công: Thông tin địa điểm được cập nhật<br>- Xóa thành công: Địa điểm bị xóa khỏi toàn bộ hệ thống<br>- Nếu thất bại: Hiển thị thông báo lỗi |

---

### Bảng 23 Đặc tả chức năng Phê duyệt địa điểm chờ duyệt

| Mã chức năng | 23 |
|---|---|
| Tên chức năng | Phê duyệt / Từ chối địa điểm do người dùng gửi (Pending Places Approval) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Có địa điểm đang chờ phê duyệt trong hệ thống |
| Quy trình nghiệp vụ | Quản trị viên mở trang địa điểm chờ duyệt → Kiểm tra thông tin địa điểm → Nhấn nút "Phê duyệt" hoặc "Từ chối" |
| Kết quả | - Phê duyệt thành công: Địa điểm chuyển trạng thái "đã duyệt" và hiển thị trên website ngay<br>- Từ chối thành công: Địa điểm chuyển trạng thái "đã từ chối" và bị ẩn khỏi website<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy địa điểm" |

---

### Bảng 24 Đặc tả chức năng Quản lý danh mục

| Mã chức năng | 24 |
|---|---|
| Tên chức năng | Quản lý danh mục địa điểm (Manage Categories) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Đã đăng nhập với quyền quản trị viên |
| Quy trình nghiệp vụ | Quản trị viên mở trang quản lý danh mục → Thêm danh mục mới (tên, loại chính) hoặc xóa danh mục hiện có |
| Kết quả | - Thêm thành công: Danh mục mới hiển thị trong hệ thống<br>- Xóa thành công: Danh mục bị xóa khỏi hệ thống<br>- Nếu thất bại: Hiển thị thông báo "Danh mục đã tồn tại" hoặc "Không tìm thấy danh mục" |

---

### Bảng 25 Đặc tả chức năng Quản lý người dùng

| Mã chức năng | 25 |
|---|---|
| Tên chức năng | Quản lý người dùng trong hệ thống (Manage Users) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Đã đăng nhập với quyền quản trị viên |
| Quy trình nghiệp vụ | Quản trị viên mở trang quản lý người dùng → Xem danh sách người dùng → Chọn tạm khóa tài khoản hoặc khôi phục tài khoản |
| Kết quả | - Tạm khóa thành công: Tài khoản bị khóa, người dùng không thể đăng nhập (có thể khôi phục trong 3 ngày)<br>- Khôi phục thành công: Tài khoản hoạt động trở lại bình thường<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy người dùng" hoặc "Quá 3 ngày không thể khôi phục" |

---

### Bảng 26 Đặc tả chức năng Phê duyệt quyền đăng bài

| Mã chức năng | 26 |
|---|---|
| Tên chức năng | Phê duyệt / Từ chối quyền đăng bài của người dùng (Approve Post Permission) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Có người dùng đang chờ phê duyệt quyền đăng bài |
| Quy trình nghiệp vụ | Quản trị viên mở trang yêu cầu quyền đăng bài → Xem xét yêu cầu → Nhấn nút "Phê duyệt" hoặc "Từ chối" |
| Kết quả | - Phê duyệt thành công: Người dùng được cấp quyền đăng địa điểm mới<br>- Từ chối thành công: Trạng thái người dùng chuyển sang "đã từ chối"<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy người dùng" |

---

### Bảng 27 Đặc tả chức năng Quản lý đánh giá

| Mã chức năng | 27 |
|---|---|
| Tên chức năng | Quản lý đánh giá trong hệ thống (Manage Comments) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Đã đăng nhập với quyền quản trị viên |
| Quy trình nghiệp vụ | Quản trị viên mở trang quản lý đánh giá → Xem danh sách đánh giá tất cả → Nhấn nút "Xóa" đối với đánh giá không phù hợp |
| Kết quả | - Nếu thành công: Đánh giá bị xóa khỏi hệ thống<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy đánh giá" |

---

### Bảng 28 Đặc tả chức năng Quản lý tin nhắn liên hệ

| Mã chức năng | 28 |
|---|---|
| Tên chức năng | Quản lý tin nhắn liên hệ từ người dùng (Manage Contact Messages) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Đã đăng nhập với quyền quản trị viên |
| Quy trình nghiệp vụ | Quản trị viên mở trang quản lý tin nhắn → Xem danh sách (tin nhắn chưa đọc hiển thị trước) → Nhấp để mở đọc → Trả lời |
| Kết quả | - Đọc thành công: Trạng thái tin nhắn chuyển sang "đã đọc"<br>- Trả lời thành công: Trạng thái chuyển sang "đã trả lời"<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy tin nhắn" |

---

### Bảng 29 Đặc tả chức năng Cài đặt website

| Mã chức năng | 29 |
|---|---|
| Tên chức năng | Cài đặt website và quản lý ảnh Hero Banner (Site Settings) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Đã đăng nhập với quyền quản trị viên |
| Quy trình nghiệp vụ | Quản trị viên mở trang cài đặt → Tải ảnh Hero Banner mới lên hoặc xóa ảnh hiện có |
| Kết quả | - Tải lên thành công: Ảnh được lưu và hiển thị trên trang chủ (tối đa 10 ảnh mỗi tab)<br>- Xóa thành công: Ảnh bị xóa khỏi máy chủ và cơ sở dữ liệu<br>- Nếu thất bại: Hiển thị thông báo "Tệp phải là ảnh" hoặc "Đã đủ 10 ảnh" |

---

### Bảng 30 Đặc tả chức năng Huấn luyện mô hình AI

| Mã chức năng | 30 |
|---|---|
| Tên chức năng | Huấn luyện mô hình AI gợi ý địa điểm (Train GNN Model) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Có đủ dữ liệu nhật ký tương tác trong hệ thống |
| Quy trình nghiệp vụ | Quản trị viên mở bảng điều khiển → Nhấn nút "Huấn luyện mô hình AI" → Hệ thống xây dựng đồ thị từ nhật ký tương tác và huấn luyện mô hình GNN (SAGEConv) 100 vòng lặp |
| Kết quả | - Nếu thành công: Lưu trọng số mô hình vào tệp gnn_model.pt và thông báo giá trị Loss<br>- Nếu thất bại: Hiển thị thông báo "Không đủ dữ liệu tương tác để huấn luyện" |

---

### Bảng 31 Đặc tả chức năng Quản lý nội dung phần địa điểm

| Mã chức năng | 31 |
|---|---|
| Tên chức năng | Quản lý nội dung phong phú của địa điểm (Manage Place Sections) |
| Đối tượng sử dụng | Quản trị viên (Admin) |
| Tiền điều kiện | Đã đăng nhập với quyền quản trị viên và có địa điểm trong hệ thống |
| Quy trình nghiệp vụ | Quản trị viên mở trang chỉnh sửa địa điểm → Thêm / chỉnh sửa / xóa phần nội dung (hình ảnh + bài viết) → Xác định thứ tự hiển thị |
| Kết quả | - Thêm thành công: Phần nội dung mới hiển thị trong trang chi tiết địa điểm theo thứ tự đã đặt<br>- Chỉnh sửa thành công: Nội dung được cập nhật<br>- Xóa thành công: Phần nội dung bị xóa<br>- Nếu thất bại: Hiển thị thông báo "Không tìm thấy địa điểm" hoặc "Không tìm thấy phần nội dung" |

---

*Tài liệu đặc tả chức năng — Được tạo từ mã nguồn ngày 23 tháng 5 năm 2026*
