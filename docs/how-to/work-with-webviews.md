# 4.9 Working with WebViews

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Working with iFrames](/docs/how-to/work-with-iframes.md)  
→ Next: [REST API Testing](/docs/how-to/api-testing-rest-client.md)

---

Hybrid applications combine **native UI** with **web content** rendered inside WebViews.

Most automation frameworks treat WebViews as fragile, special cases that require:
- manual context switching
- explicit context identifiers
- defensive logic around visibility
- duplicated test flows

Hyperion follows a different model.

This guide explains **how WebViews are handled safely and idiomatically** —
using the same structural principles as pages, widgets, and iFrames.

---

## Mental model: WebView as an application-level context boundary

A WebView in Hyperion represents:

- a real Python object
- a boundary between **native** and **web** execution contexts
- a structural component of the Page Object hierarchy

Conceptually:

- Pages, widgets, and iFrames operate *within* a document
- A WebView switches the **entire execution backend** between native and web

Despite this difference, the **user-facing model stays the same**.

---

## Key difference from iFrames

Although WebViews and iFrames look similar in Page Objects,
there are important differences:

| Aspect                  | iFrame                           | WebView                          |
|-------------------------|----------------------------------|----------------------------------|
| Scope                   | Inside a web document            | Application-level                |
| Nesting                 | Can be nested                    | Not nested                       |
| Active instances        | Multiple at once                 | Only one active at a time        |
| Context selection       | Hierarchical                     | Visibility-based                 |
| Locator requirement     | Required                         | Not required                     |

These differences are intentional and reflect real application behavior.

---

## Visibility-based context selection

In most hybrid applications:

- only **one WebView is visible at a time**
- others may exist but remain hidden or in background
- user interaction always targets the visible one

Hyperion models this reality directly.

When interacting with a WebView:
- the framework automatically selects the **currently visible WebView**
- context switching happens implicitly
- no explicit identifiers are required

This matches the dominant real-world app behavior.

---

## No locator required for WebViews

Unlike iFrames, WebViews:

- do not require locators
- often have dynamically assigned identifiers
- usually expose no meaningful, stable attributes

In practice:
- the most recently created visible WebView is the correct target
- this aligns with how most hybrid apps behave

Hyperion therefore does **not require a locator** when defining a WebView.

Known edge cases exist (multiple visible WebViews),
but they are rare and not currently implemented, as they are not needed
for the vast majority of real applications.

---

## Caching WebView references is preferred

Switching between native and web contexts is a **heavy operation**.

For this reason:
- caching WebView references is encouraged
- repeated access via cached objects reduces unnecessary switching
- object identity remains stable

Example:

```python
web = app.main_webview
web.login("user", "password")
```

This works because:
- WebView objects preserve hierarchy and parent context
- only internal automation handles are recreated
- Python references remain valid

As with iFrames:
> **Structure is stable. Execution details are replaceable.**

---

## The Scenario

We’ll model a simple hybrid application:

- native shell application
- embedded WebView for user account management
- standard web UI inside the WebView
- iFrames may exist inside the WebView and work as usual

---

## Step 1: Define the WebView

```python
from hyperiontf import WebView, element, By


class AccountWebView(WebView):

    @element
    def username_input(self):
        return By.id("username")

    @element
    def password_input(self):
        return By.id("password")

    @element
    def login_button(self):
        return By.id("login")

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

Key points:
- no locator is defined for the WebView itself
- internal elements behave exactly like normal web elements
- iFrames inside this WebView would work identically to browser iFrames

---

## Step 2: Attach the WebView to a native screen

```python
from hyperiontf import MobileScreen, webview
from .account_webview import AccountWebView


class MainScreen(MobileScreen):

    @webview(klass=AccountWebView)
    def account(self):
        pass
```

The decorator:
- declares the existence of a WebView
- allows Hyperion to manage context switching
- keeps the Page Object structure explicit

---

## Step 3: Use the WebView in a test

```python
import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401


def test_login_via_webview(main_screen):
    main_screen.account.login(
        username="user",
        password="secret",
    )

    main_screen.account.username_input.assert_missing()
```

What happens automatically:
- context switches from native → web
- the visible WebView is selected
- interactions occur synchronously
- context returns to native when needed

No explicit switching appears in user code.

---

## WebViews and iFrames together

A common pattern is:
- WebView hosting a complex web app
- iFrames inside that web app

This works naturally in Hyperion:
- WebView selects the web execution context
- iFrames manage document-level boundaries
- both compose using the same hierarchical model

No additional logic is required.

---

## Design rules of thumb

**Do**
- cache WebView references
- encapsulate WebView behavior
- rely on visibility-based selection
- keep tests free of context mechanics

**Avoid**
- manual context switching
- exposing WebView internals to tests
- assuming multiple active WebViews
- forcing locators where none exist

---

## What You Learned

You now know:
- how WebViews differ from iFrames
- why only one WebView is active at a time
- how Hyperion selects the correct context
- why caching improves stability and performance

Most importantly:

> **WebViews are application-level boundaries,  
> not special cases that require special handling.**

---

## Next Guides

Continue with:
- [/docs/how-to/eql-recipes.md](/docs/how-to/eql-recipes.md)
- [/docs/how-to/logging-and-reports.md](/docs/how-to/logging-and-reports.md)

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Working with iFrames](/docs/how-to/work-with-iframes.md)  
→ Next: [REST API Testing](/docs/how-to/api-testing-rest-client.md)
