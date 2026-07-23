# Free Claude Code

**Local proxy** that connects Claude Code, OpenCode, and Codex CLI to any compatible AI provider — from cloud APIs (NVIDIA NIM, OpenRouter, GitHub Models, AWS Bedrock) to local servers (LM Studio, Ollama, llama.cpp).

## Features

- **25+ providers** — NVIDIA NIM, OpenRouter, LM Studio, Ollama, llama.cpp, GitHub Models, AWS Bedrock, Google Vertex, Groq, DeepSeek, and more.
- **Key pool** — assign multiple API keys per provider; the proxy cycles keys with automatic rate-limit and concurrency management.
- **Image / vision** — images are forwarded to vision-capable models; non-vision models receive a graceful refusal ("This model can't read images — send the content as text"), never a broken proxy.
- **Streaming, tool use, reasoning** — fully preserved through the proxy.
- **Admin UI** — local web interface at `http://127.0.0.1:<port>/admin` for provider configuration, credential validation, and model browsing.
- **Discord & Telegram bots** — run coding agents through messaging platforms.
- **Claude Code model picker** — preserved end-to-end.

## Quick Start

```bash
# Install
curl -fsSL https://raw.githubusercontent.com/King-Jboy/josiah-claude-code/main/scripts/install.sh | sh

# Set your first provider key and start the server
export NVIDIA_NIM_API_KEY=nvapi-...
fcc-server
```

Open `http://127.0.0.1:8082/admin` (the port is printed at startup) to configure additional providers, set model mappings, and manage messaging integrations.

## Choose A Provider

Configure a supported provider:

