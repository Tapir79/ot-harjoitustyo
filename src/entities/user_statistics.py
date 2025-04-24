from dataclasses import dataclass
from typing import Optional


@dataclass
class UserStatistics:
    user_id: int
    high_score: int
    level: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
