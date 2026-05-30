from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional

def get_la_start_of_day() -> datetime:
    """Returns the start of the current day (00:00:00) in Los Angeles time."""
    tz = ZoneInfo("America/Los_Angeles")
    now_la = datetime.now(tz)
    return datetime(now_la.year, now_la.month, now_la.day, tzinfo=tz)

@dataclass
class ModelTokenBudget:
    model_name: str
    remaining_input_tokens: int
    remaining_output_tokens: int
    created_at_timestamp: datetime = field(default_factory=get_la_start_of_day)
    id: Optional[str] = None

    def to_dict(self):
        return {
            "model_name": self.model_name,
            "remaining_input_tokens": self.remaining_input_tokens,
            "remaining_output_tokens": self.remaining_output_tokens,
            "created_at_timestamp": self.created_at_timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict, doc_id: str):
        return cls(
            model_name=data.get("model_name", ""),
            remaining_input_tokens=data.get("remaining_input_tokens", 0),
            remaining_output_tokens=data.get("remaining_output_tokens", 0),
            created_at_timestamp=data.get("created_at_timestamp"),
            id=doc_id
        )
