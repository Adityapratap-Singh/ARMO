# ARMO Runtime Architecture

This document defines the runtime architecture of ARMO.

Goals:
- Separate orchestration logic from model execution.
- Keep switching policy independent of executors.
- Support multiple execution backends (Ollama, OpenAI, Anthropic).
- Make topologies interchangeable.
- Maintain a single runtime state shared across all components.