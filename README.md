# Meteor Dodge Repair Lab

Meteor Dodge is a Python/Pygame space-survival game. Pilot the ship, dodge meteors, and use lasers and shield power-ups to survive.

## Setup

Requires Python 3.10 or newer.

```bash
python -m pip install -r requirements.txt
python main.py
```

On Windows, `py -m pip install -r requirements.txt` and `py main.py` are alternatives if the `python` command is unavailable.

## Controls

| Key | Action |
|---|---|
| SPACE (title screen) | Start the game |
| SPACE (during gameplay) | Fire a defensive laser |
| W/A/S/D or Arrow Keys | Move the ship |
| SPACE (Game Over screen) | Restart |

## Implemented features

- **Laser firing:** SPACE fires a projectile during active gameplay. Lasers destroy meteors.
- **Meteor splitting:** Destroying a large meteor creates two smaller fragments that diverge outward. Small meteors disappear when destroyed.
- **Shield power-ups:** Drifting cyan energy orbs can be collected. Each collected orb absorbs one meteor collision.
- **Survival multiplier:** The score multiplier increases every 10 seconds of continuous survival. Taking a hit that consumes a shield resets the streak and multiplier.
- **Existing gameplay:** Starfield, ship trail, moving/rotating meteors, collision detection, increasing spawn difficulty, survival timer, and restart screen.

## Testing checklist

- [ ] SPACE starts the game from the title screen.
- [ ] SPACE fires lasers during gameplay.
- [ ] Lasers destroy meteors; large meteors split into smaller fragments.
- [ ] Collecting a shield orb displays the shield and grants one-hit protection.
- [ ] The multiplier increases after each 10-second uninterrupted survival interval.
- [ ] Without a shield, a meteor collision ends the run.
- [ ] SPACE restarts after Game Over.

## Lab submission

Follow your instructor's Lab 4 handout. Record the original 10-second gameplay video before modifying the starter code, and record a second 10-second video after testing all features. Push the completed code to your own repository (not the SETAPESU26 repository), use separate commits for each task, and upload the required videos, code, and exported chat history to your Lab-4 folder.
