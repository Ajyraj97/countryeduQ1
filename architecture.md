# Production Architecture

Ticket Sources
    |
    v
Kafka / Event Bus (50K events/sec)
    |
    +--> Stream Processing (Spark/Flink)
    |        |
    |        +--> Data Quality / Missingness Flags
    |        +--> Feature Generation
    |        +--> Real-time aggregates
    |
    +--> Data Lake / Warehouse
             |
             +--> SQL / Power BI
             |
             +--> Model Training

Real-time path:
New Ticket -> Feature Store/Cache -> Pre-trained Model -> Escalation Risk
           -> Routing Decision -> Ticketing System

Latency target:
- Feature lookup: sub-second
- Model inference: milliseconds to low hundreds of ms
- End-to-end decision: comfortably below 5 seconds

Production controls:
- Model versioning
- Feature drift monitoring
- Data quality checks
- Prediction latency monitoring
- Probability calibration
- Human override for high-impact routing decisions