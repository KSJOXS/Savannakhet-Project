# CHƯƠNG 3: TRIỂN KHAI VÀ KẾT QUẢ ĐẠT ĐƯỢC

## 3.1. Môi trường của ứng dụng

Dựa trên mô hình dịch vụ, hệ thống **Savannakhet Smart Travel** được thiết kế theo kiến trúc Client-Server hiện đại, chia làm bốn lớp chính để đảm bảo khả năng mở rộng và bảo mật:

- **Frontend Service (Giao diện người dùng):** Sử dụng thư viện **Vue 3** kết hợp công cụ đóng gói **Vite** để xây dựng giao diện web động (Single Page Application). Lớp này chịu trách nhiệm hiển thị thông tin trực quan, xử lý tương tác trực tiếp với người dùng qua Internet và gửi các yêu cầu xác thực cũng như truy xuất dữ liệu tới Backend qua giao thức HTTP (Axios). Giao diện được thiết kế bằng Vanilla CSS theo phong cách Glassmorphism sang trọng với các chuyển động vi mô (micro-animations) sinh động.
- **Backend Service (Dịch vụ xử lý):** Trung tâm của hệ thống là **FastAPI**, một framework Python hiệu năng cao. FastAPI đóng vai trò điều phối, xử lý logic nghiệp vụ, xác thực phân quyền qua JWT Token và quản lý luồng dữ liệu giữa người dùng, cơ sở dữ liệu và phân hệ trí tuệ nhân tạo.
- **Data Store (Lưu trữ dữ liệu):** Hệ thống sử dụng hệ quản trị cơ sở dữ liệu **MySQL Server 8.0**, một cơ sở dữ liệu quan hệ mạnh mẽ, giúp lưu trữ thông tin về người dùng, danh mục địa điểm, chi tiết điểm đến, log hành vi tương tác và các lịch trình du lịch cá nhân.
- **Recommendation AI (Trí tuệ nhân tạo):** Một phân hệ AI học sâu trên đồ thị dị thể sử dụng thư viện **PyTorch Geometric (GraphSAGE)** được tích hợp trực tiếp với Backend để thực hiện huấn luyện dự đoán liên kết (Link Prediction) và đưa ra gợi ý địa điểm cá nhân hóa (Hybrid Recommendation) kèm cơ chế giải thích lý do (Explainable AI) cho từng người dùng.

---

## 3.2. Hướng dẫn cài đặt và kết quả demo

### 3.2.1. Hướng dẫn cài đặt

Toàn bộ mã nguồn của dự án được quản lý và lưu trữ tập trung trên nền tảng GitHub, giúp đảm bảo tính đồng bộ và thuận tiện trong việc phát triển nhóm. Để vận hành chương trình hoàn chỉnh dưới môi trường máy cục bộ (Local), chúng ta thực hiện theo các bước chi tiết sau:

#### a. Phía máy chủ (Backend Service - FastAPI)

Backend đóng vai trò là "bộ não" điều phối toàn bộ logic nghiệp vụ và tích hợp các module AI thông minh. Quy trình khởi chạy bao gồm:

**Tải mã nguồn:** Sử dụng lệnh `git clone [URL_Backend]` để tải toàn bộ mã nguồn từ GitHub về máy tính cá nhân, sau đó truy cập vào thư mục `backend` của dự án.

**Khởi tạo môi trường:** Trước khi chạy, cần tạo môi trường ảo Python bằng lệnh `python -m venv .venv` và kích hoạt bằng lệnh `.venv\Scripts\Activate.ps1` (trên Windows PowerShell). Tiếp theo, cài đặt các thư viện cần thiết bằng cách sử dụng trình quản lý gói `pip` để đảm bảo các gói như **FastAPI**, **PyTorch**, **PyTorch Geometric (torch-geometric)**, **SQLAlchemy**, **PyMySQL** và các thư viện hỗ trợ AI được tích hợp đầy đủ thông qua tệp `requirements.txt`.

**Cấu hình cơ sở dữ liệu:** Tạo tệp cấu hình `.env` tại thư mục gốc Backend để kết nối hệ quản trị cơ sở dữ liệu MySQL Server 8.0. Hệ thống SQLAlchemy ORM sẽ tự động khởi tạo và đồng bộ cấu trúc bảng khi máy chủ được khởi chạy lần đầu.

**Khởi chạy hệ thống:** Để kích hoạt Server, chúng ta sử dụng lệnh:

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Lệnh này khởi động máy chủ API ở chế độ phát triển (Development Mode) với tính năng tự động tải lại mã (hot-reload), lắng nghe trên cổng 8000.

#### b. Phía giao diện người dùng (Frontend – Web Application)

Frontend được xây dựng để cung cấp giao diện tương tác trực quan cho du khách, kết nối trực tiếp với Backend qua API.

