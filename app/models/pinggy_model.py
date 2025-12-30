from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PinggyModel(BaseModel):
    active: bool
    since: Optional[datetime]
