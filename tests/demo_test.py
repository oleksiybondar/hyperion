# import pytest
# from hyperiontf.executors.pytest import automatic_log_setup  # noqa: F401
# from page_objects.calculator.calculator import (
#     WebCalculator,
#     MobileCalculator,
#     DesktopCalculator,
#     HybridCalculator,
# )
# from hyperiontf import expect
# import os
# from misc.simple_http_server import SimpleHTTPServer
#
# dirname = os.path.dirname(__file__)
# resources_dir = os.path.join(dirname, "resources/test_pages/")
# calculator_page = os.path.join(dirname, "resources/test_pages/calculator.html")
# calculator_url = f"file://{calculator_page}"
# calculator_http_url = "http://localhost:8000/resources/test_pages/calculator.html"
#
#
# @pytest.fixture
# def server():
#     server_instance = SimpleHTTPServer(resources_dir)
#     server_instance.start()
#     yield server_instance
#     server_instance.stop()
#
#
# def actual_test_case(page):
#     page.evaluate_expression(5.6, "+", 10.4)
#     result = page.get_result()
#     expect(result).to_be(16)
#
#
# @pytest.mark.tags("Web", "Calculator", "Cross-platform", "Selenium")
# def test_web_calculator():
#     """
#     Demo test to show that a single Page Object can be applied to a Web application.
#     Demonstrates coverage for applications that may have different designs but align in functionality.
#     """
#     page = WebCalculator.start_browser()
#     page.open(calculator_url)
#     actual_test_case(page)
#
#
# @pytest.mark.tags("Mobile", "Calculator", "Android", "Cross-platform", "Appium")
# def test_mobile_android_calculator():
#     """
#     Demo test to show that a single Page Object can be applied to a Mobile Android application.
#     Demonstrates coverage for applications that may have different designs but align in functionality.
#     Note: The caps specified are for very specific local runtime environments and may need modification to work in
#           different environments.
#     """
#     caps = {
#         "automation": "appium",
#         "automationName": "UiAutomator2",
#         "platformName": "Android",
#         "platformVersion": "12.0",
#         "appPackage": "com.google.android.calculator",
#         "appActivity": "com.android.calculator2.Calculator",
#         "uiautomator2ServerInstallTimeout": 60000,
#     }
#     page = MobileCalculator.launch_app(caps)
#     actual_test_case(page)
#
#
# @pytest.mark.tags(
#     "Mobile", "Web", "HybridApp", "iOS", "Calculator", "Cross-platform", "Appium"
# )
# def test_hybrid_calculator(server):
#     """
#     Demo test to show a Hybrid application using iOS + Safari.
#     Demonstrates coverage for the same application functionality across different stacks.
#     P.S. The iOS simulator does not ship with a calculator app, so this demo is used to illustrate automatic content
#          switching and page object descriptions.
#     Note: The caps specified are for very specific local runtime environments and may need modification to work in
#           different environments.
#     """
#     caps = {
#         "automation": "appium",
#         "automationName": "XCUITest",
#         "platformName": "iOS",
#         "deviceName": "iPhone 14",
#         "bundleId": "com.apple.mobilesafari",
#         "includeSafariInWebviews": True,
#         "wdaLaunchTimeout": 3000,
#         "usePrebuiltWDA": True,
#     }
#     page = HybridCalculator.launch_app(caps)
#     page.open_url(calculator_http_url)
#     actual_test_case(page)
#
#
# @pytest.mark.tags("Desktop", "Calculator", "Cross-platform", "Appium")
# def test_mac_os_calculator():
#     """
#     Demo test to show that a single Page Object can be applied to a Desktop (Mac OS) application.
#     Demonstrates coverage for applications that may have different designs but align in functionality.
#     Note: The caps specified are for very specific local runtime environments and may need modification to work in
#           different environments.
#     """
#     caps = {
#         "automation": "appium",
#         "automationName": "Mac2",
#         "platformName": "Mac",
#         "deviceName": "Mac",
#         "bundleId": "com.apple.calculator",
#         "remote_url": "http://10.211.55.2:4723"
#     }
#     page = DesktopCalculator.launch_app(caps)
#     actual_test_case(page)
#
#
# @pytest.mark.tags("Web", "Calculator", "Cross-platform", "Playwright")
# def test_web_calculator_with_playwright():
#     """
#     Demo test to show that a single Page Object can be applied to a Web application.
#     Demonstrates coverage for applications that may have different designs but align in functionality.
#     """
#     caps = {"automation": "playwright", "browser": "webkit"}
#     page = WebCalculator.start_browser(caps)
#     page.open(calculator_url)
#     actual_test_case(page)
