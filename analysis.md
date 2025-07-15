# Credit Score Analysis – Aave V2

## Score Distribution

The distribution of credit scores shows that wallet behavior varies widely, with scores spread evenly across all deciles after applying percentile-based normalization and filtering out inactive wallets.

## Highlights

- Total wallets scored: ~3,000
- Inactive wallets (< 3 total txns) were excluded
- Most active wallets show balanced protocol usage
- Few outliers scored below 100 (mostly flashloan or borrow-only usage)

## Score Buckets

| Score Range | Wallet Behavior                   |
|-------------|------------------------------------|
| 0–100       | High-risk or flashloan-only users |
| 100–500     | Basic interaction, no repayments  |
| 500–800     | Balanced users, moderate volume   |
| 800–1000    | Highly active, responsible users  |

## Next Steps

- Integrate into lending dashboards
- Flag low-score wallets before allowing credit
- Add value-weighted scoring and real-time pipeline
