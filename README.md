# autoduel
Autoduel game in python with fluid mechanics.

## Overview
A fluid vehicle combat game where you control a vehicle fighting against enemy vehicles. The game features smooth physics-based movement, real-time combat, and responsive controls.

## Features
- **Fluid Movement**: Physics-based acceleration and friction for smooth, realistic vehicle control
- **Real-time Combat**: Fast-paced weapon system with cooldowns and range-based hit calculations
- **Dynamic AI**: Enemies that pursue and attack the player
- **Score System**: Earn points by destroying enemy vehicles
- **Two Play Modes**: Simple mode for quick demos, curses mode for interactive gameplay

## Installation
No external dependencies required! Just Python 3.6+

```bash
git clone https://github.com/kishisaka/autoduel.git
cd autoduel
```

## How to Play

### Simple Demo Mode
```bash
python3 autoduel.py
```

### Interactive Mode (requires curses - Unix/Linux/Mac)
```bash
python3 autoduel.py --curses
```

## Controls
- **W/A/S/D**: Move your vehicle (up/left/down/right)
- **SPACE**: Fire weapon at nearest enemy
- **Q**: Quit game

## Gameplay Tips
- Keep moving to avoid enemy fire
- Manage your weapon cooldown - time your shots carefully
- Watch your health bar - when it reaches 0, game over!
- Get close to enemies for better accuracy, but not too close!
- Your speed affects your ability to dodge

## Game Mechanics
- **Acceleration**: Smooth buildup of speed when moving
- **Friction**: Gradual slowdown when not accelerating (feels fluid and natural)
- **Weapon Range**: 10 units - get closer for better hit chance
- **Hit Calculation**: Distance-based accuracy system
- **Armor**: Reduces incoming damage

Enjoy the fluid combat! 
