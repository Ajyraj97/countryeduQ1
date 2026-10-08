# CountryEdu Data Analyst Case Study — IT Support Cost Optimization

## What is included
- `support_tickets_sample_200k.csv` — synthetic 200,000-ticket dataset for demonstration.
- `generate_2m_dataset.py` — generator for the case's 2,000,000-ticket annual dataset.
- `analysis.py` — Python analysis starter.
- `analysis_queries.sql` — SQL queries.
- `executive_metrics.csv`, `cost_by_category.csv`, `cost_by_client.csv`, `cost_by_priority.csv` — analysis outputs.
- `powerbi_dashboard_spec.md` — Power BI dashboard design and DAX measures.
- `architecture.md` — streaming + ML architecture for 50K events/sec and <5-second prediction.
- `final_recommendations.md` — management recommendations.
- `CountryEdu_Data_Analyst_Case_Study.pdf` — submission-ready written report.
- `CountryEdu_Data_Analyst_Presentation.pptx` — presentation deck.
- `charts/` — generated analysis charts.

## Important
The employer did not provide the real ticket dataset. Therefore this project uses synthetic data.
Do not claim that synthetic figures are CountryEdu's real performance.

## How to run
1. Install:
   `pip install pandas numpy scikit-learn matplotlib`
2. Run:
   `python analysis.py`
3. To create the full case-scale dataset:
   `python generate_2m_dataset.py`
4. Import the CSV into Power BI using the dashboard specification.

## Interview talking point
"I built the analytical framework so that once the production dataset is supplied, the synthetic layer can be replaced without changing the business logic. I intentionally separated KPI calculation, missing-data treatment, predictive modeling and real-time architecture."