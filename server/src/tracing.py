# server/src/tracing.py
"""
Single source of truth for Phoenix tracing.
Every module can do `from src.tracing import tracer`.
"""

from dotenv import load_dotenv
load_dotenv()                        # reads PHOENIX_* and DB_* etc.

import os
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

# ---- Configure the global tracer provider ---------------------------
tracer_provider = register(
    protocol="http/protobuf",
    project_name="Wine Rag 0722 730pm",
)

# The tracer object everyone will import
tracer = tracer_provider.get_tracer(__name__)
