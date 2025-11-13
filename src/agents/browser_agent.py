"""BrowserAgent: Web browser control for macOS"""

import structlog
from appscript import app as appscript_app
from typing import List, Dict

logger = structlog.get_logger()


def browser_open_url(url: str, browser: str = "Safari") -> str:
    """Open a URL in the specified browser.

    Args:
        url: The URL to open (e.g., "https://google.com")
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        appscript_app(browser).open_location(url)
        result = f"Opened {url} in {browser}"
        logger.info("browser_open_url executed", url=url, browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to open URL in {browser}: {str(e)}"
        logger.error("browser_open_url failed", url=url, browser=browser, error=str(e))
        return error_msg


def browser_close_tab(browser: str = "Safari") -> str:
    """Close the current tab in the browser.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        appscript_app(browser).windows[1].current_tab.close()
        result = f"Closed tab in {browser}"
        logger.info("browser_close_tab executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to close tab in {browser}: {str(e)}"
        logger.error("browser_close_tab failed", browser=browser, error=str(e))
        return error_msg


def browser_new_tab(url: str, browser: str = "Safari") -> str:
    """Open a new tab with the specified URL.

    Args:
        url: The URL to open in new tab
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        # For Safari - use AppleScript: tell window 1 to make new tab with properties
        if browser.lower() == "safari":
            safari = appscript_app(browser)
            # Make new tab in first window with URL property
            safari.windows[1].make(new='tab', with_properties={'URL': url})
        else:
            # For Chrome/Firefox
            appscript_app(browser).open_location(url)

        result = f"Opened new tab with {url} in {browser}"
        logger.info("browser_new_tab executed", url=url, browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to open new tab in {browser}: {str(e)}"
        logger.error("browser_new_tab failed", url=url, browser=browser, error=str(e))
        return error_msg


def browser_get_current_url(browser: str = "Safari") -> str:
    """Get the current URL from the active tab.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        The current URL or error description
    """
    try:
        if browser.lower() == "safari":
            url = appscript_app(browser).windows[1].current_tab.URL()
        else:
            url = appscript_app(browser).windows[1].active_tab.URL()

        result = f"Current URL: {url}"
        logger.info("browser_get_current_url executed", browser=browser, url=url, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to get current URL from {browser}: {str(e)}"
        logger.error("browser_get_current_url failed", browser=browser, error=str(e))
        return error_msg


def browser_get_page_title(browser: str = "Safari") -> str:
    """Get the title of the current page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        The page title or error description
    """
    try:
        if browser.lower() == "safari":
            title = appscript_app(browser).windows[1].current_tab.name()
        else:
            title = appscript_app(browser).windows[1].active_tab.title()

        result = f"Page title: {title}"
        logger.info("browser_get_page_title executed", browser=browser, title=title, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to get page title from {browser}: {str(e)}"
        logger.error("browser_get_page_title failed", browser=browser, error=str(e))
        return error_msg


def browser_reload(browser: str = "Safari") -> str:
    """Reload the current page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_JavaScript(
                "location.reload()",
                in_=appscript_app(browser).windows[1].current_tab
            )
        else:
            appscript_app(browser).reload()

        result = f"Reloaded page in {browser}"
        logger.info("browser_reload executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to reload page in {browser}: {str(e)}"
        logger.error("browser_reload failed", browser=browser, error=str(e))
        return error_msg


def browser_scroll_down(browser: str = "Safari", amount: int = 300) -> str:
    """Scroll down on the current page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari
        amount: Pixels to scroll down. Default: 300

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_JavaScript(
                f"window.scrollBy(0, {amount})",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Scrolled down {amount}px in {browser}"
        logger.info("browser_scroll_down executed", browser=browser, amount=amount, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to scroll in {browser}: {str(e)}"
        logger.error("browser_scroll_down failed", browser=browser, error=str(e))
        return error_msg


def browser_scroll_up(browser: str = "Safari", amount: int = 300) -> str:
    """Scroll up on the current page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari
        amount: Pixels to scroll up. Default: 300

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_JavaScript(
                f"window.scrollBy(0, -{amount})",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Scrolled up {amount}px in {browser}"
        logger.info("browser_scroll_up executed", browser=browser, amount=amount, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to scroll in {browser}: {str(e)}"
        logger.error("browser_scroll_up failed", browser=browser, error=str(e))
        return error_msg


def browser_scroll_to_top(browser: str = "Safari") -> str:
    """Scroll to the top of the page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_JavaScript(
                "window.scrollTo(0, 0)",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Scrolled to top in {browser}"
        logger.info("browser_scroll_to_top executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to scroll in {browser}: {str(e)}"
        logger.error("browser_scroll_to_top failed", browser=browser, error=str(e))
        return error_msg


def browser_scroll_to_bottom(browser: str = "Safari") -> str:
    """Scroll to the bottom of the page.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_JavaScript(
                "window.scrollTo(0, document.body.scrollHeight)",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Scrolled to bottom in {browser}"
        logger.info("browser_scroll_to_bottom executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to scroll in {browser}: {str(e)}"
        logger.error("browser_scroll_to_bottom failed", browser=browser, error=str(e))
        return error_msg


def browser_find_text(text: str, browser: str = "Safari") -> str:
    """Find text on the current page.

    Args:
        text: The text to search for
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_JavaScript(
                f"window.find('{text}')",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Searched for '{text}' in {browser}"
        logger.info("browser_find_text executed", text=text, browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to find text in {browser}: {str(e)}"
        logger.error("browser_find_text failed", text=text, browser=browser, error=str(e))
        return error_msg


def browser_click_link(text: str, browser: str = "Safari") -> str:
    """Click a link by its visible text content.

    Args:
        text: The text content of the link to click
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            js_code = f"""
            var links = Array.from(document.querySelectorAll('a'));
            var link = links.find(a => a.textContent.includes('{text}'));
            if (link) {{
                link.click();
                'clicked';
            }} else {{
                'not found';
            }}
            """
            result_js = appscript_app(browser).do_JavaScript(
                js_code,
                in_=appscript_app(browser).windows[1].current_tab
            )

            if result_js == 'clicked':
                msg = f"Clicked link containing '{text}' in {browser}"
                logger.info("browser_click_link executed", text=text, browser=browser, success=True)
                return msg
            else:
                msg = f"Link containing '{text}' not found"
                logger.warning("browser_click_link failed", text=text, browser=browser, error="Link not found")
                return msg
    except Exception as e:
        error_msg = f"Failed to click link in {browser}: {str(e)}"
        logger.error("browser_click_link failed", text=text, browser=browser, error=str(e))
        return error_msg


def browser_go_back(browser: str = "Safari") -> str:
    """Navigate back in browser history.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_JavaScript(
                "history.back()",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Navigated back in {browser}"
        logger.info("browser_go_back executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to go back in {browser}: {str(e)}"
        logger.error("browser_go_back failed", browser=browser, error=str(e))
        return error_msg


def browser_go_forward(browser: str = "Safari") -> str:
    """Navigate forward in browser history.

    Args:
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).do_JavaScript(
                "history.forward()",
                in_=appscript_app(browser).windows[1].current_tab
            )

        result = f"Navigated forward in {browser}"
        logger.info("browser_go_forward executed", browser=browser, success=True)
        return result
    except Exception as e:
        error_msg = f"Failed to go forward in {browser}: {str(e)}"
        logger.error("browser_go_forward failed", browser=browser, error=str(e))
        return error_msg


def browser_switch_tab(index: int, browser: str = "Safari") -> str:
    """Switch to a specific tab by index.

    Args:
        index: Tab index (1-based, 1 is first tab)
        browser: Browser name (Safari, Chrome, Firefox). Default: Safari

    Returns:
        A success message or error description
    """
    try:
        if browser.lower() == "safari":
            appscript_app(browser).windows[1].current_tab.set(
                appscript_app(browser).windows[1].tabs[index]
            )
            result = f"Switched to tab {index} in {browser}"
            logger.info("browser_switch_tab executed", index=index, browser=browser, success=True)
            return result
        else:
            return f"Tab switching not supported for {browser}. Only Safari is supported."
    except Exception as e:
        error_msg = f"Failed to switch tab in {browser}: {str(e)}"
        logger.error("browser_switch_tab failed", index=index, browser=browser, error=str(e))
        return error_msg


class BrowserAgent:
    """Agent for web browser control"""

    @classmethod
    def get_tool_functions(cls) -> List[callable]:
        """Return list of tool functions for Ollama SDK"""
        return [
            browser_open_url,
            browser_close_tab,
            browser_new_tab,
            browser_get_current_url,
            browser_get_page_title,
            browser_reload,
            browser_scroll_down,
            browser_scroll_up,
            browser_scroll_to_top,
            browser_scroll_to_bottom,
            browser_find_text,
            browser_click_link,
            browser_go_back,
            browser_go_forward,
            browser_switch_tab,
        ]

    @classmethod
    def get_available_functions(cls) -> Dict[str, callable]:
        """Return dictionary mapping function names to callables"""
        return {
            'browser_open_url': browser_open_url,
            'browser_close_tab': browser_close_tab,
            'browser_new_tab': browser_new_tab,
            'browser_get_current_url': browser_get_current_url,
            'browser_get_page_title': browser_get_page_title,
            'browser_reload': browser_reload,
            'browser_scroll_down': browser_scroll_down,
            'browser_scroll_up': browser_scroll_up,
            'browser_scroll_to_top': browser_scroll_to_top,
            'browser_scroll_to_bottom': browser_scroll_to_bottom,
            'browser_find_text': browser_find_text,
            'browser_click_link': browser_click_link,
            'browser_go_back': browser_go_back,
            'browser_go_forward': browser_go_forward,
            'browser_switch_tab': browser_switch_tab,
        }
