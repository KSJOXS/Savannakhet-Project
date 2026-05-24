# CHƯƠNG 1: CƠ SỞ LÝ THUYẾT

## 1.1 Tổng quan về Hệ thống Gợi ý (Recommendation System)

Trong lĩnh vực xây dựng các ứng dụng thông minh, hệ thống gợi ý (Recommendation System) đóng vai trò then chốt trong việc cá nhân hóa trải nghiệm người dùng. Hệ thống gợi ý hoạt động dựa trên nguyên lý phân tích dữ liệu hành vi và sở thích của người dùng để đề xuất các mục (item) phù hợp nhất, từ đó giải quyết bài toán **quá tải thông tin (Information Overload)** — một vấn đề phổ biến khi người dùng phải đối mặt với hàng trăm lựa chọn địa điểm du lịch.

Trong phạm vi đề tài "Xây dựng website hỗ trợ khuyến nghị du lịch tỉnh Savannakhet", hệ thống gợi ý được xây dựng nhằm đề xuất các địa điểm du lịch (điểm tham quan, nhà hàng, khách sạn, di tích văn hóa) phù hợp với từng du khách dựa trên lịch sử tương tác và sở thích cá nhân. Dữ liệu tương tác được thu thập từ ba hành vi chính của người dùng trên nền tảng:

- **Xem (View):** Du khách xem thông tin chi tiết của một địa điểm — trọng số tương tác: 1.0.
- **Thích (Like):** Du khách bấm thích một địa điểm — trọng số tương tác: 2.0.
- **Đánh giá (Review):** Du khách viết bài đánh giá và cho điểm — trọng số tương tác: 3.0.

Toàn bộ dữ liệu hành vi này được lưu trữ trong bảng `interaction_logs` của cơ sở dữ liệu MySQL, bao gồm các trường: `user_id`, `place_id`, `action_type`, `interaction_weight` và `created_at`, phục vụ trực tiếp cho quá trình xây dựng đồ thị tương tác và huấn luyện mô hình AI.

Trong lĩnh vực hệ thống gợi ý, có hai phương pháp tiếp cận truyền thống phổ biến nhất là Lọc dựa trên nội dung (Content-Based Filtering) và Lọc cộng tác (Collaborative Filtering). Đề tài nghiên cứu và kết hợp cả hai phương pháp này, đồng thời ứng dụng thêm công nghệ Mạng nơ-ron đồ thị (Graph Neural Networks) để xây dựng một hệ thống gợi ý lai hiệu quả hơn.

---

## 1.2 Các Phương pháp Gợi ý

Trong lĩnh vực xây dựng hệ thống khuyến nghị, việc lựa chọn phương pháp tiếp cận đóng vai trò quyết định đến độ chính xác và trải nghiệm người dùng. Nhìn chung, các hệ thống hiện đại thường xoay quanh hai phương pháp kinh điển là Lọc dựa trên nội dung (Content-Based Filtering) và Lọc cộng tác (Collaborative Filtering), cùng với xu hướng kết hợp để tối ưu hóa hiệu suất.

**A. Phương pháp lọc dựa nội dung (Content-Based Filtering)**

Phương pháp này hoạt động dựa trên nguyên lý: "Gợi ý những thứ tương tự với những gì người dùng đã thích trong quá khứ". Hệ thống tập trung phân tích các đặc tính nội tại của địa điểm (Item Features) để xây dựng hồ sơ sở thích cá nhân.

- **Cơ chế hoạt động:** Hệ thống tiến hành trích xuất các thuộc tính (metadata) của địa điểm như tên, danh mục, mô tả và nhãn (tags). Đối với website du lịch Savannakhet, nếu người dùng thường xuyên tương tác với các địa điểm thuộc danh mục "cafe" và "nature", hệ thống sẽ xác định các đặc trưng quan trọng: *Danh mục: cafe, Loại hình: thiên nhiên*.

