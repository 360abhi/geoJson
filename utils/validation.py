from playwright.sync_api import Page
import allure
from datetime import datetime
import re


class Validations:

    def __init__(self, page: Page, timeout: int = 10000):
        self.page = page
        self.timeout = timeout

    def verify_delete_marker_in_map(self):
        with allure.step('Verify delete marker in map'):
            try:
                self.page.wait_for_timeout(500)
                assert self.page.locator("//span[text()='\"Point\"']").count() == 0,"Deletion Failed"
                allure.attach(
                    self.page.screenshot(full_page=True),
                    name=f"Verify Delete Marker",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                allure.attach(
                    str(e),
                    name=f"Verify Delete Marker",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise


    def verify_marker_exist_in_map(self):
         with allure.step(f"Verify Marker"):
            try:
                self.page.wait_for_timeout(500)
                # Checking marker exists
                marker = self.page.locator("//div[@aria-label='Map marker']")
                assert marker.is_visible(), "Marker not visible on map"

                allure.attach(
                        self.page.screenshot(full_page=True),
                        name=f"Verify Marker",
                        attachment_type=allure.attachment_type.PNG
                    )

            except Exception as e:
                allure.attach(
                    str(e),
                    name="Marker Validation",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise


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

    def verify_search_marker(self, expected_coords: list, tolerance: float = 0.5,initial_url="https://geojson.io/#map=2/0/20"):
        """
        Verify that a search placed a marker and map URL has expected coordinates.
        """
        with allure.step(f"Verify Search Result Marker at {expected_coords}"):
            try:
                # Checking marker exists
                marker = self.page.locator("//div[@aria-label='Map marker']")
                assert marker.is_visible(), "Search marker not visible on map"
                current_url = self.page.url
                self.page.wait_for_timeout(1000)
                attempts = 0
                while current_url == initial_url:
                    self.page.wait_for_timeout(1000)
                    attempts += 1
                    current_url = self.page.url
                    if attempts > 10:
                        raise Exception("Search marker not visible on map")
                parts = current_url.split("#map=")[1].split("/")
                zoom, lat, lon = float(parts[0]), float(parts[1]), float(parts[2])

                assert abs(lon - expected_coords[0]) <= tolerance, f"Longitude mismatch: {lon} vs {expected_coords[0]}"
                assert abs(lat - expected_coords[1]) <= tolerance, f"Latitude mismatch: {lat} vs {expected_coords[1]}"

                allure.attach(
                    f"Expected: {expected_coords}\nActual: [{lon}, {lat}]\nZoom: {zoom}",
                    name="Search Validation Details",
                    attachment_type=allure.attachment_type.TEXT
                )
                allure.attach(
                    self.page.screenshot(),
                    name="Search Result Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception as e:
                allure.attach(
                    str(e),
                    name="Search Marker Validation Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise

    def validate_zoom_level(self, expected_zoom: int, tc_id: str):
        with allure.step(f"Validate Zoom Level - {tc_id}"):
            self.page.wait_for_load_state(state="networkidle")
            url = self.page.url
            actual_zoom = url.split('/')[-3][-1]

            try:
                assert actual_zoom == expected_zoom, (
                    f"Expected zoom {expected_zoom}, but got {actual_zoom}"
                )

                allure.attach(
                    self.page.screenshot(full_page=True),
                    name=f"Zoom Validation Success - {tc_id}",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    f"Expected: {expected_zoom}, Actual: {actual_zoom}",
                    name=f"Zoom Values - {tc_id}",
                    attachment_type=allure.attachment_type.TEXT
                )

            except AssertionError as e:
                allure.attach(
                    self.page.screenshot(full_page=True),
                    name=f"Zoom Validation Failure - {tc_id}",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    str(e),
                    name="Zoom Validation Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise

    def validate_properties(self,expected:list,actual:list):
        with allure.step("Validate Properties"):
            try:
                for val1,val2 in zip(expected,actual):
                    assert val1.lower().strip() == val2.lower().strip(),f"Longitude mismatch: {val1} vs {val2}"
                    allure.attach(
                        self.page.screenshot(full_page=True),
                        name=f"Validate Properties",
                        attachment_type=allure.attachment_type.PNG
                    )
                    allure.attach(
                        f"Expected: {val1}, Actual: {val2}",
                        name=f"Validate Properties",
                        attachment_type=allure.attachment_type.TEXT
                    )

            except AssertionError as e:
                allure.attach(
                    self.page.screenshot(full_page=True),
                    name=f"Validate Properties",
                    attachment_type=allure.attachment_type.PNG
                )
                allure.attach(
                    str(e),
                    name="Validate Properties",
                    attachment_type=allure.attachment_type.TEXT
                )
                raise
