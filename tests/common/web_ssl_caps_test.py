import pytest

from hyperiontf.ui.adapters.selenium.page import Page as SeleniumPage


def test_selenium_chrome_caps_set_accept_insecure_certs_true_by_default():
    options = SeleniumPage.process_chrome_caps({})
    assert options.capabilities.get("acceptInsecureCerts") is True


def test_selenium_chrome_caps_set_accept_insecure_certs_false_when_disabled():
    options = SeleniumPage.process_chrome_caps({"accept_ssl_certificate_errors": False})
    assert options.capabilities.get("acceptInsecureCerts") is False


def test_selenium_firefox_caps_set_accept_insecure_certs_true_by_default():
    options = SeleniumPage.process_firefox_caps({})
    assert options.capabilities.get("acceptInsecureCerts") is True


def test_selenium_firefox_caps_set_accept_insecure_certs_false_when_disabled():
    options = SeleniumPage.process_firefox_caps(
        {"accept_ssl_certificate_errors": False}
    )
    assert options.capabilities.get("acceptInsecureCerts") is False


@pytest.mark.web
def test_playwright_context_sets_ignore_https_errors_from_caps(monkeypatch):
    playwright_api = pytest.importorskip("playwright.sync_api")
    assert playwright_api is not None

    from hyperiontf.ui.adapters.playwright.page import Page as PlaywrightPage

    captured = {}

    class DummyContext:
        def new_page(self):
            return object()

    class DummyBrowserInstance:
        def new_context(self, **kwargs):
            captured["new_context_kwargs"] = kwargs
            return DummyContext()

    class DummyBrowserFactory:
        def launch(self, **kwargs):
            captured["launch_kwargs"] = kwargs
            return DummyBrowserInstance()

    class DummyService:
        chromium = DummyBrowserFactory()
        firefox = DummyBrowserFactory()
        webkit = DummyBrowserFactory()

    monkeypatch.setattr(
        PlaywrightPage,
        "start_playwright",
        staticmethod(lambda: DummyService()),
    )

    PlaywrightPage.start_browser(
        "chrome",
        {"headless": True, "accept_ssl_certificate_errors": False},
    )

    assert captured["launch_kwargs"]["headless"] is True
    assert captured["new_context_kwargs"]["ignore_https_errors"] is False