- **Kỹ thuật thực hiện:**
  - **Biểu diễn dữ liệu:** Sử dụng mô hình không gian vector để biểu diễn địa điểm. Mỗi địa điểm trong bảng `places` được biểu diễn bằng vector 11 chiều gồm mã hóa một nóng (One-Hot Encoding) của 10 danh mục theo trường `parent_type` trong bảng `categories`, và điểm đánh giá trung bình được chuẩn hóa về khoảng [0, 1].
  - **Đo lường độ tương đồng:** Sử dụng **Độ tương đồng Cosine (Cosine Similarity)** để tìm ra các địa điểm có khoảng cách gần nhất với hồ sơ sở thích của người dùng trong không gian vector. Sở thích người dùng được lưu trong trường `preferences` (kiểu JSON) của bảng `users` và được mã hóa thành vector nhiều nóng (Multi-Hot Encoding) 10 chiều.

- **Ưu điểm:** * Giải quyết tốt vấn đề "Cold Start" cho địa điểm mới: Ngay khi một địa điểm được đăng lên với đầy đủ thông tin danh mục, hệ thống có thể gợi ý ngay cho những du khách có sở thích phù hợp mà không cần dữ liệu tương tác từ người dùng khác.
  - Tính minh bạch cao, dễ dàng giải thích cho người dùng lý do tại sao họ nhận được đề xuất đó.

- **Nhược điểm:** * Khả năng mở rộng sở thích bị hạn chế (User bị đóng khung trong những gì họ đã biết), hệ thống khó gợi ý được những địa điểm nằm ngoài danh mục quen thuộc của người dùng.

**B. Phương pháp lọc cộng tác (Collaborative Filtering)**

Khác với cách tiếp cận dựa trên thuộc tính, lọc cộng tác khai thác hành vi tập thể của cộng đồng người dùng. Phương pháp này giả định rằng nếu nhóm người dùng A và B có sự tương đồng về hành vi tương tác trong quá khứ, họ có xu hướng sẽ lựa chọn những địa điểm giống nhau trong tương lai.

Phương pháp này được chia thành hai nhánh chính:

- **User-User Collaborative Filtering:** Tìm kiếm các "láng giềng" (neighbors) có lịch sử tương tác giống với người dùng hiện tại. Nếu người dùng A và B cùng thích địa điểm X, Y; khi người dùng B tương tác thêm với địa điểm Z, hệ thống sẽ gợi ý Z cho người dùng A.

- **Item-Item Collaborative Filtering:** Tập trung vào mối quan hệ giữa các địa điểm dựa trên lượt tương tác chung. Nếu phần lớn người dùng tương tác với "Đền Wat Sainyaphum" cũng thường xuyên tương tác với "Bảo tàng Savannakhet" từ cùng một nhóm, hệ thống sẽ ghi nhận mối liên kết giữa hai địa điểm này để thực hiện gợi ý chéo.

- **Ưu điểm:** * Có khả năng tạo ra những gợi ý bất ngờ và thú vị (Serendipity), giúp du khách khám phá ra những nhu cầu mới mà chính họ cũng chưa nhận ra.
  - Không yêu cầu hiểu biết sâu về nội dung/thuộc tính của địa điểm, chỉ cần dữ liệu về hành vi (Click, Like, Review).

- **Nhược điểm:** * **Vấn đề Cold Start:** Không thể gợi ý cho người dùng mới hoàn toàn (chưa có dữ liệu hành vi) hoặc địa điểm mới đăng (chưa có ai tương tác).
  - **Vấn đề độ thưa thớt (Sparsity):** Khi số lượng địa điểm lớn nhưng mỗi người dùng chỉ tương tác với một số ít, ma trận tương tác trở nên rất thưa, ảnh hưởng đến chất lượng gợi ý.
  - **Thiên kiến phổ biến (Popularity Bias):** Các địa điểm nổi tiếng có nhiều lượt tương tác được gợi ý nhiều hơn, trong khi các địa điểm ít người biết nhưng phù hợp với sở thích cá nhân lại bị bỏ qua.

