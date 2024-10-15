import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

file_path = '分地区投放数据.xlsx'
sheet_name = '国家数据拆分'
screeningBaseCount=50
data = pd.read_excel(file_path,sheet_name=sheet_name,usecols='C:R')
data = data.iloc[3:]
data = data[data['预注册数'] > screeningBaseCount]

data['Ratio_a'] = data['8.25-9.10'] + data['2.22-4.6']- data['预估CPA']*2
data['Ratio_b']=data['8.25-9.10']+data['2.22-4.6']
X = data[['Ratio_a','Ratio_b']]
kmeans = KMeans(n_clusters=3)  # 根据需要调整聚类数
data['Cluster'] = kmeans.fit_predict(X)
sorted_data = data.sort_values(by=['Ratio_a','Ratio_b'], ascending=[False,False])
mean_ratios = data.groupby('Cluster')[['Ratio_a', 'Ratio_b']].mean().sort_values(by='Ratio_a', ascending=False)
#  可视化结果
plt.figure(figsize=(10, 6))
scatter = plt.scatter(data.index, data['Ratio_a'], c=data['Cluster'], cmap='viridis')
# 添加国家名标注
for i in range(len(data)):
    plt.annotate(data['国家'].iloc[i], (data.index[i], data['Ratio_a'].iloc[i]), fontsize=15, ha='left')
plt.xlabel('X')
plt.ylabel('LTV-CPA')
plt.title('Tier by LTV&LTV-CPA')
plt.colorbar(scatter, label='Cluster')
plt.show()

print("\n分组后的数据：")
print(sorted_data)
print(mean_ratios)
# output_file = '国际拆分重定向.xlsx'  # 指定导出文件名
# sorted_data.to_excel(output_file, index=False)  # 导出数据，不保留索引
# print(f"\n数据已导出到 {output_file}")