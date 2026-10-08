# Power BI Dashboard Specification

## Page 1 — Executive Overview
Cards:
- Total Tickets
- Total Support Cost
- Cost / Ticket
- Avg Resolution Time
- Escalation Rate
- Avg CSAT

Target cards:
- Cost reduction target: 20%
- CSAT target: >4.2

## Page 2 — Cost Optimization
Visuals:
1. Cost by issue category
2. Pareto cumulative cost
3. Cost by client type
4. Cost by priority
5. Average resolution time by category

## Page 3 — Customer Experience
Visuals:
1. CSAT by category
2. CSAT by resolution-time bucket
3. CSAT vs escalation count
4. CSAT by client type

## Page 4 — Workforce
Visuals:
1. Tickets by category
2. Resolution hours by category
3. Escalation rate by category
4. Engineer utilization (when engineer-level capacity data is available)

## Recommended slicers
- Date
- Issue category
- Priority
- Client type

## Core DAX measures
Total Cost =
SUMX(SupportTickets,
    SupportTickets[resolution_time_hours] *
    SupportTickets[engineer_cost_per_hour]
)

Cost per Ticket =
DIVIDE([Total Cost], COUNTROWS(SupportTickets))

Escalation Rate =
DIVIDE(
    CALCULATE(COUNTROWS(SupportTickets), SupportTickets[escalation_count] > 0),
    COUNTROWS(SupportTickets)
)

Average CSAT =
AVERAGE(SupportTickets[csat])