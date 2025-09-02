
from pathlib import Path
import os,sys
from configparser import ConfigParser
curr_file_path = Path(__file__)
root_dir = curr_file_path.parent.parent.absolute()
sys.path.append(str(root_dir))
con = ConfigParser()
con.read(f"{root_dir}/Configuration/application.properties")

class ConfigVariables:
    MARKER_DATA = con.get('FILE','MARKER_TEST_DATA')
    ZOOM_DATA = con.get('FILE', 'ZOOM_TEST_DATA')
    SEARCH_DATA = con.get('FILE', 'SEARCH_TEST_DATA')
    LOAD_DATA = con.get('FILE', 'LOAD_TEST_DATA')
