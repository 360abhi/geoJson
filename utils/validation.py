from playwright.sync_api import Page
import allure
from datetime import datetime


class Validations:

    def __init__(self, page: Page, timeout: int = 10000):
        self.page = page
        self.timeout = timeout

    def verify_marker_exists_in_editor(self, expected_coords: list, tolerance: float = 0.001):
        """
        Assert that marker coordinates exist in CodeMirror editor DOM.
        expected_coords: [longitude, latitude]
        """
        with allure.step(f"Verify Marker Exists - {expected_coords}"):
            try:
                numbers = self.page.locator(".cm-number").all_inner_texts()
                coords = [float(n) for n in numbers[:2]]

                assert len(coords) >= 2, "Not enough coordinates found in editor"
                assert abs(coords[0] - expected_coords[
                    0]) <= tolerance, f"Longitude mismatch: {coords[0]} vs {expected_coords[0]}"
                assert abs(coords[1] - expected_coords[
                    1]) <= tolerance, f"Latitude mismatch: {coords[1]} vs {expected_coords[1]}"

                allure.attach(
                    f"Expected: {expected_coords}\nActual: {coords}",
                    name="Marker Validation - PASS",
                    attachment_type=allure.attachment_type.TEXT
                )
                screenshot = self.page.screenshot()
                allure.attach(
                    screenshot,
                    name="Marker Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception as e:
                allure.attach(
                    str(e),
                    name="Marker Validation Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                screenshot = self.page.screenshot()
                allure.attach(
                    screenshot,
                    name="Marker Screenshot on Failure",
                    attachment_type=allure.attachment_type.PNG
                )
                raise

    def validate_map_loaded(self, tcid: str = None):
        """Assert that the map loaded successfully"""
        with allure.step(f"Validate Map Loaded - {tcid}"):
            try:
                self.page.wait_for_timeout(1000)
                self.page.wait_for_load_state(state="networkidle")
                canvas = self.page.query_selector('canvas.mapboxgl-canvas, canvas.leaflet-canvas')
                assert canvas is not None, "Map canvas not found"
                assert canvas.is_visible(), "Map canvas is not visible"

                screenshot_bytes = self.page.screenshot()

                allure.attach(
                    f"Map loaded successfully at {datetime.now().isoformat()}",
                    name=f"Map Load Validation - {tcid}",
                    attachment_type=allure.attachment_type.TEXT
                )

                allure.attach(
                    screenshot_bytes,
                    name=f"Map Screenshot - {tcid}",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception as e:
                allure.attach(
                    str(e),
                    name="Map Load Validation Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise
