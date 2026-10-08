import pandas as pd

df = pd.read_csv("support_tickets_sample_200k.csv", parse_dates=["created_at"])

# Missing-data treatment
df["resolution_time_hours"] = df["resolution_time_hours"].fillna(
    df.groupby("issue_category")["resolution_time_hours"].transform("median")
)
df["engineer_cost_per_hour"] = df["engineer_cost_per_hour"].fillna(
    df.groupby("client_type")["engineer_cost_per_hour"].transform("median")
)
df["client_type"] = df["client_type"].fillna("Unknown")
df["csat"] = df["csat"].fillna(df["csat"].median())

df["support_cost"] = df["resolution_time_hours"] * df["engineer_cost_per_hour"]
df["escalated"] = (df["escalation_count"].fillna(0) > 0).astype(int)

print("Total support cost:", df["support_cost"].sum())
print("Average ticket cost:", df["support_cost"].mean())
print("Average resolution hours:", df["resolution_time_hours"].mean())
print("Escalation rate:", df["escalated"].mean())
print("Average CSAT:", df["csat"].mean())

print("\nCost by category:")
print(df.groupby("issue_category")["support_cost"].agg(["count","sum","mean"]).sort_values("sum", ascending=False))