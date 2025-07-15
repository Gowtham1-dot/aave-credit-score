# Aave V2 Wallet Credit Scoring Engine

This project presents a behavioral credit scoring model (scale: 0–1000) for wallets interacting with the Aave V2 protocol. The system evaluates wallet activity based on transaction patterns to assign a credit score that reflects user trustworthiness, protocol engagement, and risk level.

## Project Objective

DeFi lending platforms currently lack transparent, data-driven tools to assess wallet-level reliability. This project addresses that gap by:

- Analyzing 100,000 raw transaction records from Aave V2
- Engineering behavioral features per wallet
- Producing a transparent, explainable credit score between 0 and 1000
- Highlighting user segments (reliable, moderate, risky)

## Features Extracted

The scoring model is based on the following features extracted from raw JSON data:

| Feature             | Description                                                                 |
|---------------------|-----------------------------------------------------------------------------|
| total_txns          | Total number of transactions initiated by the wallet                       |
| repay_ratio         | Ratio of repayments to borrow actions                                       |
| flashloan_count     | Number of flashloans (higher = riskier)                                     |
| liquidation_count   | Number of liquidations experienced                                          |
| unique_actions      | Number of different DeFi actions performed (e.g., deposit, repay, borrow)   |
| avg_txn_interval    | Average time gap between wallet actions (in seconds)                        |

## Scoring Logic

Each wallet is scored using a weighted formula:

score = 4 × repay_ratio + 3 × unique_actions + 0.5 × total_txns − 1.5 × flashloans − 2.5 × liquidations

pgsql
Copy code

Wallets with fewer than 3 total transactions are considered inactive and excluded from scoring.

Scores are scaled to the range 0–1000 using **percentile ranking** to ensure a balanced distribution.

## Score Interpretation

| Score Range | Classification        |
|-------------|------------------------|
| 0–100       | Risky or inactive wallet |
| 100–500     | Limited or inconsistent behavior |
| 500–800     | Reliable and balanced usage |
| 800–1000    | Highly trustworthy wallet |

## Project Structure

aave-credit-score/
├── data/
│ └── user_transactions.json # Raw input data
├── score_wallets.py # Feature engineering and scoring
├── plot_distribution.py # Generates score distribution chart
├── wallet_scores.csv # Output with scores for each wallet
├── score_distribution.png # Histogram of wallet score ranges
├── analysis.md # Observations and score behavior analysis
├── README.md # This file
└── requirements.txt # Python dependencies

perl
Copy code

## How to Run the Project

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
Generate wallet credit scores:

bash
Copy code
python score_wallets.py
Plot the score distribution:

bash
Copy code
python plot_distribution.py
Results Summary
Transactions processed: 100,000

Wallets scored: approximately 3,000

Scores distributed across all ranges (0–1000)

Credit scoring based on real protocol behavior

Potential Enhancements
Support for multi-chain scoring (e.g., Ethereum + Polygon)

Incorporate transaction amounts and time-weighted scoring

Add ESG or protocol loyalty indicators

Deploy as a browser-based DeFi wallet risk checker

License
This project is open source under the MIT License.

Author
Developed by Gowtham Baratam as part of an applied machine learning and DeFi protocol analysis project.