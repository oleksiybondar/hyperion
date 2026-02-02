← [Back to Documentation Index](/docs/index.md)  
→ Next: [Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)

---

# 1.1 Installation

This section explains how to install **Hyperion Testing Framework**.

Hyperion is distributed as a single Python package.  
All supported integrations are installed at the **Python level** by default, while runtime dependencies are enabled only when you use them.

---

## Python requirement

Hyperion requires **Python 3.11 or newer**.

You can check your Python version with:

{codeblock}
python --version
{codeblock}

---

## Installing Hyperion

Install Hyperion using `pip`:

{codeblock}
pip install hyperiontf
{codeblock}

This installs the full framework, including Python bindings and helpers for:

- Web UI automation
- Mobile and desktop automation
- REST API testing
- CLI and SSH testing
- Visual testing and image comparison
- OCR and image processing (via `opencv-python`)
- pytest integration and logging

No feature is activated unless you use it.

---

## Automation engines

Hyperion supports multiple automation engines.  
All Python bindings are installed automatically, but **runtime setup depends on the engine you choose**.

### Selenium and Appium (recommended)

Selenium and Appium are the **recommended automation engines** for most use cases.

You are responsible for providing:
- browsers (for Selenium)
- mobile devices, simulators, or emulators (for Appium)
- any required drivers or remote endpoints

Hyperion does not change or restrict how these tools are configured — it integrates with them as-is.

---

### Playwright

Playwright bindings are included, but **Playwright is not initialized automatically**.

No browsers are downloaded during installation.

If you choose to use Playwright, you must explicitly install its browser binaries:

{codeblock}
playwright install
{codeblock}

Playwright can be useful in CLI-driven or pipeline-based environments, but it is not required to use Hyperion.

---

## Visual testing and OCR

Visual testing, image comparison, and OCR support are included by default.

Hyperion uses `opencv-python` internally for image processing.  
If you do not use visual or OCR features, no additional setup is required.

---

## Verifying the installation

After installation, you should be able to import Hyperion in Python:

{codeblock}
python -c "import hyperiontf; print(hyperiontf.__version__)"
{codeblock}

If the import succeeds, Hyperion is installed correctly.

---

## Next steps

Once Hyperion is installed, continue with:

- [1.2 Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)

---

← [Back to Documentation Index](/docs/index.md)  
→ Next: [Project Setup (pytest)](/docs/getting-started/project-setup-pytest.md)