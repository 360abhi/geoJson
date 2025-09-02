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
    search_input = ".mapboxgl-ctrl-geocoder--input"

    coordinates = ".cm-number"
    canvas = "//canvas"
    map_marker = "//div[@aria-label='Map marker']"

    def __init__(self,page:Page):
        self.page = page

    # ===== Actions =====

    def zoom(self,zoom:str):
        actions = zoom.split(';')
        for act in actions:
            if act == 'zoom_in':
                self.click_zoom_in()
            else:
                self.click_zoom_out()

    def click_zoom_in(self):
        self.page.locator(self.zoomin).click()
        self.page.wait_for_timeout(500)

    def click_zoom_out(self):
        self.page.locator(self.zoomout).click()
        self.page.wait_for_timeout(500)

    def select_marker_tool(self):
        self.page.locator(self.marker).click()

    def select_line_tool(self):
        self.page.locator(self.line).click()

    def select_polygon_tool(self):
        self.page.locator(self.polygon).click()

    def select_rectangular_polygon_tool(self):
        self.page.locator(self.rectangular_polygon).click()

    def search_location(self, query: str):
        self.page.type(self.search_input, query)
        self.page.click("(//div[@class='mapboxgl-ctrl-geocoder--suggestion-title'])[1]",timeout=12000)
        self.page.wait_for_timeout(500)



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
