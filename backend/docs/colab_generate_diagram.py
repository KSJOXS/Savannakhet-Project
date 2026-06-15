# =============================================================
# COPY โค้ดทั้งหมดนี้ไปวางใน Google Colab Cell แล้วรันได้เลย!
# Biểu đồ kiến trúc mô hình: HeteroGraphSAGE Hybrid Recommendation
# =============================================================

# ── 1. ติดตั้ง library (Colab มี matplotlib อยู่แล้ว ไม่ต้อง install)
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

print("matplotlib version:", matplotlib.__version__)

# ── 2. กำหนด path สำหรับบันทึกไฟล์
OUTPUT_PATH = "/content/model_architecture.png"   # <-- บันทึกใน Colab

# ── 3. สีทั้งหมด
C_BG        = "#FAFBFF"
C_INPUT_BD  = "#4A90D9"
C_INPUT_BG  = "#EEF4FF"
C_USER_BG   = "#DBEAFE"
C_USER_BD   = "#2563EB"
C_PLACE_BG  = "#D1FAE5"
C_PLACE_BD  = "#059669"
C_GRAPH_BG  = "#EDE9FE"
C_GRAPH_BD  = "#7C3AED"
C_GNN_BG    = "#F3E8FF"
C_GNN_BD    = "#9333EA"
C_LAYER_BG  = "#FAF5FF"
C_EMB_BG    = "#EDE9FE"
C_SGNN_BG   = "#DBEAFE"
C_SGNN_BD   = "#1D4ED8"
C_SCB_BG    = "#D1FAE5"
C_SCB_BD    = "#047857"
C_FUSE_BG   = "#FEF3C7"
C_FUSE_BD   = "#D97706"
C_OUT_BG    = "#FEE2E2"
C_OUT_BD    = "#DC2626"
C_XAI1_BG  = "#E0F2FE"
C_XAI2_BG  = "#ECFDF5"
C_ARROW     = "#475569"
C_TEXT_DARK = "#1E293B"
C_TEXT_MID  = "#334155"
C_TEXT_LIGHT= "#64748B"

# ── 4. Helper functions
fig, ax = plt.subplots(figsize=(14, 20))
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)
ax.set_xlim(0, 14)
ax.set_ylim(0, 20)
ax.axis("off")

def draw_box(ax, x, y, w, h, fc, ec, radius=0.25, lw=1.8):
    box = FancyBboxPatch((x, y), w, h,
                         boxstyle=f"round,pad=0,rounding_size={radius}",
                         facecolor=fc, edgecolor=ec,
                         linewidth=lw, zorder=3)
    ax.add_patch(box)

def txt(ax, x, y, s, fs=9, fw="normal", color=C_TEXT_DARK,
        ha="center", va="center", style="normal"):
    ax.text(x, y, s, fontsize=fs, fontweight=fw, color=color,
            ha=ha, va=va, fontstyle=style, zorder=5)

def arrow(ax, x1, y1, x2, y2, color=C_ARROW, lw=1.6):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw,
                                connectionstyle="arc3,rad=0"))

# ── 5. TITLE
txt(ax, 7, 19.55,
    "Kien Truc Mo Hinh Goi Y Lai (Hybrid Recommendation System)",
    fs=13, fw="bold", color="#1E1B4B")
txt(ax, 7, 19.12,
    "HeteroGraphSAGE + Content-Based Filtering",
    fs=9.5, color="#6D28D9", style="italic")
ax.plot([1, 13], [18.88, 18.88], color="#C4B5FD", lw=1.5, zorder=4)

# ── 6. SECTION 1 — INPUT DATA
draw_box(ax, 0.8, 15.6, 12.4, 3.1, C_INPUT_BG, C_INPUT_BD, radius=0.3, lw=2)
txt(ax, 7, 18.55, "(1) DU LIEU DAU VAO  (Input Data)", fs=10, fw="bold", color=C_USER_BD)