---

## 1.3 Lý thuyết Đồ thị và Mạng Nơ-ron Đồ thị (Graph Neural Networks)

### 1.3.1 Khái quát về Lý thuyết Đồ thị

Đồ thị (Graph) là một cấu trúc dữ liệu gồm tập hợp các **nút (nodes/vertices)** và các **cạnh (edges)** nối các nút với nhau. Cấu trúc này đặc biệt phù hợp để biểu diễn các mối quan hệ phức tạp trong thực tế, chẳng hạn như mạng xã hội (người dùng và bạn bè), mạng lưới giao thông (điểm đến và tuyến đường), hay trong bài toán gợi ý — mạng lưới tương tác giữa du khách và địa điểm du lịch.

**Đồ thị dị thể (Heterogeneous Graph)** là dạng đồ thị chứa nhiều kiểu nút và nhiều kiểu cạnh khác nhau. Đây là cấu trúc phù hợp nhất để biểu diễn dữ liệu du lịch, vì trong hệ thống có hai loại thực thể hoàn toàn khác nhau: người dùng (`user`) và địa điểm (`place`).

Trong hệ thống Savannakhet Smart Travel, mạng lưới tương tác du lịch được xây dựng thành một **đồ thị dị thể lưỡng phân** với cấu trúc:

- **Tập nút người dùng:** Mỗi tài khoản du khách trong bảng `users` là một nút, được biểu diễn bằng vector đặc trưng 10 chiều từ trường `preferences`.
- **Tập nút địa điểm:** Mỗi địa điểm trong bảng `places` là một nút, được biểu diễn bằng vector đặc trưng 11 chiều (10 danh mục + điểm đánh giá chuẩn hóa).
- **Cạnh xuôi `(user, interacts_with, place)`:** Biểu diễn hành vi tương tác thực tế từ bảng `interaction_logs`. Các cạnh trùng lặp (cùng user tương tác với cùng place nhiều lần) được gộp lại bằng cách cộng tổng trọng số, sau đó chuẩn hóa theo giá trị lớn nhất để giảm thiên kiến phổ biến.
- **Cạnh đảo ngược `(place, rev_interacts_with, user)`:** Được tự động tạo ra để đảm bảo thông tin lan truyền hai chiều trong quá trình học đồ thị, giúp các nút địa điểm cũng có thể tổng hợp đặc trưng từ người dùng đã tương tác với mình.

Toàn bộ cấu trúc đồ thị này được xây dựng trong hàm `build_gnn_graph()` thuộc file `gnn_service.py`, sử dụng đối tượng `HeteroData` của thư viện PyTorch Geometric. Hình ảnh trực quan của đồ thị tương tác được xuất ra tại file `graph_structure.png` trong thư mục `ai_demo`.

### 1.3.2 Mạng Nơ-ron Đồ thị (Graph Neural Networks - GNN)

Mạng nơ-ron đồ thị (GNN) là một họ mô hình học sâu được thiết kế đặc biệt để xử lý dữ liệu có cấu trúc đồ thị. Điểm đặc biệt của GNN so với các mạng nơ-ron truyền thống là khả năng khai thác thông tin từ **cấu trúc liên kết** của dữ liệu, không chỉ từ các thuộc tính riêng lẻ của từng nút.

Cơ chế cốt lõi của GNN là **Truyền thông điệp (Message Passing)**: Tại mỗi tầng huấn luyện, mỗi nút sẽ thu thập thông tin từ các nút lân cận (neighbors) và tổng hợp lại để cập nhật biểu diễn của chính mình. Sau nhiều tầng, vector nhúng (embedding) của mỗi nút sẽ mã hóa thông tin không chỉ của chính nút đó mà còn của toàn bộ vùng lân cận xung quanh. Điều này giúp GNN nắm bắt được các mối quan hệ tương tác **phi tuyến và bậc cao** mà các phương pháp truyền thống như Matrix Factorization không thể biểu diễn được.

