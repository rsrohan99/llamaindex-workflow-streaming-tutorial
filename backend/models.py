from pydantic import BaseModel, field_validator, Field


class EssayData(BaseModel):
    topic: str
    word_limit: int = 100

    class Config:
        json_schema_extra = {"example": {"topic": "Climate change", "word_limit": 100}}

    @field_validator("topic")
    def topic_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("Topic must not be empty")
        return v
