# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

*NOTE: Pre v1.0.0 Version Clarification*

As of our initial release (v0.1.0), this framework has been focused on providing a comprehensive yet streamlined experience for UI testing, which is our primary objective. Despite this focus, the framework is designed with flexibility in mind, offering robust API testing capabilities from the outset. Plans to extend our testing capabilities to include CLI and database interactions are underway, aiming to make this framework versatile across various testing scenarios.

It is important to acknowledge that versions prior to v1.0.0 are considered to be in a developmental stage where not all envisioned features have been fully implemented. However, this does not detract from the core functionality which has been our cornerstone: to deliver a high-level and simplistic API that caters to both API and UI testing needs.

From its first version, our framework has included a dedicated REST client equipped with extensive, built-in logging features, alongside a UI harness that simplifies page object creation. This harness supports a unified API compatible with Selenium, Appium, and Playwright, ensuring a seamless and efficient testing process.

## [0.6.12] - 2024-10-14

### added

- added possibility to connect to already existing session

#### Features

- new Framework specific capability: sessionId, which substitutes session creation, with session attachment, which is natively, does not supported by WinApplicationDriver

#### Notes

This feature added because when using Root as application, e.g. connect to desktop, then session is not destroyed and persists, therefore WinAppDriver must be explicitly restarted, or else when sessions count/memory limit reaches the application will crash. So adding a possibility to connect to not destroyed sessions instead of spawning new.

This is an edge case scenario and needed only when using WinAppDriver directly and the environments where its difficult to manage win app driver, for example remote execution on static environments.

Using WinAppDriver over appium will nto cause the issue, as Appium server manages WinAppDriver instance and terminate it when appium session is ended.


## [0.6.11] - 2024-10-13

### added

- own XPath engine for WindowsApplication driver
- ability to use widgets recursively 

#### Features

- support of relative element search with ./
- support XPath axes

### fixed

- improved finalizer for pytest execute


## [0.6.5] - 2024-10-07

### fixed

- incorrect element instantiation
- session ID handling fix
- proper JSON-WIRE communication logging source
- custom base path support for bridge

## [0.6.1] - 2024-10-07

#### Features

- SSH interactive client with built-in logging and assertions helpers

## [0.6.0] - 2024-10-06

### Added

- basic CLI support

#### Features

- bash/sh/zsh interactive client with built-in logging and assertions helpers

## [0.5.0] - 2024-10-04

### Added

- Action builder implementation

#### Features

- New complex element actions like drag&drop
- Action Builder public API, allowing to perform complex manipulations like image drawing

## [0.4.0] - 2024-10-02

### Added

- Window Application Driver Client - own selenium like client

## [0.3.6] - 2024-09-11

### Added

- REST Client: Introduced the default_event_logging_level property, enabling users to reduce the default logging level for standard events to debug.

### fixed

- Logger: Logger now properly handles sequential folder operations, ensuring that messages are correctly nested and do not break between folders. Previously, messages from different folders were incorrectly grouped under the same parent folder.
- Automatic Logging for Page Objects: no auto decoration for properties
- Window Application Driver: fixed missing post morten screen snaps and source dumps when connecting to entire desktop

## [0.3.5] - 2024-04-02

### Added

- Viewport adjustment API web

### fixed

- Visual testing: autoscale issue, now scales both images to a smallest common resolution to reduce level of noice

## [0.3.1] - 2024-03-23

### fixed

- WinApplicationDriver find_element incompatible response fix

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