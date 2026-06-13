from dataclasses import dataclass, field
from datetime import datetime, timedelta
from utils.get_la_start_of_day import get_la_start_of_day
from typing import Optional

@dataclass
class User:
    email: str
    request_count: int = 0
    created_at_timestamp: datetime = field(default_factory=get_la_start_of_day)
    expires_at: Optional[datetime] = None
    id: Optional[str] = None

    def __post_init__(self):
        if self.expires_at is None:
            self.expires_at = self.created_at_timestamp + timedelta(hours=24)

    def to_dict(self):
        data = {
            "email": self.email,
            "request_count": self.request_count,
            "created_at_timestamp": self.created_at_timestamp,
            "expires_at": self.expires_at,
        }
        return data

    @classmethod
    def from_dict(cls, data: dict, doc_id: str):
        return cls(
            email=data.get("email", ""),
            request_count=data.get("request_count", 0),
            created_at_timestamp=data.get("created_at_timestamp"),
            expires_at=data.get("expires_at"),
            id=doc_id
        )
