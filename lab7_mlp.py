# ────────────────────────────────────────────────────────
# ไลบรารีสำหรับการจัดการข้อมูล
import numpy as np
import pandas as pd

# ────────────────────────────────────────────────────────
# ไลบรารีสำหรับ Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# ────────────────────────────────────────────────────────
# ไลบรารีจาก scikit-learn สำหรับ Preprocessing
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score

# ────────────────────────────────────────────────────────
# ไลบรารีสำหรับ MLP Model
from sklearn.neural_network import MLPClassifier

# ────────────────────────────────────────────────────────
# ไลบรารีสำหรับการประเมินผล
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# ขั้นตอนที่ 2: โหลดข้อมูล
df = pd.read_csv('coffee_beans.csv')

print("Shape:", df.shape)
print("\nข้อมูล 5 แถวแรก:")
print(df.head())

print("\nข้อมูลสถิติ:")
print(df.describe())

print("\nตรวจสอบค่า Missing:")
print(df.isnull().sum())

print("\nการกระจายของ Class:")
print(df['Species'].value_counts())

# ขั้นตอนที่ 3: Encoding
# 3.1 Label Encoding สำหรับ Target Variable
le = LabelEncoder()
df['Species_encoded'] = le.fit_transform(df['Species'])

label_mapping = dict(zip(le.classes_, le.transform(le.classes_)))
print("\nLabel Mapping:")
for species, label in label_mapping.items():
    print(f"  {species}  →  {label}")

# 3.2 One-Hot Encoding สำหรับ Roast_Level
roast_dummies = pd.get_dummies(
    df['Roast_Level'],
    prefix='Roast',
    drop_first=False
)
print("\nOne-Hot Encoded Roast_Level:")
print(roast_dummies.head())

df_encoded = pd.concat([df, roast_dummies], axis=1)
df_encoded = df_encoded.drop(columns=['Roast_Level'])

# ขั้นตอนที่ 4: แบ่งข้อมูลและ Scaling
numeric_features = ['Altitude', 'Acidity', 'Caffeine_Content', 'Density']
encoded_features = ['Roast_1', 'Roast_2', 'Roast_3']

X = df_encoded[numeric_features + encoded_features].values
y = df_encoded['Species_encoded'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"\nTrain set: {X_train.shape[0]} records")
print(f"Test set:  {X_test.shape[0]} records")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ขั้นตอนที่ 5: สร้างและฝึก MLP Model
mlp = MLPClassifier(
    hidden_layer_sizes=(64, 32),
    activation='relu',
    solver='adam',
    learning_rate_init=0.001,
    max_iter=500,
    batch_size=16,
    random_state=42,
    verbose=False,
    early_stopping=True,
    validation_fraction=0.1
)

print("\nTraining MLP Model...")
mlp.fit(X_train_scaled, y_train)

print(f"จำนวน Iteration ที่ใช้จริง: {mlp.n_iter_}")
print(f"Final Training Loss: {mlp.loss_:.4f}")

# ขั้นตอนที่ 6: ประเมินผล Model
y_pred = mlp.predict(X_test_scaled)
y_pred_proba = mlp.predict_proba(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
print(f"\nTest Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

print("\nClassification Report:")
target_names = le.classes_
print(classification_report(y_test, y_pred, target_names=target_names))

cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(
    cm,
    annot=True,
    fmt='d',
    cmap='Blues',
    xticklabels=target_names,
    yticklabels=target_names
)
plt.title('Confusion Matrix: Coffee Beans Classification')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150)
print("Saved confusion_matrix.png")

# ขั้นตอนที่ 7: วิเคราะห์ Learning Curve
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(mlp.loss_curve_, label='Training Loss', color='steelblue')
if mlp.validation_scores_ is not None:
    val_loss = [1 - s for s in mlp.validation_scores_]
    plt.plot(val_loss, label='Validation Loss', color='orange', linestyle='--')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Loss Curve')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
if hasattr(mlp, 'validation_scores_') and mlp.validation_scores_:
    plt.plot(mlp.validation_scores_, label='Validation Accuracy', color='green')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.title('Validation Accuracy Curve')
    plt.legend()
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('learning_curve.png', dpi=150)
print("Saved learning_curve.png")
# plt.show()

# ────────────────────────────────────────────────────────
# ขั้นตอนที่ 8: ทดสอบทำนายข้อมูลใหม่ (Predicting New Data)
print("\n" + "="*50)
print("ขั้นตอนที่ 8: ทดสอบทำนายข้อมูลใหม่ (Predicting New Data)")

# สร้างลูปสำหรับให้ผู้ใช้กรอกข้อมูลเอง
while True:
    print("\nกรุณากรอกข้อมูลเมล็ดกาแฟที่ต้องการจำแนก (หรือพิมพ์ 'q' เพื่อออก)")
    try:
        altitude_input = input("1. ความสูงของแหล่งปลูก (Altitude) [200-2500 m]: ")
        if altitude_input.lower() == 'q':
            break
        altitude = float(altitude_input)
        
        acidity = float(input("2. ระดับความเป็นกรด (Acidity) [3.5-7.0 pH]: "))
        caffeine = float(input("3. ปริมาณคาเฟอีน (Caffeine_Content) [0.8-4.0 %]: "))
        density = float(input("4. ความหนาแน่นของเมล็ด (Density) [0.6-1.2 g/cm³]: "))
        roast_level_input = input("5. ระดับการคั่ว (Roast_Level) [1=Light, 2=Medium, 3=Dark]: ")
        
        # แปลง Roast Level เป็น One-Hot Encoding [Roast_1, Roast_2, Roast_3]
        roast_1, roast_2, roast_3 = 0, 0, 0
        if roast_level_input == '1':
            roast_1 = 1
        elif roast_level_input == '2':
            roast_2 = 1
        elif roast_level_input == '3':
            roast_3 = 1
        else:
            print(">> กรุณากรอกระดับการคั่วเป็นเลข 1, 2, หรือ 3 เท่านั้น!\n")
            continue
            
        # สร้าง Array ข้อมูลใหม่ 1 ตัวอย่าง
        new_sample = np.array([[altitude, acidity, caffeine, density, roast_1, roast_2, roast_3]])
        
        # แปลงข้อมูลใหม่ด้วย Scaler ตัวเดียวกับที่ใช้ใน Train Set
        new_sample_scaled = scaler.transform(new_sample)

        # ใช้โมเดลทำนาย
        predicted_label = mlp.predict(new_sample_scaled)
        predicted_prob = mlp.predict_proba(new_sample_scaled)

        species_name = le.inverse_transform(predicted_label)[0]
        confidence = np.max(predicted_prob) * 100
        
        print("\n" + "-"*40)
        print(">>> ผลการทำนาย <<<")
        print(f"คุณสมบัติ: ความสูง={altitude}m, กรด={acidity}pH, คาเฟอีน={caffeine}%, หนาแน่น={density}, ระดับคั่ว={roast_level_input}")
        print(f"ทำนายสายพันธุ์เป็น: '{species_name}' (ความมั่นใจ: {confidence:.2f}%)")
        print("-"*40 + "\n")

    except ValueError:
        print(">> กรุณากรอกข้อมูลเป็นตัวเลขที่ถูกต้อง!\n")
        
print("="*50 + "\nจบการทำงานขั้นตอนทำนายข้อมูล")