# User box
draw_box(ax, 1.1, 15.9, 3.6, 2.45, C_USER_BG, C_USER_BD, lw=1.8)
txt(ax, 2.9, 18.05, "Nguoi Dung (User)", fs=9.5, fw="bold", color=C_USER_BD)
txt(ax, 2.9, 17.65, r"$x_u \in \mathbb{R}^{10}$", fs=9, color=C_TEXT_DARK)
txt(ax, 2.9, 17.30, "Multi-hot Encoding", fs=8, color=C_TEXT_LIGHT, style="italic")
txt(ax, 2.9, 16.95, "10 danh muc so thich", fs=8, color=C_TEXT_LIGHT)
txt(ax, 2.9, 16.58,
    "[■ ■ ■ □ □ □ □ □ □ □]",
    fs=8.5, color=C_USER_BD)

# Place box
draw_box(ax, 5.3, 15.9, 3.6, 2.45, C_PLACE_BG, C_PLACE_BD, lw=1.8)
txt(ax, 7.1, 18.05, "Dia Diem (Place)", fs=9.5, fw="bold", color=C_PLACE_BD)
txt(ax, 7.1, 17.65, r"$x_p \in \mathbb{R}^{11}$", fs=9, color=C_TEXT_DARK)
txt(ax, 7.1, 17.30, "One-hot Encoding", fs=8, color=C_TEXT_LIGHT, style="italic")
txt(ax, 7.1, 16.95, "Danh muc + Rating chuan hoa", fs=8, color=C_TEXT_LIGHT)
txt(ax, 7.1, 16.58,
    "[□ □ ■ □ □ □ □ □ □ □ | 0.87]",
    fs=8.5, color=C_PLACE_BD)

# Graph box
draw_box(ax, 9.1, 15.9, 3.7, 2.45, C_GRAPH_BG, C_GRAPH_BD, lw=1.8)
txt(ax, 10.95, 18.05, "Do Thi Di The", fs=9.5, fw="bold", color=C_GRAPH_BD)
txt(ax, 10.95, 17.65,
    r"$\mathcal{G} = (\mathcal{V}, \mathcal{E})$", fs=9, color=C_TEXT_DARK)
txt(ax, 10.95, 17.30, "Canh duong: View, Like, Review", fs=7.8, color=C_TEXT_LIGHT)
txt(ax, 10.95, 16.97, "Canh am: Negative Sampling", fs=7.8, color=C_TEXT_LIGHT)

# Mini bipartite graph inside Graph box
ux = [9.55, 9.55, 9.55]; uy = [16.65, 16.40, 16.15]
px = [11.55, 11.55];     py = [16.55, 16.25]
for xi, yi in zip(ux, uy):
    ax.plot(xi, yi, 'o', color=C_USER_BD, ms=6, zorder=6)
for xi, yi in zip(px, py):
    ax.plot(xi, yi, 's', color=C_PLACE_BD, ms=6, zorder=6)
for ui, pi in [(0,0),(0,1),(1,0),(2,1)]:
    ax.plot([ux[ui], px[pi]], [uy[ui], py[pi]], color="#94A3B8", lw=1, zorder=5)

# Arrows input -> GNN
for xc in [2.9, 7.1, 10.95]:
    arrow(ax, xc, 15.9, xc, 15.38, color=C_ARROW)

# ── 7. SECTION 2 — HeteroGraphSAGE
draw_box(ax, 0.8, 12.0, 12.4, 3.2, C_GNN_BG, C_GNN_BD, radius=0.3, lw=2.5)
txt(ax, 7, 15.07,
    "(2) HeteroGraphSAGE  (K = 2 Tang, hidden_dim = 64)",
    fs=10, fw="bold", color=C_GNN_BD)

# Layer 1
draw_box(ax, 1.1, 13.6, 5.5, 1.3, C_LAYER_BG, "#A78BFA", lw=1.5)
txt(ax, 3.85, 14.60, "Tang 1 - Sample & Aggregate", fs=9, fw="bold", color="#5B21B6")
txt(ax, 3.85, 14.18,
    r"$h^{(1)}_{\mathrm{agg}} = \mathrm{MEAN}(\{h^{(0)}_u \mid u \in \mathcal{S}(v)\})$",
    fs=9, color=C_TEXT_DARK)

# Arrow layer1 -> layer2
ax.annotate("", xy=(7.35, 14.25), xytext=(6.6, 14.25),
            arrowprops=dict(arrowstyle="->", color="#7C3AED", lw=1.5))

