import os
import socket
import subprocess
import sys
import time

import pytest
from playwright.sync_api import expect, sync_playwright

BASE_URL = "http://localhost:8080/index.html"
APP_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
PORT = 8080


def _port_is_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        return sock.connect_ex(("127.0.0.1", port)) == 0


@pytest.fixture(scope="session", autouse=True)
def http_server():
    """Serve the application under test locally.

    Skipped if something is already listening on the port.
    """
    if _port_is_open(PORT):
        yield
        return

    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=APP_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(100):
            if _port_is_open(PORT):
                break
            time.sleep(0.1)
        else:
            raise RuntimeError(f"HTTP server did not start on port {PORT}")
        yield
    finally:
        proc.terminate()
        proc.wait(timeout=5)


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


@pytest.fixture()
def issues_page(page):
    """Navigate from index.html to the fully loaded Data Issues grid.

    Returns a FrameLocator for the innermost application frame.
    """
    page.goto(BASE_URL)

    # Dismiss the welcome modal (appears ~800ms after load).
    page.get_by_role("button", name="Got it").click()

    # The app is nested two iframes deep:
    # index.html -> #outerFrame (vf-container.html) -> #appFrame (app.html)
    app = page.frame_locator("#outerFrame").frame_locator("#appFrame")

    app.get_by_role("button", name="Review & Fix Issues").click()

    # The grid renders after a random delay (up to 5s).
    cards = app.locator(".issue-card")
    cards.first.wait_for(timeout=15000)
    expect(cards).to_have_count(10, timeout=15000)
    return app
