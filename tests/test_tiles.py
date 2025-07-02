import unittest
import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from tiler_cache_cleaner.utils.tiles import generate_patterns_tiles

class TestTileFunctionsFromJSON(unittest.TestCase):

    def test_from_json(self):
        json_path = os.path.join(os.path.dirname(__file__), "fixture.json")
        with open(json_path, "r") as f:
            data = json.load(f)

        for test_case in data["tests"]:
            with self.subTest(msg=test_case["name"]):
                tiles_input = test_case["tiles_input"]
                zoom_levels = test_case["zoom_levels"]
                expected = test_case["expected"]
                print("Input tiles: ", tiles_input, "Zoom levels: ",zoom_levels )
                result = generate_patterns_tiles(tiles_input, zoom_levels)
                # print(result)
                self.assertEqual(sorted(result), sorted(expected))


if __name__ == "__main__":
    unittest.main()