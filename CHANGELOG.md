# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-03-10

### Added

- Image comparison tools

#### Features

- Basic Visual testing API for Page object

## [0.2.5] - 2024-03-05

### Added

- 'windows application driver' automation name, allowing directly use WinApplicationDriver without appium

#### Automation Tools support

- Window Application Driver

## [0.2.4] - 2024-02-26

### Added

- Elements Query Language(EQL) simplifying element selection from elements/widgets arrays by attributes or child attributes
- tests covering new functionality
- Refactored Expect object

## [0.2.3.1] - 2024-01-07

### Linting changes

- added code complexity analyses using Xenon
- refactored code to match A benchmarks


## [0.2.3] - 2024-01-03

### Added

- wait API for element/elements/widget/iframe/webview classes
- tests covering new functionality
- added a helper for new Page Object creation from current one, encapsulating implementation peculiarities with new class instantiation

### Fixed

- hardcoded screen width for mobile and desktop platforms
- open in a new window handling for playwright


### Docs

- added Wait API subsection under Advanced section


## [0.1.4] - 2023-10-23
- upgraded dependencies
- migrated appium client from v2 to v3

## [0.1.2] - 2023-10-23
- added accessibility_id locator strategy replacing deprecated windows uiautomation

## [0.1.0] - 2023-08-06

### Added

- Initial release with

#### Features

- Cross-platform(Web/Mobile/Hybrid/Desktop) Page Object Harness
- Rest Client
- Build in logging
- pytest automatic log hepper and fixture decorator

#### Automation Tools support
- Selenium
- Appium 
- Playwright