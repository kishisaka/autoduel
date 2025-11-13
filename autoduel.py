#!/usr/bin/env python3
"""
Autoduel - A fluid vehicle combat game
"""
import sys
import time
import random
import math
from typing import Tuple, List
import os

# Try to import curses for better terminal control
try:
    import curses
    CURSES_AVAILABLE = True
except ImportError:
    CURSES_AVAILABLE = False


class Vector2:
    """2D vector for smooth position and velocity calculations"""
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self):
        mag = self.magnitude()
        if mag > 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(0, 0)
    
    def distance_to(self, other) -> float:
        return (self - other).magnitude()


class Vehicle:
    """Vehicle class with fluid movement and combat capabilities"""
    def __init__(self, name: str, x: float, y: float, symbol: str = '@'):
        self.name = name
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.5
        self.max_speed = 3.0
        self.friction = 0.92
        self.health = 100
        self.max_health = 100
        self.armor = 10
        self.weapon_damage = 15
        self.weapon_range = 10.0
        self.weapon_cooldown = 0.0
        self.weapon_cooldown_time = 1.0
        self.symbol = symbol
        self.is_player = False
        
    def accelerate(self, direction: Vector2, delta_time: float):
        """Apply acceleration in a direction with fluid physics"""
        if direction.magnitude() > 0:
            normalized = direction.normalize()
            self.velocity = self.velocity + (normalized * self.acceleration * delta_time)
            
            # Cap speed
            if self.velocity.magnitude() > self.max_speed:
                self.velocity = self.velocity.normalize() * self.max_speed
    
    def update(self, delta_time: float):
        """Update vehicle physics and position"""
        # Apply friction for smooth deceleration
        self.velocity = self.velocity * self.friction
        
        # Update position based on velocity
        self.position = self.position + (self.velocity * delta_time)
        
        # Update weapon cooldown
        if self.weapon_cooldown > 0:
            self.weapon_cooldown -= delta_time
    
    def can_fire(self) -> bool:
        return self.weapon_cooldown <= 0
    
    def fire(self, target: 'Vehicle') -> Tuple[bool, int]:
        """Fire at target vehicle, returns (hit, damage)"""
        if not self.can_fire():
            return False, 0
        
        distance = self.position.distance_to(target.position)
        if distance > self.weapon_range:
            return False, 0
        
        self.weapon_cooldown = self.weapon_cooldown_time
        
        # Calculate hit chance based on distance
        hit_chance = 1.0 - (distance / self.weapon_range) * 0.5
        if random.random() < hit_chance:
            damage = max(0, self.weapon_damage - target.armor // 2)
            target.health -= damage
            return True, damage
        
        return False, 0
    
    def is_alive(self) -> bool:
        return self.health > 0


class Game:
    """Main game class with fluid gameplay loop"""
    def __init__(self, width: int = 60, height: int = 20):
        self.width = width
        self.height = height
        self.running = True
        self.player = Vehicle("Player", width // 4, height // 2, '@')
        self.player.is_player = True
        self.enemies: List[Vehicle] = []
        self.game_time = 0.0
        self.score = 0
        self.messages: List[str] = []
        self.max_messages = 5
        
        # Spawn initial enemies
        self.spawn_enemy()
    
    def add_message(self, message: str):
        """Add a message to the message log"""
        self.messages.append(message)
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)
    
    def spawn_enemy(self):
        """Spawn a new enemy vehicle"""
        # Spawn on right side
        x = self.width - 5
        y = random.randint(2, self.height - 3)
        enemy = Vehicle(f"Enemy{len(self.enemies) + 1}", x, y, 'E')
        enemy.armor = 5
        enemy.health = 50
        self.enemies.append(enemy)
    
    def update_ai(self, enemy: Vehicle, delta_time: float):
        """Simple AI for enemy vehicles"""
        if not enemy.is_alive():
            return
        
        # Move towards player
        direction = self.player.position - enemy.position
        if direction.magnitude() > 0:
            enemy.accelerate(direction.normalize(), delta_time)
        
        # Try to fire at player
        if enemy.can_fire():
            distance = enemy.position.distance_to(self.player.position)
            if distance <= enemy.weapon_range:
                hit, damage = enemy.fire(self.player)
                if hit:
                    self.add_message(f"{enemy.name} hits you for {damage} damage!")
    
    def constrain_position(self, vehicle: Vehicle):
        """Keep vehicle within bounds"""
        vehicle.position.x = max(1, min(self.width - 2, vehicle.position.x))
        vehicle.position.y = max(1, min(self.height - 2, vehicle.position.y))
    
    def update(self, delta_time: float):
        """Update game state"""
        self.game_time += delta_time
        
        # Update player
        self.player.update(delta_time)
        self.constrain_position(self.player)
        
        # Update enemies
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.update(delta_time)
                self.update_ai(enemy, delta_time)
                self.constrain_position(enemy)
        
        # Remove dead enemies
        dead_enemies = [e for e in self.enemies if not e.is_alive()]
        for enemy in dead_enemies:
            self.score += 10
            self.add_message(f"{enemy.name} destroyed! +10 points")
            self.enemies.remove(enemy)
        
        # Spawn new enemies periodically
        if len(self.enemies) < 3 and random.random() < 0.02:
            self.spawn_enemy()
        
        # Check game over
        if not self.player.is_alive():
            self.running = False
    
    def render(self) -> str:
        """Render the game state as a string"""
        # Create empty grid
        grid = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # Draw borders
        for x in range(self.width):
            grid[0][x] = '='
            grid[self.height - 1][x] = '='
        for y in range(self.height):
            grid[y][0] = '|'
            grid[y][self.width - 1] = '|'
        
        # Draw enemies
        for enemy in self.enemies:
            if enemy.is_alive():
                x, y = int(enemy.position.x), int(enemy.position.y)
                if 0 <= x < self.width and 0 <= y < self.height:
                    grid[y][x] = enemy.symbol
        
        # Draw player
        x, y = int(self.player.position.x), int(self.player.position.y)
        if 0 <= x < self.width and 0 <= y < self.height:
            grid[y][x] = self.player.symbol
        
        # Convert grid to string
        output = '\n'.join(''.join(row) for row in grid)
        
        # Add status bar
        status = f"\nHealth: {self.player.health}/{self.player.max_health} | "
        status += f"Speed: {self.player.velocity.magnitude():.1f} | "
        status += f"Score: {self.score} | "
        status += f"Enemies: {len(self.enemies)}"
        
        # Add weapon status
        weapon_status = " | Weapon: "
        if self.player.can_fire():
            weapon_status += "READY"
        else:
            weapon_status += f"Cooldown {self.player.weapon_cooldown:.1f}s"
        
        output += status + weapon_status + "\n"
        
        # Add messages
        output += "\n--- Messages ---\n"
        for msg in self.messages[-self.max_messages:]:
            output += msg + "\n"
        
        # Add controls
        output += "\n--- Controls ---\n"
        output += "WASD: Move | SPACE: Fire | Q: Quit\n"
        
        return output


def main_simple():
    """Simple non-curses game loop"""
    game = Game()
    last_time = time.time()
    
    print("Autoduel - Fluid Vehicle Combat")
    print("=" * 60)
    print("This is a simple mode. For better experience, install curses support.")
    print("\nControls: WASD to move, SPACE to fire, Q to quit")
    print("Press ENTER to start...")
    input()
    
    frame_count = 0
    
    while game.running:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        
        # Simple input (non-blocking not available without curses)
        if frame_count % 2 == 0:  # Update every other frame
            # Clear screen
            os.system('clear' if os.name != 'nt' else 'cls')
            print(game.render())
            print("\nEnter command (w/a/s/d/space/q): ", end='', flush=True)
        
        # For demo purposes, update with simple AI
        game.update(delta_time)
        
        # Simple auto-play for demo
        if frame_count % 10 == 0:
            # Auto move player right
            direction = Vector2(1, 0)
            game.player.accelerate(direction, delta_time)
            
            # Auto fire at nearest enemy
            if game.enemies and game.player.can_fire():
                nearest = min(game.enemies, key=lambda e: game.player.position.distance_to(e.position))
                hit, damage = game.player.fire(nearest)
                if hit:
                    game.add_message(f"You hit {nearest.name} for {damage} damage!")
        
        time.sleep(0.05)
        frame_count += 1
        
        # Run for demo duration
        if frame_count > 200:
            break
    
    print(f"\nGame Over! Final Score: {game.score}")


def main_curses(stdscr):
    """Curses-based game loop with real-time input"""
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(50)  # Input timeout in ms
    
    game = Game()
    last_time = time.time()
    
    while game.running:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        
        # Handle input
        key = stdscr.getch()
        direction = Vector2(0, 0)
        
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('w') or key == ord('W'):
            direction.y = -1
        elif key == ord('s') or key == ord('S'):
            direction.y = 1
        elif key == ord('a') or key == ord('A'):
            direction.x = -1
        elif key == ord('d') or key == ord('D'):
            direction.x = 1
        elif key == ord(' '):
            # Fire at nearest enemy
            if game.enemies and game.player.can_fire():
                nearest = min(game.enemies, key=lambda e: game.player.position.distance_to(e.position))
                hit, damage = game.player.fire(nearest)
                if hit:
                    game.add_message(f"You hit {nearest.name} for {damage} damage!")
                else:
                    game.add_message("Miss!")
        
        # Apply movement
        game.player.accelerate(direction, delta_time)
        
        # Update game
        game.update(delta_time)
        
        # Render
        stdscr.clear()
        try:
            stdscr.addstr(0, 0, game.render())
        except curses.error:
            pass  # Ignore if screen is too small
        stdscr.refresh()
    
    # Game over screen
    stdscr.clear()
    stdscr.addstr(0, 0, f"Game Over! Final Score: {game.score}")
    stdscr.addstr(1, 0, "Press any key to exit...")
    stdscr.nodelay(0)
    stdscr.getch()


def main():
    """Main entry point"""
    if CURSES_AVAILABLE and len(sys.argv) > 1 and sys.argv[1] == '--curses':
        curses.wrapper(main_curses)
    else:
        main_simple()


if __name__ == "__main__":
    main()
