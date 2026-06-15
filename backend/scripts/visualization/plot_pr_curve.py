import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

# 1. สร้างข้อมูลจำลองแบบซับซ้อนขึ้นนิดหน่อย
X, y = make_classification(n_samples=1000, n_classes=2, weights=[0.8, 0.2], 
                           n_informative=4, n_redundant=1, random_state=42)

# 2. แบ่งข้อมูล
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

plt.figure(figsize=(9, 7))

# ==========================================
# โมเดลที่ 1: Logistic Regression (โมเดลเส้นตรงพื้นฐาน)
# ==========================================
lr_model = LogisticRegression()
lr_model.fit(X_train, y_train)
lr_y_scores = lr_model.predict_proba(X_test)[:, 1]

lr_precision, lr_recall, _ = precision_recall_curve(y_test, lr_y_scores)
lr_ap = average_precision_score(y_test, lr_y_scores)

plt.plot(lr_recall, lr_precision, color='blue', lw=2, linestyle='--', 
         label=f'Logistic Regression (AP = {lr_ap:.2f})')

# ==========================================
# โมเดลที่ 2: Random Forest (โมเดลต้นไม้ตัดสินใจ ซับซ้อนและเก่งขึ้น)
# ==========================================
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_y_scores = rf_model.predict_proba(X_test)[:, 1]

rf_precision, rf_recall, _ = precision_recall_curve(y_test, rf_y_scores)
rf_ap = average_precision_score(y_test, rf_y_scores)

plt.plot(rf_recall, rf_precision, color='red', lw=2.5, 
         label=f'Random Forest (AP = {rf_ap:.2f})')
plt.fill_between(rf_recall, rf_precision, alpha=0.1, color='red')

# ==========================================
# ตกแต่งกราฟ
# ==========================================
plt.xlabel('Recall', fontsize=12)
plt.ylabel('Precision', fontsize=12)
plt.title('Precision-Recall Curve Comparison\n(Logistic Regression vs Random Forest)', fontsize=14)
plt.legend(loc="lower left", fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)

# บันทึกรูปภาพ
import os
plots_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots')
os.makedirs(plots_dir, exist_ok=True)
output_path = os.path.join(plots_dir, 'pr_curve_comparison.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Successfully saved comparison image: {output_path}")
