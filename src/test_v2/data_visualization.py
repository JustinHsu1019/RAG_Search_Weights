import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

data = {
    'Weights': ['10:0', '9:1', '8:2', '7:3', '6:4', '5:5', '4:6', '3:7', '2:8', '1:9'],
    'Retrieval Accuracy': [70.0, 73.33, 83.33, 83.33, 83.33, 80.0, 86.67, 83.33, 83.33, 83.33],
}
df = pd.DataFrame(data)

# 檢索準確性柱狀圖
plt.figure(figsize=(10, 6))
plt.bar(df['Weights'], df['Retrieval Accuracy'], color='skyblue')
plt.xlabel('Weights')
plt.ylabel('Retrieval Accuracy (%)')
plt.title('Retrieval Accuracy for Different Weight Configurations')
plt.savefig('data/第二次試驗/純語意_img/retrieval_accuracy.png')
