---
name: agent-self-development
description: "Agent self-development plugin based on Piaget's cognitive development theory: metacognition, working memory, and assimilation/accommodation"
metadata:
  {
    "openclaw":
      {
        "events": ["before_prompt_build", "llm_output", "agent_end", "before_tool_call", "after_tool_call", "gateway_start", "gateway_stop"],
      },
  }
---

# Agent Self-Development Hook

## What it does

This plugin provides three core modules for agent self-development:

1. **Metacognition**: Planning, monitoring, and regulation of agent execution.
   - Generates execution plans and injects them into system context.
   - Monitors LLM output for deviation from the plan.
   - Triggers revision when significant deviation is detected.

2. **Working Memory**: Tracks subagent/agent session lifecycle and archives completed sessions.
   - Records subagent spawn and completion events.
   - Maintains a session list per run.
   - Archives completed sessions to daily memory tables.

3. **Assimilation & Accommodation**: Daily self-reflection and identity update service.
   - Runs a scheduled daily update (default: 00:00 Asia/Shanghai).
   - Generates a diary from yesterday's events via LLM.
   - Analyzes assimilation/accommodation signals and applies updates.

## Events

### `before_prompt_build`

Generates an execution plan for the current run (if not already present) and
injects it into `prependSystemContext`. Also infers session assignments for
multi-step tasks.

### `llm_output`

Monitors the LLM output against the current plan. Detects errors, blocked
states, or off-track behavior and stores deviation signals.

### `agent_end`

Cleans up run-scoped plan and deviation state. Archives completed sessions
from working memory.

### `before_tool_call`

For `agent` and `subagent` tool calls, records the spawn event into working
memory and initializes session tracking.

### `after_tool_call`

Records tool errors to the daily event log. For `agent`/`subagent` tools,
updates session status (`completed` or `killed`) in working memory.

### `gateway_start`

Starts the daily assimilation cron job or fallback timer when the gateway
starts.

### `gateway_stop`

Stops the daily assimilation cron job or fallback timer when the gateway
stops.

## Configuration

All settings live under `plugins.entries["agent-self-development"]` in `openclaw.json`.
See `openclaw.plugin.json` for the full config schema and defaults.

## Required Permissions

- `plugins.entries.agent-self-development.hooks.allowConversationAccess = true`
  (required for plan injection and deviation detection)