**Tải mã nguồn:** Thực hiện lệnh `git clone [URL_Frontend]` để sao chép bộ mã chương trình giao diện về máy, sau đó truy cập vào thư mục `frontend` của dự án.

**Cài đặt thư viện:** Tại thư mục gốc của mã nguồn Frontend, chạy lệnh `npm install`. Trình quản lý gói NPM sẽ tự động phân tích tệp cấu hình `package.json` và tải về các gói thư viện liên quan như **Vue 3**, **Vue Router**, **Axios** và các plugin hỗ trợ đa ngôn ngữ (i18n).

**Cấu hình kết nối API:** Thiết lập URL kết nối máy chủ Backend trong tệp `.env` với biến `VITE_API_URL=http://localhost:8000` để Frontend có thể giao tiếp với Backend qua giao thức HTTP.

**Vận hành ứng dụng:** Cuối cùng, thực hiện lệnh `npm run dev`. Lệnh này khởi động môi trường phát triển (Development Mode) của công cụ đóng gói **Vite**, biên dịch mã nguồn và chạy ứng dụng web trên trình duyệt tại địa chỉ mặc định `http://localhost:5173`.

#### c. Huấn luyện mô hình AI (GNN Recommender)

Hệ thống tích hợp phân hệ trí tuệ nhân tạo sử dụng mô hình mạng nơ-ron đồ thị (Graph Neural Network) để đưa ra các gợi ý cá nhân hóa. Quy trình xây dựng và huấn luyện mô hình bao gồm các bước chính sau:

**Xây dựng mô hình học sâu:** Sử dụng kiến trúc mạng nơ-ron đồ thị dị thể (Heterogeneous GNN) dựa trên các lớp **SAGEConv (GraphSAGE)** từ thư viện PyTorch Geometric để thực hiện việc học biểu diễn (representation learning) các thực thể User và Place. Mô hình bao gồm hai lớp tích chập đồ thị (Graph Convolution) với kích thước ẩn (hidden channels) là 64 chiều. Lớp đầu ra sử dụng phép tính tích vô hướng (dot product) kết hợp hàm kích hoạt Sigmoid để dự đoán xác suất liên kết giữa người dùng và địa điểm.

**Tối ưu hóa:** Sử dụng thuật toán tối ưu hóa **Adam Optimizer** với tốc độ học (learning rate) là 0.01 để cập nhật trọng số của mạng đồ thị trong quá trình huấn luyện.

**Hàm mất mát:** Sử dụng **Binary Cross Entropy with Logits Loss (BCEWithLogitsLoss)** cho bài toán dự đoán liên kết (Link Prediction) thông qua phương pháp lấy mẫu tiêu cực (Negative Sampling). Phương pháp này tạo ra các cặp liên kết giả (negative edges) bên cạnh các liên kết thật (positive edges) để mô hình học cách phân biệt mối quan hệ thật sự giữa người dùng với địa điểm.

**Kích hoạt huấn luyện:** Quản trị viên có thể kích hoạt quá trình huấn luyện mô hình AI trực tiếp từ giao diện Admin Dashboard thông qua nút "Train GNN" trong phòng điều khiển AI (AI Control Room). Khi huấn luyện hoàn tất, trọng số mô hình được lưu vào tệp `gnn_model.pt` trên máy chủ và sẵn sàng phục vụ việc đề xuất địa điểm cho người dùng.

Dưới đây là cấu trúc mã nguồn xây dựng và huấn luyện mô hình AI:

```python
# 1. Định nghĩa cấu trúc mô hình GNN (BaseGNN)
class BaseGNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super().__init__()
        self.conv1 = SAGEConv((-1, -1), hidden_channels)
        self.conv2 = SAGEConv((-1, -1), hidden_channels)

    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

# Chuyển đổi mô hình sang đồ thị dị thể (Heterogeneous Graph)
model = to_hetero(BaseGNN(hidden_channels=64), metadata=data.metadata())

# 2. Compile/Thiết lập bộ tối ưu hóa (Optimizer)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# 3. Huấn luyện mô hình (Training Loop với Epochs=100)
for epoch in range(1, 101):
    optimizer.zero_grad()
    out_dict = model(data.x_dict, data.edge_index_dict)
    
    # Dự đoán liên kết tích cực (Positive Edges)
    pos_src, pos_dst = pos_edge_index[0], pos_edge_index[1]
    pos_out = (out_dict['user'][pos_src] * out_dict['place'][pos_dst]).sum(dim=-1)
    
    # Lấy mẫu tiêu cực (Negative Sampling)
    neg_edge_index = negative_sampling(
        edge_index=pos_edge_index,
        num_nodes=(data['user'].num_nodes, data['place'].num_nodes),
        num_neg_samples=pos_edge_index.size(1)
    )
    neg_src, neg_dst = neg_edge_index[0], neg_edge_index[1]
    neg_out = (out_dict['user'][neg_src] * out_dict['place'][neg_dst]).sum(dim=-1)
    
    # Tính toán loss (Binary Cross Entropy) và thực hiện lan truyền ngược
    loss = F.binary_cross_entropy_with_logits(
        torch.cat([pos_out, neg_out]),
        torch.cat([torch.ones(pos_out.size(0)), torch.zeros(neg_out.size(0))])
    )
    loss.backward()
    optimizer.step()
```
*Hình 3.5: Cấu trúc mô hình và quy trình huấn luyện GNN*

