from __future__ import annotations

from hyperiontf import By, WebPage, radiogroup, RadioGroupBySpec  # type: ignore[attr-defined]


class RadioGroupsPage(WebPage):
    """
    Page Object for `radiogroups.html`.

    Covers four common DOM shapes:
    - wrapper item nodes with separate input + label
    - label wrapping input (label is the item root)
    - sibling input + label with no dedicated item wrapper
    - JavaScript-only radios with no native inputs
    """

    @radiogroup
    def wrapper_group(self) -> RadioGroupBySpec:
        """
        Scenario 1: Wrapper items.

        DOM:
          <div id="rg-wrapper">
            <div class="radio-item">
              <input type="radio" ...>
              <label ...>...</label>
            </div>
            ...
          </div>
        """
        return RadioGroupBySpec(
            root=By.id("rg-wrapper"),
            items=By.css(".radio-item"),
            input=By.css("input[type='radio']"),
            label=By.css("label"),
        )

    @radiogroup
    def nested_label_group(self) -> RadioGroupBySpec:
        """
        Scenario 2: Label wraps input.

        DOM:
          <div id="rg-nested">
            <label class="radio-item">
              <input type="radio" ...>
              Text...
            </label>
            ...
          </div>
        """
        return RadioGroupBySpec(
            root=By.id("rg-nested"),
            items=By.css("label.radio-item"),
            input=By.css("input[type='radio']"),
        )

    @radiogroup
    def sibling_group(self) -> RadioGroupBySpec:
        """
        Scenario 3: Input and label are siblings (no item wrapper).

        DOM:
          <div id="rg-siblings">
            <input type="radio" ...>
            <label for="...">...</label>
            ...
          </div>

        Here, the input is the item root, so `input` is omitted and the consuming
        component should fall back to using the item itself as the state source.
        """
        return RadioGroupBySpec(
            root=By.id("rg-siblings"),
            items=By.css("input[type='radio']"),
            label=By.xpath("./following-sibling::label[1]"),
        )

    @radiogroup
    def js_only_group(self) -> RadioGroupBySpec:
        """
        Scenario 4: JavaScript-only radios (no native inputs).

        DOM:
          <div id="rg-js-only">
            <div class="js-radio"
                 data-selected="true|false"
                 aria-checked="true|false">
              Text...
            </div>
            ...
          </div>

        There are no <input type="radio"> elements.
        Selection is driven entirely by JavaScript and exposed via attributes.

        The checked state is evaluated using `checked_expression`, which is applied
        directly to each item node.
        """
        return RadioGroupBySpec(
            root=By.id("rg-js-only"),
            items=By.css(".js-radio"),
            checked_expression="attribute:data-selected == 'true'",
        )
