import pytest
from pathlib import Path
import os,sys
root = Path(__file__).parent.parent.absolute()
sys.path.append(str(root))
print(root)
from playwright.sync_api import Page
from utils.commonutils import CommonUtils
from utils.validation import Validations
from Pages.Home import Home
from Configuration.ConfigVariables import ConfigVariables

@pytest.mark.parametrize("test_case", CommonUtils().load(ConfigVariables.MARKER_DATA))
def test_markers(page: Page, test_case):
    try:
        validations = Validations(page)
        home = Home(page)

        page.goto(test_case['map_url'])
        home.select_marker_tool()
        validations.validate_map_loaded(test_case['tc_id'])
        home.place_marker_by_ratio(city_name=test_case['city_name'])
        validations.verify_marker_exists_in_editor(test_case['expected_feature']['coordinates'])
    except Exception as exc:
        print(str(exc))
        raise exc

    


