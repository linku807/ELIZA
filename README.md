# Project ELIZA

An AI agent that manages Discord servers using Google's Gemini and Discord Function Calling.

> ⚠️ This project is currently under active development. and developed by junior developer

## Features

- AI-powered Discord server management
- Native Gemini Function Calling
- Discord moderation tools
  - Read messages
  - Delete messages
  - Send messages
  - User lookup
  - Channel lookup
  - Timeout users
- Per-server AI configuration
- Custom Gemini API Key support

## Tech Stack

- Python
- discord.py
- Google GenAI SDK (Gemini)

## Goal

Unlike traditional Discord bots that rely on predefined commands,
Project ELIZA aims to act as an autonomous AI administrator capable of
understanding natural language and performing moderation tasks through
tool calling.

## Current Status

Current MVP supports:

- Function Calling
- Discord moderation tools
- Guild-based contexts
- AI memory (basic)
- Custom ID encoding (Hangul512)

## Roadmap

- [x] Basic Discord tools
- [x] Function Calling
- [x] Guild Context
- [ ] SQLite database
- [ ] Approval workflow
- [ ] Long-term memory
- [ ] Better moderation policies

## License
gpl 3.0 license