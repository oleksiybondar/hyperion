# Hyperion Testing Framework

> "One Framework to unite them all, One Framework to streamline interfaces, One Framework to simplify the way and bring harmony in automation."

## Introduction

Hyperion Testing Framework is a robust Python testing platform designed to streamline the testing process. It offers an all-encompassing solution for web, mobile, and API automation testing. By promoting clean code design and maintaining a high degree of flexibility, Hyperion provides simple and efficient tools to write reliable tests, ultimately wrapping complexity behind its easy-to-use interface.

### Creator's Note

In the vast landscape of web and application development, having a versatile, robust, and adaptable testing framework is critical to ensure high-quality user experiences across multiple platforms. At the heart of the Hyperion Testing Framework, the motivation to address this need and more is firmly embedded.

The idea to create this framework was driven by the inherent redundancy in testing similar user flows across multiple platforms—web, iOS, Android, and desktop. Consider the scenario of many companies having multiple products or subsystems. In most cases, their client apps may be designed for various platforms but ultimately serve the same purposes and provide identical user flows. Some applications even have hybrid designs that function across mobile and desktop platforms, exemplifying the same principle.

Instead of reinventing the wheel by implementing the same flow for each client individually, a single comprehensive approach for all platforms makes more sense. The reusability that Hyperion offers allows testing common functionalities across different platforms efficiently while preserving the flexibility to cover platform-specific features separately.

Furthermore, when it comes to client-server apps, the backend services are common for all clients. The Hyperion Testing Framework extends beyond front-end testing and allows for backend API testing as well. Shared models codebase for test data preparation becomes a practical reality with Hyperion. Consequently, if a backend change occurs, you adjust the data preparation for all clients at once instead of fixing issues individually.

So, this is the rationale behind the Hyperion Testing Framework—creating a tool that can navigate the complexities of cross-platform testing with a focus on reusability and efficiency. The ambition of Hyperion is to provide a solution that allows for seamless, efficient testing across all platforms—because we believe in the power of comprehensive and integrated testing solutions.

## Key Features

1. **Hyperion Page Object Model (POM)**: Provides a high-level API for interacting with web pages or mobile apps, simplifies test creation and maintenance, and promotes code reuse. The framework enriches the POM with automatic page objects instantiation for straightforward test setup and writing.

2. **Automatic StaleElementError Recovery**: Allows tests to continue uninterrupted, even when elements go stale.

3. **Automatic Context Switching**: Manages content, context, and window switching automatically when working with child elements, simplifying interactions with elements that require context switching, such as iframes or new windows.

4. **Robust Error Handling and Reporting**: Generates detailed, clear reports and handles errors internally to aid troubleshooting and test review.

5. **Flexible and Versatile**: Supports web, mobile, and API automation testing, providing a unified interface for various testing requirements.

6. **Cross Browser and Platform Compatibility**: Ensures wide-ranging coverage of tests across different browsers and platforms.

The Hyperion Page Object Model is designed for ease of use, requiring minimal knowledge to create robust and reusable code. It shares similarities with frameworks like SitePrism (Ruby), but provides more capabilities and leverages Python's strengths.

### Page Object Harness

Hyperion provides base classes and decorator methods to allow testers to define tree-structured page objects, abstracting away automation intricacies.

