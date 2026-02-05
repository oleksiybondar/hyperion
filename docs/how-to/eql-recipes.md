# 4.14 Elements Query Language (EQL) Recipes

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Visual Testing and Baselines](/docs/how-to/visual-testing-baselines.md)  
→ Next: [Logging and Reporting](/docs/how-to/logging-and-reports.md)

---

Elements Query Language (EQL) allows you to select elements and widgets **by meaning**, not by position.

Use EQL to express intent such as:

- “the product card with title *Coffee Mug*”
- “the row whose status is ACTIVE”
- “the element whose style indicates it is hidden”

Instead of brittle indexing like `items[3]`.

EQL is a **selection and decision tool**, not a validation tool:
- use EQL to decide *what* to act on
- use assertions (`assert_*`, `expect`) to validate outcomes

---

## Mental model

### EQL is property access + typed comparison

An EQL expression is evaluated like real code:

- dot (`.`) traverses **structure and properties**
- colon (`:`) switches into **attribute or style namespaces**
- literals are parsed into real types (string, number, bool, regex, color)
- comparisons follow strict, typed semantics

There is no JavaScript-style loose coercion.

---

## Where EQL is used

EQL is applied to an `Elements` collection:

```python
card = products['title.text == "Coffee Mug"']
```

The result is a selected element or widget instance,
which you then use normally.

---

## Dot vs Colon (important rule)

- **Dot (`.`)**  
  Resolves Page Object structure and properties.

- **Colon (`:`)**  
  Accesses element metadata namespaces:
  - `attribute:<name>`
  - `style:<name>`

These two compose naturally.

---

## Recipe 1: Select a widget by child element text

**Use case:** choose a product card by its title.

```python
class ProductsPage(WebPage):

    @widgets(klass=ProductCard)
    def products(self):
        return By.css(".product-card")

    def card_by_title(self, title: str) -> ProductCard:
        return self.products[f'title.text == "{title}"']
```

Usage:

```python
products_page.card_by_title("Coffee Mug").add_to_cart()
products_page.cart_confirmation.assert_text("Product added to cart")
```

---

## Recipe 2: Select by attribute or style

EQL provides explicit **attribute** and **style** namespaces.

Syntax:
- `attribute:<name>`
- `style:<name>`

```python
# Attribute examples
button = buttons['attribute:disabled == true']
input_ = inputs['attribute:readonly == true']

# Style examples
badge = badges['style:display ~= /none/']
header = headers['style:background-color ~= /rgb$begin:math:text$255\, 0\, 0$end:math:text$/']
```

`attribute` and `style` are namespaces, not properties.  
They are resolved directly on the element.

---

## Recipe 3: Attribute or style of a child element

Because dot access resolves an element,  
namespaces can be applied **after traversal**.

```python
# Attribute of a nested element
card = products['title.attribute:class == "h5"']

# Style of a nested element
card = products['title.style:font-size >= 16']
```

Rule of thumb:

> Dot (`.`) resolves structure.  
> Colon (`:`) accesses metadata on the resolved element.

---

## Recipe 4: Numeric comparisons and ranges

EQL supports numeric literals and standard comparisons.

```python
row = rows["count >= 10"]
```

Chained comparisons are supported and evaluated as logical `and`:

```python
row = rows["10 <= count <= 100"]
```

Literal types are preserved, and comparisons follow strict semantics.

---

## Recipe 5: Combine conditions with `and` / `or`

```python
row = rows['status.text == "ACTIVE" and name.text ~= /Admin.*/']
```

Using `or`:

```python
row = rows['status.text == "PENDING" or status.text == "ACTIVE"']
```

---

## Recipe 6: Approximate matching (`~=`)

The `~=` operator supports **typed approximate matching**.

### Regex matching

Either side may be a regex literal:

```python
card = products['title.text ~= /Coffee.*/']
card = products['/Coffee.*/ ~= title.text']
```

Use this for:
- flexible labels
- dynamic UI text
- pattern-based selection

### Color approximate matching

Color literals (hex, rgb, rgba) are supported:

```python
icon = icons['style:color ~= #ffcc00']
```

This is useful for:
- visual indicators
- theme validation
- state-based styling

---

## Recipe 7: Use EQL as a decision point (recommended)

EQL works best when used inside Page Objects or widgets.

```python
class UsersTable(Widget):

    @widgets(klass=TableRow)
    def rows(self):
        return By.css("tbody tr")

    def delete_user(self, username: str) -> None:
        row = self.rows[f'name.text == "{username}"']
        row.delete()
```

Test code stays clean:

```python
dashboard_page.users_table.delete_user("alice")
dashboard_page.success_message.assert_text("User deleted successfully")
```

---

## Debugging EQL: decision logging

EQL evaluation is fully traceable.

For each candidate element, Hyperion logs:
- what was expected
- what was observed
- why it matched or didn’t match

This makes EQL safe to use even in deep, dynamic hierarchies.

---

## Common mistakes

### Using EQL as validation

Bad:

```python
_ = products['title.text == "Coffee Mug"']
```

Good:

```python
card = products['title.text == "Coffee Mug"']
card.title.assert_text("Coffee Mug")
```

---

### Overusing indexing

Indexing is fine when order matters.  
EQL is better when identity matters.

---

## What You Learned

You now know how to:
- select elements and widgets by meaning
- traverse structure and access metadata
- use typed comparisons and ranges
- apply regex and approximate matching
- structure EQL decisions cleanly

Most importantly:

> **EQL helps you decide *what* to interact with —  
> not *whether* it is correct.**

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [Visual Testing and Baselines](/docs/how-to/visual-testing-baselines.md)  
→ Next: [Logging and Reporting](/docs/how-to/logging-and-reports.md)
