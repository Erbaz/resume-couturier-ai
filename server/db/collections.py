from .client import db

users_collection = db.collection("users")
model_token_budgets_collection = db.collection("model_token_budgets")
daily_budget_collection = db.collection("daily_budget")
