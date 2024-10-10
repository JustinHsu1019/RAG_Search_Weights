import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

data = {
    "Weights": ["10:0", "9:1", "8:2", "7:3", "6:4", "5:5", "4:6", "3:7", "2:8", "1:9", "0:10"],
    "Retrieval Accuracy": [
        69.14,
        77.44,
        83.42,
        86.77,
        86.69,
        86.32,
        85.69,
        84.57,
        83.45,
        82.48,
        81.33
    ],
}
df = pd.DataFrame(data)

# 檢索準確性柱狀圖
plt.figure(figsize=(10, 6))
plt.bar(df["Weights"], df["Retrieval Accuracy"], color="skyblue")
plt.xlabel("Weights")
plt.ylabel("Retrieval Accuracy (%)")
plt.title("Retrieval Accuracy for Different Weight Configurations")
plt.savefig("result/test_1006/retrieval_accuracy.png")
