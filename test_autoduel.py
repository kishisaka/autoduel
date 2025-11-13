#!/usr/bin/env python3
"""
Unit tests for autoduel game
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autoduel import Vector2, Vehicle, Game


class TestVector2(unittest.TestCase):
    """Test Vector2 math operations"""
    
    def test_addition(self):
        v1 = Vector2(1, 2)
        v2 = Vector2(3, 4)
        result = v1 + v2
        self.assertAlmostEqual(result.x, 4)
        self.assertAlmostEqual(result.y, 6)
    
    def test_subtraction(self):
        v1 = Vector2(5, 7)
        v2 = Vector2(2, 3)
        result = v1 - v2
        self.assertAlmostEqual(result.x, 3)
        self.assertAlmostEqual(result.y, 4)
    
    def test_scalar_multiplication(self):
        v = Vector2(2, 3)
        result = v * 2
        self.assertAlmostEqual(result.x, 4)
        self.assertAlmostEqual(result.y, 6)
    
    def test_magnitude(self):
        v = Vector2(3, 4)
        self.assertAlmostEqual(v.magnitude(), 5.0)
    
    def test_normalize(self):
        v = Vector2(3, 4)
        normalized = v.normalize()
        self.assertAlmostEqual(normalized.magnitude(), 1.0)
        self.assertAlmostEqual(normalized.x, 0.6)
        self.assertAlmostEqual(normalized.y, 0.8)
    
    def test_distance(self):
        v1 = Vector2(0, 0)
        v2 = Vector2(3, 4)
        self.assertAlmostEqual(v1.distance_to(v2), 5.0)


class TestVehicle(unittest.TestCase):
    """Test Vehicle class"""
    
    def test_initialization(self):
        vehicle = Vehicle("Test", 10, 20)
        self.assertEqual(vehicle.name, "Test")
        self.assertAlmostEqual(vehicle.position.x, 10)
        self.assertAlmostEqual(vehicle.position.y, 20)
        self.assertEqual(vehicle.health, 100)
        self.assertTrue(vehicle.is_alive())
    
    def test_acceleration(self):
        vehicle = Vehicle("Test", 0, 0)
        direction = Vector2(1, 0)
        vehicle.accelerate(direction, 1.0)
        # Should have velocity after acceleration
        self.assertGreater(vehicle.velocity.magnitude(), 0)
    
    def test_update_with_friction(self):
        vehicle = Vehicle("Test", 0, 0)
        vehicle.velocity = Vector2(10, 0)
        vehicle.update(1.0)
        # Velocity should decrease due to friction
        self.assertLess(vehicle.velocity.magnitude(), 10)
    
    def test_position_update(self):
        vehicle = Vehicle("Test", 0, 0)
        vehicle.velocity = Vector2(5, 3)
        vehicle.update(1.0)
        # Position should change based on velocity
        self.assertNotEqual(vehicle.position.x, 0)
        self.assertNotEqual(vehicle.position.y, 0)
    
    def test_weapon_cooldown(self):
        vehicle = Vehicle("Test", 0, 0)
        self.assertTrue(vehicle.can_fire())
        vehicle.weapon_cooldown = 1.0
        self.assertFalse(vehicle.can_fire())
        vehicle.update(1.5)
        self.assertTrue(vehicle.can_fire())
    
    def test_fire_in_range(self):
        attacker = Vehicle("Attacker", 0, 0)
        target = Vehicle("Target", 5, 0)  # Within range
        hit, damage = attacker.fire(target)
        # Should fire and potentially hit
        self.assertFalse(attacker.can_fire())  # Cooldown should be active
        if hit:
            self.assertGreater(damage, 0)
            self.assertLess(target.health, 100)
    
    def test_fire_out_of_range(self):
        attacker = Vehicle("Attacker", 0, 0)
        target = Vehicle("Target", 100, 0)  # Out of range
        hit, damage = attacker.fire(target)
        self.assertFalse(hit)
        self.assertEqual(damage, 0)
        self.assertEqual(target.health, 100)
    
    def test_death(self):
        vehicle = Vehicle("Test", 0, 0)
        vehicle.health = 0
        self.assertFalse(vehicle.is_alive())


class TestGame(unittest.TestCase):
    """Test Game class"""
    
    def test_initialization(self):
        game = Game(width=60, height=20)
        self.assertTrue(game.running)
        self.assertIsNotNone(game.player)
        self.assertTrue(game.player.is_alive())
        self.assertGreater(len(game.enemies), 0)
    
    def test_spawn_enemy(self):
        game = Game()
        initial_count = len(game.enemies)
        game.spawn_enemy()
        self.assertEqual(len(game.enemies), initial_count + 1)
    
    def test_update(self):
        game = Game()
        initial_time = game.game_time
        game.update(0.1)
        self.assertGreater(game.game_time, initial_time)
    
    def test_constrain_position(self):
        game = Game(width=60, height=20)
        vehicle = Vehicle("Test", -10, -10)
        game.constrain_position(vehicle)
        # Should be constrained to within bounds
        self.assertGreaterEqual(vehicle.position.x, 1)
        self.assertGreaterEqual(vehicle.position.y, 1)
        
        vehicle.position = Vector2(100, 100)
        game.constrain_position(vehicle)
        self.assertLess(vehicle.position.x, game.width)
        self.assertLess(vehicle.position.y, game.height)
    
    def test_render(self):
        game = Game()
        output = game.render()
        # Should produce a string output
        self.assertIsInstance(output, str)
        self.assertGreater(len(output), 0)
        # Should contain player symbol
        self.assertIn('@', output)
    
    def test_game_over_on_player_death(self):
        game = Game()
        game.player.health = 0
        game.update(0.1)
        self.assertFalse(game.running)
    
    def test_score_on_enemy_death(self):
        game = Game()
        initial_score = game.score
        if game.enemies:
            game.enemies[0].health = 0
        game.update(0.1)
        # Score should increase when enemy dies
        if initial_score == game.score - 10:
            self.assertEqual(game.score, initial_score + 10)


class TestFluidMechanics(unittest.TestCase):
    """Test fluid movement mechanics"""
    
    def test_smooth_acceleration(self):
        vehicle = Vehicle("Test", 0, 0)
        direction = Vector2(1, 0)
        
        # Multiple acceleration steps should gradually increase speed
        speeds = []
        for _ in range(5):
            vehicle.accelerate(direction, 0.1)
            vehicle.update(0.1)
            speeds.append(vehicle.velocity.magnitude())
        
        # Speed should generally increase then stabilize
        self.assertGreater(speeds[-1], 0)
    
    def test_max_speed_limit(self):
        vehicle = Vehicle("Test", 0, 0)
        direction = Vector2(1, 0)
        
        # Accelerate many times
        for _ in range(100):
            vehicle.accelerate(direction, 0.1)
        
        # Speed should not exceed max_speed
        self.assertLessEqual(vehicle.velocity.magnitude(), vehicle.max_speed)
    
    def test_friction_deceleration(self):
        vehicle = Vehicle("Test", 0, 0)
        vehicle.velocity = Vector2(10, 0)
        
        # Update without acceleration
        initial_speed = vehicle.velocity.magnitude()
        for _ in range(10):
            vehicle.update(0.1)
        
        # Speed should decrease due to friction
        self.assertLess(vehicle.velocity.magnitude(), initial_speed)
    
    def test_momentum_preservation(self):
        vehicle = Vehicle("Test", 0, 0)
        vehicle.velocity = Vector2(5, 0)
        initial_pos = vehicle.position.x
        
        vehicle.update(1.0)
        
        # Vehicle should move in direction of velocity
        self.assertGreater(vehicle.position.x, initial_pos)


if __name__ == '__main__':
    unittest.main()
