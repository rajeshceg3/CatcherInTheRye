import time
from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a large viewport to ensure sidebar is likely open
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        print("Navigating to app...")
        page.goto("http://localhost:8501")

        # Wait for the app to load
        print("Waiting for app to load...")
        page.wait_for_selector("text=The Catcher in the Rye", timeout=10000)

        # Look for the Start Guided Tour button in the sidebar
        print("Looking for Start Guided Tour button...")
        # We look for a button that contains the text.
        start_btn = page.locator('button:has-text("Start Guided Tour")')

        try:
            start_btn.wait_for(state="visible", timeout=5000)
            print("Found Start Guided Tour button.")
        except:
            print("Start Guided Tour button not visible immediately.")
            # If sidebar is collapsed, we might need to open it.
            # But with 1920px width, it should be open.
            # Let's take a screenshot to debug if we fail here.
            page.screenshot(path="debug_initial.png")
            print("Saved debug_initial.png")

            # Try to force sidebar open if we can identify the trigger?
            # Or just proceed and hope the JS click works (it worked before).

        print("Clicking Start Guided Tour button...")
        # Use JS click to avoid viewport issues if it's slightly off-screen or obscured
        start_btn.evaluate("element => element.click()")

        # Wait for the tour overlay to appear
        print("Waiting for Tour Overlay...")
        # The tour overlay has "Step 1 of 7" text.
        try:
            page.wait_for_selector("text=Step 1 of 7", timeout=10000)
            print("Tour overlay found: 'Step 1 of 7' is visible.")
        except:
            print("Timeout waiting for 'Step 1 of 7'.")
            page.screenshot(path="verification_failed_overlay.png")
            print("Saved verification_failed_overlay.png")

            # Check if maybe the "Next" button is there
            if page.locator('button:has-text("Next")').is_visible():
                 print("Found 'Next' button though.")
            else:
                 print("Did not find 'Next' button either.")

            browser.close()
            exit(1)

        # Check for the Next button
        print("Checking for Next button...")
        next_btn = page.locator('button:has-text("Next")')
        if next_btn.is_visible():
            print("Next button is visible.")
            page.screenshot(path="tour_success.png")
            print("Saved tour_success.png")
        else:
            print("Next button not found.")
            exit(1)

        print("Tour UI verification successful!")
        browser.close()

if __name__ == "__main__":
    run_test()