# Layer 2
draw_box(ax, 7.4, 13.6, 5.5, 1.3, C_LAYER_BG, "#A78BFA", lw=1.5)
txt(ax, 10.15, 14.60, "Tang 2 - Update", fs=9, fw="bold", color="#5B21B6")
txt(ax, 10.15, 14.18,
    r"$h^{(k)}_v = \sigma(W^k \cdot \mathrm{CONCAT}(h^{(k-1)}_v, h^{(k)}_{\mathrm{agg}}))$",
    fs=9, color=C_TEXT_DARK)

# Embedding output box
draw_box(ax, 3.0, 12.15, 8.0, 1.2, C_EMB_BG, C_GNN_BD, lw=2)
txt(ax, 7.0, 12.95, "Output Embeddings", fs=9.5, fw="bold", color=C_GNN_BD)
txt(ax, 7.0, 12.55,
    r"$h^{(2)}_u \in \mathbb{R}^{64}$   va   $h^{(2)}_p \in \mathbb{R}^{64}$   -- ma hoa thong tin 2 buoc lang gieng",
    fs=9, color=C_TEXT_DARK)

arrow(ax, 3.85, 13.6, 5.5, 13.35, color="#7C3AED", lw=1.3)
arrow(ax, 10.15, 13.6, 8.5, 13.35, color="#7C3AED", lw=1.3)

# ── 8. ARROWS GNN -> split
arrow(ax, 5.0,  12.15, 3.5,  11.5, color=C_SGNN_BD)
arrow(ax, 9.0,  12.15, 10.5, 11.5, color=C_SCB_BD)

# ── 9. SECTION 3 — TWO SCORES
# GNN Score
draw_box(ax, 0.8, 10.45, 5.3, 1.0, C_SGNN_BG, C_SGNN_BD, lw=1.8)
txt(ax, 3.45, 11.18, "GNN Score  (trong so 60%)", fs=9, fw="bold", color=C_SGNN_BD)
txt(ax, 3.45, 10.77,
    r"$S_{\mathrm{GNN}} = \mathrm{sigmoid}(h^{(2)}_u \cdot h^{(2)}_p)$",
    fs=9, color=C_TEXT_DARK)

# Content-Based Score
draw_box(ax, 7.9, 10.45, 5.3, 1.0, C_SCB_BG, C_SCB_BD, lw=1.8)
txt(ax, 10.55, 11.18, "Content-Based Score  (trong so 40%)", fs=9, fw="bold", color=C_SCB_BD)
txt(ax, 10.55, 10.77,
    r"$S_{\mathrm{CB}} = \mathrm{cosine}(x_u, x_p)$",
    fs=9, color=C_TEXT_DARK)

# Arrows -> Fusion
arrow(ax, 3.45, 10.45, 5.5, 9.78, color=C_SGNN_BD)
arrow(ax, 10.55, 10.45, 8.5, 9.78, color=C_SCB_BD)

# ── 10. SECTION 4 — HYBRID FUSION
draw_box(ax, 2.5, 8.85, 9.0, 1.15, C_FUSE_BG, C_FUSE_BD, radius=0.3, lw=2.5)
txt(ax, 7.0, 9.68, "(4) Hybrid Fusion", fs=10, fw="bold", color="#92400E")
txt(ax, 7.0, 9.22,
    r"$S_{\mathrm{final}}(u,p) = 0.6 \cdot S_{\mathrm{GNN}}(u,p) + 0.4 \cdot S_{\mathrm{CB}}(u,p)$",
    fs=10, color=C_TEXT_DARK)

arrow(ax, 7.0, 8.85, 7.0, 8.37, color=C_FUSE_BD, lw=2)

# ── 11. SECTION 5 — OUTPUT
draw_box(ax, 2.5, 7.35, 9.0, 1.0, C_OUT_BG, C_OUT_BD, radius=0.3, lw=2)
txt(ax, 7.0, 8.10, "(5) Sap xep & Tra ve  Top-K = 10 Dia Diem", fs=10, fw="bold", color=C_OUT_BD)
txt(ax, 7.0, 7.65,
    r"sort $\downarrow$ $S_{\mathrm{final}}$  -->  Loai tru da Review  -->  Top-10 ket qua",
    fs=8.5, color=C_TEXT_DARK)

