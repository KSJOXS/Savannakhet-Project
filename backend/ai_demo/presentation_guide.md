# Presentation Guide: GNN Recommendation System (English & Thai)

This guide provides formal answers to the key questions regarding the Machine Learning component of the Savannakhet Project.

---

### 1. Dataset: Standard vs. Collected?
- **English:** We use a **User-Collected Dataset** (NSD Dataset). Data is pulled directly from our database (14 users, 31 places, 600+ interactions). See `graph_structure.png` for proof.
- **Thai:** โค้ดดึงข้อมูลมาจาก Database (Users & Places) และสร้างเส้นเชื่อม (Edges) จากประวัติการเข้าชมจริง (Interaction Log)

### 2. Model: GNN Application
- **English:** We implemented a **Heterogeneous GNN** using **GraphSAGE** (SAGEConv) layers. It performs "Message Passing" between different node types.
- **Thai:** ใช้โมเดล **HeteroGNN** ร่วมกับเลเยอร์ **SAGEConv** ในการเรียนรู้ข้อมูลจากโหนดเพื่อนบ้าน (Message Passing) เพื่อสร้างตัวแทนข้อมูล (Embeddings)

### 3. Training Evaluation
- **English:** Evaluated using **Link Prediction Loss** with **Negative Sampling**. Refer to `loss_chart.png` for the performance curve.
- **Thai:** ใช้เทคนิค **Link Prediction** และ **Negative Sampling** มาเทรน โดยคำนวณความแม่นยำด้วย Loss Function (BCE) เพื่ออัปเดตให้น้ำหนักโมเดลฉลาดขึ้น

### 4. Personalized Recommendations
- **English:** Generated through **Embedding Similarity** (Dot Product). The closest places in the embedding space are recommended to the user.
- **Thai:** นำค่า Embedding ของ User ไปคำนวณหาความคล้ายคลึง (**Similarity**) กับสถานที่ทั้งหมด แล้วเรียงลำดับคะแนนเพื่อดึง Top-K มาแสดงผล

### 5. Why use two tables: `interaction_logs` vs `user_interactions`?
- **English:** 
    - `interaction_logs` captures **Implicit Feedback** (Views, Clicks). It shows potential interest.
    - `user_interactions` captures **Explicit Feedback** (Ratings, Likes). It shows confirmed preference.
    - **Logic:** The GNN uses both to build a "Rich Graph". Implicit data gives us volume, while Explicit data gives us accuracy (weights).
- **Thai:**
    - `interaction_logs` เก็บข้อมูล **Implicit Feedback** (การเข้าชม/การคลิก) เพื่อให้รู้ว่าผู้ใช้ "สนใจ" อะไรในเบื้องต้น
    - `user_interactions` เก็บข้อมูล **Explicit Feedback** (การให้คะแนน/การกดหัวใจ) เพื่อยืนยันว่าผู้ใช้ "ชอบ" อะไรจริงๆ
    - **เหตุผล:** ระบบ GNN ใช้ทั้งสองอย่างเพื่อสร้างความสัมพันธ์ที่แม่นยำ ข้อมูลการเข้าชมช่วยให้รู้ความชอบกว้างๆ ข้อมูลการกดไลก์ช่วยให้คำแนะนำเจาะจงมากยิ่งขึ้น

---
*Prepared by Antigravity AI Assistant for Savannakhet Project Presentation.*
