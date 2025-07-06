# Hedra CLI

A command-line interface for the Hedra API to create digital avatars and talking heads.

## Features

- **Character Generation**: Create digital avatars from images and audio
- **Smart Face Selection**: AI-powered face detection for multi-person images
- **Voice Management**: List and preview voices (from API or local files)
- **Project Management**: List, view, and download your Hedra projects
- **Interactive Mode**: Step-by-step guided workflow
- **Bounding Box Targeting**: Precise lip-sync control for specific faces

## Prerequisites

- **Python 3.8+**
- **uv**: A fast Python package installer and resolver. If you don't have it, install it following the instructions at [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv).
- Ensure you are on paid plan of creator or above at hedra.com/plans
- **Hedra API Key**: navigate to https://hedra.com/api-profile and accept our terms of service. For volume discounts or use in production reach out to sales@hedra.com
- `opencv-python` library (optional, for face selection): `pip install opencv-python`
- Audio player (optional): ffplay, mpg123, or mplayer (for voice preview)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/hedra-labs/hedra-cli.git
   cd hedra-cli
   ```

2. Set up your API Key:
   The script requires your Hedra API key. You can provide it in one of two ways:
   - **Environment Variable:** Set the `HEDRA_API_KEY` environment variable in your shell:
     ```bash
     export HEDRA_API_KEY='your_actual_api_key'
     ```
   - **.env File:** Create a file named `.env` in the project's root directory and add the following line:
     ```
     HEDRA_API_KEY=your_actual_api_key
     ```
     *(Note: The `.env` file is included in `.gitignore` to prevent accidentally committing your API key.)*

3. Install Dependencies:
   Use `uv` to install the required Python packages listed in `pyproject.toml`:
   ```bash
   uv sync
   ```
   *(This command creates a virtual environment if one doesn't exist and installs/syncs the dependencies.)*

4. Make the script executable (for CLI tool):
   ```bash
   chmod +x hedra
   ```

5. Configure your API key (for CLI tool):
   ```bash
   ./hedra config --api-key YOUR_API_KEY
   ```

## Usage

### Character Generation

Generate a talking avatar with text-to-speech:
```bash
<<<<<<< HEAD
./hedra generate --text "Hello world!" --img portrait.jpg --voice-id <voice_id>
```

Generate with an uploaded audio file:
```bash
./hedra generate --audio-file audio.wav --img portrait.jpg
```

Generate a character with an AI-created image:
```bash
./hedra generate --text "Hello world" --voice-id <voice_id> --img-prompt "A professional woman with glasses"
```

### Smart Face Selection (Multi-Person Images)

For images with multiple people, you can precisely select which face should have lip-sync:

**Interactive Selection** (shows ASCII layout):
```bash
./hedra generate --text "Hello!" --img group_photo.jpg --select-face
```

**Auto-Select Best Face**:
```bash
./hedra generate --text "Hello!" --img photo.jpg --auto-face
```

**Preview Faces Only**:
```bash
./hedra generate --preview-faces --img news_panel.jpg
```

**Manual Coordinates** (fallback):
```bash
./hedra generate --text "Hello!" --img photo.jpg --bounding-box "0.3,0.4"
```

#### Example: News Panel Selection
```
🔍 Detected 2 face(s)
🎭 DETECTED FACES
┌────────────────────────┐
│                        │
│    ███        ███      │
│    ███        ███      │
│                        │
└────────────────────────┘

[1] Left person     (0.243, 0.277)
[2] Right person    (0.753, 0.323)
[q] Cancel

Choose face (1-2): 1
✅ Selected Face 1
📍 Coordinates: (0.243, 0.277)
```

### Voice Management

List available voices:
```bash
./hedra voice list
```

Preview a voice by ID or name:
```bash
./hedra voice preview <voice_id_or_name>
```

### Project Management

List your recent generations:
```bash
./hedra project list
```

Get generation details:
```bash
./hedra project get <generation_id>
```

Download a generation's output:
```bash
./hedra project download <generation_id> --output my_video.mp4
```

### Interactive Mode

For a guided experience:
```bash
./hedra interactive
```

## Using Local Voice Files

The client can use voice files in the `assets` folder for previews:

1. Put your voice samples in the `assets` directory (e.g., `assets/Laura.mp3`)
2. When listing voices, those with matching local files will be marked with ✓ in the LOCAL column
3. Use `hedra voice preview Laura` to play the local file directly

You can set a custom assets directory:
```bash
./hedra config --assets-dir /path/to/your/voices
```

## Examples with Sample Assets

The repository includes sample assets that can be used:

```bash
# Generate with 16:9 aspect ratio
./hedra generate --audio-file assets/audio.wav --img assets/16_9.jpg --aspect-ratio 16:9

# Generate with 9:16 aspect ratio
./hedra generate --audio-file assets/audio.wav --img assets/9_16.jpg --aspect-ratio 9:16

# Preview a voice from the assets folder
./hedra voice preview Alice

# Test face detection on sample images
./hedra generate --preview-faces --img assets/16_9.jpg
```

## Complete Examples

### Single Person Video
```bash
./hedra generate \
  --text "Welcome to our presentation!" \
  --img portrait.jpg \
  --voice-id "voice-123" \
  --aspect-ratio 16:9 \
  --output welcome_video.mp4