arrow(ax, 7.0, 7.35, 7.0, 6.87, color=C_OUT_BD, lw=2)

# ── 12. SECTION 6 — XAI
draw_box(ax, 0.8, 5.4, 12.4, 1.4, "#FFF7ED", "#EA580C", radius=0.3, lw=2)
txt(ax, 7, 6.67,
    "(6) Explainable AI (XAI) - Giai Thich Ly Do Goi Y",
    fs=10, fw="bold", color="#EA580C")

draw_box(ax, 1.0, 5.55, 5.4, 0.85, C_XAI1_BG, C_SGNN_BD, lw=1.3)
txt(ax, 3.7, 6.25, "GNN chiem uu the:", fs=8.5, fw="bold", color=C_SGNN_BD)
txt(ax, 3.7, 5.90,
    '"Du khach co gu tuong dong cung yeu thich noi nay"',
    fs=8, color=C_TEXT_DARK, style="italic")

txt(ax, 7.0, 5.97, "neu  0.6*S_GNN > 0.4*S_CB",
    fs=7.5, color="#EA580C", fw="bold")

draw_box(ax, 7.6, 5.55, 5.4, 0.85, C_XAI2_BG, C_SCB_BD, lw=1.3)
txt(ax, 10.3, 6.25, "Content chiem uu the:", fs=8.5, fw="bold", color=C_SCB_BD)
txt(ax, 10.3, 5.90,
    '"Phu hop voi the loai yeu thich [X] cua ban"',
    fs=8, color=C_TEXT_DARK, style="italic")

# ── 13. Side labels
for label, yc, color in [
    ("INPUT",  17.15, C_INPUT_BD),
    ("GNN",    13.55, C_GNN_BD),
    ("SCORE",  10.97, C_TEXT_MID),
    ("FUSION",  9.43, "#B45309"),
    ("OUTPUT",  7.85, C_OUT_BD),
    ("XAI",     6.10, "#EA580C"),
]:
    txt(ax, 0.38, yc, label, fs=7, fw="bold", color=color, ha="center")

# ── 14. Training info
draw_box(ax, 0.8, 3.9, 12.4, 1.3, "#F0FDF4", "#16A34A", lw=1.5)
txt(ax, 7, 4.97, "Cau Hinh Huan Luyen (Training Configuration)",
    fs=9.5, fw="bold", color="#15803D")
cols = [
    ("Nhiem vu",  "Link Prediction"),
    ("Ham loi",   "BCE With Logits Loss"),
    ("Toi uu",    "Adam  (lr = 0.01)"),
    ("Epochs",    "100"),
    ("Accuracy",  "85% - 93.5%"),
]
for i, (k, v) in enumerate(cols):
    xc = 1.5 + i * 2.4
    txt(ax, xc, 4.55, k, fs=7.5, fw="bold", color="#166534")
    txt(ax, xc, 4.18, v, fs=7.5, color=C_TEXT_DARK)

# ── 15. Footer
ax.plot([0.8, 13.2], [3.75, 3.75], color="#CBD5E1", lw=1)
txt(ax, 7, 3.45,
    "Do an tot nghiep: Xay dung website ho tro khuyen nghi du lich tinh Savannakhet",
    fs=8, color=C_TEXT_LIGHT, style="italic")
txt(ax, 7, 3.1,
    "Sinh vien: Phoutthasinh Xaysongkham  |  Cong nghe: PyTorch Geometric (PyG), FastAPI, Vue.js 3",
    fs=7.5, color=C_TEXT_LIGHT)

# ── 16. SAVE + SHOW
plt.savefig(OUTPUT_PATH, dpi=180, bbox_inches="tight",
            facecolor=C_BG, edgecolor="none")
plt.show()
print(f"[OK] Saved: {OUTPUT_PATH}")

# ── 17. Download file (เฉพาะ Google Colab)
try:
    from google.colab import files
    files.download(OUTPUT_PATH)
    print("[OK] Downloading file to your computer...")
except ImportError:
    print("[INFO] Not running on Colab - file saved locally.")
