# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python CLI tool for the Hedra API, which creates digital avatars and talking heads from images and audio. The main executable is `hedra`, a Python script that provides a command-line interface for generating AI-powered video content.

## Key Architecture

### Core Components

- **Main Entry Point**: `hedra` - A Python 3 script that serves as the CLI interface
- **Configuration**: Uses `~/.hedra.conf` for storing API keys and settings
- **Asset Management**: Local assets stored in `assets/` directory for voice previews
- **API Integration**: Communicates with Hedra API at `https://mercury.dev.dream-ai.com/api`

### Key Functions

- `generate_avatar_payload()` - Creates the complete payload for avatar generation
- `wait_for_completion()` - Polls API for job completion with progress tracking
- `interactive_mode()` - Provides guided workflow for users
- `api_request()` - Handles all API communication with error handling

## Development Commands

### Prerequisites
- Python 3.6+
- `requests` library: `pip install requests`
- Audio player (optional): ffplay, mpg123, or mplayer

### Running the Tool
```bash
# Make executable
chmod +x hedra

# Configure API key
./hedra config --api-key YOUR_API_KEY

# Run interactive mode
./hedra interactive

# Generate avatar
./hedra generate --text "Hello world!" --img portrait.jpg --voice-id <voice_id>
```

### Testing
No formal test suite is present. Test by running commands:
```bash
# Test voice listing
./hedra voice list

# Test project listing
./hedra project list

# Test interactive mode
./hedra interactive
```

## API Structure

The tool interfaces with the Hedra API using these main endpoints:
- `/public/assets` - Asset management (voices, images, audio)
- `/public/assets/{id}/upload` - File upload
- `/public/generations` - Generation management (video, audio, image)
- `/public/generations/{id}/status` - Generation status polling
- `/public/billing/credits` - Credit balance checking

## Configuration

Settings are stored in `~/.hedra.conf`:
- `api_key` - Hedra API key
- `base_url` - API base URL (default: https://api.hedra.com/web-app)
- `default_output_dir` - Where generated videos are saved (default: outputs)
- `assets_dir` - Local voice files directory (default: assets)
- `default_ai_model_id` - Default AI model for generations (default: d1dd37a3-e39a-4854-a298-6510289f9cf2)

## Common Workflows

### Character Generation
1. Image source: Upload file OR generate from text prompt
2. Voice selection: Choose from API voices or use local files
3. Audio source: Text-to-speech OR upload audio file
4. Configuration: Set aspect ratio, seed, animation prompts
5. Generation: Submit to API and poll for completion

### Voice Management
- List available voices with `voice list`
- Preview voices with `voice preview <name>`
- Use local voice files from `assets/` directory

### Project Management
- List recent generations with `project list`
- Download completed generations with `project download <id>`
- Get generation details with `project get <id>`
- Note: Sharing and deletion are not supported in the new API

## Error Handling

The tool includes comprehensive error handling:
- 401: Authentication failed
- 404: Resource not found
- 422: Validation error
- 504: Gateway timeout
- Network errors and API failures are handled gracefully

## File Structure

- `hedra` - Main CLI script
- `assets/` - Local voice files for previews
- `openapi.json` - API specification
- `README.md` - User documentation

## Development Notes

- The tool uses polling for generation completion with progress bars
- Audio playback is cross-platform (macOS, Linux, Windows)
- Local voice files are matched case-insensitively
- All file paths should be absolute when possible
- The tool creates output directories automatically
- Uses new asset-based upload system (create asset, then upload file)
- Supports bounding box targeting for Character3 model
- TTS and image generation happen as separate steps before video generation