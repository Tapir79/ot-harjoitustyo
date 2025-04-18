import unittest
from services.level_service import LevelService


class TestLevelService(unittest.TestCase):
    def setUp(self):
        self.level_service = LevelService()

    def test_final_level_is_set_correctly(self):
        self.assertEqual(self.level_service.get_final_level(), 15)
