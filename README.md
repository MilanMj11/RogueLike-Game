# Dungeons Master

## Introduction

**Dungeons Master** is a roguelike game developed using Pygame. This project is a work in progress and was created for learning purposes. The game involves a character exploring dungeons, fighting enemies, and collecting coins to upgrade his abilities.

## Game Description

In **Dungeons Master**, you play as a little character who starts in a castle lobby. Although the upgrade system isn't fully implemented, the character's goal is to explore dungeons, defeat enemies, and collect coins for future upgrades. The game includes:

- **Enemies**: Skeleton archers and fighters
- **Weapons**: Fireball for distant attacks and a sword for melee attacks
- **Items**: Chests for extra coins and health potions for recovery
- **Levels**: Each dungeon is created using a personal level editor with a start and finish requiring exploration to find the exit

## Features

- Easy to create dungeons due to the level editor.
- Player movement and combat system with cooldowns
- Basic enemy AI with different types of skeletons
- Collectibles including coins and health potions
- Exploration with unknown dungeon exits

## Gameplay

![Gameplay](RogueLikeGame/Animation1.gif)
![Gameplay](RogueLikeGame/Animation2.gif)
The game runs in 90 fps, the gifs are 15 fps :)

In **Dungeons Master**, the player navigates through dungeons, battles skeleton enemies, collects coins, and searches for the dungeon exit. The game is designed to progressively challenge the player with stronger enemies and more complex dungeon layouts.

## Installation

To run this game on your local machine, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/MilanMj11/RogueLike-Game
    ```
2. Navigate to the project directory:
    ```sh
    cd RogueLike-Game
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Run the game:
    ```sh
    python main.py
    ```

## Controls

- **WASD or Arrow Keys**: Move the player
- **Left Click**: Use fireball attack
- **Right Click**: Use sword attack
- **E**: Interaction with objects/exits
- **Esc**: Open the menu

## My Learning Process

The primary purpose of creating this game was to explore the capabilities of Pygame and to learn the fundamentals of game development, without using a game engine.
This project helped me learn various aspects of game development using Pygame, including:

- Camera movement
- Render optimizations
- Simple player movement and collision detection
- Fixing movement jitter bugs
- Object interactions
- Managing scenes and switching between one another
- Inheritance and object-oriented programming concepts
- Creating simple enemy behaviours
- Keeping the project structured and being open to scalability

## Final thoughts

Although the game is unfinished and will remain so as I have moved on to other projects, it was a fun challenge and an excellent opportunity to learn new concepts and skills.
