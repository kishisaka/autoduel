#!/usr/bin/env python3
"""
Demo script showing the fluid mechanics of autoduel
"""
import time
from autoduel import Vector2, Vehicle, Game


def demo_fluid_acceleration():
    """Demonstrate smooth acceleration"""
    print("=" * 60)
    print("DEMO 1: Fluid Acceleration")
    print("=" * 60)
    print("Watch how the vehicle smoothly accelerates from 0 to max speed\n")
    
    vehicle = Vehicle("Demo Vehicle", 10, 10)
    direction = Vector2(1, 0)
    
    print(f"Initial speed: {vehicle.velocity.magnitude():.2f}")
    print("\nAccelerating...")
    
    for i in range(20):
        vehicle.accelerate(direction, 0.1)
        vehicle.update(0.1)
        speed = vehicle.velocity.magnitude()
        bars = int(speed / vehicle.max_speed * 40)
        print(f"Step {i+1:2d}: Speed {speed:.2f} |{'█' * bars}{' ' * (40-bars)}|")
        time.sleep(0.1)
    
    print(f"\nFinal speed: {vehicle.velocity.magnitude():.2f} (max: {vehicle.max_speed})")


def demo_fluid_friction():
    """Demonstrate smooth deceleration via friction"""
    print("\n" + "=" * 60)
    print("DEMO 2: Fluid Friction/Deceleration")
    print("=" * 60)
    print("Watch how friction smoothly slows down the vehicle\n")
    
    vehicle = Vehicle("Demo Vehicle", 10, 10)
    vehicle.velocity = Vector2(3.0, 0)
    
    print(f"Initial speed: {vehicle.velocity.magnitude():.2f}")
    print("\nCoasting (no acceleration)...")
    
    for i in range(30):
        vehicle.update(0.1)
        speed = vehicle.velocity.magnitude()
        if speed < 0.01:
            break
        bars = int(speed / 3.0 * 40)
        print(f"Step {i+1:2d}: Speed {speed:.2f} |{'█' * bars}{' ' * (40-bars)}|")
        time.sleep(0.1)
    
    print(f"\nFinal speed: {vehicle.velocity.magnitude():.2f}")


def demo_smooth_turning():
    """Demonstrate smooth direction changes"""
    print("\n" + "=" * 60)
    print("DEMO 3: Fluid Direction Changes")
    print("=" * 60)
    print("Watch how the vehicle smoothly changes direction\n")
    
    vehicle = Vehicle("Demo Vehicle", 30, 15)
    
    directions = [
        (Vector2(1, 0), "Right"),
        (Vector2(0, 1), "Down"),
        (Vector2(-1, 0), "Left"),
        (Vector2(0, -1), "Up"),
    ]
    
    for direction, name in directions:
        print(f"\nAccelerating {name}...")
        for _ in range(8):
            vehicle.accelerate(direction, 0.1)
            vehicle.update(0.1)
            print(f"  Position: ({vehicle.position.x:.1f}, {vehicle.position.y:.1f}), "
                  f"Velocity: ({vehicle.velocity.x:.1f}, {vehicle.velocity.y:.1f})")
            time.sleep(0.05)


def demo_combat_mechanics():
    """Demonstrate fluid combat"""
    print("\n" + "=" * 60)
    print("DEMO 4: Combat Mechanics")
    print("=" * 60)
    print("Testing weapon cooldowns and hit calculations\n")
    
    attacker = Vehicle("Player", 10, 10)
    target = Vehicle("Enemy", 15, 10)
    
    print(f"Distance: {attacker.position.distance_to(target.position):.1f} units")
    print(f"Weapon range: {attacker.weapon_range} units\n")
    
    for i in range(5):
        if attacker.can_fire():
            hit, damage = attacker.fire(target)
            if hit:
                print(f"Shot {i+1}: HIT! {damage} damage dealt. Enemy health: {target.health}/{target.max_health}")
            else:
                print(f"Shot {i+1}: MISS! Enemy health: {target.health}/{target.max_health}")
        else:
            print(f"Shot {i+1}: Weapon cooling down... ({attacker.weapon_cooldown:.2f}s)")
        
        attacker.update(0.3)
        time.sleep(0.3)
    
    print(f"\nFinal enemy health: {target.health}/{target.max_health}")


def demo_game_state():
    """Show a complete game state"""
    print("\n" + "=" * 60)
    print("DEMO 5: Full Game State")
    print("=" * 60)
    print("Showing the complete game with all fluid mechanics\n")
    
    game = Game(width=50, height=15)
    
    for i in range(10):
        print(f"\n--- Frame {i+1} ---")
        
        # Player moves right
        game.player.accelerate(Vector2(1, 0), 0.2)
        
        # Try to fire
        if game.enemies and game.player.can_fire():
            nearest = min(game.enemies, key=lambda e: game.player.position.distance_to(e.position))
            hit, damage = game.player.fire(nearest)
            if hit:
                print(f"Player hits enemy for {damage} damage!")
        
        game.update(0.2)
        
        # Show simplified state
        print(f"Player: Pos({game.player.position.x:.1f}, {game.player.position.y:.1f}) "
              f"Speed: {game.player.velocity.magnitude():.1f} Health: {game.player.health}")
        print(f"Enemies: {len(game.enemies)}, Score: {game.score}")
        
        time.sleep(0.5)


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("AUTODUEL - FLUID MECHANICS DEMONSTRATION")
    print("=" * 60)
    print("\nThis demo showcases the fluid gameplay mechanics:")
    print("- Smooth acceleration and deceleration")
    print("- Physics-based movement with friction")
    print("- Responsive controls and momentum")
    print("- Real-time combat with cooldowns")
    print("\n")
    
    try:
        demo_fluid_acceleration()
        time.sleep(1)
        
        demo_fluid_friction()
        time.sleep(1)
        
        demo_smooth_turning()
        time.sleep(1)
        
        demo_combat_mechanics()
        time.sleep(1)
        
        demo_game_state()
        
        print("\n" + "=" * 60)
        print("DEMO COMPLETE!")
        print("=" * 60)
        print("\nTo play the actual game, run: python3 autoduel.py")
        print("For interactive mode (curses): python3 autoduel.py --curses")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted. Thanks for watching!")


if __name__ == "__main__":
    main()
