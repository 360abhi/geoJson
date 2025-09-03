import pytest
from pathlib import Path
import os, sys

root = Path(__file__).parent.parent.absolute()
sys.path.append(str(root))
print(root)
from playwright.sync_api import Page
from utils.commonutils import CommonUtils
from utils.validation import Validations
from Pages.Home import Home
from Configuration.ConfigVariables import ConfigVariables


@pytest.mark.parametrize("test_case", CommonUtils().load(ConfigVariables.POLYGON_DATA))
def test_polygon(page: Page, test_case):
    try:
        validations = Validations(page)
        home = Home(page)
        page.goto(test_case['map_url'])
        validations.validate_map_loaded(test_case['tc_id'])
        home.select_polygon_tool()
        home.draw_shape(test_case['coordinates'])
        validations.verify_polygon_in_map()
    except Exception as exc:
        print(str(exc))
        raise exc




