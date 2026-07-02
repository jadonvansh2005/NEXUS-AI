DATA_SCIENCE_PROMPT = """

Previous Conversation:

{memory_context}

Current Query:

{user_query}

User Query:
{user_query}

Detected Domain:
{domain}

Execution Plan:
{execution_plan}

Tool Outputs:
{tool_outputs}

Generate a detailed report in the following format:

1. Dataset Overview
2. Data Quality Analysis
3. EDA Insights
4. Problem Type
5. Target Variable

6. Model Leaderboard
7. Top 3 Models
8. Hyperparameter Tuning Results
9. Best Model
10. Feature Importance
11. Recommendations

Do NOT skip any section.
"""