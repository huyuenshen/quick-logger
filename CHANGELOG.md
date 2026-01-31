# CHANGELOG.md
All notable changes to `quick-logger` will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.7] - 2026-01-31
### Fixed
- ✅ Fixed package configuration error in `setup.cfg` (resolved path matching anomaly of original `packages.find` rule), completely solved "global module import failure" and "running failure in external directories".
- ✅ Simplified `setup.cfg` configuration logic by removing redundant `packages.find` rules, improved installation stability and reduce future maintenance costs.

### Optimized
- ✅ Added "Quick Verification After Installation" guide in README to help users quickly confirm the validity of the installation.


## [0.3.6] - 2026-01-30
### Fixed
- ✅ Fixed error: DIR Name in ``asynclog.py`` wrong.

## [0.3.5] - 2026-01-30
### Added
- ✅ Added ``enable_color`` column in Config file.
###Fixed
- ✅ Fixed some errors in ``asynclog.py``.

## [0.3.4] - 2026-01-30
### Added
- ✅ Added **blinking effect** to the FATAL level log output for more prominent visual alerts (terminal must support ANSI escape codes).

## [0.3.0] - 2026-01-30
### Changed
- ✅ Project name: quick-datalog -> quick-logger-colorful

## [0.2.0] - 2026-01-09
### Added
- ✅ FATAL log level (type=4) with red background + bold white text for critical error scenarios.
- ✅ Independent `asynclog` module, provides `AsyncDatalog` async logger class.
- ✅ `async_start_logger` decorator for auto-capturing exceptions in async functions.
- ✅ Non-blocking asynchronous log file writing based on asyncio, no blocking for async coroutine workflow.
- ✅ Context manager support for synchronous logger, safer file operation.

### Changed
- ✅ Adjusted color configuration: ERROR level (3) → pure red (\033[31m), FATAL level (4) → red bg + white bold (\033[41;1;37m).
- ✅ Full English localization, removed all Chinese language configurations, simplified code logic.
- ✅ Optimized log file naming: replace {time} with {date} in config, more semantic naming.
- ✅ Improved stack trace parsing, accurately obtain the real business function name of log caller.
- ✅ Optimized log pattern variable mapping: unified use of `{type}` and `{inform}`.

### Fixed
- ✅ Fixed potential file handle leakage problem, auto-close log files via destructor.
- ✅ Fixed the problem of incorrect function name acquisition in nested call scenarios.
- ✅ Fixed the cross-platform path compatibility problem of log directory creation.

### Compatibility
- ✅ Backward compatible with v0.1.1 and all previous versions.
- ✅ Minimum supported Python version: 3.7+
- ✅ No third-party dependencies, zero installation cost.

## [0.1.1] - 2026-01-05
### Fixed
- Critical import bug: Resolved the failure of `from quick_datalog import Datalog, start_logger`.
- Optimized log file path generation logic for Windows system compatibility.
- Improved exception stack trace display format.

## [0.1.0] - 2026-01-01
### Added
- Initial release of quick-datalog core functions.
- Synchronous logger `Datalog` with DEBUG/INFO/WARN/ERROR four log levels.
- `start_logger` decorator for auto exception capture and logging.
- Auto creation of log directory and configuration file, zero configuration to use.
- Date-based log file splitting, production mode switch via `-O` parameter.