```

### Multi-Person Selection (News Panel)
```bash
./hedra generate \
  --text "Good evening, I'm your host" \
  --img news_panel.jpg \
  --select-face \
  --voice-id "host-voice" \
  --aspect-ratio 16:9 \
  --output news_intro.mp4
```

### Auto-Generated Character
```bash
./hedra generate \
  --text "Hello from the future!" \
  --img-prompt "A friendly robot with blue eyes" \
  --voice-id "robotic-voice" \
  --animation-prompt "slight head movements, blinking" \
  --seed 42 \
  --output robot_greeting.mp4
```

## Advanced Options

### Aspect Ratio

Specify the aspect ratio of the output video:
```bash
./hedra generate --text "Hello" --voice-id <voice_id> --img <path> --aspect-ratio 16:9
```

### Seed for Reproducibility

Set a seed for reproducible image generation:
```bash
./hedra generate --text "Hello" --voice-id <voice_id> --img-prompt "A teacher" --seed 42
```

### Animation Prompt

Add instructions for the animation style:
```bash
./hedra generate --text "Hello" --voice-id <voice_id> --img <path> --animation-prompt "nodding and smiling"
```

### Custom Output Path

Specify where to save the generated video:
```bash
./hedra generate --text "Hello" --voice-id <voice_id> --img <path> --output my_video.mp4
```

### Advanced Video Options

**Aspect Ratio**:
```bash
./hedra generate --text "Hello" --voice-id <voice_id> --img <path> --aspect-ratio 16:9
```

**Video Duration**:
```bash
./hedra generate --audio-file speech.mp3 --img <path> --duration-ms 10000
```

**Resolution**:
```bash
./hedra generate --text "Hello" --voice-id <voice_id> --img <path> --resolution 1440p
```

**AI Model Selection**:
```bash
./hedra generate --text "Hello" --voice-id <voice_id> --img <path> --ai-model-id "d1dd37a3-e39a-4854-a298-6510289f9cf2"
```

## Limitations

- The Hedra API supports generating videos up to 4 minutes in length
- Supported aspect ratios: 1:1, 16:9, 9:16
- Image files should be in JPG or PNG format
- Audio files should be in WAV or MP3 format
- Face detection works best with clear, front-facing faces
- OpenCV required for automatic face selection features

## Troubleshooting

### Face Detection Issues

**No faces detected:**
- Ensure good lighting and clear face visibility
- Try different images with more direct face angles
- Use manual `--bounding-box` coordinates as fallback

**Too many false faces detected:**
- The system automatically filters overlapping detections
- Use `--preview-faces` to verify detection quality
- Consider using `--auto-face` for automatic best selection

**OpenCV not available:**
```bash
pip install opencv-python
```

### API Issues

**Authentication errors:**
```bash
./hedra config --api-key YOUR_NEW_API_KEY
```

**Network timeouts:**
- Check internet connection
- Try with smaller image files
- Increase `--max-retries` if needed

## Configuration

All settings are stored in `~/.hedra.conf`:

```
api_key=your_api_key
base_url=https://api.hedra.com/web-app
default_output_dir=outputs
assets_dir=/path/to/assets
default_ai_model_id=d1dd37a3-e39a-4854-a298-6510289f9cf2
```

## Face Selection Requirements

For the face selection features, you need OpenCV:

```bash
pip install opencv-python
```

If OpenCV is not available, the tool will gracefully fall back to manual coordinate entry:
```bash
./hedra generate --text "Hello" --img photo.jpg --bounding-box "0.5,0.4"
```

### Common Face Selection Scenarios

- **News Panels**: Select left host or right guest
- **Group Photos**: Choose the main speaker
- **Interviews**: Pick interviewer or interviewee
- **Family Photos**: Target specific person for animation

### Face Selection Tips

- **Good lighting** improves detection accuracy
- **Front-facing angles** work best
- **Clear, unobstructed faces** are easier to detect
- **Higher resolution images** provide better results

### Using the Python API Script

You can also use the Python API script directly:

```bash
uv run main.py \
    --aspect_ratio <ratio> \
    --resolution <res> \
    --text_prompt "<your_prompt>" \
    --audio_file <path/to/audio.mp3> \
    --image <path/to/image.png>
```

**Command-Line Arguments:**

*   `--aspect_ratio` (Required): Aspect ratio for the video. Choices: `16:9`, `9:16`, `1:1`.
*   `--resolution` (Required): Resolution for the video. Choices: `540p`, `720p`.
*   `--text_prompt` (Required): Text prompt describing the desired video content (enclose in quotes if it contains spaces).
*   `--audio_file` (Required): Path to the input audio file (e.g., `.mp3`, `.wav`).
*   `--image` (Required): Path to the input image file (e.g., `.png`, `.jpg`).
*   `--duration` (Optional): Desired duration for the video in seconds (float). Defaults to the length of the audio if not specified.
*   `--seed` (Optional): Seed for the generation process (integer). Allows for reproducible results if the model and other parameters are the same.

**Example:**

```bash
uv run main.py \
    --aspect_ratio 9:16 \
    --resolution 540p \
    --text_prompt "A woman talking at the camera" \
    --audio_file assets/audio.wav \
    --image assets/9_16.jpg
```

The script will:
1.  Upload the image and audio assets.
2.  Submit the generation request to the Hedra API.
3.  Poll the API for the status of the generation job.
4.  Once complete, download the generated video file (e.g., `asset_id.mp4`) to the project directory.

Check the console output for progress and the final video file location.
