from pathlib import Path
import sys
from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext

curr_file_path = Path(__file__)
root_dir = curr_file_path.parent.parent.absolute()
sys.path.append(str(root_dir))


class BrowserManager:
    def __init__(self) -> None:
        self.playwright = sync_playwright().start()
        self.browser: Browser = self.playwright.chromium.launch(headless=False)

    def get_browser(self) -> Browser:
        return self.browser

    def get_page(self, test_case):
        unique_id = test_case.get("tc_id", "default_id")
        trace_filename = f"{unique_id}_trace.zip"
        trace_path = Path(__file__).parent / "traces" / trace_filename

        context = self.browser.new_context(
            record_video_dir=f"{root_dir}/videos/",
            viewport={"width": 1280, "height": 720},
            record_video_size={"width": 1920, "height": 1080}
        )
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        print(f"Started tracing for {unique_id}")

        page = context.new_page()
        return context, page, trace_path

    def close_browser(self):
        self.browser.close()
        self.playwright.stop()
        print("Browser and Playwright stopped.")
