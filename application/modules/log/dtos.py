from pydantic import BaseModel


class LogDTO(BaseModel):
    start_time: str
    end_time: str
    details: str
    user_id: str
