# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2021-11-15
### Changed
- Performance increased by using persistent connection via `request.Session` object

## [1.0.0] - 2021-11-02
### Added
- High-level ModelingAPI that allows for much easier scheduling and commanding
- Integration tests that run against a local instance of Major Tom

### Changed
- The signature for the `UpdateCommandDefinition` mutation has changed in a non-backwards-compatible way. If you were using this API to star/unstar commands, you will have to remove the non-nullable constraint. (i.e. instead of `$starred:Boolean!`, it's just `$starred:Boolean`, without the exclamation mark.)

## [0.1.0] - 2021-10-07
### Changed
- ScriptAPI no longer makes a query on initialization. The query for script information (such as the script id) is now lazy and happens when the property is first accessed.

## 0.0.2 - 2021-06-20
### Added
- CHANGELOG!
- Automatic CI/CD process
- Multi-environment testing 


[Unreleased]: https://github.com/kubos/majortom_scripting_package/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/kubos/majortom_scripting_package/releases/tag/v1.0.1
[1.0.0]: https://github.com/kubos/majortom_scripting_package/releases/tag/v1.0.0
[0.1.0]: https://github.com/kubos/majortom_scripting_package/releases/tag/v0.1.0