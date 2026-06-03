from dataclasses import dataclass, field
from datetime import datetime
from utils.get_la_start_of_day import get_la_start_of_day
from typing import Optional

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
