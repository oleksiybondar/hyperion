← [Back to Documentation Index](/docs/index.md)  
← Previous: [ActionBuilder](/docs/reference/public-api/action-builder.md)  
→ Next: [Verify](/docs/reference/public-api/verify.md)

---

# Expect

`expect(...)` is Hyperion’s **assertion-oriented expectation API**.

It provides a fluent matcher surface for validating values in tests and raises immediately
when expectations fail.

This page documents:
- the `expect(...)` entry point
- the matcher surface exposed by the returned `Expect` object
- matcher applicability based on subject type

> **Important global rules**
>
> - **Type mismatch raises immediately** (for all matchers)
> - On **success**: matchers return an `ExpectationResult`
> - On **failure**: `expect(...)` raises (assertion semantics)

---

## Entry point

### expect

**Signature**

`expect(actual_value: Any, value_type: Optional[str] = None, content_type: Optional[str] = None, logger: Optional[Logger] = None, sender: str = LoggerSource.EXPECT) -> Expect`

**Contract**

Creates an assertion-oriented `Expect` bound to `actual_value`.

- Failed expectations raise immediately.
- Successful expectations return an `ExpectationResult`.

The returned `Expect` exposes matcher methods documented below.

**Arguments**

- `actual_value`: The value under test.
- `value_type`: Optional type hint used by the expectation entry point.
- `content_type`: Optional content hint used by the expectation entry point.
- `logger`: Optional logger override.
- `sender`: Log sender identifier.

**Returns**

- `Expect`

---

## Supported subject types

Matchers are applied based on the **runtime type** of the subject value.

Hyperion currently provides specialized behavior for:

- **Numeric:** `bool`, `int`, `float`
- **String:** `str`
- **Collections:** `list`, `set`, `tuple`
- **Mapping:** `dict`
- **Filesystem:** `File`, `Dir`
- **Color:** `Color`
- **Image:** `Image`

Calling a matcher on an unsupported subject type raises immediately.

---

## ExpectationResult

Most matchers return an `ExpectationResult` on success.

### ExpectationResult.__bool__

**Signature**

`ExpectationResult.__bool__() -> bool`

**Contract**

Returns `True` when the expectation passed and `False` when it failed.

Although `expect(...)` raises on failure, the boolean behavior is useful for symmetry
with `verify(...)` and for advanced control flow patterns.

---

# Matchers

All matchers listed below:

- Return `ExpectationResult` on success
- Raise on failure when used via `expect(...)`
- Raise immediately on type mismatch

---

## Type-insensitive matchers

These apply to all supported subject types unless stated otherwise.

### Expect.to_be / Expect.not_to_be

**Signature**

- `Expect.to_be(expected_value: Any) -> ExpectationResult`
- `Expect.not_to_be(expected_value: Any) -> ExpectationResult`

**Contract**

Checks equality / inequality between the subject and `expected_value`.

Equality semantics are type-dependent (value equality for primitives, structural equality
for collections).

---

### Expect.is_none / Expect.is_not_none

**Signature**

- `Expect.is_none() -> ExpectationResult`
- `Expect.is_not_none() -> ExpectationResult`

**Contract**

Checks whether the subject is `None` / not `None`.

---

### Expect.is_a / Expect.is_not_a

**Signature**

- `Expect.is_a(cls: type) -> ExpectationResult`
- `Expect.is_not_a(cls: type) -> ExpectationResult`

**Contract**

Checks whether the subject is (or is not) an instance of `cls`.

---

### Expect.is_type_of / Expect.is_not_type_of

**Signature**

- `Expect.is_type_of(cls: type) -> ExpectationResult`
- `Expect.is_not_type_of(cls: type) -> ExpectationResult`

**Contract**

Checks whether the subject’s **exact type** is (or is not) `cls`.

---

## Type predicate helpers

### Expect.is_string / Expect.is_not_string

**Contract**

Checks whether the subject is (or is not) a `str`.

---

### Expect.is_int / Expect.is_not_int

**Contract**

Checks whether the subject is (or is not) an `int`.

---

### Expect.is_float / Expect.is_not_float

**Contract**

Checks whether the subject is (or is not) a `float`.

---

### Expect.is_bool / Expect.is_not_bool

**Contract**

Checks whether the subject is (or is not) a `bool`.

---

### Expect.is_date / Expect.is_not_date

**Contract**

Checks whether the subject is (or is not) a `datetime.date`.

---

### Expect.is_time / Expect.is_not_time

**Contract**

Checks whether the subject is (or is not) a `datetime.time`.

---

### Expect.is_datetime / Expect.is_not_datetime

**Contract**

Checks whether the subject is (or is not) a `datetime.datetime`.

---

### Expect.is_list / Expect.is_not_list

