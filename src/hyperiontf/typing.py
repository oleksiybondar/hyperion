from typing import Type, Union, TypeVar, Literal

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Browser Section
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

BrowserType = Literal[
    "chrome",
    "firefox",
    "edge",
    "safari",
    "electron",
    "chromium",
    "webkit",
    "remote",
    "windows application driver",
]


class Browser:
    CHROME: BrowserType = "chrome"
    FIREFOX: BrowserType = "firefox"
    EDGE: BrowserType = "edge"
    SAFARI: BrowserType = "safari"
    ELECTRON: BrowserType = "electron"
    CHROMIUM: BrowserType = "chromium"
    WEBKIT: BrowserType = "webkit"
    REMOTE: BrowserType = "remote"
    WIN_APP_DRIVER: BrowserType = "windows application driver"


# Browser families
CHROME_FAMILY = [Browser.CHROME, Browser.CHROMIUM, Browser.ELECTRON]
FIREFOX_FAMILY = [Browser.FIREFOX]
EDGE_FAMILY = [Browser.EDGE]
SAFARI_FAMILY = [Browser.SAFARI, Browser.WEBKIT]
REMOTE_FAMILY = [Browser.REMOTE, Browser.WIN_APP_DRIVER]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Automation types section
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


AutomationToolType = Literal[
    "selenium",
    "playwright",
    "appium",
    "autoit",
    "xdotool",
    "pyautogui",
    "windows application driver",
]


class AutomationTool:
    SELENIUM: AutomationToolType = "selenium"
    PLAYWRIGHT: AutomationToolType = "playwright"
    APPIUM: AutomationToolType = "appium"
    AUTOIT: AutomationToolType = "autoit"
    XDOTOOL: AutomationToolType = "xdotool"
    PYAUTOGUI: AutomationToolType = "pyautogui"
    WIN_APP_DRIVER: AutomationToolType = "windows application driver"


PlatformType = Literal[
    "web",
    "mobile",
    "desktop",
]


class Platform:
    WEB: PlatformType = "web"
    MOBILE: PlatformType = "mobile"
    DESKTOP: PlatformType = "desktop"


# Platform families
WEB_FAMILY = [AutomationTool.SELENIUM, AutomationTool.PLAYWRIGHT]
MOBILE_FAMILY = [AutomationTool.APPIUM]
DESKTOP_FAMILY = [
    AutomationTool.APPIUM,
    AutomationTool.AUTOIT,
    AutomationTool.XDOTOOL,
    AutomationTool.PYAUTOGUI,
    AutomationTool.WIN_APP_DRIVER,
]

WIN_APP_DRIVER_ROOT_HANDLE: str = "---root---"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Log Sources
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class LoggerSource:
    TEST_CASE: str = "TestCase"
    FIXTURE: str = "Fixture"
    PAGE_OBJECT: str = "PageObject"
    WEB_PAGE: str = "WebPage"
    MOBILE_SCREEN: str = "MobileScreen"
    DESKTOP_SCREEN: str = "DesktopScreen"
    ELEMENT: str = "Element"
    WIDGET: str = "Widget"
    IFRAME: str = "IFrame"
    WEB_VIEW: str = "WebView"
    EXPECT: str = "Expect"
    SILENT_FAILURES: str = "SilentFailures"
    REST_CLIENT: str = "RestClient"
    WIN_APP_DRIVER: str = "WindowsApplicationDriverClient"
    ACTION_BUILDER: str = "ActionBuilder"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Page Object Harness Typing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

LocatorStrategiesType = Literal[
    "id",
    "xpath",
    "link text",
    "partial link text",
    "name",
    "tag name",
    "class name",
    "css selector",
    "ios class chain",
    "ios predicate",
    "android datamatcher",
    "android uiautomator",
    "android viewtag",
    "android viewmatcher",
    "accessibility id",
    "script",
    "data-testid",
    "elements item",
    "automation id",
    "unsupported",
]


class LocatorStrategies:
    """
    Enumeration of locator strategies used for element identification in Selenium and Playwright.
    """

    ID: LocatorStrategiesType = "id"
    XPATH: LocatorStrategiesType = "xpath"
    LINK_TEXT: LocatorStrategiesType = "link text"
    PARTIAL_LINK_TEXT: LocatorStrategiesType = "partial link text"
    NAME: LocatorStrategiesType = "name"
    TAG_NAME: LocatorStrategiesType = "tag name"
    CLASS_NAME: LocatorStrategiesType = "class name"
    CSS_SELECTOR: LocatorStrategiesType = "css selector"
    IOS_CLASS_CHAINE: LocatorStrategiesType = "ios class chain"
    IOS_PREDICATE: LocatorStrategiesType = "ios predicate"
    ANDROID_DATA_MATCHER: LocatorStrategiesType = "android datamatcher"
    ANDROID_UIAUTOMATOR: LocatorStrategiesType = "android uiautomator"
    ANDROID_VIEWTAG: LocatorStrategiesType = "android viewtag"
    ANDROID_VIEW_MATCHER: LocatorStrategiesType = "android viewmatcher"
    WINDOWS_ACCESSIBILITY_ID: LocatorStrategiesType = "accessibility id"
    SCRIPT: LocatorStrategiesType = "script"
    TEST_ID: LocatorStrategiesType = "data-testid"
    ELEMENTS_ITEM: LocatorStrategiesType = "elements item"
    UNSUPPORTED: LocatorStrategiesType = "unsupported"


