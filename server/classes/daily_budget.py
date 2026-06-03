from dataclasses import dataclass, field
from datetime import datetime
from utils.get_la_start_of_day import get_la_start_of_day
from typing import Optional

@dataclass
class DailyBudget:
    starting_timestamp: datetime = field(default_factory=get_la_start_of_day)
    gemini_budget_utilized: float = 0.0
    number_of_requests: int = 0
    id: Optional[str] = None

    def to_dict(self):
        return {
            "starting_timestamp": self.starting_timestamp,
            "gemini_budget_utilized": self.gemini_budget_utilized,
            "number_of_requests": self.number_of_requests,
        }
