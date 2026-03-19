import pandas as pd
import numpy as np
import time
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.preprocessing import StandardScaler


# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data/processed/cleaned_data.csv")

target = "Category"  # change if needed
X = df.drop(columns=[target])
y = df[target]

feature_names = X.columns.tolist()

# -----------------------------
# Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Scaling (VERY IMPORTANT for KNN)
# -----------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -----------------------------
# Hyperparameter Tuning (K)
# -----------------------------
k_values = list(range(1, 21))
cv_scores = []
test_scores = []

print("Running K tuning...")

for k in k_values:
    model = KNeighborsClassifier(n_neighbors=k)

    # Cross-validation
    scores = cross_val_score(model, X_train, y_train, cv=5)
    cv_scores.append(scores.mean())

    # Test score
    model.fit(X_train, y_train)
    test_scores.append(model.score(X_test, y_test))

best_k = k_values[np.argmax(cv_scores)]
print(f"Best K: {best_k}")

# -----------------------------
# Train Final Model
# -----------------------------
knn = KNeighborsClassifier(n_neighbors=best_k)

start = time.time()
knn.fit(X_train, y_train)
end = time.time()

print(f"Training Time: {end - start:.4f} seconds")

# -----------------------------
# Predictions
# -----------------------------
y_pred = knn.predict(X_test)

# -----------------------------
# Metrics
# -----------------------------
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

train_acc = knn.score(X_train, y_train)
test_acc = knn.score(X_test, y_test)

print("Train Accuracy:", train_acc)
print("Test Accuracy:", test_acc)

# -----------------------------
# Confusion Matrix
# -----------------------------
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title(f"KNN Confusion Matrix (k={best_k})")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("outputs/knn/knn_confusion_matrix.png")
plt.close()

# -----------------------------
# K vs Accuracy Plot
# -----------------------------
plt.figure(figsize=(8,6))
plt.plot(k_values, cv_scores, label="CV Accuracy")
plt.plot(k_values, test_scores, label="Test Accuracy")
plt.axvline(best_k, color='red', linestyle='--', label=f"Best k={best_k}")
plt.xlabel("K")
plt.ylabel("Accuracy")
plt.title("KNN Hyperparameter Tuning")
plt.legend()
plt.grid(True)
plt.savefig("outputs/knn/knn_k_tuning.png")
plt.close()

# -----------------------------
# Distance Metric Experiment
# -----------------------------
print("\nDistance Metric Comparison:")
for metric in ["euclidean", "manhattan"]:
    model = KNeighborsClassifier(n_neighbors=best_k, metric=metric)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"{metric}: {acc:.4f}")

# -----------------------------
# Save Metrics
# -----------------------------
report_dict = classification_report(y_test, y_pred, output_dict=True)
metrics_df = pd.DataFrame(report_dict).T
metrics_df.to_csv("outputs/knn/knn_metrics.csv")

# -----------------------------
# Save Model
# -----------------------------
with open("models/knn_model.pkl", "wb") as f:
    pickle.dump({
        "model": knn,
        "scaler": scaler,
        "features": feature_names,
        "best_k": best_k
    }, f)

print("KNN model saved successfully.")