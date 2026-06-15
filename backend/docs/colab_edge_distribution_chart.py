# =============================================================
# COPY โค้ดทั้งหมดนี้ไปวางใน Google Colab Cell แล้วรันได้เลย!
# Pie Chart: Edge Distribution (View / Like / Review)
# บทรายงาน: ระบบแนะนำสถานที่ท่องเที่ยว จ.สะหวันนะเขต
# =============================================================

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUTPUT_PATH = "/content/edge_distribution_piechart.png"

# ── ข้อมูล ──
sizes = [60, 25, 15]
colors = ['#3B82F6', '#10B981', '#F59E0B']   # Blue, Green, Amber
explode = (0.04, 0.04, 0.08)

fig, ax = plt.subplots(figsize=(8, 6.5))
fig.patch.set_facecolor('#FAFBFF')
ax.set_facecolor('#FAFBFF')

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=None,
    autopct='%1.0f%%',
    colors=colors,
    explode=explode,
    startangle=140,
    pctdistance=0.72,
    wedgeprops=dict(linewidth=2, edgecolor='white', antialiased=True),
    shadow=False,
)

# ── ปรับ style ตัวเลข % ──
for at in autotexts:
    at.set_fontsize(15)
    at.set_fontweight('bold')
    at.set_color('white')

# ── วงกลมตรงกลาง (Donut style) ──
centre_circle = plt.Circle((0, 0), 0.42, fc='#FAFBFF',
                           linewidth=1.5, edgecolor='#E2E8F0')
ax.add_artist(centre_circle)

# ── ข้อความตรงกลาง ──
ax.text(0, 0.06, 'Interactions', ha='center', va='center',
        fontsize=11, color='#64748B')
ax.text(0, -0.12, '~500-1,500', ha='center', va='center',
        fontsize=13, fontweight='bold', color='#1E293B')

# ── Legend ──
legend_elements = [
    mpatches.Patch(
        facecolor=colors[0], edgecolor='white', label='View   - (w = 1.0)  ~60%'),
    mpatches.Patch(
        facecolor=colors[1], edgecolor='white', label='Like   - (w = 2.0)  ~25%'),
    mpatches.Patch(
        facecolor=colors[2], edgecolor='white', label='Review - (w = 3.0)  ~15%'),
]
ax.legend(handles=legend_elements, loc='lower center',
          bbox_to_anchor=(0.5, -0.15), ncol=1,
          frameon=True, framealpha=0.9,
          fontsize=10.5, handlelength=1.4,
          edgecolor='#CBD5E1')

# ── Title ──
ax.set_title(
    'Edge Distribution - Savannakhet GNN',
    fontsize=13, fontweight='bold', color='#1E293B', pad=18
)

ax.axis('equal')
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=180, bbox_inches='tight',
            facecolor='#FAFBFF', edgecolor='none')
plt.show()
print(f"[OK] Saved: {OUTPUT_PATH}")

# ── Download ──
try:
    from google.colab import files
    files.download(OUTPUT_PATH)
    print("[OK] Downloading...")
except ImportError:
    print("[INFO] Not on Colab — file saved locally")