---


## 3.3. Kết quả demo

Phần này trình bày chi tiết kết quả thực hiện giao diện người dùng thực tế của hệ thống khuyến nghị du lịch **Savannakhet Smart Travel** sau khi hoàn thiện đóng gói. Các hình ảnh minh họa phản ánh kết quả thẩm mỹ về mặt thiết kế (UI) cùng khả năng tối ưu hóa trải nghiệm người dùng (UX) thông qua các tính năng cốt lõi:

### 3.3.1. Đăng ký và Đăng nhập
- **Đăng ký:** Cho phép khách du lịch tạo tài khoản, nhập các thông tin cá nhân và tích chọn danh mục sở thích du lịch (Preferences) gồm 10 loại hình. Dữ liệu sở thích này được chuyển đổi thành vector Multi-hot phục vụ cho thuật toán gợi ý AI.
- **Đăng nhập:** Là "cổng chào" bảo mật xác thực tài khoản qua mật khẩu mã hóa bcrypt và cấp JWT Token cho phiên làm việc của người dùng. Hệ thống hỗ trợ tính năng Reset mật khẩu qua mã OTP gửi tới Email.

### 3.3.2. Khám phá địa điểm du lịch và Gợi ý AI (For You)
- **Khám phá:** Giao diện hiển thị danh sách địa điểm trực quan với bộ lọc danh mục (Tham quan, Khách sạn, Nhà hàng, Quán cafe). Người dùng có thể xem chi tiết thông tin địa điểm bao gồm hình ảnh, bản đồ tọa độ GPS, ngân sách đề xuất hàng ngày và các liên kết đặt phòng nhanh.
- **Gợi ý AI "For You":** Tích hợp phân hệ đề xuất cá nhân hóa từ mô hình GNN (GraphSAGE). Mỗi địa điểm đề xuất hiển thị đi kèm thanh tiến trình phần trăm (%) độ tương thích tổng thể (kết hợp 60% GNN Collaborative và 40% Content-based) cùng nhãn lý do thuyết phục rõ ràng (XAI): *"Phù hợp sở thích cà phê của bạn"* hay *"Được yêu thích cao bởi nhóm người dùng có gu tương đồng"*.

### 3.3.3. Lập lịch trình du lịch tự động (Trip Planner)
- Trình lập lịch trình tự động phân bổ địa điểm hợp lý vào 3 buổi: **Sáng (09:00), Chiều (14:00), Tối (19:00)** tùy theo mùa du lịch và ngân sách người dùng chọn.
- Người dùng có thể hoán đổi nhanh (Swap) các địa điểm trong buổi học để tùy biến lộ trình theo ý muốn, sau đó thực hiện lưu lịch trình cá nhân vào tài khoản.

### 3.3.4. Community Feed và Đánh giá (Review)
- Khách du lịch có thể chia sẻ các bài viết, đăng ảnh chụp và viết bài đánh giá địa điểm từ 1 đến 5 sao. Hệ thống tự động tính toán lại điểm trung bình địa điểm.
- Cộng đồng người dùng có thể thực hiện tương tác xã hội thông qua các nút bấm thích (Like) và viết bình luận (Comments) trên bài đăng.

### 3.3.5. Giao diện quản trị viên (Admin Dashboard & AI Control Room)
- **Dashboard:** Thống kê tổng số lượng người dùng, địa điểm, bài đánh giá và các biểu đồ phân tích lượt tương tác trong hệ thống.
- **Quản lý & Phê duyệt:** Admin thực hiện kiểm duyệt, phê duyệt các địa điểm mới do cộng đồng đóng góp và quản lý trạng thái khóa tài khoản người dùng.
- **AI Control Room:** Nút bấm kích hoạt huấn luyện lại mô hình AI (Train GNN) trực tiếp từ giao diện Admin. Khi bấm, hệ thống sẽ tự động vẽ lại biểu đồ Loss, cập nhật độ chính xác (Accuracy) và ghi đè file trọng số mô hình `gnn_model.pt` thời gian thực trên server.

  Dưới đây là kết quả đồ họa của biểu đồ sau khi kết thúc quá trình huấn luyện:

  ![Hình 3.7 Biểu đồ dữ liệu sau khi train](backend/ai_demo/loss_chart.png)
  *Hình 3.7: Biểu đồ dữ liệu sau khi train (Model Accuracy & Model Loss)*
