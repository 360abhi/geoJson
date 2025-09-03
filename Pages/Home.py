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
    open_menu = "//a[.=' Open']"
    prop_key = "(//th/input[@type='text'])[last()]"
    prop_val = "(//td/input[@type='text'])[last()]"
    save_btn = "//button[@type='submit']"
    add_row = "//div[contains(@class,'add-row-button')]/span"
    property_key_first = """(//span[@class='cm-string cm-property' and text()='"properties"']/../../../following-sibling::div/pre/span/span[@class='cm-string cm-property'])[1]"""
    property_val_first = """(//span[@class='cm-string cm-property' and text()='"properties"']/../../../following-sibling::div/pre/span/span[@class='cm-string'])[1]"""
    delete_feature = "//button[contains(@class,'delete-invert')]"
    span_feature = """//span[.='"Point"']"""

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

    def delete_marker(self):
        self.page.locator(self.map_marker).click()
        self.page.locator(self.delete_feature).click()

    def add_properties(self,properties:dict):
        self.page.locator(self.map_marker).click()
        keys = list(properties.keys())
        for i in range(len(keys)):
            if i == 0:
                self.page.locator(self.prop_key).fill(keys[i])
                self.page.locator(self.prop_val).fill(properties[keys[i]])
            else:
                self.page.locator(self.add_row).click()
                self.page.locator(self.prop_key).fill(keys[i])
                self.page.locator(self.prop_val).fill(properties[keys[i]])
        self.page.locator(self.save_btn).click()
        self.page.wait_for_timeout(500)
        return len(keys)

    def draw_shape(self, coordinates: list):

        box = self.page.locator(self.canvas).bounding_box()

        for idx, (lat, lon) in enumerate(coordinates):
            if idx == len(coordinates) - 1:
                self.page.mouse.dblclick(box["x"] + lat, box["y"] + lon)
            else:
                self.page.mouse.click(box["x"] + lat, box["y"] + lon)

    def fetch_properties(self,num:int):
        values = []
        for i in range(num):
            key = f"""(//span[@class='cm-string cm-property' and text()='"properties"']/../../../following-sibling::div/pre/span/span[@class='cm-string cm-property'])[{i+1}]"""
            key = self.page.locator(key).text_content().strip('"')
            val = f"""(//span[@class='cm-string cm-property' and text()='"properties"']/../../../following-sibling::div/pre/span/span[@class='cm-string'])[{i+1}]"""
            val = self.page.locator(val).text_content().strip('"')
            values.append(key)
            values.append(val)
        
        return values


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

    def load_geoJson(self,file_path:str):
        with self.page.expect_file_chooser() as fc_info:
            self.page.click(self.open_menu)
        file_chooser = fc_info.value

        # Set the geojson file
        file_chooser.set_files(file_path)


    def place_marker_by_ratio(self,city_name: str = "default"):
        """Click using predetermined ratios for known cities"""
        # Pre-calculated ratios for Indian cities
        city_ratios = {
            "mumbai": {"x_ratio": 0.43, "y_ratio": 0.5875},
            "delhi": {"x_ratio": 0.525, "y_ratio": 0.32},
            "default":{"x_ratio":0.1, "y_ratio": 0.1}
        }

        # Get ratios for the city or use [1,1]
        ratios = city_ratios.get(city_name.lower(),[1,1])

        canvas = self.page.locator('canvas.mapboxgl-canvas')
        box = canvas.bounding_box()

        click_x = box["x"] + box["width"] * ratios["x_ratio"]
        click_y = box["y"] + box["height"] * ratios["y_ratio"]

        self.page.mouse.click(click_x, click_y)
        print(f"Clicked at approximate position for {city_name}: {click_x}, {click_y}")
