import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('wallet_scores.csv')

df['score_bucket'] = pd.cut(df['credit_score'], bins=range(0, 1101, 100))
bucket_counts = df['score_bucket'].value_counts().sort_index()

plt.figure(figsize=(10, 6))
bucket_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Wallet Credit Score Distribution')
plt.xlabel('Credit Score Range')
plt.ylabel('Number of Wallets')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("score_distribution.png")
print(" score_distribution.png saved")
