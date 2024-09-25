import unittest
from oops import Gate_Env, Pin

class TestGateEnv(unittest.TestCase):

    def test_initialization(self):
        gate = Gate_Env(1, 10, 20)
        self.assertEqual(gate.width, 10)
        self.assertEqual(gate.height, 20)
        self.assertEqual(gate.gate_index, 1)
        self.assertFalse(gate.is_packed)

    def test_set_env(self):
        gate = Gate_Env(1, 10, 20)
        gate.set_env(100, 200)
        self.assertEqual(gate.envelope_width, 100)
        self.assertEqual(gate.envelope_height, 200)

    def test_set_coord_env(self):
        gate = Gate_Env(1, 10, 20)
        gate.set_coord_env(50, 60)
        self.assertEqual(gate.envelope_x, 50)
        self.assertEqual(gate.envelope_y, 60)

    def test_set_coord_rel_env(self):
        gate = Gate_Env(1, 10, 20)
        gate.set_env(100, 200)
        gate.set_coord_env(50, 60)
        gate.set_coord_rel_env(30, 40)
        self.assertEqual(gate.x_relative_env, 30)
        self.assertEqual(gate.y_relative_env, 40)
        self.assertEqual(gate.x, 80)
        self.assertEqual(gate.y, 100)

    def test_add_pin(self):
        gate = Gate_Env(1, 10, 20)
        gate.add_pin(1, 5, 5)
        self.assertIn(1, gate.pins)
        self.assertEqual(gate.pins[1].pin_x, 5)
        self.assertEqual(gate.pins[1].pin_y, 5)

    def test_get_global_coord(self):
        gate = Gate_Env(1, 10, 20)
        gate.set_env(100, 200)
        gate.set_coord_env(50, 60)
        gate.set_coord_rel_env(30, 40)
        self.assertEqual(gate.get_global_coord(), (80, 100))

    def test_get_global_coord_pin(self):
        gate = Gate_Env(1, 10, 20)
        gate.set_env(100, 200)
        gate.set_coord_env(50, 60)
        gate.set_coord_rel_env(30, 40)
        gate.add_pin(1, 5, 5)
        self.assertEqual(gate.get_global_coord_pin(1), (85, 115))

    def test_pin_connected_to(self):
        pin = Pin(1, 1, 5, 5)
        pin.connected_to(2, 2)
        self.assertIn(2, pin.connected_pins)
        self.assertIn(2, pin.connected_pins)
        self.assertEqual(pin.connected_pins[2], [2])
        pin.connected_to(2,6)
        self.assertIn(2, pin.connected_pins)
        self.assertEqual(pin.connected_pins[2], [2,6])

if __name__ == '__main__':
    
    unittest.main()