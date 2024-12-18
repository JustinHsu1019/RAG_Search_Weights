import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")

data = {
    "Weights": [
        "10:0",
        "9:1",
        "8:2",
        "7:3",
        "6:4",
        "5:5",
        "4:6",
        "3:7",
        "2:8",
        "1:9",
        "0:10",
    ],
    "Retrieval Accuracy": [
        63.67,
        72.18,
        78.20,
        81.47,
        80.85,
        79.97,
        78.78,
        77.27,
        75.87,
        74.52,
        72.91,
    ],
}
df = pd.DataFrame(data)


if __name__ == "__main__1":
    """生成檢索準確性柱狀圖"""
    plt.figure(figsize=(10, 6))
    plt.bar(df["Weights"], df["Retrieval Accuracy"], color="skyblue")
    plt.xlabel("Weights")
    plt.ylabel("Retrieval Accuracy (%)")
    plt.title("Retrieval Accuracy for Different Weight Configurations")
    plt.savefig("result/test_1006/問題分類/短語句.png")


if __name__ == "__main__2":
    """生成準確率 list"""
    accuracy_data = """
檢索結果_1.0 準確率: 63.67%
檢索結果_0.9 準確率: 72.18%
檢索結果_0.8 準確率: 78.20%
檢索結果_0.7 準確率: 81.47%
檢索結果_0.6 準確率: 80.85%
檢索結果_0.5 準確率: 79.97%
檢索結果_0.4 準確率: 78.78%
檢索結果_0.3 準確率: 77.27%
檢索結果_0.2 準確率: 75.87%
檢索結果_0.1 準確率: 74.52%
檢索結果_0.0 準確率: 72.91%
    """
    accuracy_values = [
        line.split(": ")[1].replace("%", "")
        for line in accuracy_data.splitlines()
        if ": " in line
    ]
    formatted_accuracy = ",\n".join(accuracy_values)
    print(formatted_accuracy)
