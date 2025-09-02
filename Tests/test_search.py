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


@pytest.mark.parametrize("test_case", CommonUtils().load(ConfigVariables.SEARCH_DATA))
def test_search(page: Page, test_case):
    try:
        validations = Validations(page)
        home = Home(page)
        page.goto(test_case['map_url'])
        validations.validate_map_loaded(test_case['tc_id'])
        home.search_location(test_case['search_query'])
        validations.verify_search_marker(expected_coords=test_case['expected_feature']['coordinates'])
    except Exception as exc:
        print(str(exc))
        raise exc