**Lý do lựa chọn GNN cho hệ thống gợi ý du lịch:**

- Phương pháp Lọc cộng tác truyền thống chỉ xem xét mối quan hệ trực tiếp giữa người dùng và địa điểm (bậc 1). GNN cho phép khai thác thông tin ở nhiều bậc cao hơn: hai du khách không cùng tương tác với bất kỳ địa điểm nào nhưng đều tương tác với các địa điểm của những người dùng có cùng gu thẩm mỹ — mối liên kết gián tiếp này rất có giá trị.
- GNN hoạt động tự nhiên trên cấu trúc đồ thị dị thể, phù hợp với bài toán biểu diễn quan hệ User-Place.

---

## 1.4 Thuật toán GraphSAGE (Sample and Aggregate)

### 1.4.1 Giới thiệu và Nguyên lý

**GraphSAGE (Graph Sample and Aggregate)** là thuật toán GNN học quy nạp (Inductive Learning) được Hamilton và cộng sự đề xuất năm 2017. Đây là thuật toán được lựa chọn để xây dựng hệ thống gợi ý trong đề tài này, được triển khai thông qua lớp `SAGEConv` của thư viện PyTorch Geometric.

Điểm khác biệt quan trọng nhất của GraphSAGE so với các GNN trước đó là khả năng **học quy nạp (Inductive Learning)**: thay vì học một vector nhúng cố định cho từng nút trong đồ thị (Transductive), GraphSAGE học một **hàm tổng hợp đặc trưng** có khả năng tổng quát hóa. Khi một du khách mới đăng ký tài khoản hoặc một địa điểm mới được thêm vào hệ thống, mô hình có thể **ngay lập tức tạo ra vector nhúng** cho nút mới dựa trên đặc trưng ban đầu và cấu trúc lân cận, mà không cần huấn luyện lại từ đầu. Đây là yếu tố quyết định giúp GraphSAGE giải quyết bài toán Cold Start mà các phương pháp truyền thống thất bại.

### 1.4.2 Kiến trúc Mô hình trong Hệ thống

Trong file `recommendation.py`, kiến trúc mô hình được định nghĩa qua hai lớp:

**Lớp `BaseGNN`:** Xây dựng mạng nơ-ron đồ thị cơ sở với hai tầng `SAGEConv`. Tầng đầu tiên (`conv1`) áp dụng phép tích chập đồ thị và kích hoạt bằng hàm ReLU. Tầng thứ hai (`conv2`) tạo ra vector nhúng cuối cùng. Cả hai tầng đều sử dụng kích thước đầu vào động `(-1, -1)` để tự động điều chỉnh theo số chiều đặc trưng của từng loại nút.

**Lớp `SavannakhetRecommender`:** Bọc `BaseGNN` bên trong hàm `to_hetero()` của PyG, chuyển đổi mạng nơ-ron đơn kiểu thành mạng dị thể. Hàm `to_hetero()` tự động nhân bản các lớp `SAGEConv` cho từng kiểu cạnh trong đồ thị (`interacts_with` và `rev_interacts_with`), đảm bảo mỗi kiểu quan hệ được xử lý bằng bộ trọng số học riêng biệt.

**Quá trình lan truyền thuận (Forward Pass):**

1. Mô hình nhận đầu vào là `x_dict` (từ điển vector đặc trưng cho từng kiểu nút) và `edge_index_dict` (từ điển chỉ số cạnh cho từng kiểu cạnh).
2. Với mỗi kiểu cạnh, `SAGEConv` thực hiện: lấy mẫu láng giềng → tổng hợp đặc trưng bằng phép tính trung bình (Mean Aggregation) → ghép nối với đặc trưng của nút nguồn → biến đổi tuyến tính → kích hoạt ReLU.
3. Kết quả trả về là `out_dict` — từ điển chứa vector nhúng đã học được cho tất cả nút `user` và `place`.

