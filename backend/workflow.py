from os import environ
from textwrap import dedent
from typing import Optional, List
from dotenv import load_dotenv

from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter as HTTPSpanExporter,
)
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor

from llama_index.core.workflow import (
    Workflow,
    Event,
    StartEvent,
    StopEvent,
    Context,
    step,
)
from llama_index.core.prompts import PromptTemplate
from llama_index.llms.openai import OpenAI


load_dotenv()


environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={environ.get('PHOENIX_API_KEY')}"

# Add Arize Phoenix
span_phoenix_processor = SimpleSpanProcessor(
    HTTPSpanExporter(endpoint="https://app.phoenix.arize.com/v1/traces")
)

# Add them to the tracer
tracer_provider = trace_sdk.TracerProvider()
tracer_provider.add_span_processor(span_processor=span_phoenix_processor)

# Instrument the application
LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)


class TokenEvent(Event):
    token: str


class SimpleEssayWorkflow(Workflow):
    def __init__(
        self,
        timeout: int = 360,
    ):
        super().__init__(timeout=timeout)
        self.llm = OpenAI(model="gpt-4o-mini")

    @step
    async def write_essay(self, ev: StartEvent, ctx: Context) -> StopEvent:
        topic = ev.topic
        word_limit = ev.word_limit
        prompt = PromptTemplate(
            dedent(
                """
                Write an essay on the topic: "{topic}" under {word_limit} words.
                Essay: 
                """
            )
        )
        response_generator = await self.llm.astream(
            prompt=prompt,
            topic=topic,
            word_limit=word_limit,
        )

        async for token in response_generator:
            ctx.write_event_to_stream(TokenEvent(token=token))

        return StopEvent(result="Done")
