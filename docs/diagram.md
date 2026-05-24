# 📊 Biểu đồ Hệ thống — Savannakhet Smart Travel

> Hệ thống du lịch thông minh với **2 Role: User (Khách du lịch)** và **Admin (Quản trị viên)**  
> Tech Stack: **Vue 3 + FastAPI + MySQL + GNN (PyTorch)**

---

## 1. Sơ đồ Use Case (Use Case Diagram)

> Mô tả các chức năng của 2 Actor: **User** và **Admin**

![Use Case Diagram](images/use_case_diagram.png)

---

## 2. Biểu đồ Hoạt động (Activity Diagram)

### 2.1 Quy trình Đăng nhập

> Luồng xử lý từ khi User nhập thông tin đến khi điều hướng theo Role

![Activity Diagram - Đăng nhập](images/activity_login.png)

---

## 3. Sơ đồ Tuần tự (Sequence Diagram)

### 3.1 Đăng nhập hệ thống

> Giao tiếp giữa: **Người dùng → Vue 3 → FastAPI → MySQL**

![Sequence Diagram - Đăng nhập](images/sequence_login.png)

---

### 3.2 Lập lịch trình du lịch (Trip Planner)

> Luồng tạo lịch trình tự động theo Sáng/Chiều/Tối, hỗ trợ Swap địa điểm

![Sequence Diagram - Trip Planner](images/sequence_trip_planner.png)

---

## 4. Sơ đồ ERD (Entity Relationship Diagram)

> Cấu trúc 9 bảng cơ sở dữ liệu và mối quan hệ giữa các bảng

![ERD Diagram](images/erd_diagram.png)

---

## 📋 Tóm tắt các bảng DB

| Bảng | Mô tả |
|------|-------|
| `users` | Tài khoản User & Admin, lưu role, preferences, soft-delete |
| `categories` | Danh mục địa điểm, có `parent_type` phục vụ AI |
| `places` | Địa điểm du lịch, ảnh, tọa độ, giờ mở cửa, ngân sách |
| `user_interactions` | Review + Community Post (rating, comment, ảnh, likes) |
| `post_comments` | Comment trên bài đăng Community |
| `favorites` | Danh sách yêu thích của User |
| `interaction_logs` | Log hành vi (view/like/review) phục vụ GNN AI |
| `itineraries` | Lịch trình du lịch được User lưu |
| `itinerary_items` | Chi tiết lịch trình (ngày, buổi, địa điểm) |

---

## 🗂️ Danh sách Routes (API & Frontend)

### API Backend (FastAPI)

| Method | Endpoint | Chức năng |
|--------|----------|-----------|
| POST | `/register` | Đăng ký |
| POST | `/login` | Đăng nhập → JWT |
| POST | `/forgot-password` | Gửi email reset |
| POST | `/reset-password` | Đặt lại mật khẩu |
| GET | `/places` | Danh sách địa điểm |
| GET | `/places/trending` | Địa điểm hot |
| GET | `/places/{id}` | Chi tiết địa điểm |
| POST | `/places/submit` | User submit địa điểm mới |
| POST | `/reviews` | Viết đánh giá |
| GET | `/community/feed` | Community Feed |
| POST | `/reviews/{id}/like` | Like/Unlike post |
| GET | `/api/recommendations/{user_id}` | Gợi ý AI GNN |
| POST | `/api/itinerary/generate` | Tạo lịch trình |
| POST | `/api/itinerary/swap` | Hoán đổi địa điểm |
| POST | `/api/itinerary/save` | Lưu lịch trình |
| GET | `/admin/stats` | Dashboard thống kê |
| PUT | `/admin/places/{id}/status` | Duyệt địa điểm |
| POST | `/admin/gnn/train` | Huấn luyện AI |

### Frontend Routes (Vue 3)

| Path | Tên trang | Truy cập |
|------|-----------|---------|
| `/` | Home | Public |
| `/login` | Đăng nhập | Public |
| `/register` | Đăng ký | Public |
| `/explore` | Khám phá địa điểm | User |
| `/places/:id` | Chi tiết địa điểm | User |
| `/trip-planner` | Lập lịch trình | User |
| `/community` | Community Feed | User |
| `/favorites` | Yêu thích | User |
| `/profile` | Hồ sơ cá nhân | User |
| `/submit-place` | Submit địa điểm | User |
| `/admin/dashboard` | Dashboard | Admin |
| `/admin/places` | Quản lý địa điểm | Admin |
| `/admin/pending-places` | Duyệt địa điểm | Admin |
| `/admin/manage-users` | Quản lý User | Admin |
| `/admin/comments` | Kiểm duyệt Review | Admin |
| `/admin/settings` | Cài đặt hệ thống | Admin |
