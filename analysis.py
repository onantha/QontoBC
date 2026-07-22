import pandas as pd

# Load dataset (adjust filename/path if needed)
df = pd.read_csv('data_set.csv')

# Ensure date column is datetime
# Replace 'time_settled' with the actual date column name in your CSV
df['time_settled'] = pd.to_datetime(df['time_settled'])

# 1. Global Metrics
total_tx = len(df)
total_amount = df['movement_amount_euros'].sum()

fraud_df = df[df['is_fraud'] == 1]
total_fraud_tx = len(fraud_df)
total_fraud_loss = fraud_df['movement_amount_euros'].sum()

fraud_rate_count = (total_fraud_tx / total_tx) * 100
fraud_rate_amount = (total_fraud_loss / total_amount) * 100
avg_fraud_amount = fraud_df['movement_amount_euros'].mean()
avg_legit_amount = df[df['is_fraud'] == 0]['movement_amount_euros'].mean()

print("=== GLOBAL STAKES ===")
print(f"Total Volume: €{total_amount:,.2f} across {total_tx:,} transactions")
print(f"Total Fraud Loss: €{total_fraud_loss:,.2f} ({total_fraud_tx:,} transactions)")
print(f"Fraud Rate (by Volume/Loss): {fraud_rate_amount:.2f}%")
print(f"Fraud Rate (by Count): {fraud_rate_count:.2f}%")
print(f"Average Fraud Tx Amount: €{avg_fraud_amount:.2f} vs Legit: €{avg_legit_amount:.2f}")

# 2. Time Evolution (Weekly or Monthly)
# Grouping by Week/Month to see trend
df['period'] = df['time_settled'].dt.to_period('M') # or 'M' for monthly
time_series = df.groupby('period').agg(
    total_amount=('movement_amount_euros', 'sum'),
    fraud_amount=('movement_amount_euros', lambda x: x[df.loc[x.index, 'is_fraud'] == 1].sum()),
    fraud_count=('is_fraud', 'sum'),
    total_count=('is_fraud', 'count')
)
time_series['fraud_rate_amt'] = (time_series['fraud_amount'] / time_series['total_amount']) * 100

print("\n=== TIME EVOLUTION ===")
print(time_series)