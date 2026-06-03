from dataclasses import dataclass, field
from datetime import datetime
from utils.get_la_start_of_day import get_la_start_of_day
from typing import Optional

@dataclass
class User:
    email: str
    request_count: int = 0
    created_at_timestamp: datetime = field(default_factory=get_la_start_of_day)
    id: Optional[str] = None

    def to_dict(self):
        data = {
            "email": self.email,
            "request_count": self.request_count,
            "created_at_timestamp": self.created_at_timestamp,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict, doc_id: str):
        return cls(
            email=data.get("email", ""),
            request_count=data.get("request_count", 0),
            created_at_timestamp=data.get("created_at_timestamp"),
            id=doc_id
        )
