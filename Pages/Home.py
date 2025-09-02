from pathlib import Path
import sys
root = Path(__file__).parent.parent.absolute()
sys.path.append(str(root))
from playwright.sync_api import Page

class Home:

    zoomin = "//span[@title='Zoom in']"
    zoomout = "//span[@title='Zoom out']"
    marker = "//button[@title='Draw Point (m)']"
    line = "//button[@title='Draw LineString (l)']"
    polygon = "//button[@title='Draw Polygon (p)']"
    rectangular_polygon = "//button[@title='Draw Rectangular Polygon (r)']"

    coordinates = ".cm-number"
    canvas = "//canvas"

    def __init__(self,page:Page):
        self.page = page

    # ===== Actions =====
    def click_zoom_in(self):
        self.page.locator(self.zoomin).click()

    def click_zoom_out(self):
        self.page.locator(self.zoomout).click()

    def select_marker_tool(self):
        self.page.locator(self.marker).click()

    def select_line_tool(self):
        self.page.locator(self.line).click()

    def select_polygon_tool(self):
        self.page.locator(self.polygon).click()

    def select_rectangular_polygon_tool(self):
        self.page.locator(self.rectangular_polygon).click()


    def place_marker_by_ratio(self,city_name: str = ""):
        """Click using predetermined ratios for known cities"""
        # Pre-calculated ratios for Indian cities
        city_ratios = {
            "mumbai": {"x_ratio": 0.43, "y_ratio": 0.5875},
            "delhi": {"x_ratio": 0.525, "y_ratio": 0.32},
        }

        # Get ratios for the city or use [1,1]
        ratios = city_ratios.get(city_name.lower(),[1,1])

        canvas = self.page.locator('canvas.mapboxgl-canvas')
        box = canvas.bounding_box()

        click_x = box["x"] + box["width"] * ratios["x_ratio"]
        click_y = box["y"] + box["height"] * ratios["y_ratio"]

        self.page.mouse.click(click_x, click_y)
        print(f"Clicked at approximate position for {city_name}: {click_x}, {click_y}")
