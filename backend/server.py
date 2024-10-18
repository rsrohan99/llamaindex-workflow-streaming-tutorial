import json
import time

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from pydantic import BaseModel

from models import RequestData
from workflow import SimpleEssayWorkflow, TokenEvent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    message: str


@app.post("/essay")
async def chat(request: Request, data: RequestData):
    try:
        workflow = SimpleEssayWorkflow(
            timeout=360,
        )

        handler = workflow.run(topic=data.prompt, word_limit=data.word_limit)

        await handler

        async def event_generator():
            async for ev in handler.stream_events():
                if await request.is_disconnected():
                    break
                if isinstance(ev, TokenEvent):
                    time.sleep(0.1)
                    yield f"0:{json.dumps(ev.token)}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={"X-Experimental-Stream-Data": "true"},
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in workflow: {e}",
        ) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