| Provider | Type | How to configure | Example model ref |
|---|---|---|---|
| [NVIDIA NIM](https://build.nvidia.com/settings/api-keys) | cloud, vision | `NVIDIA_NIM_API_KEY` | `nvidia_nim/meta/llama-3.1-8b-instruct` |
| [OpenRouter](https://openrouter.ai/keys) | cloud, vision, reasoning | `OPENROUTER_API_KEY` | `open_router/meta-llama/llama-3.1-8b-instruct` |
| [AWS Bedrock](https://aws.amazon.com/bedrock/) | cloud | `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` | `bedrock/anthropic.claude-v2` |
| [Google Vertex](https://cloud.google.com/vertex-ai) | cloud | `GOOGLE_APPLICATION_CREDENTIALS` | `vertex/claude-3-sonnet` |
| [GitHub Models](https://github.com/marketplace/models) | cloud | `GITHUB_TOKEN` | `github_models/gpt-4o` |
| [Groq](https://groq.com) | cloud | `GROQ_API_KEY` | `groq/llama3-8b-8192` |
| [DeepSeek](https://platform.deepseek.com/api_keys) | cloud | `DEEPSEEK_API_KEY` | `deepseek/deepseek-chat` |
| [Mistral](https://console.mistral.ai) | cloud | `MISTRAL_API_KEY` | `mistral/mistral-small-latest` |
| [Mistral Codestral](https://console.mistral.ai) | cloud | `MISTRAL_API_KEY` | `mistral_codestral/codestral-latest` |
| [Cohere](https://dashboard.cohere.com/api-keys) | cloud | `COHERE_API_KEY` | `cohere/command-r-plus` |
| [Fireworks](https://fireworks.ai) | cloud | `FIREWORKS_API_KEY` | `fireworks/accounts/fireworks/models/llama-v3p1-8b` |
| [Gemini](https://aistudio.google.com/apikey) | cloud, vision | `GEMINI_API_KEY` | `gemini/gemini-2.0-flash-exp` |
| [Cerebras](https://cloud.cerebras.ai) | cloud | `CEREBRAS_API_KEY` | `cerebras/llama3.1-8b` |
| [Cloudflare](https://cloudflare.com) | cloud | `CLOUDFLARE_API_KEY` | `cloudflare/@cf/meta/llama-3.1-8b-instruct` |
| [SambaNova](https://sambanova.ai) | cloud | `SAMBANOVA_API_KEY` | `sambanova/Meta-Llama-3.1-8B-Instruct` |
| [Hugging Face](https://huggingface.co/inference-api) | cloud | `HUGGINGFACE_API_KEY` | `huggingface/meta-llama/Meta-Llama-3.1-8B-Instruct` |
| [Vercel](https://vercel.com) | cloud | `VERCEL_API_KEY` | `vercel/meta-llama/Meta-Llama-3.1-8B-Instruct` |
| [Kimi](https://kimi.moonshot.cn) | cloud | `KIMI_API_KEY` | `kimi/kimi-v1` |
| [Kimi Code](https://kimi.moonshot.cn) | cloud | `KIMI_API_KEY` | `kimi_code/kimi-v1` |
| [ZAI](https://zai.ai) | cloud | `ZAI_API_KEY` | `zai/gpt-4o-mini` |
| [MiniMax](https://minimax.io) | cloud | `MINIMAX_API_KEY` | `minimax/MiniMax-Text-01` |
| [LM Studio](https://lmstudio.ai) | local | `http://127.0.0.1:1234/v1` | `lmstudio/local-model` |
| [Ollama](https://ollama.com) | local | `http://127.0.0.1:11434/v1` | `ollama/llama3.2` |
| [Ollama Cloud](https://ollama.com) | cloud | `OLLAMA_API_KEY` | `ollama_cloud/llama3.2` |
| [llama.cpp](https://github.com/ggerganov/llama.cpp) | local | `http://127.0.0.1:8080/v1` | `llamacpp/local-model` |
| [OpenCode](https://opencode.ai) | cloud | `OPENCODE_API_KEY` | `opencode/gpt-4o` |
| [OpenCode Go](https://opencode.ai) | cloud | `OPENCODE_API_KEY` | `opencode_go/gpt-4o` |
| [Wafer](https://wafer.ai) | cloud | `WAFER_API_KEY` | `wafer/llama-3.1-8b` |

Provider-specific configuration (model aliases, reasoning defaults, tool schemas) is done through the Admin UI.

## Key Pool

Assign multiple API keys to a provider so the proxy can rotate through them, respecting per-key rate limits and concurrency caps.

The simplest way is to set a JSON array of keys via the provider's `*_API_KEYS` environment variable:

```bash
export NVIDIA_NIM_API_KEYS='["nvapi-key1","nvapi-key2","nvapi-key3"]'
fcc-server
```

For multi-provider pools or keys with limits, use the `--key-pool` flag:

```bash
fcc-server --key-pool 'nvidia_nim:key1@ratelimit:10@concurrency:3,openrouter:key2@concurrency:5'
```

When a key reaches its rate limit or concurrency cap, the pool transparently switches to the next available key. If all keys are exhausted, the request is queued until a slot opens.

Enabling a key pool also enables HTTP/2 multiplexing — concurrent requests to the same upstream host share one TCP+TLS connection instead of opening new ones per request. (Without a key pool or SOCKS proxy, HTTP/2 is not used.)

A per-key rate limit can be set via:

```bash
export NVIDIA_NIM_RPM_PER_KEY=40
```

## Image / Vision Support

When Claude Code, OpenCode, or Codex sends an image through the proxy, the behaviour depends on the target model:

- **Vision-capable models** — the image is forwarded as-is. The model receives the image and can reason about it.
- **Non-vision models** — the proxy refuses proactively (OpenRouter advertises text-only *modality*) or catches the upstream rejection and returns a friendly assistant message instead of breaking:

  > "I can't read images — *model* doesn't support image input. Please send the content of the image as text instead."

  The proxy never errors out — it always replies gracefully and ends the turn, waiting for the user to send text.

No configuration is needed. Vision capability is detected from provider model metadata (OpenRouter exposes input/output *modality*; other providers use a model-name heuristic).

## Admin UI

The Admin UI is served at `/admin` — loopback-only (accessible only from the machine running the proxy). It lets you:

- View and configure providers (API keys, base URLs, rate limits)
- Browse the model catalog (with thinking and vision capability annotations)
- Configure model config defaults, messaging integrations
- Validate credentials and apply changes

## Clients

Point your clients to the proxy:

- **Claude Code**: `CLAUDE_CODE_PROXY=http://127.0.0.1:PORT claude`
- **OpenCode**: `OPENCODE_ENDPOINT=http://127.0.0.1:PORT fcc-opencode`
- **Codex CLI**: `CODEX_CLI_ENDPOINT=http://127.0.0.1:PORT codex`

The proxy also ships launcher wrappers (`fcc-claude`, `fcc-opencode`) that handle the env vars automatically.

## Messaging Integrations

The proxy can run as a Discord bot or a Telegram bot. Inbound messages are forwarded to the configured AI model, and the model's response is rendered back to the chat (including tool calls, reasoning, and thinking blocks).

Configure messaging through the Admin UI or via environment variables (`TELEGRAM_BOT_TOKEN`, `DISCORD_BOT_TOKEN`).

## Uninstall

```bash
curl -fsSL "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/uninstall.sh" | sh
```

PowerShell:

```powershell
& ([scriptblock]::Create((irm "https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/scripts/uninstall.ps1")))
```

The uninstaller removes FCC binaries, clears the key chain entry, and verifies every FCC command is gone.

## Architecture

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the proxy pipeline, provider adapter system, request lifecycle, and deployment topology.
