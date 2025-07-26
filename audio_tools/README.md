# Audio Tools & Sound Generation

Tools for generating audio files for games and simulations. This folder contains the sound generation scripts - the actual audio files are stored with the projects that use them.

## Files
- `generate_sounds.py` - Script for generating various game sound effects

## How to Use
```bash
cd audio_tools
python generate_sounds.py
```

This will generate:
- `shoot.wav` - Shooting sound effect
- `explosion.wav` - Explosion sound effect  
- `refuel.wav` - Refueling sound effect

**Note:** The generated audio files will be created in the current directory. You may need to move them to the appropriate project folders that use them.

## Requirements
- pygame (for sound generation)
- numpy (for waveform manipulation)

Install with: `pip install pygame numpy`

## Usage in Projects
The generated sounds are used by:
- **River Raid Game** - Uses all three sound effects for gameplay audio 