Element = TypeVar("Element")
Elements = TypeVar("Elements")
# Corresponding class types
WebPage = TypeVar("WebPage")
MobileScreen = TypeVar("MobileScreen")
DesktopWindow = TypeVar("DesktopWindow")
Widget = TypeVar("Widget")
IFrame = TypeVar("IFrame")
WebView = TypeVar("WebView")

AnyWebPage = Type[WebPage]
AnyMobileScreen = Type[MobileScreen]
AnyDesktopScreen = Type[DesktopWindow]
AnyWidget = Type[Widget]
AnyIFrame = Type[IFrame]
AnyWebView = Type[WebView]
# Page object harness constants
AnyContentContainer = Union[AnyWebView, AnyWebPage]
AnyContextContainer = Union[AnyMobileScreen, AnyDesktopScreen]
AnyPageObject = Union[
    AnyWebPage, AnyMobileScreen, AnyDesktopScreen, AnyWidget, AnyIFrame, AnyWebView
]
# Defining AnyElement to be an Element, Elements, any widget, any iframe, or any web view
AnyElement = Union[Element, Elements, AnyWidget, AnyIFrame, AnyWebView]

DEFAULT_CONTENT: str = "default"

ViewportLabelType = Literal[
    "xs",
    "sm",
    "md",
    "lg",
    "xl",
    "xxl",
]


class ViewportLabel:
    XS: ViewportLabelType = "xs"
    SM: ViewportLabelType = "sm"
    MD: ViewportLabelType = "md"
    LG: ViewportLabelType = "lg"
    XL: ViewportLabelType = "xl"
    XXL: ViewportLabelType = "xxl"


APPIUM_DEFAULT_URL: str = "http://localhost:4723"

ContextType = Literal[
    "NATIVE_APP",
    "web",
]


class Context:
    NATIVE: ContextType = "NATIVE_APP"
    WEB: ContextType = "web"


AppiumAutomationNameType = Literal[
    "UiAutomator1",
    "UiAutomator2",
    "XCUITest",
    "Mac",
    "Windows",
    "Espresso",
]


class AppiumAutomationName:
    UIAUTOMATOR1: AppiumAutomationNameType = "UiAutomator1"
    UIAUTOMATOR2: AppiumAutomationNameType = "UiAutomator2"
    XCUITest: AppiumAutomationNameType = "XCUITest"
    MAC: AppiumAutomationNameType = "Mac"
    WINDOWS_APP_DRIVER: AppiumAutomationNameType = "Windows"
    ESPRESSO: AppiumAutomationNameType = "Espresso"


ANDROID_AUTOMATION_FAMILY = [
    AppiumAutomationName.UIAUTOMATOR1,
    AppiumAutomationName.UIAUTOMATOR2,
    AppiumAutomationName.ESPRESSO,
]
IOS_AUTOMATION_FAMILY = [AppiumAutomationName.XCUITest]

OSType = Literal[
    "Windows",
    "Darwin",  # platform.system() returns 'Darwin' for macOS
    "Linux",
    "Android",
    "iOS",
]


class OS:
    WINDOWS: OSType = "Windows"
    MAC: OSType = "Darwin"  # platform.system() returns 'Darwin' for macOS
    LINUX: OSType = "Linux"
    ANDROID: OSType = "Android"
    IOS: OSType = "iOS"


# OS Families
DESKTOP_OS_FAMILY = [OS.WINDOWS, OS.MAC, OS.LINUX]
MOBILE_OS_FAMILY = [OS.ANDROID, OS.IOS]

MouseButtonType = Literal["left", "middle", "right", "back", "forward"]


class MouseButton:
    LEFT: MouseButtonType = "left"
    MIDDLE: MouseButtonType = "middle"
    RIGHT: MouseButtonType = "right"
    BACK: MouseButtonType = "back"
    FORWARD: MouseButtonType = "forward"


TouchFingerType = Literal["one", "two", "three", "four", "five"]


class TouchFinger:
    ONE: TouchFingerType = "one"
    TWO: TouchFingerType = "two"
    THREE: TouchFingerType = "three"
    FOUR: TouchFingerType = "four"
    FIVE: TouchFingerType = "five"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Elements Query Language
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
ASTType = Literal[
    "logical_expression",
    "comparison",
    "element_chain",
    "attribute",
    "element",
    "string",
    "regex",
    "number",
    "bool",
    "date",
    "color",
]