### 1.4.3 Quy trình Huấn luyện Mô hình

Hệ thống sử dụng nhiệm vụ **Dự đoán Liên kết (Link Prediction)** làm mục tiêu huấn luyện. Quá trình này được thực hiện trong hàm `train_gnn_link_prediction()` và script `demo_gnn.py` với các bước sau:

**Bước 1 — Tạo cạnh dương (Positive Edges):** Trích xuất tất cả các cạnh tương tác thực tế từ bảng `interaction_logs`. Mỗi cặp `(user_id, place_id)` trong đồ thị là một ví dụ huấn luyện dương — thể hiện tương tác thực sự tồn tại.

**Bước 2 — Lấy mẫu âm (Negative Sampling):** Với mỗi cạnh dương `(user, place+)`, hàm `negative_sampling()` của PyG tự động sinh ngẫu nhiên một cạnh âm `(user, place-)` — trong đó `place-` là địa điểm mà người dùng chưa từng tương tác. Số lượng cạnh âm bằng đúng số cạnh dương (tỉ lệ 1:1) để cân bằng tập huấn luyện.

**Bước 3 — Tính điểm dự đoán (Scoring):** Điểm số cho mỗi cặp (user, place) được tính bằng **tích vô hướng (Dot Product)** giữa vector nhúng của user và place: `pos_out = (out_dict['user'][pos_src] * out_dict['place'][pos_dst]).sum(dim=-1)`. Giá trị này phản ánh mức độ căn chỉnh giữa hai vector trong không gian nhúng.

**Bước 4 — Tính hàm lỗi BCE:** Hàm lỗi **Binary Cross Entropy With Logits** (`F.binary_cross_entropy_with_logits`) được sử dụng để tối ưu hóa mô hình. Hàm này kết hợp hàm sigmoid và BCE trong một bước tính toán ổn định về số học. Nhãn của cạnh dương là `1.0` (tương tác thực), nhãn của cạnh âm là `0.0`.

**Bước 5 — Cập nhật trọng số:** Thuật toán tối ưu hóa **Adam** với tốc độ học `lr=0.01` cập nhật toàn bộ tham số của mô hình qua phép lan truyền ngược. Mô hình được huấn luyện qua **100 chu kỳ (Epochs)**.

Kết quả huấn luyện thực nghiệm cho thấy giá trị Loss giảm từ khoảng `0.693` tại Epoch 1 xuống khoảng `0.100–0.200` tại Epoch 100, với độ chính xác dự đoán liên kết đạt **85% đến 93.5%**. Đường cong học tập được lưu tại file `loss_chart.png` trong thư mục `ai_demo`.

---

## 1.5 Hệ thống Gợi ý Lai (Hybrid Recommendation System)

### 1.5.1 Lý do Kết hợp

Mỗi phương pháp đơn lẻ đều có hạn chế riêng: Content-Based bị đóng khung trong vùng sở thích đã biết của người dùng, trong khi GNN cần đủ dữ liệu tương tác để hoạt động hiệu quả. Để khắc phục các hạn chế này, hệ thống áp dụng chiến lược **Gợi ý Lai (Hybrid Recommendation)** — kết hợp tuyến tính có trọng số của cả hai phương pháp.

### 1.5.2 Công thức Điểm số Lai

Tại bước tính điểm số cuối cùng trong hàm `get_recommendations_for_user()`, hệ thống thực hiện:

1. **Tính điểm GNN Collaborative Score (`gnn_scores`):** Độ tương đồng Cosine giữa vector nhúng GNN của người dùng (`user_emb`) và tất cả vector nhúng địa điểm (`place_embs`) sau khi đã qua huấn luyện: `gnn_scores = F.cosine_similarity(place_embs, user_emb.unsqueeze(0))`.

