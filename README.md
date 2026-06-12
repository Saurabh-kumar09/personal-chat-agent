## Personal Chat Agent 
Personal Chat Agent is an experimental AI chatbot project built to integrate large language model capabilities with Telegram and spreadsheet workflows.
It is designed as a modular Python application that connects Gemini LLM prompts, session-aware chat state, and Google Sheets logging through a Telegram bot interface.

Phase - Early development with integration focus

### Features:
- Conversational AI chat with intelligent responses
- Save useful links, ideas, and notes directly to a spreadsheet
- Summarize web pages quickly
- Short-term memory for maintaining context within a chat session
- Lightweight session state tracking for smoother follow-up replies

### Technical details:
- Python-based architecture with separate modules for bot logic, chat engine, helpers, and integrations
- Gemini LLM prompt management for adaptive conversational behavior
- Google Sheets integration for capturing user notes and links
- Telegram bot interface for chat interactions and command handling
- Session-aware caching to preserve context across conversational turns
- Config-driven external service setup via `integrations/` and `prompts/`