class AST:
    LOGICAL_EXPRESSION: ASTType = "logical_expression"
    COMPARISON: ASTType = "comparison"
    ELEMENT_CHAIN: ASTType = "element_chain"
    ATTRIBUTE: ASTType = "attribute"
    ELEMENT: ASTType = "element"
    STRING: ASTType = "string"
    REGEX: ASTType = "regex"
    NUMBER: ASTType = "number"
    BOOL: ASTType = "bool"
    DATE: ASTType = "date"
    COLOR: ASTType = "color"


LogicalOperator = Literal["and", "or"]

ComparisonOperator = Literal["==", "!=", "~=", "<", "<=", ">", ">="]


class LogicalOp:
    AND: LogicalOperator = "and"
    OR: LogicalOperator = "or"


class ComparisonOp:
    EQUAL: ComparisonOperator = "=="
    NOTEQUAL: ComparisonOperator = "!="
    APPROX: ComparisonOperator = "~="
    LT: ComparisonOperator = "<"
    LE: ComparisonOperator = "<="
    GT: ComparisonOperator = ">"
    GE: ComparisonOperator = ">="


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Visual Section
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

VisualModeType = Literal[
    "collect",
    "compare",
]


class VisualMode:
    COLLECT: VisualModeType = "collect"
    COMPARE: VisualModeType = "compare"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Rest Client Typing
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

HTTPMethodType = Literal["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"]


class HTTPMethod:
    GET: HTTPMethodType = "GET"
    POST: HTTPMethodType = "POST"
    PUT: HTTPMethodType = "PUT"
    DELETE: HTTPMethodType = "DELETE"
    HEAD: HTTPMethodType = "HEAD"
    OPTIONS: HTTPMethodType = "OPTIONS"
    PATCH: HTTPMethodType = "PATCH"


AuthTypeType = Literal["basic", "digest", "jwt", "oauth"]


class AuthType:
    BASIC: AuthTypeType = "basic"
    DIGEST: AuthTypeType = "digest"
    JWT: AuthTypeType = "jwt"
    OAUTH: AuthTypeType = "oauth"


class HTTPHeader:
    ACCEPT = "Accept"
    CONTENT_TYPE = "Content-Type"
    AUTHORIZATION = "Authorization"
    USER_AGENT = "User-Agent"
    ACCEPT_ENCODING = "Accept-Encoding"
    ACCEPT_LANGUAGE = "Accept-Language"
    COOKIE = "Cookie"
    SET_COOKIE = "Set-Cookie"
    LOCATION = "Location"


class ContentType:
    JSON = "application/json"
    XML = "application/xml"
    PLAIN = "text/plain"
    HTML = "text/html"
    FORM_URLENCODED = "application/x-www-form-urlencoded"
    MULTIPART_FORM_DATA = "multipart/form-data"


TokenTypeType = Literal["Bearer", "MAC"]


class TokenType:
    BEARER: TokenTypeType = "Bearer"
    MAC: TokenTypeType = "MAC"


SuccessResponse = TypeVar("SuccessResponse")
RedirectResponse = TypeVar("RedirectResponse")
ErrorResponse = TypeVar("ErrorResponse")

Client = TypeVar("Client")

AnyClient = Type[Client]

Request = TypeVar("Request")
AnyRequest = Type[Request]

# Any Response
AnyResponse = Union[SuccessResponse, RedirectResponse, ErrorResponse]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Expect
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

ComparisonTypeType = Literal["assertion", "verification"]


class ComparisonType:
    ASSERTION: ComparisonTypeType = "assertion"
    VERIFICATION: ComparisonTypeType = "verification"


ExpectationStatusType = Literal["Pass", "Fail"]


class ExpectationStatus:
    PASS: ExpectationStatusType = "Pass"
    FAIL: ExpectationStatusType = "Fail"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Exceptions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class HyperionException(Exception):
    pass


class FailedExpectationException(HyperionException):
    pass


class TimeoutException(HyperionException):
    pass


class HyperionUIException(HyperionException):
    pass


class HyperionAPIException(HyperionException):
    pass


class ElementQueryLanguageParseException(HyperionException):
    pass


class ElementQueryLanguageBadOperatorException(HyperionException):
    pass


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# UI Exceptions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class UnsupportedAutomationTypeException(HyperionException):
    pass


class StaleElementReferenceException(HyperionUIException):
    pass


class NoSuchElementException(HyperionUIException):
    pass


class IncorrectLocatorException(HyperionUIException):
    pass


class ContentSwitchingException(HyperionUIException):
    pass


class ContextSwitchingException(HyperionUIException):
    pass


class UnknownUIException(HyperionUIException):
    pass


class UnsupportedLocatorException(HyperionUIException):
    pass


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# API Exceptions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class FailedHTTPRequestException(HyperionAPIException):
    pass


class ExceededRedirectionLimitException(HyperionAPIException):
    pass


class NotARedirectionException(HyperionAPIException):
    pass


class ConnectionErrorException(HyperionAPIException):
    pass


class JSONSchemaFailedAssertionException(HyperionAPIException):
    pass
