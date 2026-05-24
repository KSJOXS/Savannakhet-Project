# Danh sách mã Code Sequence Diagram cho tất cả 31 chức năng
Bạn có thể copy từng khối mã dưới đây và dán vào [sequencediagram.org](https://sequencediagram.org/) để tạo hình ảnh.

---

## 1. Người dùng thông thường (User)

### 01. Đăng ký tài khoản
```text
title 01: Đăng ký tài khoản (Register)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Mở trang đăng ký
activate Frontend
Người dùng->Frontend: Nhập Username, Email, Mật khẩu, Sở thích\nNhấn "Đăng ký"
Frontend->Backend: POST /register
activate Backend
Backend->Database: Kiểm tra trùng lặp (Username/Email)
activate Database
Database->Backend: Kết quả kiểm tra
deactivate Database

Backend->Backend: Mã hóa mật khẩu (bcrypt)\nTạo tài khoản mới
Backend->Database: Lưu người dùng
activate Database
Database->Backend: Xác nhận lưu
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Người dùng: Thông báo thành công\nChuyển đến trang đăng nhập
deactivate Frontend
```

### 02. Đăng nhập
```text
title 02: Đăng nhập vào hệ thống (Login)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Mở trang đăng nhập\nNhập Username, Mật khẩu
activate Frontend
Người dùng->Frontend: Nhấn "Đăng nhập"
Frontend->Backend: POST /login
activate Backend
Backend->Database: Truy vấn người dùng theo Username
activate Database
Database->Backend: Dữ liệu người dùng (Hash password)
deactivate Database

Backend->Backend: Kiểm tra mật khẩu (bcrypt)\nTạo JWT Token
Backend->Frontend: Trả về Token và thông tin User
deactivate Backend

Frontend->Frontend: Lưu Token
Frontend->Người dùng: Chuyển hướng đến trang Khám phá
deactivate Frontend
```

### 03. Quên mật khẩu
```text
title 03: Quên mật khẩu (Forgot Password)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Mở trang quên mật khẩu\nNhập Email
activate Frontend
Người dùng->Frontend: Nhấn "Gửi liên kết"
Frontend->Backend: POST /forgot-password
activate Backend
Backend->Database: Kiểm tra Email tồn tại
activate Database
Database->Backend: Kết quả
deactivate Database

Backend->Backend: Tạo Token ngẫu nhiên\nGửi Email chứa link reset
Backend->Database: Lưu Token vào DB
Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Người dùng: Hiển thị "Đã gửi liên kết qua Email"
deactivate Frontend
```

### 04. Đặt lại mật khẩu
```text
title 04: Đặt lại mật khẩu (Reset Password)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhấp link từ Email\nNhập Mật khẩu mới
activate Frontend
Người dùng->Frontend: Nhấn "Lưu mật khẩu mới"
Frontend->Backend: POST /reset-password {token, new_password}
activate Backend
Backend->Database: Kiểm tra Token hợp lệ
activate Database
Database->Backend: Kết quả kiểm tra
deactivate Database

Backend->Backend: Mã hóa mật khẩu mới
Backend->Database: Cập nhật mật khẩu\nXóa Token
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Người dùng: Chuyển đến trang đăng nhập
deactivate Frontend
```

### 05. Chỉnh sửa hồ sơ
```text
title 05: Chỉnh sửa hồ sơ (Edit Profile)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Sửa thông tin (Tên, Email, Sở thích, Ảnh)
activate Frontend
Người dùng->Frontend: Nhấn "Lưu"
Frontend->Backend: PUT /profile
activate Backend
Backend->Database: Kiểm tra trùng lặp Username/Email
activate Database
Database->Backend: Kết quả
deactivate Database

Backend->Database: Cập nhật thông tin người dùng
activate Database
Database->Backend: Xác nhận cập nhật
deactivate Database

Backend->Frontend: Thông tin hồ sơ mới
deactivate Backend
Frontend->Người dùng: Hiển thị hồ sơ đã cập nhật
deactivate Frontend
```

### 06. Khám phá địa điểm
```text
title 06: Tìm kiếm và xem địa điểm (Explore Places)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Vào trang Khám phá\nChọn bộ lọc (Danh mục)
activate Frontend
Frontend->Backend: GET /places?category=...
activate Backend
Backend->Database: Truy vấn danh sách địa điểm (approved)
activate Database
Database->Backend: Kết quả danh sách
deactivate Database

Backend->Frontend: Dữ liệu địa điểm
deactivate Backend
Frontend->Người dùng: Hiển thị danh sách địa điểm
deactivate Frontend
```

### 07. Xem chi tiết địa điểm
```text
title 07: Xem chi tiết địa điểm (Place Detail)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhấn vào một địa điểm
activate Frontend
Frontend->Backend: GET /places/{id}
activate Backend
Backend->Database: Truy vấn chi tiết địa điểm, hình ảnh, review
activate Database
Database->Backend: Dữ liệu chi tiết
deactivate Database

Backend->Database: Ghi nhật ký tương tác (View, Weight=1.0)
Backend->Backend: Gọi AI tìm địa điểm tương tự (Similar)
Backend->Frontend: Trả về chi tiết + Similar places
deactivate Backend

Frontend->Người dùng: Hiển thị trang chi tiết địa điểm
deactivate Frontend
```

### 08. Lưu địa điểm yêu thích
```text
title 08: Lưu / Hủy địa điểm yêu thích (Toggle Favorite)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhấn nút Trái tim (Yêu thích)
activate Frontend
Frontend->Backend: POST /favorites/{place_id}
activate Backend
Backend->Database: Kiểm tra đã yêu thích chưa
activate Database
Database->Backend: Kết quả
deactivate Database

Backend->Database: Thêm vào hoặc Xóa khỏi favorites
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi trạng thái (Added/Removed)
deactivate Backend
Frontend->Người dùng: Cập nhật màu sắc nút Trái tim
deactivate Frontend
```

### 09. Viết đánh giá
```text
title 09: Viết đánh giá (Write Review)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Chọn số sao, viết bình luận, tải ảnh
activate Frontend
Người dùng->Frontend: Nhấn "Gửi đánh giá"
Frontend->Backend: POST /reviews (multipart)
activate Backend
Backend->Backend: Lưu ảnh tải lên
Backend->Database: Lưu đánh giá (Rating, Comment, Images)
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Database: Tính lại Rating trung bình cho địa điểm
Backend->Database: Ghi log tương tác (Weight theo sao)
Backend->Frontend: Phản hồi thành công
deactivate Backend

Frontend->Người dùng: Hiển thị đánh giá mới
deactivate Frontend
```

### 10. Chỉnh sửa và xóa đánh giá
```text
title 10: Chỉnh sửa / Xóa đánh giá (Edit/Delete Review)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhấn "Sửa" hoặc "Xóa" đánh giá
activate Frontend
Frontend->Backend: PUT hoặc DELETE /reviews/{id}
activate Backend
Backend->Database: Kiểm tra quyền sở hữu đánh giá
activate Database
Database->Backend: Kết quả
deactivate Database

Backend->Database: Cập nhật hoặc Xóa dòng dữ liệu
Backend->Database: Tính toán lại Rating trung bình của địa điểm
Backend->Frontend: Phản hồi thành công
deactivate Backend

Frontend->Người dùng: Cập nhật giao diện
deactivate Frontend
```

### 11. Xem bảng tin cộng đồng
```text
title 11: Xem bảng tin cộng đồng (Community Feed)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Vào trang Bảng tin Cộng đồng
activate Frontend
Frontend->Backend: GET /community-feed
activate Backend
Backend->Database: Truy vấn Top 50 bài đánh giá mới nhất + Bình luận
activate Database
Database->Backend: Dữ liệu Bảng tin
deactivate Database

Backend->Frontend: Trả về danh sách bài đăng
deactivate Backend
Frontend->Người dùng: Hiển thị các bài đăng và hình ảnh
deactivate Frontend
```

### 12. Thích bài đánh giá
```text
title 12: Thích / Bỏ thích bài đánh giá (Toggle Like)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhấn "Like" trên bài đăng
activate Frontend
Frontend->Backend: POST /reviews/{id}/like
activate Backend
Backend->Database: Kiểm tra User đã Like chưa
activate Database
Database->Backend: Kết quả
deactivate Database

Backend->Database: Thêm/Xóa User khỏi mảng liked_by
Backend->Frontend: Trả về số lượng Like mới
deactivate Backend

Frontend->Người dùng: Cập nhật số Like và màu nút
deactivate Frontend
```

### 13. Bình luận bài đăng
```text
title 13: Bình luận bài đăng (Post Comment)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhập Text và nhấn "Gửi" bình luận
activate Frontend
Frontend->Backend: POST /reviews/{id}/comments
activate Backend
Backend->Database: Lưu bình luận mới
activate Database
Database->Backend: Xác nhận lưu
deactivate Database

Backend->Frontend: Dữ liệu bình luận vừa đăng
deactivate Backend
Frontend->Người dùng: Hiển thị bình luận ngay dưới bài đăng
deactivate Frontend
```

### 14. Lập kế hoạch du lịch bằng AI
```text
title 14: Lập kế hoạch du lịch AI (AI Trip Planner)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhập số ngày, ngân sách, tháng, sở thích\nNhấn "Tạo kế hoạch"
activate Frontend
Frontend->Backend: POST /itinerary/generate
activate Backend
Backend->Database: Truy vấn địa điểm theo danh mục và trạng thái
activate Database
Database->Backend: Danh sách địa điểm tiềm năng
deactivate Database

Backend->Backend: Phân loại Sáng/Chiều/Tối\nTính Season Boost\nLọc và sắp xếp
Backend->Frontend: Lịch trình Day 1, Day 2...
deactivate Backend

Frontend->Người dùng: Hiển thị bảng lịch trình chi tiết
deactivate Frontend
```

### 15. Lưu lịch trình du lịch
```text
title 15: Lưu lịch trình (Save Itinerary)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhấn "Lưu kế hoạch" và đặt tên
activate Frontend
Frontend->Backend: POST /itinerary/save
activate Backend
Backend->Database: Tạo Itinerary mới
activate Database
Database->Backend: Itinerary ID
deactivate Database

Backend->Database: Lưu chi tiết từng địa điểm (Itinerary_Items)
Backend->Frontend: Phản hồi thành công
deactivate Backend

Frontend->Người dùng: Cập nhật trạng thái đã lưu
deactivate Frontend
```

### 16. Đổi địa điểm trong kế hoạch
```text
title 16: Đổi địa điểm (Swap Place)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Nhấn "Đổi địa điểm" tại 1 slot
activate Frontend
Frontend->Backend: POST /itinerary/swap {time_slot, used_ids}
activate Backend
Backend->Database: Truy vấn địa điểm thay thế phù hợp
activate Database
Database->Backend: Danh sách ứng viên
deactivate Database

Backend->Backend: Chọn địa điểm tốt nhất chưa dùng
Backend->Frontend: Trả về địa điểm thay thế
deactivate Backend

Frontend->Người dùng: Thay thế Card địa điểm trên màn hình
deactivate Frontend
```

### 17. Gửi địa điểm mới
```text
title 17: Gửi địa điểm mới (Submit Place)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Điền form thông tin địa điểm mới, tải ảnh
activate Frontend
Người dùng->Frontend: Nhấn "Gửi"
Frontend->Backend: POST /places/submit
activate Backend
Backend->Backend: Upload ảnh
Backend->Database: Lưu địa điểm (status='pending')
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Người dùng: Thông báo đang chờ phê duyệt
deactivate Frontend
```

### 18. Yêu cầu quyền đăng bài
```text
title 18: Yêu cầu quyền đăng bài (Request Post Permission)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Vào trang hồ sơ\nNhấn "Yêu cầu quyền đăng bài"
activate Frontend
Frontend->Backend: POST /users/request-permission
activate Backend
Backend->Database: Cập nhật post_permission_status='pending'
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Người dùng: Hiển thị trạng thái "Đang chờ duyệt"
deactivate Frontend
```

### 19. Xem địa điểm gợi ý bởi AI
```text
title 19: Xem gợi ý AI (AI Recommendations)

actor Người dùng
participant Frontend
participant FastAPI Backend
participant PyTorch (GNN)
participant Database

Người dùng->Frontend: Mở trang Gợi ý
activate Frontend
Frontend->FastAPI Backend: GET /recommendations/{user_id}
activate FastAPI Backend
FastAPI Backend->PyTorch (GNN): Gọi hàm gợi ý AI
activate PyTorch (GNN)

PyTorch (GNN)->Database: Tải logs tương tác và preferences
activate Database
Database->PyTorch (GNN): Dữ liệu đồ thị
deactivate Database

PyTorch (GNN)->PyTorch (GNN): Tính điểm Hybrid (60% GNN + 40% Content)\nLoại trừ địa điểm đã xem\nXếp hạng Top K
PyTorch (GNN)->FastAPI Backend: Trả về Top K kèm Lý do
deactivate PyTorch (GNN)

FastAPI Backend->Frontend: JSON gợi ý
deactivate FastAPI Backend
Frontend->Người dùng: Hiển thị thẻ địa điểm + % Phù hợp
deactivate Frontend
```

### 20. Gửi tin nhắn liên hệ
```text
title 20: Liên hệ (Contact Us)

actor Người dùng
participant Frontend
participant Backend
participant Database

Người dùng->Frontend: Điền form Liên hệ (Tên, Email, Tin nhắn)
activate Frontend
Người dùng->Frontend: Nhấn "Gửi tin nhắn"
Frontend->Backend: POST /contact
activate Backend
Backend->Database: Lưu tin nhắn vào bảng contact_messages
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Người dùng: Thông báo "Gửi thành công"
deactivate Frontend
```

---

## 2. Quản trị viên (Admin)

### 21. Xem bảng điều khiển thống kê
```text
title 21: Bảng điều khiển (Admin Dashboard)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Truy cập Dashboard
activate Frontend
Frontend->Backend: GET /admin/dashboard
activate Backend
Backend->Database: Truy vấn Count(User, Place, Review)\nTruy vấn Chart Data
activate Database
Database->Backend: Dữ liệu thống kê
deactivate Database

Backend->Frontend: Gửi dữ liệu Dashboard
deactivate Backend
Frontend->Admin: Hiển thị Biểu đồ và Số liệu
deactivate Frontend
```

### 22. Quản lý địa điểm
```text
title 22: Quản lý địa điểm (Manage Places)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Thêm/Sửa/Xóa địa điểm
activate Frontend
Frontend->Backend: POST/PUT/DELETE /admin/places
activate Backend
Backend->Database: Thực thi thao tác CSDL
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Kết quả thao tác
deactivate Backend
Frontend->Admin: Cập nhật bảng danh sách địa điểm
deactivate Frontend
```

### 23. Phê duyệt địa điểm
```text
title 23: Phê duyệt địa điểm chờ duyệt (Pending Places Approval)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Nhấn "Phê duyệt" hoặc "Từ chối" địa điểm
activate Frontend
Frontend->Backend: PUT /admin/places/{id}/status
activate Backend
Backend->Database: Cập nhật trạng thái (approved / rejected)
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Admin: Loại bỏ dòng khỏi danh sách chờ
deactivate Frontend
```

### 24. Quản lý danh mục
```text
title 24: Quản lý danh mục (Manage Categories)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Thêm danh mục (Tên, Parent Type)
activate Frontend
Frontend->Backend: POST /admin/categories
activate Backend
Backend->Database: Lưu danh mục mới
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Dữ liệu danh mục mới
deactivate Backend
Frontend->Admin: Cập nhật giao diện quản lý
deactivate Frontend
```

### 25. Quản lý người dùng
```text
title 25: Quản lý người dùng (Manage Users)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Nhấn "Khóa tài khoản"
activate Frontend
Frontend->Backend: DELETE /admin/users/{id}
activate Backend
Backend->Database: Cập nhật deleted_at (Soft Delete)
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Admin: Hiển thị trạng thái "Bị khóa"
deactivate Frontend
```

### 26. Phê duyệt quyền đăng bài
```text
title 26: Phê duyệt quyền đăng bài (Approve Post Permission)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Xem yêu cầu cấp quyền\nNhấn "Phê duyệt"
activate Frontend
Frontend->Backend: PUT /admin/users/{id}/permission
activate Backend
Backend->Database: Cập nhật post_permission_status='approved'
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Admin: Ẩn yêu cầu khỏi danh sách chờ
deactivate Frontend
```

### 27. Quản lý đánh giá
```text
title 27: Quản lý đánh giá (Manage Comments)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Nhấn "Xóa" một bình luận tiêu cực
activate Frontend
Frontend->Backend: DELETE /admin/reviews/{id}
activate Backend
Backend->Database: Xóa dòng đánh giá
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Database: Tính toán lại Rating của địa điểm đó
Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Admin: Xóa dòng khỏi bảng
deactivate Frontend
```

### 28. Quản lý tin nhắn liên hệ
```text
title 28: Quản lý tin nhắn liên hệ (Manage Contact Messages)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Nhấn mở một tin nhắn
activate Frontend
Frontend->Backend: PUT /admin/messages/{id}/read
activate Backend
Backend->Database: Đánh dấu is_read=true
activate Database
Database->Backend: Xác nhận
deactivate Database
Backend->Frontend: Cập nhật trạng thái
deactivate Backend

Admin->Frontend: Gõ phản hồi và gửi
Frontend->Backend: POST /admin/messages/{id}/reply
activate Backend
Backend->Backend: Gửi Email phản hồi tới User
Backend->Database: Đánh dấu is_replied=true
Backend->Frontend: Thành công
deactivate Backend
Frontend->Admin: Đổi nhãn thành "Đã trả lời"
deactivate Frontend
```

### 29. Cài đặt website
```text
title 29: Cài đặt website (Site Settings - Hero Banner)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Tải lên hình ảnh Hero Banner
activate Frontend
Frontend->Backend: POST /admin/settings/hero-images
activate Backend
Backend->Backend: Lưu file ảnh
Backend->Database: Cập nhật mảng JSON trong bảng site_settings
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: URL ảnh mới
deactivate Backend
Frontend->Admin: Cập nhật danh sách ảnh Hero
deactivate Frontend
```

### 30. Huấn luyện mô hình AI
```text
title 30: Huấn luyện mô hình AI (Train GNN Model)

actor Admin
participant Frontend
participant FastAPI Backend
participant PyTorch (GNN)
participant Database

Admin->Frontend: Nhấn "Train AI Model"
activate Frontend
Frontend->FastAPI Backend: POST /admin/gnn/train
activate FastAPI Backend
FastAPI Backend->PyTorch (GNN): Gọi hàm huấn luyện
activate PyTorch (GNN)

PyTorch (GNN)->Database: Tải toàn bộ Interaction Logs
activate Database
Database->PyTorch (GNN): Dữ liệu đồ thị
deactivate Database

PyTorch (GNN)->PyTorch (GNN): Build HeteroData Graph\nTrain 100 epochs (Negative Sampling)\nTính Loss (BCE)
PyTorch (GNN)->PyTorch (GNN): Lưu mô hình (gnn_model.pt)
PyTorch (GNN)->FastAPI Backend: Trả về Loss Value
deactivate PyTorch (GNN)

FastAPI Backend->Frontend: Thông báo huấn luyện xong
deactivate FastAPI Backend
Frontend->Admin: Hiển thị "Huấn luyện thành công, Loss: ..."
deactivate Frontend
```

### 31. Quản lý nội dung phong phú của địa điểm
```text
title 31: Quản lý nội dung (Manage Place Sections)

actor Admin
participant Frontend
participant Backend
participant Database

Admin->Frontend: Thêm Section (Hình ảnh + Đoạn văn) cho địa điểm
activate Frontend
Frontend->Backend: POST /admin/places/{id}/sections
activate Backend
Backend->Backend: Upload hình ảnh Section
Backend->Database: Lưu vào bảng place_sections (có order_index)
activate Database
Database->Backend: Xác nhận
deactivate Database

Backend->Frontend: Phản hồi thành công
deactivate Backend
Frontend->Admin: Hiển thị Section mới được thêm
deactivate Frontend
```
