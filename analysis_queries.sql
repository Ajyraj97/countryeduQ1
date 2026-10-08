-- CountryEdu IT Support Cost Optimization
-- SQL dialect: PostgreSQL-style SQL

-- 1. Ticket-level cost
SELECT
    ticket_id,
    resolution_time_hours * engineer_cost_per_hour AS support_cost
FROM support_tickets;

-- 2. Executive KPIs
SELECT
    COUNT(*) AS tickets,
    SUM(resolution_time_hours * engineer_cost_per_hour) AS total_support_cost,
    AVG(resolution_time_hours * engineer_cost_per_hour) AS avg_cost_per_ticket,
    AVG(resolution_time_hours) AS avg_resolution_hours,
    AVG(CASE WHEN escalation_count > 0 THEN 1.0 ELSE 0.0 END) AS escalation_rate,
    AVG(csat) AS avg_csat
FROM support_tickets;

-- 3. Cost by issue category
SELECT
    issue_category,
    COUNT(*) AS tickets,
    SUM(resolution_time_hours * engineer_cost_per_hour) AS total_cost,
    AVG(resolution_time_hours) AS avg_resolution_hours,
    AVG(CASE WHEN escalation_count > 0 THEN 1.0 ELSE 0.0 END) AS escalation_rate,
    AVG(csat) AS avg_csat
FROM support_tickets
GROUP BY issue_category
ORDER BY total_cost DESC;

-- 4. Cost by client
SELECT
    client_type,
    COUNT(*) AS tickets,
    SUM(resolution_time_hours * engineer_cost_per_hour) AS total_cost,
    AVG(resolution_time_hours * engineer_cost_per_hour) AS avg_cost
FROM support_tickets
GROUP BY client_type
ORDER BY total_cost DESC;

-- 5. High-risk escalation segments
SELECT
    issue_category,
    priority,
    client_type,
    COUNT(*) AS tickets,
    AVG(CASE WHEN escalation_count > 0 THEN 1.0 ELSE 0.0 END) AS escalation_rate,
    AVG(resolution_time_hours) AS avg_resolution_hours
FROM support_tickets
GROUP BY issue_category, priority, client_type
HAVING COUNT(*) >= 100
ORDER BY escalation_rate DESC;

-- 6. CSAT vs resolution time bucket
SELECT
    CASE
        WHEN resolution_time_hours < 1 THEN '<1h'
        WHEN resolution_time_hours < 2 THEN '1-2h'
        WHEN resolution_time_hours < 4 THEN '2-4h'
        WHEN resolution_time_hours < 8 THEN '4-8h'
        ELSE '8h+'
    END AS resolution_bucket,
    COUNT(*) AS tickets,
    AVG(csat) AS avg_csat
FROM support_tickets
GROUP BY resolution_bucket
ORDER BY resolution_bucket;