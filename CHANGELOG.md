# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-04

### Added
- Initial release of Skylight integration for Home Assistant
- `skylight.create_chore` service to create chores programmatically
- Support for custom emoji icons on chores
- Support for assigning chores to categories
- Automatic date setting (uses today's date)
- Config flow for easy setup via Home Assistant UI
- Auto-reauthentication on token expiry
- Support for multiple Skylight accounts
- Optional `config_entry_id` parameter (auto-selects if only one account configured)

### Security
- Secure credential storage using Home Assistant's config entry system
- Automatic token regeneration on each service call

[1.0.0]: https://github.com/riyadchowdhury/ha-skylight-tasks/releases/tag/v1.0.0

