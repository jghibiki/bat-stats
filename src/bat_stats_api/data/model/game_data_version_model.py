from pydantic import BaseModel
from datetime import datetime


class GameDataVersionModel(BaseModel):
    id: int
    capture_date_time: datetime
