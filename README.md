# Space Invaders

A classic arcade-style **Space Invaders** game built with **Python** and **Pygame**.

---

## Description

This project recreates the classic **Space Invaders arcade game** using Python and the Pygame library. Battle waves of aliens, dodge their attacks, and try to achieve the highest score possible.

---

## Features

- Classic Space Invaders gameplay
- Health system with visual health bar
- Score tracking with star counter
- Multiple enemy types with unique lasers
- Custom retro font
- Sound effects
- Progressive difficulty system

---

## Requirements

- Windows OS
- Python (already included in the virtual environment)
- Pygame (already installed inside the virtual environment)

⚠️ This repository includes a **preconfigured virtual environment (`pygame-env`)** so you do not need to install dependencies manually.

---

## Installation

### 1. Clone the repository

```cmd
git clone https://github.com/RaviduSenavirathna/Space-Invaders.git
cd Space-Invaders
```

## Directory Structure
```
Space-Invaders/
├── fonts/
│   └── ByteBounce.ttf
├── images/
│   ├── blue_ship.png
│   ├── enemy1.png - enemy4.png
│   ├── enemy1l.png - enemy4l.png
│   ├── laser1.png
│   ├── star.png
│   └── hb0.png - hb5.png
├── sound effects/
│   └── laser_shoot.wav
└── src/
    └── ...
```

## How to Play

1. Activate the virtual envirnment and run main.py

```cmd
pygame-env\Scripts\activate
python main.py
```

2. Controls:
- `A` - Move left
- `D` - Move right
- `Left Mouse Button` - Shoot
- `R` - Restart game (when game over)

3. Gameplay:
- Control your spaceship at the bottom of the screen
- Shoot the incoming aliens before they reach you
- Avoid enemy lasers
- Each alien hit awards 10 points
- Clear waves of aliens to progress
- You have 5 health points
- Clearing a wave restores 1 health point

## Game Features
- Health System: You start with 5 health points
- Score System: Earn points by destroying aliens
- Progressive Difficulty: Aliens move faster as you progress
- Health Recovery: Gain 1 health point after clearing each wave

## Contributing
Feel free to fork this repository and submit pull requests to contribute to this project.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Original Space Invaders game by Tomohiro Nishikado
- Pygame community for the excellent game development library
- ByteBounce font creator


