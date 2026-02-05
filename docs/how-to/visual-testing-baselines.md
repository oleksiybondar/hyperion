← [Back to Documentation Index](/docs/index.md)  
← Previous: [SSH Testing](/docs/how-to/ssh-testing-ssh-client.md)  
→ Next: [Elements Query Language (EQL) Recipes](/docs/how-to/eql-recipes.md)

---

# Visual Testing: Baselines, Regions, and Stability

This guide explains **how to use Hyperion’s visual testing API effectively**.

Unlike the API Reference, this document is **opinionated** and focuses on:
- test stability
- debuggability
- practical usage patterns

All examples use **only Hyperion public APIs** and follow real framework usage.

---

## 1. The Visual Testing Mental Model

In Hyperion, visual testing always follows the same core flow:

> **capture an image → compare it → assert the outcome**

Everything else (UI helpers, modes, regions) exists only to make that flow safer
and more expressive.

The most important rule:

> **Visual tests must end with an explicit assertion.**

---

## 2. Collecting a Baseline Image

Baseline collection is a **controlled activity**.
It should not happen accidentally during normal test execution.

Hyperion supports this via *visual mode*.

### Example: Collecting a baseline for a stable UI region

{codeblock}
from hyperiontf.typing import VisualMode

def test_collect_dashboard_header(dashboard_page):
    header = dashboard_page.header

    # Collect baseline image
    result = header.verify_visual_match(
        "dashboard_header.png",
        mode=VisualMode.COLLECT,
    )

    # Explicit assertion: baseline must exist after collection
    assert result is True
{codeblock}

**Why this works**
- The element screenshot is captured
- The baseline image is written
- The test asserts that collection succeeded

Baseline collection is **explicit**, observable, and intentional.

---

## 3. Full Image Comparison (Use Sparingly)

Full image comparison is appropriate when:
- the UI is deterministic
- layout and content are stable
- no animations or dynamic regions are present

### Example: Full image comparison

{codeblock}
def test_dashboard_header_visual(dashboard_page):
    header = dashboard_page.header

    result = header.verify_visual_match(
        "dashboard_header.png",
        mismatch_threshold=0,
    )

    assert result is True
{codeblock}

**Guideline**
- Use full image comparison for **simple, static components**
- Prefer region-based comparison for most real-world pages

---

## 4. Region-Based Comparison (Recommended Default)

Most UIs contain dynamic areas:
- timestamps
- counters
- user-specific data
- animated elements

Region-based comparison allows you to assert **what matters**, and ignore noise.

### Example: Compare only stable regions

{codeblock}
def test_dashboard_header_core_layout(dashboard_page):
    header = dashboard_page.header

    result = header.verify_visual_match(
        "dashboard_header.png",
        compare_regions=[
            {"x": 0, "y": 0, "width": 600, "height": 80},
        ],
        mismatch_threshold=1.0,
    )

    assert result is True
{codeblock}

**Why this is stable**
- Only the structural region is compared
- Dynamic content outside the region is ignored
- Small rendering differences are tolerated

---

## 5. Excluding Dynamic Regions

Sometimes it’s easier to describe what *should not* be compared.

Typical exclusions:
- clocks
- notification badges
- rotating banners

### Example: Excluding unstable regions

{codeblock}
def test_dashboard_header_excluding_clock(dashboard_page):
    header = dashboard_page.header

    result = header.verify_visual_exclusion_match(
        "dashboard_header.png",
        exclude_regions=[
            {"x": 520, "y": 0, "width": 80, "height": 40},
        ],
        mismatch_threshold=1.0,
    )

    assert result is True
{codeblock}

**Warning**
- Overusing exclusions can hide real regressions
- Prefer *small, targeted* exclusions

---

## 6. `verify` vs `assert` in Visual Tests

Visual helpers come in two forms:
- `verify_visual_*`
- `assert_visual_*`

### Recommended rule

- Use `verify_visual_*` **inside Page Objects or decision logic**
- Use `assert_visual_*` **at the test boundary**

### Example: Decision inside Page Object, assertion in test

{codeblock}
class DashboardPage:

    def is_compact_layout(self) -> bool:
        return self.header.verify_visual_match(
            "dashboard_header_compact.png",
            mismatch_threshold=2.0,
        )

def test_dashboard_layout(dashboard_page):
    is_compact = dashboard_page.is_compact_layout()

    assert is_compact is True
{codeblock}

This preserves:
- readable logs
- clear intent
- explicit test outcomes

---

## 7. Visual Mode: `collect` vs `compare`

Visual mode controls **orchestration**, not correctness.

### Rules of thumb

- `collect`
  - used during controlled baseline creation
  - typically not enabled in CI
- `compare`
  - default mode
  - used during validation runs

Mode does **not** change comparison semantics.
It only decides whether to:
- save an image
- or compare against an existing one

---

## 8. Debugging Visual Failures

When a visual comparison fails, Hyperion logs:
- the actual image
- the expected image
- a difference image (when applicable)

This makes failures **investigable**, not just binary.

**Best practice**
- Inspect diffs before changing thresholds
- Prefer narrowing regions over increasing tolerance

---

## 9. Common Anti-Patterns

Avoid the following:

### ❌ Visual checks without assertions

{codeblock}
dashboard_page.header.verify_visual_match("header.png")
# no assertion → test result is ambiguous
{codeblock}

### ❌ Accumulating visual verifications

{codeblock}
ok = True
ok &= header.verify_visual_match("a.png")
ok &= footer.verify_visual_match("b.png")
assert ok
{codeblock}

This hides intent and degrades logs.

### ✅ Preferred

{codeblock}
assert header.verify_visual_match("a.png") is True
assert footer.verify_visual_match("b.png") is True
{codeblock}

---

## Summary

Visual testing in Hyperion works best when:

- `Image` is treated as the core artifact
- region-based comparison is the default
- exclusions are used sparingly
- visual mode is explicit
- every test ends with an assertion

When done this way, visual tests become:
- stable
- explainable
- easy to debug

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [SSH Testing](/docs/how-to/ssh-testing-ssh-client.md)  
→ Next: [Elements Query Language (EQL) Recipes](/docs/how-to/eql-recipes.md)