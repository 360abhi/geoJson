from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://geojson.io/")

    # Click the "Point" button from toolbar
    # page.click("a[title='Add a marker']")

    # Click somewhere on the canvas
        # Get the bounding box of the canvas element
    canvas = page.query_selector('canvas.mapboxgl-canvas')
    bbox = canvas.bounding_box()
    page.locator("//button[@title='Draw Point (m)']").click()

    # Click at specific coordinates relative to the canvas
    x = bbox['x'] + bbox['width'] * 0.5  # Center X
    y = bbox['y'] + bbox['height'] * 0.5  # Center Y
    page.mouse.click(x, y)

    # Or using the canvas element directly
    canvas.click(position={'x': 100, 'y': 200})

    # Verify JSON updated with "Point"
    # assert "Point" in page.locator(".json-editor").inner_text()

    browser.close()