**Contract**

Checks whether the subject is (or is not) a `list`.

---

### Expect.is_dict / Expect.is_not_dict

**Contract**

Checks whether the subject is (or is not) a `dict`.

---

## String matchers

**Applicable subject types:** `str`

### Expect.to_start_with / Expect.not_to_start_with

**Contract**

Checks whether the string starts with / does not start with `prefix`.

---

### Expect.to_end_with / Expect.not_to_end_with

**Contract**

Checks whether the string ends with / does not end with `suffix`.

---

### Expect.to_match / Expect.not_to_match

**Contract**

Checks whether the string matches / does not match `pattern`.

---

### Expect.to_be_empty / Expect.not_to_be_empty

**Contract**

Checks whether the string is empty / not empty.

---

## Collection matchers

**Applicable subject types:** `list`, `set`, `tuple`  
(Some also apply to `str`, where noted.)

### Expect.to_have_length / Expect.not_to_have_length

**Contract**

Checks the length of the subject.

---

### Expect.to_contain / Expect.not_to_contain

**Contract**

Checks containment.

Containment semantics:
- `str`: substring containment
- collections: membership containment
- `dict`: key containment

---

### Expect.to_contain_in_order

**Contract**

Checks whether a collection contains values in the specified order.

---

### Expect.to_contain_exactly

**Contract**

Checks whether a collection contains exactly the specified values.

---

### Expect.to_contain_any_of / Expect.not_to_contain_any_of

**Contract**

Checks whether at least one (or none) of the specified values is present.

---

## Mapping matchers

**Applicable subject types:** `dict`

### Expect.to_contain_key / Expect.not_to_contain_key

**Contract**

Checks whether the dict contains / does not contain a key.

---

### Expect.to_contain_keys / Expect.not_to_contain_keys

**Contract**

Checks whether the dict contains / does not contain all specified keys.

---

### Expect.to_contain_value / Expect.not_to_contain_value

**Contract**

Checks whether the dict contains / does not contain a value.

---

### Expect.to_match_schema

**Contract**

Validates the dict-like subject against a schema supported by Hyperion’s schema validation.

---

## Filesystem matchers

**Applicable subject types:** `File`, `Dir`

### Expect.to_exist / Expect.not_to_exist

**Contract**

Checks whether the filesystem entity exists / does not exist.

---

### Expect.to_be_file

**Contract**

Checks whether the subject represents a file.

---

### Expect.to_be_directory

**Contract**

Checks whether the subject represents a directory.

---

### Expect.to_have_size / Expect.not_to_have_size

**Contract**

Checks the size of the filesystem entity.

---

## Numeric matchers

**Applicable subject types:** `bool`, `int`, `float`

### Expect.to_be_odd / Expect.not_to_be_odd  
### Expect.to_be_even / Expect.not_to_be_even  
### Expect.to_be_positive / Expect.not_to_be_positive  
### Expect.to_be_negative / Expect.not_to_be_negative  
### Expect.to_be_zero  

**Contract**

Checks numeric properties of the subject.

---

### Expect.to_be_in_between / Expect.not_to_be_in_between

**Contract**

Checks whether the number is (or is not) between two values.

---

### Expect.to_be_close_to / Expect.not_to_be_close_to

**Contract**

Checks numeric closeness within a tolerance.

---

### Expect.to_be_multiple_of / Expect.not_to_be_multiple_of  
### Expect.to_be_divisible_by  

**Contract**

Checks divisibility / multiplicity.

---

### Expect.to_be_in_range / Expect.not_to_be_in_range

**Contract**

Checks whether the number is in the inclusive range.

---

### Expect.to_be_greater_than / Expect.to_be_less_than  
### Expect.to_be_greater_than_or_equal_to / Expect.to_be_less_than_or_equal_to

**Contract**

Checks numeric ordering.

---

### Expect.to_be_approximately_equal

**Contract**

Checks approximate equality within a tolerance.

---

## Image matchers

**Applicable subject types:** `Image`

### Expect.to_be_similar

**Contract**

Checks whether the image is similar to another image within a similarity threshold.

---

### Expect.to_match_in_specified_regions

**Contract**

Checks similarity only inside specified regions.

---

### Expect.to_match_excluding_regions

**Contract**

Checks similarity outside excluded regions.

---

## Example

```python
from hyperiontf import expect

def test_example(value):
    expect(value).is_not_none()
    expect(value).to_be_in_range(1, 10)

    # explicit test assertion
    assert value >= 1
```

---

← [Back to Documentation Index](/docs/index.md)  
← Previous: [ActionBuilder](/docs/reference/public-api/action-builder.md)  
→ Next: [Verify](/docs/reference/public-api/verify.md)
