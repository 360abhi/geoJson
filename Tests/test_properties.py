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

@pytest.mark.parametrize("test_case", CommonUtils().load(ConfigVariables.PROPERTY_DATA))
def test_properties(page: Page, test_case):
    try:
        validations = Validations(page)
        home = Home(page)
        page.goto(test_case['map_url'])
        validations.validate_map_loaded(test_case['tc_id'])
        home.select_marker_tool()
        home.place_marker_by_ratio()
        validations.verify_marker_exist_in_map()
        num = home.add_properties(properties=test_case['properties'])
        actual_list = home.fetch_properties(num)
        expected_list = [item for pair in test_case['properties'].items() for item in pair]
        validations.validate_properties(expected=expected_list,actual=actual_list)
    except Exception as exc:
        print(str(exc))
        raise exc

    