2. **Tính điểm Content-Based Score (`content_scores`):** Độ tương đồng Cosine giữa vector sở thích thô của người dùng (`user_pref_vec`) được xây dựng từ trường `preferences` và vector danh mục của từng địa điểm (10 chiều đầu của `data['place'].x`): `content_scores = F.cosine_similarity(place_cat_vecs, user_pref_vec.unsqueeze(0))`.

3. **Kết hợp Hybrid Score:** Điểm số cuối cùng được tính theo công thức với trọng số `alpha = 0.6`:

   > `final_scores = 0.6 * gnn_scores + 0.4 * content_scores`

   Trọng số 60% được phân bổ cho GNN vì phương pháp này khai thác được hành vi tập thể và mối quan hệ bậc cao trong mạng lưới tương tác, mang lại gợi ý đa dạng hơn. Trọng số 40% cho Content-Based đảm bảo gợi ý luôn có tính liên quan đến sở thích trực tiếp của người dùng, đặc biệt hữu ích với người dùng mới.

4. **Cơ chế Lọc Loại trừ (Exclusion Filter):** Trước khi xếp hạng, hệ thống loại trừ tất cả địa điểm mà người dùng đã từng **viết đánh giá (action_type = 'review')** bằng cách đặt điểm số về `-infinity`. Điều này đảm bảo tính mới mẻ (Novelty) — du khách luôn được gợi ý những địa điểm chưa từng trải nghiệm.

5. **Chuyển đổi sang phần trăm:** Điểm Cosine trong khoảng [-1, 1] được chuyển đổi sang phần trăm thân thiện [0%, 100%] theo công thức: `overall_pct = (overall_score + 1) / 2 * 100`.

---

## 1.6 Trí tuệ Nhân tạo Giải thích được (Explainable AI - XAI)

Một trong những yêu cầu quan trọng của hệ thống gợi ý hiện đại là tính minh bạch — người dùng không chỉ cần biết **được gợi ý gì** mà còn cần hiểu **tại sao** hệ thống đề xuất điều đó. Đây chính là lĩnh vực của **Trí tuệ nhân tạo giải thích được (Explainable AI - XAI)**.

Trong hệ thống, chức năng giải thích được triển khai qua hai cơ chế:

**Cơ chế 1 — Phân tích thành phần điểm số:** Trong `demo_gnn.py`, sau khi tính được `overall_score`, `gnn_score` và `content_score` cho từng địa điểm gợi ý, hệ thống phân tích từng thành phần để tạo lý do tự động:

- Nếu danh mục của địa điểm (`cat_name`) nằm trong danh sách sở thích của người dùng (`prefs`), hệ thống hiển thị: *"Là địa điểm trùng với danh mục mà bạn yêu thích ('cafe')"*.
- Nếu `gnn_pct > 70%`, hệ thống hiển thị: *"Có xu hướng cao được yêu thích từ nhóm người dùng có gu tương đồng trong mạng lưới"*.

**Cơ chế 2 — Hàm `get_explainability()`:** Hàm này truy vấn trực tiếp cơ sở dữ liệu để tìm địa điểm có `interaction_weight >= 3.0` (tức là các địa điểm người dùng đã đánh giá cao nhất) và sử dụng thông tin đó để tạo câu giải thích có ngữ cảnh, gắn kết với lịch sử cá nhân của người dùng.

Cả hai cơ chế đều nhằm xây dựng sự tin tưởng giữa người dùng và hệ thống AI, giúp du khách cảm thấy gợi ý có căn cứ rõ ràng và phù hợp với bản thân.

---

## 1.7 Công nghệ Sử dụng

### 1.7.1 Ngôn ngữ lập trình và Thư viện AI

