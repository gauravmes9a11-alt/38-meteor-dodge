# ☄️ Meteor Dodge

A fast-paced space-survival arcade game built with **Python** and **Pygame**. Pilot your ship through an endless meteor field, blast rocks apart with lasers, grab shield orbs, and see how long you can last while your score multiplier climbs.

| Before | After |
|---|---|
| [`Before.mp4`](Before.mp4) – original starter gameplay | [`After.mp4`](After.mp4) – gameplay with all new features |

---

## Features

- **Laser firing** – Press `SPACE` in flight to fire a defensive laser. Lasers destroy meteors on contact.
- **Meteor splitting** – Large meteors (radius ≥ 20) break into two smaller fragments that fly apart. Small meteors are simply destroyed.
- **Shield power-ups** – Cyan energy orbs drift down the screen roughly every 9 seconds. Each orb you collect absorbs one meteor collision, and charges stack.
- **Survival multiplier** – Your score multiplier goes up by 1 for every 10 seconds of uninterrupted survival. Using a shield to absorb a hit resets the streak and multiplier.
- **Escalating difficulty** – Meteors spawn faster over time (down to a minimum spawn interval).
- **Polish** – Parallax-style starfield, fading ship trail, rotating irregular meteors, a shield ring around the ship, and a Game Over / restart screen.

## Getting Started

### Requirements

- Python 3.10 or newer
- [Pygame](https://www.pygame.org/) 2.5.2 (pinned in `requirements.txt`)

### Install and run

```bash
git clone https://github.com/gauravmes9a11-alt/38-meteor-dodge.git
cd 38-meteor-dodge

python -m pip install -r requirements.txt
python main.py
```

On Windows, use `py -m pip install -r requirements.txt` and `py main.py` if the `python` command isn't available.

> **Note:** If `pygame==2.5.2` fails to install on a very recent Python version, install a newer Pygame release instead (`pip install pygame`).

## Controls

| Key | Action |
|---|---|
| `SPACE` (title screen) | Start the game |
| `SPACE` (during gameplay) | Fire a laser |
| `W` `A` `S` `D` / Arrow keys | Move the ship |
| `SPACE` (Game Over screen) | Restart |

## How It Plays

1. Survive as long as possible. Your score increases every frame by your current multiplier.
2. Shoot meteors before they reach you, but remember that big ones split into more (smaller, faster-diverging) hazards.
3. Collect shield orbs to buy yourself a second chance. A shield-absorbed collision also destroys (and splits) the meteor that hit you.
4. Any meteor collision without a shield ends the run.

The HUD shows elapsed time, score, current multiplier (`x2`, `x3`, …), and remaining shield charges.

## Project Structure

```
38-meteor-dodge/
├── main.py              # Entry point – creates and runs the GameEngine
├── requirements.txt     # Python dependencies (pygame)
├── game/
│   ├── __init__.py
│   ├── game_engine.py   # Game loop, input, spawning, collisions, HUD, Laser & ShieldOrb classes
│   ├── meteor.py        # Meteor: movement, rotation, collision, rendering
│   └── ship.py          # Ship: movement, trail, rendering
├── Before.mp4           # Demo of the original starter game
└── After.mp4            # Demo with all features implemented
```

## Configuration

Key gameplay constants live at the top of `game/game_engine.py` and in the classes below it:

| Setting | Location | Default |
|---|---|---|
| Window size | `WIDTH`, `HEIGHT` | 700 × 520 |
| Frame rate | `FPS` | 60 |
| Ship speed | `SPEED` in `game/ship.py` | 5 px/frame |
| Laser speed | `Laser.speed` | 9 px/frame |
| Shield orb spawn rate | `update()` (`FPS * 9`) | every 9 s |
| Multiplier step | `update()` (`FPS * 10`) | every 10 s |
| Initial / minimum meteor spawn interval | `reset()` / `update()` | 60 / 20 frames |

## Testing Checklist

- [ ] `SPACE` starts the game from the title screen.
- [ ] `SPACE` fires lasers during gameplay.
- [ ] Lasers destroy meteors; large meteors split into smaller fragments.
- [ ] Collecting a shield orb displays the shield ring and grants one-hit protection.
- [ ] The multiplier increases after each uninterrupted 10-second survival interval.
- [ ] A shield-absorbed hit resets the multiplier.
- [ ] Without a shield, a meteor collision ends the run.
- [ ] `SPACE` restarts after Game Over.

## Possible Future Improvements

- Sound effects and background music
- Persistent high-score tracking
- Additional power-ups (rapid fire, slow-motion, magnet)
- Boss meteors and varied meteor types
- Pause menu and difficulty settings

## Author

Built by [@gauravmes9a11-alt](https://github.com/gauravmes9a11-alt).
