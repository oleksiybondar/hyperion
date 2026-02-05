← [Back to Documentation Index](/docs/index.md)  
← Previous: [SSH Client](/docs/reference/public-api/ssh-client.md)  
→ Next: [Configuration](/docs/reference/public-api/configuration.md)

---

# Visual Testing API

The Visual Testing API defines Hyperion’s **public, contract-based interface** for
image capture, comparison, and visual assertions.

Visual testing in Hyperion is built around a single core abstraction:

> **`Image` represents a captured visual artifact.**

All visual comparisons, assertions, and UI visual helpers ultimately operate on
`Image` objects.

This document describes:
- the `Image` API (core contract)
- visual comparison via `expect(...)` / `verify(...)`
- UI-level visual helpers and visual mode orchestration
- result types and failure behavior

This document does **not** describe:
- internal image-processing algorithms
- comparison engines or thresholds implementation
- baseline storage layout or internal file management

---

## 1. Core Contract: `Image`

### Class: `Image`

`Image` represents a still visual snapshot that can be:
- loaded from disk
- created from base64-encoded image data
- compared against another `Image`

---

### Constructor

{codeblock}
Image(
    path: Optional[str] = None,
    img_data: Optional[str] = None,
    mode: str = "rb",
)
{codeblock}

**Arguments**
- `path`  
  Absolute or relative filesystem path to an image file.

- `img_data`  
  Base64-encoded image data (optionally prefixed with a data URL header).

- `mode`  
  File open mode when reading from `path`. Defaults to `"rb"`.

**Rules**
- At least one of `path` or `img_data` must be provided.
- If both are provided, `img_data` takes precedence.
- Invalid paths raise immediately when the image is opened.
- Invalid base64 data raises immediately during decoding.

---

### Properties

- `width: int`  
  Width of the image in pixels.

- `height: int`  
  Height of the image in pixels.

- `has_alpha: bool`  
  Indicates whether the image contains an alpha channel.

- `aspect_ratio: str`  
  Aspect ratio formatted as `"width:height"`.

---

### Methods

{codeblock}
open() -> None
{codeblock}

Opens the image if not already opened.

{codeblock}
close() -> None
{codeblock}

Closes the underlying image resource.

{codeblock}
write(
    content: Optional[bytes] = None,
    save_path: Optional[str] = None,
) -> None
{codeblock}

Writes image content to disk.

{codeblock}
resize(
    width: Optional[int] = None,
    height: Optional[int] = None,
    keep_aspect_ratio: bool = True,
) -> None
{codeblock}

Resizes the image in memory.

{codeblock}
rotate(
    angle: float,
    scale: float = 1.0,
) -> None
{codeblock}

Rotates the image in memory.

{codeblock}
to_base64(
    image_format: str = "PNG",
) -> str
{codeblock}

Returns the image encoded as base64.

---

### Example

{codeblock}
from hyperiontf import Image

baseline = Image("/abs/path/baseline.png")
actual = Image(img_data="data:image/png;base64,...")

assert actual.width > 0
encoded = actual.to_base64()
{codeblock}

---

## 2. Visual Comparison API

Visual comparison is performed via Hyperion’s standard assertion interface:

- `expect(value)` — assertion (raises on failure)
- `verify(value)` — verification (returns result, logs decision)

When `value` is an `Image`, image-specific comparison strategies are applied.

---

### 2.1 Result Type: `ImageExpectationResult`

All image comparisons return an `ImageExpectationResult`.

**Characteristics**
- Boolean-like (`bool(result)` is valid)
- Comparable to `True` / `False`
- Carries visual debug artifacts when applicable

---

### 2.2 Equality Comparison

{codeblock}
expect(image).to_be(expected)
verify(image).to_be(expected)
{codeblock}

**Arguments**
- `expected` — another `Image`

**Behavior**
- Performs an exact image comparison
- Assertion variant raises on mismatch
- Verification variant returns `ImageExpectationResult`

---

### 2.3 Similarity Comparison

{codeblock}
expect(image).to_be_similar(
    expected,
    mismatch_threshold,
    compare_regions=None,
    exclude_regions=None,
)
{codeblock}

**Arguments**
- `expected` — `Image` or image path (`str`)
- `mismatch_threshold` — numeric tolerance
- `compare_regions` — optional list of regions to include
- `exclude_regions` — optional list of regions to exclude

---

### Region Format

{codeblock}
{
    "x": int,
    "y": int,
    "width": int,
    "height": int,
}
{codeblock}

---

### 2.4 Region-Only Comparison

{codeblock}
expect(image).to_match_in_specified_regions(
    expected,
    compare_regions,
    mismatch_threshold,
)
{codeblock}

Compares images **only inside specified regions**.

---

### 2.5 Exclusion-Only Comparison

{codeblock}
expect(image).to_match_excluding_regions(
    expected,
    exclude_regions,
    mismatch_threshold,
)
{codeblock}

Compares images **excluding specified regions**.

---

## 3. UI Integration and Visual Mode

UI visual helpers are **convenience orchestration layers** built on top of `Image`
capture and comparison.

They do not introduce new comparison semantics.

---

### 3.1 Image Capture from UI Elements

#### `Element.make_screenshot`

{codeblock}
make_screenshot(
    filepath: Optional[str] = None,
) -> Image
{codeblock}

Captures a screenshot of the element and returns it as an `Image`.

---

#### `Element.screenshot`

{codeblock}
screenshot(
    message: Optional[str] = "Element screen snap",
    title: Optional[str] = "Element screen snap",
) -> None
{codeblock}

Captures a screenshot and attaches it to the test log.

---

### 3.2 Visual Mode

{codeblock}
VisualModeType = Literal["collect", "compare"]
{codeblock}

Constants:
- `VisualMode.COLLECT`
- `VisualMode.COMPARE`

**Behavior**
- `collect` — capture and persist baseline
- `compare` — capture and compare against baseline

---

### 3.3 Element-Level Visual Helpers

{codeblock}
element.verify_visual_match(...)
element.assert_visual_match(...)
{codeblock}

{codeblock}
element.verify_visual_match_in_regions(...)
element.assert_visual_match_in_regions(...)
{codeblock}

{codeblock}
element.verify_visual_exclusion_match(...)
element.assert_visual_exclusion_match(...)
{codeblock}

**Rules**
- `verify_*` returns `ImageExpectationResult`
- `assert_*` raises on failure
- All helpers ultimately operate on `Image`

---

## 4. Failure Behavior Summary

| Operation | Behavior |
|---------|----------|
| Invalid image input | Raises immediately |
| Type mismatch | Raises immediately |
| Assertion failure | Raises |
| Verification failure | Returns result, logs decision |
| Visual mismatch | Attaches visual artifacts |

---

## 5. Scope and Guarantees

This API guarantees:
- consistent image comparison entry points
- deterministic failure behavior
- debuggable visual results

This API does not guarantee:
- comparison algorithms
- pixel-diff implementation details
- baseline storage structure

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [SSH Client](/docs/reference/public-api/ssh-client.md)  
→ Next: [Configuration](/docs/reference/public-api/configuration.md)
