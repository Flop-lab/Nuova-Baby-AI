"""BrowserAgent: Web browser control for macOS"""

import subprocess
import structlog
from appscript import app as appscript_app, k
from typing import List, Callable

logger = structlog.get_logger()


def browser_new_tab(browser: str = "Safari") -> str:
    """Open a new tab in the browser with the user's configured homepage.

    This command:
    1. Reads the homepage URL from browser preferences
    2. Creates a new tab in the specified browser
    3. Loads the homepage in the new tab

    Args:
        browser: Browser name (default: "Safari")

    Returns:
        A success message or error description
    """
    try:
        logger.info("browser_new_tab_start", browser=browser)

        # Step 1: Read homepage from Safari preferences
        logger.info("browser_new_tab_reading_preferences", browser=browser)
        result = subprocess.run(
            ['defaults', 'read', 'com.apple.Safari', 'HomePage'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            # Fallback to default homepage if preference not set
            homepage = "https://www.google.com"
            logger.warning(
                "browser_new_tab_no_homepage",
                browser=browser,
                message="Could not read homepage preference, using default"
            )
        else:
            homepage = result.stdout.strip()
            logger.info("browser_new_tab_homepage_read", browser=browser, homepage=homepage)

        # Step 2 & 3: Create new tab and load homepage
        # Use explicit path to avoid Cryptexes path issues
        logger.info("browser_new_tab_importing_appscript", browser=browser)
        safari = appscript_app('/Applications/Safari.app')
        logger.info("browser_new_tab_appscript_loaded", browser=browser, safari_obj=str(type(safari)))

        logger.info("browser_new_tab_creating_tab", browser=browser)
        safari.windows[1].make(new=k.tab)
        logger.info("browser_new_tab_tab_created", browser=browser)

        logger.info("browser_new_tab_setting_url", browser=browser, url=homepage)
        safari.windows[1].current_tab.URL.set(homepage)
        logger.info("browser_new_tab_url_set", browser=browser)

        logger.info(
            "browser_new_tab executed",
            browser=browser,
            homepage=homepage,
            success=True
        )
        return f"Opened new tab in {browser} with homepage: {homepage}"

    except Exception as e:
        error_msg = f"Failed to open new tab in {browser}: {str(e)}"
        logger.error("browser_new_tab failed", browser=browser, error=str(e), error_type=type(e).__name__)
        return error_msg


class BrowserAgent:
    """Agent for web browser control"""

    @classmethod
    def get_tool_functions(cls) -> List[Callable]:
        """Return list of tool functions for Ollama SDK"""
        return [
            browser_new_tab,
        ]

    @classmethod
    def get_available_functions(cls) -> dict:
        """Return dictionary mapping function names to callables"""
        return {
            'browser_new_tab': browser_new_tab,
        }