Hệ thống backend và toàn bộ engine AI được xây dựng trên ngôn ngữ **Python**. Framework **FastAPI** được lựa chọn để xây dựng REST API nhờ hiệu năng cao (dựa trên ASGI/asyncio), hỗ trợ xác thực dữ liệu tự động qua Pydantic và tài liệu API tự động sinh. Hệ thống học sâu sử dụng **PyTorch** làm nền tảng tensor và tính đạo hàm tự động, kết hợp với **PyTorch Geometric (PyG)** — thư viện chuyên dụng cung cấp các lớp `SAGEConv`, `HeteroConv`, `to_hetero()` và cấu trúc dữ liệu `HeteroData` phục vụ học trên đồ thị dị thể.

### 1.7.2 Giao diện Người dùng và Thiết kế

Giao diện người dùng được xây dựng bằng framework **Vue.js 3** kết hợp công cụ đóng gói **Vite**, triển khai theo kiến trúc Single Page Application (SPA). Hệ thống đa ngôn ngữ (tiếng Lào, Anh, Việt, Thái) được xây dựng bằng thư viện `vue-i18n`. Toàn bộ giao diện được thiết kế bằng **Vanilla CSS** theo phong cách Glassmorphism với các hiệu ứng chuyển động vi mô (micro-animations) mượt mà, không phụ thuộc vào thư viện CSS bên ngoài nhằm tối ưu hiệu suất tải trang và cho phép tùy biến sâu.

### 1.7.3 Cơ sở Dữ liệu và Tầng ORM

Cơ sở dữ liệu quan hệ **MySQL** được sử dụng để lưu trữ toàn bộ dữ liệu hệ thống. Giao tiếp giữa code Python và cơ sở dữ liệu được thực hiện thông qua **SQLAlchemy ORM**, cho phép ánh xạ các lớp Python (`User`, `Place`, `InteractionLog`, `Itinerary`, v.v. trong `models.py`) trực tiếp thành các bảng dữ liệu, đảm bảo tính an toàn kiểu dữ liệu và khả năng bảo trì cao.

---

## 1.8 Kết luận Chương 1

Chương 1 đã trình bày toàn diện cơ sở lý thuyết làm nền tảng cho hệ thống gợi ý du lịch thông minh tại tỉnh Savannakhet. Từ việc phân tích hạn chế của các phương pháp truyền thống (Content-Based Filtering và Collaborative Filtering), đề tài xác định được sự cần thiết của việc ứng dụng Mạng nơ-ron đồ thị (GNN) với thuật toán GraphSAGE nhằm khai thác cấu trúc liên kết phi tuyến trong mạng lưới tương tác User-Place, giải quyết bài toán Cold Start và Popularity Bias. Chiến lược Gợi ý Lai (Hybrid) kết hợp 60% tín hiệu GNN và 40% tín hiệu Content-Based, kết hợp với cơ chế Explainable AI, tạo thành một hệ thống gợi ý vừa chính xác, vừa đa dạng và minh bạch. Các kiến thức lý thuyết này được ánh xạ trực tiếp vào mã nguồn thực tế của hệ thống (`gnn_service.py`, `recommendation.py`) và sẽ là cơ sở cho việc phân tích, thiết kế chi tiết trong các chương tiếp theo.

---

> **Tài liệu tham khảo:**
> 1. Hamilton, W. L., Ying, R., & Leskovec, J. (2017). *Inductive Representation Learning on Large Graphs*. NeurIPS 2017.
> 2. Kipf, T. N., & Welling, M. (2017). *Semi-Supervised Classification with Graph Convolutional Networks*. ICLR 2017.
> 3. Fey, M., & Lenssen, J. E. (2019). *Fast Graph Representation Learning with PyTorch Geometric*. ICLR-W 2019.
> 4. Koren, Y., Bell, R., & Volinsky, C. (2009). *Matrix Factorization Techniques for Recommender Systems*. IEEE Computer.
> 5. He, X., et al. (2020). *LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation*. SIGIR 2020.
> 6. Zhang, S., et al. (2019). *Deep Learning Based Recommender System: A Survey and New Perspectives*. ACM Computing Surveys.
