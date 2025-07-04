# Hedra CLI Enhancement Plan

## Project Overview

**Goal**: Enhance the Hedra CLI with intelligent face detection and bounding box selection for precise lip-sync targeting in multi-person scenarios.

**Core Problem**: When generating talking head videos with multiple people in frame, users need to specify which person should have lip-sync animation applied. The current manual coordinate entry is cumbersome and error-prone.

## Current State Analysis

### ✅ Completed Updates
- [x] Migrated to new Hedra API endpoints (`/public/generations`)
- [x] Updated asset upload system (create → upload pattern)
- [x] Added bounding box parameter support (`bounding_box_target`)
- [x] Updated CLI arguments for new features
- [x] Fixed voice management for new API structure
- [x] Updated documentation (CLAUDE.md)

### 🎯 Target Enhancement
**Smart Face Selection System** with simplified, intuitive interface

## Implementation Strategy

### Phase 1: Core Face Detection (Priority: HIGH)

**Technical Approach:**
- Use OpenCV's built-in Haar cascade classifiers
- Face quality scoring based on:
  - Size (larger faces = better for lip-sync)
  - Clarity (Laplacian variance for sharpness)
  - Position (centered faces often better)
  - Feature detection (eyes, mouth visibility)

**Dependencies:**
```bash
pip install opencv-python
```

### Phase 2: Simplified UI Design (Priority: HIGH)

**Design Principles:**
- ✅ **ASCII Art Visualization** - Clear spatial representation
- ✅ **Simple Number Selection** - Just 1, 2, 3... for faces
- ✅ **Coordinate Display** - Show coords for reference/manual fallback
- ✅ **Interactive Mode** - Visual OpenCV interface as backup
- ❌ **Complex Shortcuts** - Remove confusing position/role shortcuts

**Example Interface:**
```
🎭 DETECTED FACES
┌────────────────────┐
│                    │
│  ████         ████ │
│  █1█           █2█ │  
│  ████         ████ │
│                    │
└────────────────────┘

[1] Left person    (0.283, 0.445)
[2] Right person   (0.721, 0.412)
[i] Visual mode
[q] Cancel

Choice: _
```

### Phase 3: Integration Points

**New CLI Arguments:**
```bash
# Simple face selection
./hedra generate --text "Hello" --img photo.jpg --select-face

# Quick best face (single face scenarios)
./hedra generate --text "Hello" --img photo.jpg --auto-face

# Preview faces without generating
./hedra generate --preview-faces --img photo.jpg
```

**Integration Flow:**
1. User provides image with `--select-face`
2. System detects faces and shows ASCII layout
3. User selects by number (1, 2, 3...)
4. System converts to bounding box coordinates
5. Generation proceeds with selected face

### Phase 4: User Experience Flows

**Single Face Scenario:**
```
🔍 Analyzing faces...
✅ One face detected - using automatically
📍 Coordinates: (0.5, 0.4)
🚀 Starting generation...
```

**Multi-Face Scenario:**
```
🔍 Analyzing faces...
🎭 Multiple faces detected

┌────────────────────┐
│ ████         ████  │
│ █1█           █2█  │  
│ ████         ████  │
└────────────────────┘

[1] Person on left   (0.3, 0.4)
[2] Person on right  (0.7, 0.4)
[i] Visual selection
[q] Cancel

Choose face (1-2): 1
✅ Selected Face 1
📍 Coordinates: (0.3, 0.4)
🚀 Starting generation...
```

**No Faces Detected:**
```
🔍 Analyzing faces...
❌ No faces detected
💡 Try: Better lighting, face closer to camera, frontal angle
🔧 Fallback: Use manual --bounding-box x,y coordinates
```

## Technical Implementation Details

### File Structure
```
hedra-cli/
├── hedra                    # Main CLI script (updated)
├── face_selector.py         # New face detection module
├── CLAUDE.md               # Updated documentation
├── plan.md                 # This file
└── assets/                 # Sample assets
```

### Core Functions
```python
class SimpleFaceSelector:
    def detect_faces()           # OpenCV face detection
    def create_ascii_layout()    # ASCII art generation
    def interactive_selection()  # Simple numbered selection
    def visual_selection()       # OpenCV GUI fallback
    def get_coordinates()        # Convert selection to coords
```

### Error Handling
- Graceful fallback when OpenCV not available
- Clear error messages for detection failures
- Manual coordinate entry as ultimate fallback

## Success Metrics

### User Experience Goals
- ⏱️ **Speed**: Face selection in <10 seconds
- 🎯 **Accuracy**: Users select correct face >95% of time
- 📚 **Learnability**: New users understand interface immediately
- 🔧 **Reliability**: Works with various image qualities/lighting

### Technical Goals
- 🖼️ **Detection Rate**: Detect faces in >90% of suitable images
- ⚡ **Performance**: Process images in <2 seconds
- 🔗 **Integration**: Seamless with existing CLI workflow
- 📱 **Compatibility**: Work on Linux, macOS, Windows

## Risk Mitigation

### Technical Risks
- **OpenCV dependency**: Provide pip install instructions, graceful fallback
- **Detection failures**: Clear guidance for manual coordinate entry
- **Performance**: Optimize for common image sizes, add timeout handling

### UX Risks
- **Over-complexity**: Keep interface minimal - just numbers and ASCII
- **Confusion**: Provide clear examples in help text
- **Abandonment**: Always offer manual coordinate fallback

## Implementation Timeline

### Week 1: Core Detection
- [ ] Implement SimpleFaceSelector class
- [ ] ASCII art layout generation
- [ ] Basic face detection and scoring

### Week 2: CLI Integration
- [ ] Add new command-line arguments
- [ ] Integrate with existing generate command
- [ ] Error handling and fallbacks

### Week 3: Polish & Testing
- [ ] Test with various image types
- [ ] Refine ASCII art output
- [ ] Documentation updates
- [ ] Real-world scenario testing

## Future Enhancements (Post-MVP)

### Advanced Features (Lower Priority)
- **Face Recognition**: Remember previously selected people
- **Quality Hints**: Suggest image improvements for better detection
- **Batch Processing**: Apply same face selection to multiple images
- **Configuration**: Save preferred face selection strategies

### Integration Opportunities
- **Web Interface**: Simple drag-and-drop face selection
- **Mobile App**: Camera-based face selection
- **API Endpoint**: Expose face detection as separate service

---

## Notes from Development

### Key Design Decisions
1. **Simplicity Over Features**: Chose numbered selection over complex position shortcuts
2. **ASCII Art**: Provides clear spatial context without GUI dependency
3. **Graceful Degradation**: Multiple fallback options (visual → manual → coordinates)
4. **Single Responsibility**: Face selection as focused, separate concern

### User Feedback Incorporated
- ✅ ASCII art for spatial visualization
- ✅ Simple number-based selection
- ✅ Coordinate display for reference
- ✅ Interactive visual mode as backup
- ❌ Removed complex role-based shortcuts (host/guest/etc.)
- ❌ Removed overwhelming position options

This plan provides a clear roadmap for implementing intelligent, user-friendly face selection while maintaining the CLI's simplicity and reliability.