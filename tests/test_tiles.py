import unittest
import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from tiler_cache_cleaner.utils.tiles import (
    generate_patterns_tiles,
    generate_tile_patterns_bbox,
)


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
                print("Input tiles: ", tiles_input, "Zoom levels: ", zoom_levels)
                result = generate_patterns_tiles(tiles_input, zoom_levels)
                # print(result)
                self.assertEqual(sorted(result), sorted(expected))


class TestGenerateTilePatternsBBox(unittest.TestCase):

    def test_generate_tile_patterns_bbox(self):
        test_cases = [
            {
                "name": "Ayacucho 1",
                "bbox": [-74.259875, -13.200409, -74.190009, -13.119005],
                "zoom_levels": [5],
                "expected": ["5/9"],
            },
            {
                "name": "Ayacucho 1",
                "bbox": [-74.259875, -13.200409, -74.190009, -13.119005],
                "zoom_levels": [11, 12, 13, 14, 15, 16],
                "expected": ["11/60", "12/12", "13/24", "14/48", "15/96", "16/192"],
            },
            {
                "name": "San Francisco 1",
                "bbox": [-122.453270, 37.837174, -122.453270, 37.837174],
                "zoom_levels": [7, 8],
                "expected": ["7/20", "8/40"],
            },
        ]

        for test_case in test_cases:
            with self.subTest(msg=test_case["name"]):
                bbox = test_case["bbox"]  # [minx, miny, maxx, maxy]
                zoom_levels = test_case["zoom_levels"]
                expected = test_case["expected"]

                print(f"Testing: {test_case['name']}")
                print(f"BBOX: {bbox}, Zoom levels: {zoom_levels}")

                result = []
                for z in zoom_levels:
                    result.extend(generate_tile_patterns_bbox(bbox, z))

                self.assertEqual(
                    sorted(result),
                    sorted(expected),
                    f"Mismatch for {test_case['name']}",
                )

                self.assertEqual(
                    len(result),
                    len(set(result)),
                    f"Duplicates found in result for {test_case['name']}",
                )


if __name__ == "__main__":
    unittest.main()
