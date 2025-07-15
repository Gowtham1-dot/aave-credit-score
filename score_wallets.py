import json
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
import os

def load_data(path='data/user_transactions.json'):
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def extract_features(transactions):
    print("Extracting features...")
    features = defaultdict(lambda: defaultdict(float))
    timestamps = defaultdict(list)

    for tx in tqdm(transactions):
        user = tx.get('userWallet')  # ✅ Correct key
        if not user:
            continue

        action = tx.get('action')
        timestamp = tx.get('timestamp', 0)

        features[user]['total_txns'] += 1
        features[user][f'{action}_count'] += 1
        timestamps[user].append(timestamp)

    for user in features:
        ts = sorted(timestamps[user])
        if len(ts) > 1:
            intervals = [t2 - t1 for t1, t2 in zip(ts[:-1], ts[1:])]
            features[user]['avg_txn_interval'] = sum(intervals) / len(intervals)
        else:
            features[user]['avg_txn_interval'] = 0.0

        action_types = ['deposit', 'withdraw', 'borrow', 'repay', 'liquidation', 'flashloan']
        for a in action_types:
            features[user][f'{a}_count'] = features[user].get(f'{a}_count', 0)

        features[user]['unique_actions'] = sum(
            1 for a in action_types if features[user][f'{a}_count'] > 0
        )

    return pd.DataFrame.from_dict(features, orient='index').fillna(0)

def score_wallets(df):
    print("Scoring wallets...")

    df['repay_ratio'] = df['repay_count'] / (df['borrow_count'] + 1)
    df['flashloan_penalty'] = df['flashloan_count']
    df['liquidation_penalty'] = df['liquidation_count']
    df['activity_score'] = df['total_txns']
    df['diversity_score'] = df['unique_actions']

    # Score formula
    df['raw_score'] = (
        df['repay_ratio'] * 4.0 +
        df['diversity_score'] * 3.0 +
        df['activity_score'] * 0.5 -
        df['flashloan_penalty'] * 1.5 -
        df['liquidation_penalty'] * 2.5
    )

    # Filter out inactive wallets (< 3 total txns)
    df = df[df['total_txns'] >= 3]

    # Normalize using percentile ranking instead of MinMaxScaler
    df['credit_score'] = df['raw_score'].rank(pct=True) * 1000

    return df[['credit_score']].sort_values(by='credit_score', ascending=False)

def main():
    transactions = load_data()
    print(f"\n📦 Total raw transactions: {len(transactions)}")

    df = extract_features(transactions)
    print(f"\n🧠 Total unique wallets extracted: {len(df)}")

    scores = score_wallets(df)
    print(f"\n✅ Wallets scored (active only): {len(scores)}")
    print(scores.head())

    output_file = 'wallet_scores.csv'
    if os.path.exists(output_file):
        try:
            os.rename(output_file, output_file)
        except PermissionError:
            print(f"\n❌ Please close '{output_file}' before running again.")
            return

    scores.to_csv(output_file)
    print(f"\n💾 Scores saved to {output_file}")

if __name__ == '__main__':
    main()