**Base Classes**:
- Top-level entities: WebPage, MobileScreen, DesktopWindow
- Nested page objects class: Widget, IFrame, WebView
- Simple elements (usually instantiated by the framework's internal routine): Element, Elements

**Helpers**: @element, @elements, @widget, @widgets, @iframew, @iframes

**Special Object**: `By` object defines the locator strategy and extends the locator capabilities to enable cross-platform page object creation.

### Logging

Unconditional logging of all actions provides comprehensive information for debugging and maintains test proof. Custom formatters for the standard Python logger create readable and filterable HTML logs.

### REST Client for API Testing

An integrated REST client covered by automatic logging includes a built-in JSON schema verification helper in the Response class.

### Planned Features

- **Database Interface (DBI)**: A future database client with adapters for multiple databases and automatic logging. It will implement an MVC-like router with write protection rules, offering safe direct database access during testing.
- **Non-functional Testing**:
   - **Visual Testing**: Will allow the comparison of screenshots or elements on a screen to detect visual defects.
   - **Accessibility Testing**: Will assess the application's usability by people with disabilities.

## Getting Started

### Prerequisites

Hyperion requires Python 3.11 or above, which you can check with `python --version` in the terminal. In addition to Python, Hyperion works with several automation tools, including Selenium, Playwright, Appium, and AutoIt. Please install the tools relevant to your testing needs and their respective Python bindings. For local Selenium execution, install the webdriver_manager. For Appium, install and configure the Appium server and its Python binding.

### Installation

When published, you can install Hyperion via pip: `pip install hyperiontf`. After installing the main Hyperion package, install the additional tools relevant to your use case, such as Selenium, Playwright, Appium, and AutoIt.

### Configuration

The Hyperion Testing Framework offers extensive configuration options to customize the test automation environment according to your needs. Configuration parameters can be specified in a configuration file or imported directly into your test scripts.

#### Logging Configuration

```python
from hyperiontf import config

config.log.log_folder = 'logs'
config.log.intercept_selenium_logs = True
config.log.intercept_playwright_logs = True
config.log.intercept_appium_logs = True
```

#### Page Object Configuration

```python
from hyperiontf import config

config.page_object.log_private = True
config.page_object.viewport_xs = 0
config.page_object.viewport_sm = 576
config.page_object.viewport_md = 768
config.page_object.viewport_lg = 992
config.page_object.viewport_xl = 1200
config.page_object.viewport_xxl = 1400
```

#### Element Configuration

```python
from hyperiontf import config

config.element.search_attempts = 3
config.element.search_retry_timeout = 0.5
config.element.stale_recovery_timeout = 0.5
config.element.wait_timeout = 30
config.element.missing_timeout = 5
```

#### Web Capabilities Configuration

```python
from hyperiontf import config

config.web_capabilities.automation = 'selenium'
config.web_capabilities.browser = 'safari'
config.web_capabilities.headless = False
```

#### Mobile Capabilities Configuration

```python
from hyperiontf import config

config.mobile_capabilities.automation = 'appium'
config.mobile_capabilities.automation_name = 'Mac2'
config.mobile_capabilities.platform_name = 'iOS'
config.mobile_capabilities.device_name = 'iPhone 14'
config.mobile_capabilities.platform_version = '16.2'
config.mobile_capabilities.auto_accept_alerts = False
config.mobile_capabilities.new_command_timeout = 300
```

#### Desktop Capabilities Configuration

```python
from hyperiontf import config

config.desktop_capabilities.automation = 'appium'
config.desktop_capabilities.automation_name = 'appium'
config.desktop_capabilities.platform_name = 'Mac'
config.desktop_capabilities.device_name = 'Mac'
config.desktop_capabilities.platform_version = ''
config.desktop_capabilities.new_command_timeout = 300
```

To use a configuration file, create a file named `hyperion_config.yaml`, `hyperion_config.json`, or `hyperion_config.ini`, and populate it with the desired configuration parameters. Then, you can import the configuration settings into your test scripts using the `config` module.

```python
from hyperiontf import config
config.update_from_cfg_file('path/to/hyperion_config.yaml')
```

#### Viewport-Specific Locators in Hyperion POM

Modern web applications often employ responsive design to ensure that their interfaces look good and function well on a variety of devices with different screen sizes. This responsive behavior is typically achieved using CSS media queries, which apply different styles based on the viewport width. Consequently, a web page can have different layouts under different viewport sizes, which might present challenges during automated testing.

Hyperion Testing Framework acknowledges this common design practice and provides an elegant way to handle different layouts with its viewport-specific locators.

In Hyperion, you can define different locators for different viewport sizes. This is extremely useful when the layout of your application changes depending on the viewport, and different elements are used in each layout.

Hyperion follows the same viewport sizing conventions as Facebook's Bootstrap, including the `xs`, `sm`, `md`, `lg`, `xl`, and `xxl` sizes. When defining a locator, you can specify different `By` objects for each viewport size, returning them as a dictionary.

Here's an example of defining viewport-specific locators:

```python
from hyperiontf import WebPage, element, By

class MyWebPage(WebPage):

    @element
    def responsive_button(self):
        return {
            'xs': By.css('#button-xs'),
            'md': By.css('#button-md'),
            'xl': By.css('#button-xl'),
            'default': By.css('#button-default')
        }
```

In this example, `responsive_button` will use different locators depending on the current viewport. When the viewport is `xs`, it will use the locator `By.css('#button-xs')`, when it is `md`, it will use `By.css('#button-md')`, and when it is `xl`, it will use `By.css('#button-xl')`. If the viewport is `lg`, `xxl`, or any other size, it will use the default locator `By.css('#button-default')`.

It's important to note that if a viewport-specific locator is not defined for a particular size and there is no default locator provided, Hyperion will raise an exception. Therefore, you must define locators for all viewport sizes or provide a 'default' locator to be used for those viewport sizes for which a specific locator is not defined.

This level of flexibility allows for precise control over element location under different viewport sizes, making your test scripts more robust and reliable across different devices and screen sizes.

This feature, along with automatic context switching for iframes and WebViews, is part of Hyperion's commitment to making automation testing as smooth and effortless as possible.

In the upcoming sections, we will delve into more advanced features of the Hyperion Testing Framework. Stay tuned!


## Basic Usage

Refer to the earlier section under the key features where the basic usage is outlined, demonstrating how to define a page object, interact with UI elements, and define a pytest test case using Hyperion. The framework's advanced features, such as automatic stale element recovery and context switching, can be utilized to create more robust and maintainable tests. For complex scenarios, refer to the advanced usage guide and comprehensive test examples provided.

### Examples of Usage

1. **Define a Page Object**: Start by defining a page object for each page (or part of a page) in your application. In Hyperion Testing Framework, the elements on the page are defined as class methods using the `@element` decorator and the `By` object from Selenium to specify how to locate the element:

```python
from hyperiontf import WebPage, element, By

class LoginPage(WebPage):

    @element
    def username_field(self):
        return By.id("username")

    @element
    def password_field(self):
        return By.id("password")
        
    @element
    def login_button(self):
        return By.id("login")

    
    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
```

2. **Define a Test Case with Pytest**: Define your test cases using pytest and Hyperion Testing Framework:

```python
import pytest
from hyperiontf.executors.pytest import automatic_log_setup, fixture
from page_objects.login_page import LoginPage

# The browser to use for the tests
browser = 'chrome'

# The URL of the login page
login_page_url = 'https://example.com/login'

@fixture(scope='function', log=False)
def login_page():
    page = LoginPage.start_browser(browser)
    page.open(login_page_url)
    yield page
    page.quit()


@pytest.mark.Login
@pytest.mark.TextFields 
@pytest.mark.Button
def test_login(login_page):
    """
    Test the login functionality. Using direct elements accessors. 
    """
    login_page.username_field.fill('my_username')
    login_page.password_field.fill('my_password')
    login_page.login_button.click()


@pytest.mark.Login
@pytest.mark.TextFields 
@pytest.mark.Button
def test_login2(login_page):
    """
    Test the login functionality. Using page object method. 
    """
    login_page.login('my_username', 'my_password')
```

In this example, pytest is used as the testing framework. The Hyperion Testing Framework pytest helper `automatic_log_setup` enables automatic logging for each test, and `fixture` is a special decorator that wraps pytest fixtures for logging purposes.

This basic usage example demonstrates how to define a page object, interact with UI elements, and define a pytest test case using Hyperion Testing Framework. The framework has many advanced features, such as automatic stale element recovery and context switching, which you can utilize to create more robust and maintainable tests. For complex scenarios, be sure to refer to the advanced usage guide and the comprehensive test examples provided.

## Capabilities Configuration

The framework utilizes a capabilities dictionary to configure and initiate the appropriate automation environment. Below are the key components of the capabilities dictionary and examples of how to use them with different automation tools.

### Key Components:

- `automation`: Specifies the automation tool to be used (e.g., Selenium, Appium). It is a mandatory key that directs the framework to the correct tool.
- `browser`: Defines which browser to launch for browser-based automation. This key is used for local browser executions and should be omitted for non-browser or remote automation scenarios.
- `automation_name`: An Appium-specific key that details the automation technology, like XCUITest for iOS. Relevant only when using Appium.
- `remote_url`: Required for remote executions and service-based tools like Appium and WinAppDriver. It specifies the URL of the remote server.

### Examples:

#### Selenium Firefox Automation

```json
{
  "automation": "selenium",
  "browser": "firefox"
}
```

#### Playwright Automation

```json
{
  "automation": "playwright",
  "browser": "webkit"
}
```

#### Appium iOS Automation

```json
{
  "automation": "appium",
  "automation_name": "xcuitest",
  "app": "path_to_my_app",
  "remote_url": "https://127.0.0.1:4723"
}
```

#### Windows Application Driver Desktop Automation

```json
{
  "automation": "windows application driver",
  "app": "Root",
  "remote_url": "https://127.0.0.1:4723"
}
```

### Framework-Specific vs. Tool-Specific Capabilities:

- The framework processes its specific keys (`automation`, `browser`, `automation_name`, `remote_url`) to configure the test environment.
- All other capabilities are passed directly to the respective automation tool. Users can include any tool-specific capabilities as they would normally do when using the tool directly.

By maintaining a consistent capabilities structure across different tools, the framework provides a streamlined approach to automation, enabling easy switching and configuration alignment across various environments.

### Detailed Explanation of `browser`, `browserName`, and `remote_url`:

- `browser`: This key is crucial for local browser automation, specifying which browser the framework should automate. When working locally, this key directly indicates the driver that should be instantiated, for example, ChromeDriver for Chrome, GeckoDriver for Firefox, etc.

- `browserName` vs `browser`:
   - In the context of remote execution, like with Selenium GRID, the `browser` key should be set to "remote". Additionally, the `browserName` capability becomes essential, specifying which browser the remote server should use for the test session. This distinction helps in differentiating between local and remote execution contexts.
   - For local execution, only the `browser` key is used. For remote execution, `browser` is set to "remote", and `browserName` specifies the actual browser type (e.g., "chrome", "firefox").

- `remote_url`: This key specifies the URL of the Selenium GRID or any remote server where the browser or mobile automation should be executed. When your tests are intended to run on a remote server, this URL directs the framework where to send commands. The framework will establish a connection to the remote server at this URL and execute the specified automation commands there.

#### Using `remote_url` with Selenium GRID:

When automating browsers in a distributed test execution environment like Selenium GRID, you define your capabilities with `browser` set to "remote" and provide the `remote_url` pointing to your GRID hub. Additionally, you need to specify `browserName` to indicate which browser type the GRID should initiate on its nodes.

For example, to run tests on Chrome in a remote GRID environment:

```json
{
  "automation": "selenium",
  "browser": "remote",
  "remote_url": "http://your-grid-hub-url:4444/wd/hub",
  "browserName": "chrome"
}
```

## Advanced Usage

In this section, we will delve deeper into the more sophisticated uses of the Hyperion Testing Framework, starting with a detailed exploration of the Hyperion Page Object Model (POM).

### Hyperion Page Object Model (POM)

The Hyperion Page Object Model is designed for ease of use, fostering clean code design, and maintaining a high degree of flexibility. It requires minimal knowledge to create robust and reusable code, making test writing a breeze.

#### Defining Page Objects

In Hyperion, you define Page Objects using top-level entities such as `WebPage`, `MobileScreen`, or `DesktopWindow` for web pages, mobile apps, or desktop windows, respectively. For nested page objects, you can use the `Widget` or `IFrame` classes.

Here's an example of how you can define a Page Object using Hyperion:

```python
from hyperiontf import WebPage, element, By

class LoginPage(WebPage):

    @element
    def username_field(self):
        return By.id("username")

    @element
    def password_field(self):
        return By.id("password")
        
    @element
    def login_button(self):
        return By.id("login")

    def login(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.login_button.click()
```

In the code above, the `LoginPage` is a `WebPage` object that contains three elements: `username_field`, `password_field`, and `login_button`. The `@element` decorator is used to define these elements. The method `login` is a higher-level method that encapsulates the steps to perform a login operation.

#### Using the `By` Object

The `By` object is used in Hyperion to specify how an element is located on the page. It extends the locator capabilities to enable cross-platform page object creation.

For instance, in the `LoginPage` example above, the elements are located using their `id` attributes:

```python
    @element
    def username_field(self):
        return By.id("username")
```

The `By` object provides several methods to locate elements, such as `By.name()`, `By.class_name()`, `By.css_selector()`, and others, providing great flexibility to the test writer.

#### Using Helper Decorators

Hyperion provides several helper decorators to simplify the definition of Page Objects:

- `@element`: Defines a simple UI element.
- `@elements`: Defines a list of similar UI elements.
- `@widget`: Defines a nested page object.
- `@widgets`: Defines a list of similar nested page objects.
- `@iframew`: Defines an iframe widget.

These decorators offer a high level of abstraction, hiding the complexity of locating and interacting with elements behind simple method calls.

In the next sections, we will discuss more advanced features of the Hyperion Testing Framework. Stay tuned!

### Widgets in Hyperion POM

A widget in Hyperion POM is essentially a nested page object. This concept allows for further structuring of page objects, making them more readable and manageable. Widgets are particularly useful when you have repeated structures on your page or application, like a navigation bar, a menu, or a list of items with the same structure.

Defining a widget is similar to defining a page object. You can define a widget by extending the `Widget` base class and defining the elements within the widget. Once a widget is defined, it can be used within other page objects or widgets.

Here's an example of how you can define a widget:

```python
from hyperiontf import Widget, element, By

class LoginForm(Widget):

    @element
    def username_field(self):
        return By.id("username")

    @element
    def password_field(self):
        return By.id("password")
        
    @element
    def login_button(self):
        return By.id("login")

    def fill_form(self, username, password):
        self.username_field.fill(username)
        self.password_field.fill(password)
```

In the example above, `LoginForm` is a widget that encapsulates the login form's elements and behavior. The `fill_form` method is a high-level method that fills the username and password fields.

You can then use the `LoginForm` widget within a `LoginPage` page object like so:

```python
from hyperiontf import WebPage, widget, By

class LoginPage(WebPage):

    @widget(klass=LoginForm)
    def login_form(self):
        return By.id("loginForm") 

    def login(self, username, password):
        self.login_form.fill_form(username, password)
        self.login_form.login_button.click()
```

In the code above, the `login_form` is defined as a `widget` within the `LoginPage`. When defining a widget with the `@widget` decorator, you provide the locator (how to find the widget on the page) and a class reference (`klass`) used for instance creation.

This level of abstraction makes the code more manageable, especially for larger applications with complex UIs.

In the next sections, we will discuss more advanced features of the Hyperion Testing Framework. Stay tuned!

### Using Elements Query Language (EQL)

#### Introduction
Elements Query Language (EQL) is a powerful feature of the Hyperion Testing Framework designed to streamline and simplify the process of querying and interacting with web elements in automated tests. EQL enables writing concise and intuitive queries to select elements, especially useful in complex web interfaces.

#### EQL Syntax Description
EQL allows you to write expressions to select web elements based on different criteria. Here is a simplified description of the EQL syntax:

- **Expressions**: A query in EQL is an expression, which can be either a comparison between values or a logical combination of other expressions.
- **Comparison Expressions**: Compare elements or values using operators like `==`, `!=`, `>`, `<`, `<=`, `>=`. For example, `age > 18` checks if the `age` element's value is greater than 18.
- **Logical Expressions**: Combine expressions with logical operators like `and` and `or`. For instance, `name == "John" and age > 30` combines two comparisons.
- **Element Chain Query**: Specify a path to a particular element or attribute. For example, `user.name` refers to the `name` element within a `user` element.
- **Complex Chains**: Handle more complex chains, like `user.friends[1].name`, which refers to the `name` of the second friend in the `user`'s friends list.
- **Regular Expressions**: Supports regex for flexible text matching, such as `text ~= /Element 3/`.

**Selecting Elements by Attributes or Styles**:
- By default, EQL queries are based on the text content of elements. To select elements based on attributes or styles, you need to specify this explicitly in your query.
- Use a colon (`:`) followed by `attribute` or `style` to target specific attributes or styles.

**Approximate Match (`~=`) Operator**:
- The `~=` operator is used for approximate matching and is specifically designed for color comparisons and regular expressions.
- For example, use `backgroundColor:style ~= rgba(255, 0, 0, 1)` to approximately match colors.
- Regular expression matching can be done as `text ~= /Element 3/`.
- **Note**: Using the `~=` operator with other data types than colors or regex patterns will result in an exception.


#### Examples and Use Cases

1. **Selecting Elements by Text**:

   ```python
   # EQL: 'text == "Multiple Element 2"'
   result = page.multiple_elements['text == "Multiple Element 2"']
   ```

2. **Using Regular Expressions**:

   ```python
   # EQL: "text ~= /Element 3/"
   result = page.multiple_elements["text ~= /Element 3/"]
   ```

3. **Targeting Child Elements**:

   ```python
   # EQL: 'child_element.text == "Widget Child Element 2"'
   result = page.multiple_simple_widgets['child_element.text == "Widget Child Element 2"']
   ```

4. **Example with Attribute**:

   ```python
   # EQL: 'data-value:attribute == "42"'
   result = page.my_array['data-value:attribute == "42"']
   ```

5. **Example with Style**:

   ```python
   # EQL: 'backgoundColor:style == rgba(255, 0, 0, 1)'
   result = page.my_colored_elements['backgroundColor:style == rgba(255, 0, 0, 1)']
   ```


### Wait API for `Element`/`Elements`

#### Introduction

Our framework introduces a unique Wait API designed to enhance the interaction with web elements during automation. This API goes beyond the traditional implicit and explicit waits found in most automation frameworks. Instead, we offer what we call "interactive waits" - a set of methods that actively trace the state of web objects to ensure actions are performed at the optimal time. This approach allows for more reliable and efficient automation scripts by reducing the chances of encountering timing-related errors.

#### Difference from Implicit and Explicit Waits

While implicit and explicit waits pause the execution for a set period or until a particular condition is met, respectively, our interactive waits actively monitor the state of an element or collection of elements. This dynamic approach ensures that operations like clicks or data entry are executed only when the elements are in the right state (e.g., visible, not animated, enabled), thereby enhancing the robustness of automation tasks.

#### Wait Methods

Our Wait API is divided into two main groups:

- **Single Object Wait Methods**: Applied to individual elements, including `Element`, `Widget`, `IFrame`, etc.
- **Array of Elements Wait Methods**: Utilized for operations on multiple elements encapsulated within an `Elements` object.

##### Single Object Wait Methods

1. **wait_until_visible**: Waits until the element becomes visible on the page.
   ```python
   element.wait_until_visible(timeout=2)
   ```
2. **wait_until_enabled**: Ensures the element is enabled and interactable.
   ```python
   element.wait_until_enabled(timeout=10)
   ```
3. **wait_until_animation_completed**: Waits for any ongoing animations to finish.
   ```python
   element.wait_until_animation_completed(timeout=15)
   ```
4. **wait_until_fully_interactable**: A comprehensive method that waits for the element to be visible, not animated, and enabled.
   ```python
   element.wait_until_fully_interactable(timeout=20)
   ```

##### Array of Elements Wait Methods

1. **wait_until_items_change**: Waits until the count of elements changes from its initial value.
   ```python
   elements.wait_until_items_change()
   ```
2. **wait_until_items_increase**: Monitors for an increase in the count of elements.
   ```python
   elements.wait_until_items_increase(timeout=12)
   ```
3. **wait_until_items_decrease**: Waits for the count of elements to decrease.
   ```python
   elements.wait_until_items_decrease(timeout=12)
   ```
4. **wait_until_items_count**: Waits until the number of elements matches a specific count.
   ```python
   elements.wait_until_items_count(expected_count=5, timeout=15)
   ```
5. **wait_until_missing**: Ensures all elements are no longer present or found.
   ```python
   elements.wait_until_missing(timeout=10)
   ```

#### Usage Examples

The interactive waits can be seamlessly integrated into your automation scripts. Here's a quick example demonstrating the use of `wait_until_fully_interactable` for a single element and `wait_until_items_increase` for multiple elements:

```python
# Single element wait
login_button = page.login_form.login_button
login_button.wait_until_fully_interactable(timeout=10)
login_button.click()

# Multiple elements wait
comments = page.extra_info_bar.comments
page.extra_info_bar.comments_form.post_comment(comment_info)
comments.wait_until_items_increase(timeout=15)
for comment in comments:
    comment.message.get_text()
```


### iFrames and Automatic Context Switching in Hyperion POM

In web development, an iFrame (short for inline frame) is an HTML document embedded inside another HTML document on a website. iFrames are often used to insert content from another source, such as an advertisement or a video, into a web page. iFrames can present unique challenges for automation testing due to the need to switch contexts to interact with elements inside the iFrame.

In many automation frameworks, switching to an iFrame and then switching back to the main document can be a complex and error-prone process. Hyperion simplifies this process by providing automatic context switching.

In Hyperion, an iFrame is treated like a special kind of widget. You can define an iFrame by extending the `IFrame` base class and defining the elements within the iFrame. Once defined, it can be used within other page objects or widgets.

Here's an example of how you can define an iFrame:

```python
from hyperiontf import IFrame, element, By

class AdIFrame(IFrame):

    @element
    def close_ad_button(self):
        return By.id("closeAd")
```

In the example above, `AdIFrame` is an iFrame that encapsulates the iFrame's elements and behavior. The `close_ad_button` is an element inside the iFrame.

You can then use the `AdIFrame` within a `WebPage` like so:

```python
from hyperiontf import WebPage, iframe, By

class HomePage(WebPage):

    @iframe(klass=AdIFrame)
    def ad_iframe(self):
        return By.id("adIframe") 

    def close_ad_iframe(self):
        self.ad_iframe.close_ad_button.click()
```

In the code above, the `ad_iframe` is defined as an `iframe` within the `HomePage`. When defining an iframe with the `@iframe` decorator, you provide the locator (how to find the iframe on the page) and a class reference (`klass`) used for instance creation.

When you interact with an element inside the iFrame (for example, `self.ad_iframe.close_ad_button.click()`), Hyperion automatically switches the context to the iFrame, performs the action, and then switches back to the main document. This automatic context switching makes it easier to work with iFrames and reduces the risk of errors.

#### Nested iFrames and Context Switching in Hyperion POM

Working with nested iFrames can be especially challenging, as it requires multiple context switches to reach the inner iFrame and then to switch back to the main document. Hyperion POM handles this gracefully by providing automatic context switching for nested iFrames.

In Hyperion, you can define a nested iFrame in the same way as you would define a regular iFrame, by extending the `IFrame` base class and defining the elements within the iFrame. When interacting with an element inside a nested iFrame, Hyperion automatically switches the context to the innermost iFrame, performs the action, and then switches back to the main document.

Here's an example of how you can define and interact with a nested iFrame:

```python
from hyperiontf import IFrame, iframe, By

class InnerAdIFrame(IFrame):

    @element
    def close_ad_button(self):
        return By.id("closeAd")

class OuterAdIFrame(IFrame):

    @iframe(klass=InnerAdIFrame)
    def inner_ad_iframe(self):
        return By.id("innerAdIframe") 

class HomePage(WebPage):

    @iframe(klass=OuterAdIFrame)
    def outer_ad_iframe(self):
        return By.id("outerAdIframe") 

    def close_ad_iframe(self):
        self.outer_ad_iframe.inner_ad_iframe.close_ad_button.click()
```

In the code above, `InnerAdIFrame` and `OuterAdIFrame` are defined as iFrames. The `InnerAdIFrame` is nested inside the `OuterAdIFrame`. When the `close_ad_iframe` method is called on the `HomePage`, Hyperion automatically switches the context to the `OuterAdIFrame`, then to the `InnerAdIFrame`, performs the click action, and then switches back to the main document. This capability greatly simplifies the handling of nested iFrames.

This feature not only makes your code cleaner and more readable, but also significantly reduces the risk of errors associated with manual context switching.


### WebView in Hyperion POM

In hybrid applications, there are often scenarios where part of the application is developed using native technologies (such as Swift for iOS or Java for Android), while another part of the application is developed using web technologies. This web part is embedded into the native application through a component called a WebView.

In the context of automation testing, working with a WebView can be similar to working with an iFrame in a web page, as it involves switching contexts from the native app to the WebView to interact with the web content, and then switching back to the native app.

Hyperion provides an elegant solution for handling WebViews by offering automatic context switching. This simplifies the interaction with elements inside the WebView, reducing the risk of errors and making the code cleaner and more manageable. Importantly, Hyperion also supports iframes within a WebView, including nested iframes, with automatic context resolution.

You can define a WebView by extending the `WebView` base class and defining the elements within the WebView. Even though the locator provided when defining a WebView is not used for context switching (as it happens based on the WebView's context, not its locator), a locator is still required by the Hyperion API for consistency.

Here's an example of how you can define a WebView and use it within a mobile screen:

```python
from hyperiontf import MobileScreen, WebView, webview, element, By

class WebContent(WebView):

    @element
    def close_button(self):
        return By.id("closeButton")
        
class HybridAppScreen(MobileScreen):
    
    @webview(klass=WebContent)
    def web_content(self):
        return By.name("WebView") # Note: This locator is for readability and is not used for context switching.

    def close_web_content(self):
        self.web_content.close_button.click()
```

In the code above, `WebContent` is a WebView that encapsulates the web content's elements and behavior. The `close_button` is an element inside the WebView. `HybridAppScreen` is a screen of the mobile app, and `web_content` is defined as a `webview` within the `HybridAppScreen`. When the `close_web_content` method is called, Hyperion automatically switches the context to the WebView, performs the click action, and then switches back to the native app.

To initialize a mobile screen, use the `start_browser` method if you're working with a web application, and the `launch_app` method if you're working with a mobile application. The `launch_app` method requires either a path to the Application Under Test (AUT) binary, a URL to the AUT binary, the bundle ID for iOS, or the app package and activity for Android.

Please note that WebView support in Hyperion enables consistent interaction patterns across different types of content within a hybrid application, including web content and iframes, thereby significantly improving code readability and maintainability.

In the next sections, we will cover more advanced aspects of the Hyperion Testing Framework. Stay tuned!


### Viewport-Specific Locators in Hyperion POM

Modern web applications often employ responsive design to ensure that their interfaces look good and function well on a variety of devices with different screen sizes. This responsive behavior is typically achieved using CSS media queries, which apply different styles based on the viewport width. Consequently, a web page can have different layouts under different viewport sizes, which might present challenges during automated testing.

Hyperion Testing Framework acknowledges this common design practice and provides an elegant way to handle different layouts with its viewport-specific locators.

In Hyperion, you can define different locators for different viewport sizes. This is extremely useful when the layout of your application changes depending on the viewport, and different elements are used in each layout.

Hyperion follows the same viewport sizing conventions as Facebook's Bootstrap, including the `xs`, `sm`, `md`, `lg`, and `xl` sizes. When defining a locator, you can specify different `By` objects for each viewport size, returning them as a dictionary.

Here is an example of defining viewport-specific locators:

```python
from hyperiontf import WebPage, element, By

class HomePage(WebPage):

    @element
    def my_elt(self):
       return { 
           'xs': By.id('XS-id'), 
           'sm': By.css('.small-viewport-class'), 
           'default': By.name('name-for-other-versions')
       }
```

In this example, `my_elt` will use different locators depending on the current viewport. When the viewport is `xs`, it will use the locator `By.id('XS-id')`, when it is `sm`, it will use `By.css('.small-viewport-class')`. If the viewport is `md`, `lg`, or `xl`, or any other size, it will use the default locator `By.name('name-for-other-versions')`.

It's important to note that if a viewport-specific locator is not defined for a particular size and there is no default locator provided, Hyperion will raise an exception. Therefore, you must define locators for all viewport sizes or provide a 'default' locator to be used for those viewport sizes for which a specific locator is not defined.

This level of flexibility allows for precise control over element location under different viewport sizes, making your test scripts more robust and reliable across different devices and screen sizes.

This feature, along with automatic context switching for iframes and WebViews, is part of Hyperion's commitment to making automation testing as smooth and effortless as possible.

In the upcoming sections, we will delve into more advanced features of the Hyperion Testing Framework. Stay tuned!


### OS-Specific Locators in Hyperion POM

With the proliferation of different operating systems and platforms, it's common for applications to have different implementations across these environments. When testing these applications, it might be necessary to locate elements differently depending on the platform.

To handle this, Hyperion introduces the concept of OS-specific locators, which allows you to specify different locators for different operating systems.

OS-specific locators come in handy when dealing with native applications for mobile, desktop, and hybrid apps. Hyperion supports keys for the following operating systems:

- Mobile: `iOS`, `Android`
- Desktop: `Windows`, `Linux`, `Darwin` (Mac OS)

Additionally, Hyperion supports nested viewport-specific locators inside OS-specific ones, offering an even greater level of specificity. As with viewport-specific locators, if a locator for a particular OS or viewport is not defined and there's no default, an exception will be thrown.

Here's an example of OS and viewport-specific locators in a desktop application:

```python
from hyperiontf import DesktopWindow, element, By

class ApplicationWindow(DesktopWindow):

    @element
    def my_elt(self):
       return { 
           'Windows': { 
               'xs': By.id('Win-xs-id'), 
               'default': By.name('Win-other-versions') 
           }, 
           'Darwin': By.id('Mac-id'), 
           'default': By.name('Other-OS')
       }
```

In this example, `my_elt` will use different locators depending on the current OS and viewport. For Windows OS with `xs` viewport, it uses `By.id('Win-xs-id')`. For other viewports in Windows, it uses `By.name('Win-other-versions')`. For Mac OS, it uses `By.id('Mac-id')`, and for other OS, it uses `By.name('Other-OS')`.

Please note that the resolution order of locators is as follows:

1. Check for platform keys: `web`, `mobile`, `desktop`
2. Check for OS keys
3. Check for viewport-specific keys
4. Finally, check for automation-specific keys (like `selenium`, `playwright`, `appium`, `autoit`, etc.)

This sophisticated locator resolution allows you to design tests that are robust and adaptable to various environments. Up next, we will delve into more advanced features of the Hyperion Testing Framework. Stay tuned!

## REST Client

The REST Client provides a convenient and easy-to-use interface for making HTTP requests and handling responses. It is designed to simplify the process of interacting with RESTful APIs and web services.

### Features

- Supports common HTTP methods: GET, POST, PUT, DELETE, HEAD, OPTIONS, and PATCH.
- Allows setting custom HTTP headers.
- Handles JSON and XML content types for request payload and response body.
- Automatically follows HTTP redirects (configurable).
- Validates response content against JSON Schema (optional).
- Logs HTTP requests and responses.

1. Import the necessary classes and types:

```python
from hyperiontf import HTTPClient
from hyperiontf.exceptions import FailedHTTPRequestException, JSONSchemaFailedAssertionException
```

2. Create an instance of the HTTPClient:

```python
client = HTTPClient(
    scheme='https',
    netloc='api.example.com',
    headers={'User-Agent': 'MyApp/1.0'},
)
```

3. Make a GET request and handle the response:

```python
try:
    response = client.request(method='GET', path='/users').execute()
    print(f"Response status: {response.status}")
    print(f"Response body: {response.body}")
except FailedHTTPRequestException as e:
    print(f"Request failed: {str(e)}")
```

4. Make a POST request with JSON payload and handle the response:

```python
payload = {'name': 'John Doe', 'email': 'john.doe@example.com'}
try:
    response = client.request(method='POST', path='/users', payload=payload).execute()
    print(f"Response status: {response.status}")
    print(f"Response body: {response.body}")
except FailedHTTPRequestException as e:
    print(f"Request failed: {str(e)}")
```

### Following HTTP Redirects

The REST client can automatically follow HTTP redirects. To enable this feature, set the `follow_redirects` parameter to `True` when making a request:

```python
response = client.request(method='GET', path='/redirect', follow_redirects=True).execute()
print(f"Final response status: {response.status}")
print(f"Final response body: {response.body}")
```

### JSON Schema Validation

The REST client allows you to validate the response content against a JSON Schema. First, define your JSON Schema:

```python
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"}
    },
    "required": ["name", "email"]
}
```

Then, perform a GET request and validate the response against the schema:

```python
response = client.request(method='GET', path='/user/1').execute()
try:
    response.validate_json_schema(schema)
    print("Response content is valid against the JSON Schema.")
except JSONSchemaFailedAssertionException as e:
    print(f"JSON Schema validation failed: {str(e)}")
```

## Cross-Platform Testing with Hyperion Framework

In software testing, it's a common scenario to have to deal with applications running on multiple platforms, whether they are web, mobile, or desktop applications. The Hyperion framework provides a robust way of handling these situations with its flexible and reusable APIs, offering an advanced use case that covers all platforms with a single page object model (POM) and a minimal variance in test code.

### The Problem Statement

Many companies maintain a diverse range of applications, often spanning web, mobile (iOS, Android), and even desktop clients. These different client applications generally serve the same purpose and provide similar user flows. Replicating tests for each individual platform can become an inefficient and error-prone process, especially when there are common aspects that can be streamlined.

This is where Hyperion shines by allowing for a single approach to cover all platforms. It can also handle platform-specific functionality as needed, while capitalizing on the commonality where applicable. Additionally, when considering client-server applications, Hyperion can facilitate the testing of common backend services and data models across all clients, improving maintainability and efficiency.

### The Proposed Solution: Cross-Platform Calculator Test

Let's illustrate this concept with a theoretical example of a calculator application. The calculator app exists across all major platforms, and hence provides an excellent subject for our cross-platform testing scenario.

The POM structure for this scenario comprises a top-level Page Object, `Calculator`, which encapsulates a `result` element and a `keypad` widget. The implementation strategy involves creating a common class for the child elements of the top-level page object, using Hyperion's decorators but without inheriting from Hyperion's base classes.

For each platform (web, mobile, desktop), we will then create specific classes that leverage Python's multiple inheritance feature. These classes will inherit from both the platform-specific top-level page object and the common class. This arrangement leverages Python's dynamic nature and the flexibility of multiple inheritance, making the overall design of the solution highly adaptable.

The test execution for every platform will be handled separately due to the different initialization code required for each platform. However, after initialization, the same codebase can be reused across all platforms. This design significantly reduces the amount of platform-specific code, further showcasing the efficiency and adaptability of the Hyperion framework in handling complex, cross-platform testing scenarios.

In the following sections, we will delve into the practical implementation and execution of this cross-platform testing solution.


#### Creating The KeyPad Widget

In our cross-platform calculator testing scenario, a crucial component of the application is the calculator's keypad. This is a shared element across all platforms and versions of the application. Therefore, to avoid code duplication, we will create a reusable widget to represent this element.

Here is the `KeyPad` widget:

```python
from hyperiontf import Widget, element, By


class KeyPad(Widget):
    # Define elements in the keypad
    @element
    def button_one(self):
        return {
            'web': {'default': By.css('#web-calculator-keypad-1')},
            'mobile': {
                'iOS': By.xpath('//XCUIElementTypeOther[@name="ios-calculator-keypad-1"]'),
                'Android': By.xpath('//android.widget.GridLayout[@content-desc="android-calculator-keypad-1"]')
            },
            'desktop': {
                'Windows': By.xpath('//Grid[@AutomationId="windows-calculator-keypad-1"]'),
                'Darwin': By.xpath('//AXGroup[@AXDescription="macos-calculator-keypad-1"]'),
                'Linux': By.xpath('//node[@role="grid" and @name="linux-calculator-keypad-1"]')
            },
        }

    @element
    def button_two(self):
        return {
            'web': {'default': By.css('#web-calculator-keypad-2')},
            'mobile': {
                'iOS': By.xpath('//XCUIElementTypeOther[@name="ios-calculator-keypad-2"]'),
                'Android': By.xpath('//android.widget.GridLayout[@content-desc="android-calculator-keypad-2"]')
            },
            'desktop': {
                'Windows': By.xpath('//Grid[@AutomationId="windows-calculator-keypad-2"]'),
                'Darwin': By.xpath('//AXGroup[@AXDescription="macos-calculator-keypad-2"]'),
                'Linux': By.xpath('//node[@role="grid" and @name="linux-calculator-keypad-2"]')
            },
        }

    # And so on for all the keys on the keypad

    # Define actions in the keypad
    def enter_number(self, number):
        for digit in str(number):
            getattr(self, f'button_{digit}').click()

    def perform_calculation(self, num1, num2, operator):
        self.enter_number(num1)
        self.getattr(f'button_{operator}').click()
        self.enter_number(num2)
        self.button_eq.click()
```

This `KeyPad` widget includes the definition of the buttons on the keypad, with locators that specify how to find each button in the web, mobile (iOS and Android), and desktop (Windows, Darwin/MacOS, and Linux) versions of the application. Additionally, it provides methods to interact with the keypad, such as entering a number or performing a calculation.

The `KeyPad` widget provides a solid example of how the Hyperion framework allows us to streamline our test automation by creating reusable components that work across multiple platforms. This approach significantly reduces code duplication and improves maintainability.

#### Creating Calculator Page Objects

Cross-platform testing can often prove to be a challenge, as the same functionality may be accessed differently across various platforms, requiring distinct locators for each platform. In this part of our tutorial, we demonstrate how to tackle this issue by creating platform-specific page objects that share common features.

For the calculator application that we're automating, we need to account for the differences in element locators for the different platforms (web, mobile, and desktop). Therefore, we have structured the page objects for the calculator application to encapsulate these differences using the concept of Inheritance and Composition.

We first define a common `CalculatorBase` class, which includes the shared elements and widgets (like `result_display` and `keypad`) across all platforms. This class isn't tied to any specific platform or operating system; instead, it provides a general interface for interacting with the calculator application. However, each element and widget is defined with multi-platform locators, so they are able to identify the correct UI element depending on the context in which they are used.

Next, we create platform-specific classes (`CalculatorWeb`, `CalculatorMobile`, and `CalculatorDesktop`), each inheriting from its corresponding platform-specific Hyperion base class (`WebPage`, `MobileScreen`, and `DesktopWindow` respectively) as well as the common `CalculatorBase` class. This allows each platform-specific class to utilize the shared definitions from `CalculatorBase` while providing a context that aligns with its respective platform.

Here's what the structure of our page objects look like:

```python
from hyperiontf import element, widget, By, WebPage, MobileScreen, DesktopWindow

class CalculatorBase:
    
    @element
    def result_display(self):
        return {
            'web': {'default': By.css('#web-calculator-display')},
            'mobile': {
                'iOS': By.xpath('//XCUIElementTypeOther[@name="ios-calculator-display"]'),
                'Android': By.xpath('//android.widget.GridLayout[@content-desc="android-calculator-display"]')
            },
            'desktop': {
                'Windows': By.xpath('//Grid[@AutomationId="windows-calculator-display"]'),
                'Darwin': By.xpath('//AXGroup[@AXDescription="macos-calculator-display"]'),
                'Linux': By.xpath('//node[@role="grid" and @name="linux-calculator-display"]')
            },
        }

    @widget(klass=KeyPad)
    def keypad(self):
        return {
            'web': {'default': By.css('#web-calculator-keypad')},
            'mobile': {
                'iOS': By.xpath('//XCUIElementTypeOther[@name="ios-calculator-keypad"]'),
                'Android': By.xpath('//android.widget.GridLayout[@content-desc="android-calculator-keypad"]')
            },
            'desktop': {
                'Windows': By.xpath('//Grid[@AutomationId="windows-calculator-keypad"]'),
                'Darwin': By.xpath('//AXGroup[@AXDescription="macos-calculator-keypad"]'),
                'Linux': By.xpath('//node[@role="grid" and @name="linux-calculator-keypad"]')
            },
        }

class CalculatorWeb(WebPage, CalculatorBase):
    pass

class CalculatorMobile(MobileScreen, CalculatorBase):
    pass

class CalculatorDesktop(DesktopWindow, CalculatorBase):
    pass
```

This structure allows us to write platform-agnostic test scripts, where the majority of the test steps can be reused across platforms. In the next section, we'll dive deeper into how to write such test scripts.

#### Creating Tests

The primary aim of the Hyperion test framework is to enable writing of test cases in a way that's platform-agnostic as much as possible. By encapsulating platform-specific locators and behaviors in our page object classes, we can keep the main body of our tests focused on the functionality we're testing, rather than the details of how to interact with each different platform.

Here's an example of three tests, each one written for a different platform: web, mobile, and desktop. All three tests perform the same basic operations: they launch the appropriate calculator application, perform a simple addition operation, and then verify the result:

```python
import pytest
from hyperiontf.executors.pytest import automatic_log_setup, fixture
from .pages import CalculatorWeb, CalculatorMobile, CalculatorDesktop

def test_addition_web():
    # Launch the web browser and navigate to the calculator application
    calc_page = CalculatorWeb.start_browser('chrome')
    calc_page.open("http://web-calculator-url.com")

    # Perform a simple addition operation
    calc_page.keypad.perform_calculation(2, 3, "+")

    # Verify the result
    calc_page.result_display.assert_text("5")

    # Clean up
    calc_page.quit()


def test_addition_mobile():
    # Launch the mobile application

    desired_caps = {
    'platformName': 'iOS',
    'platformVersion': '16.5',  
    'deviceName': 'iPhone 14',
    'bundleId': 'com.apple.calculator',
    'automationName': 'XCUITest'           
    }

    calc_page = CalculatorMobile.launch_app(desired_caps)

    # Perform a simple addition operation
    calc_page.keypad.perform_calculation(2, 3, "+")

    # Verify the result
    calc_page.result_display.assert_text("5")

    # Clean up
    calc_page.quit()


def test_addition_desktop():
    desired_caps = {
    'platformName': 'Windows',
    'deviceName': 'WindowsPC',  
    'platformVersion': '',
    'app': 'Microsoft.WindowsCalculator_8wekyb3d8bbwe!App'
    }

    # Launch the desktop application
    calc_page = CalculatorDesktop.launch_app(desired_caps)

    # Perform a simple addition operation
    calc_page.keypad.perform_calculation(2, 3, "+")

    # Verify the result
    calc_page.result_display.assert_text("5")

    # Clean up
    calc_page.quit()

```

As you can see, the steps performed inside each test are the same, despite being on different platforms. This consistency simplifies the process of writing and maintaining tests, particularly for applications that exist on multiple platforms.


## Expect and Verify Functionality

### Overview
The Hyperion Testing Framework introduces two pivotal constructs for assertions: `expect` and `verify`. These functionalities are essential for validating the state of an application against expected conditions, enhancing the robustness and clarity of tests.

### Expect
The `expect` function is utilized to assert conditions that are critical for the test's continuation. If an expectation is not met, the test is immediately marked as failed and terminated. This is particularly useful for conditions where the validity of subsequent test steps is compromised by the failure.

### Verify
In contrast, `verify` allows for the accumulation of test failures without halting the execution. This functionality is indispensable for tests that aim to assess multiple conditions and require a comprehensive report of all encountered failures. `verify` is especially useful in conditional branches and iterative selections for detailed debugging and understanding of test paths, enhancing the traceability of issues.

#### Conditional Branches
Utilizing `verify` within conditional branches enables detailed logging of decision-making comparisons, crucial for debugging. It helps in tracing back the cause of failures which may occur several steps away from the evaluated condition.

#### Iterative Selections
`Verify` is also beneficial in iterative selections, such as when searching for an item in an array based on custom logic. It aids in identifying and logging reasons behind the success or failure of selections, particularly useful in pinpointing issues like typographical errors in strings.

### Supported Datatypes and Methods
`Expect` and `verify` support a wide range of datatypes and comparison methods, including but not limited to:

- Equality and inequality checks for basic types (e.g., integers, strings)
- Contains checks for collections
- Custom logic for complex objects and conditions

These functionalities enable the writing of flexible and comprehensive tests across various application states and conditions.

### Conclusion
Incorporating `expect` and `verify` into test scripts significantly enhances the debugging capabilities and readability of tests, providing clear insights into the test execution path and facilitating the identification and correction of issues.

## Summary of Hyperion's Capabilities

The Hyperion Testing Framework stands out with its unique approach to cross-platform test automation. Designed with the philosophy of maximizing code reusability and minimizing redundancy, it enables testers to write a single test that can be run across multiple platforms.

Key features include:

1. **Platform-Agnostic Approach**: Create tests that can run on Web, Mobile (iOS/Android), and Desktop (Windows/Mac/Linux) platforms. This is enabled by Hyperion's advanced handling of platform-specific, OS-specific, and viewport-specific locators.

2. **Page Object Model Support**: Hyperion enhances the traditional Page Object Model (POM) by allowing the creation of Page Objects that are platform-agnostic. This allows for greater code reusability and maintainability.

3. **Cross-Platform Test Development**: Write a single set of tests that can execute across different platforms. The framework allows the use of Python's multiple inheritance to create platform-specific Page Objects while reusing common elements and behaviors.

4. **Robust Error Handling**: Hyperion takes care of undefined locators and ensures that your tests don't fail unexpectedly. The framework intelligently selects the appropriate locator based on the platform and OS, and throws meaningful exceptions when required locators are not defined.

5. **Support for Multiple Automation Tools**: While the framework doesn't impose any specific tool, it can work seamlessly with popular automation tools like Selenium, Playwright, Appium, and others.

With Hyperion, the dream of writing a single test that can run on any platform becomes a reality. This makes it an ideal choice for companies that have multi-platform products with similar functionality across platforms. Hyperion allows you to write the test once and run it everywhere, greatly reducing the time and effort needed for test development and maintenance.


## License

Hyperion Testing Framework is licensed under the Apache License 2.0.

You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
