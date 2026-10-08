"""
CountryEdu IT Support Optimization - 2M ticket generator
Run:
    python generate_2m_dataset.py
Output:
    support_tickets_2m.csv

The supplied case says the company handles 2M tickets/year.
This generator uses deterministic seed 42 and the same data-generating logic
as the 200k demonstration dataset included with the project.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 2_000_000
categories = ["Network","Software","Hardware","Access","Email","Security","Database","Other"]
cat_p = [0.20,0.26,0.13,0.18,0.10,0.05,0.04,0.04]
priorities = ["Low","Medium","High","Critical"]
priority_p = [0.28,0.45,0.21,0.06]
clients = ["Small","Medium","Enterprise"]
client_p = [0.50,0.32,0.18]
dates = pd.date_range("2025-01-01","2025-12-31",freq="h")

ticket_date = rng.choice(dates, size=N, replace=True)
category = rng.choice(categories, N, p=cat_p)
priority = rng.choice(priorities, N, p=priority_p)
client = rng.choice(clients, N, p=client_p)

base_hours = {"Network":2.1,"Software":1.5,"Hardware":3.2,"Access":0.7,
              "Email":0.8,"Security":2.6,"Database":3.4,"Other":1.2}
priority_mult = {"Low":0.75,"Medium":1.0,"High":1.45,"Critical":2.0}
client_mult = {"Small":0.85,"Medium":1.0,"Enterprise":1.25}
cost_base = {"Small":26,"Medium":34,"Enterprise":48}

resolution_hours = np.array([
    base_hours[c]*priority_mult[p]*client_mult[cl]*rng.lognormal(0,0.28)
    for c,p,cl in zip(category,priority,client)
])
resolution_hours = np.clip(resolution_hours,0.1,24)
engineer_cost = np.array([cost_base[c]*rng.normal(1.0,0.08) for c in client])
engineer_cost = np.clip(engineer_cost,18,70)

cat_esc = {"Network":.16,"Software":.10,"Hardware":.13,"Access":.035,
           "Email":.045,"Security":.20,"Database":.19,"Other":.07}
logit = (np.array([cat_esc[c] for c in category]) +
         np.where(np.isin(priority,["High","Critical"]),0.07,0) +
         np.clip((resolution_hours-2.0)/30,-0.02,0.18))
escalation_prob = np.clip(logit,0.01,0.65)
escalated = (rng.random(N) < escalation_prob).astype(int)
escalation_count = np.where(escalated,rng.integers(1,4,N),0)

csat_raw = (4.75 - 0.12*np.log1p(resolution_hours)
            - 0.20*escalation_count
            + rng.normal(0,0.28,N))
csat = np.clip(np.round(csat_raw*2)/2,1,5)

df = pd.DataFrame({
    "ticket_id":np.arange(1,N+1),
    "created_at":ticket_date,
    "issue_category":category,
    "priority":priority,
    "resolution_time_hours":np.round(resolution_hours,2),
    "engineer_cost_per_hour":np.round(engineer_cost,2),
    "client_type":client,
    "escalation_count":escalation_count,
    "csat":csat
})
for col,rate in {"resolution_time_hours":.08,"engineer_cost_per_hour":.04,
                 "client_type":.12,"csat":.18}.items():
    mask = rng.random(N) < rate
    df.loc[mask,col] = np.nan

df.to_csv("support_tickets_2m.csv",index=False)
print("Created support_tickets_2m.csv with",len(df),"rows")
