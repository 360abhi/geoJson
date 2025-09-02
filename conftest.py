import logging
import shutil
from pathlib import Path
import pytest
import sys
from playwright.sync_api import Page
from Browser.BrowserManager import BrowserManager
import Configuration.ConfigVariables as config

curr_file_path = Path(__file__)
root_dir = curr_file_path.parent.parent.absolute()
sys.path.append(str(root_dir))



@pytest.fixture(scope="session")
def browser_manager():
    manager = BrowserManager()
    yield manager
    manager.close_browser()


@pytest.fixture(scope="function")
def page(request, browser_manager):
    test_case = request.getfixturevalue('test_case')
    context, pg, trace_path = browser_manager.get_page(test_case)

    yield pg
    context.tracing.stop(path=str(trace_path))
    # video_path = pg.video.path()
    # unique_id = test_case.get("tc_id", "unknown_id")
    print(f"Tracing stopped and saved to {trace_path}")
    pg.close()
    context.close()
    # shutil.move(video_path, f"{root_dir}/videos/{unique_id}.webm")
