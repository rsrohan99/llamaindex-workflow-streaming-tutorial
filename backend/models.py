from pydantic import BaseModel, field_validator


class RequestData(BaseModel):
    prompt: str
    word_limit: int = 100

    class Config:
        json_schema_extra = {"example": {"prompt": "Climate change"}}

    @field_validator("prompt")
    def topic_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("Topic must not be empty")
        return v
