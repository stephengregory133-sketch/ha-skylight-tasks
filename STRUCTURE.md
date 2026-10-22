# Repository Structure

This document describes the structure of the Skylight-Tasks Home Assistant Integration repository.

## Directory Layout

```
ha-skylight-tasks/
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md          # Bug report template
│       └── feature_request.md     # Feature request template
│
├── custom_components/
│   └── skylight/                  # Main integration directory
│       ├── __init__.py            # Integration setup & service registration
│       ├── client.py              # Skylight API client
│       ├── config_flow.py         # Configuration flow for UI setup
│       ├── const.py               # Constants and configuration keys
│       ├── manifest.json          # Integration metadata
│       ├── services.yaml          # Service definitions
│       └── strings.json           # Localization strings
│
├── .gitignore                     # Git ignore rules
├── CHANGELOG.md                   # Version history and changes
├── hacs.json                      # HACS metadata
├── info.md                        # Short description for HACS
├── INSTALL.md                     # Detailed installation guide
├── LICENSE                        # MIT License
├── README.md                      # Main documentation
└── STRUCTURE.md                   # This file
```

## File Descriptions

### Root Directory

#### `.gitignore`
Standard Python gitignore file to exclude build artifacts, caches, and IDE files.

#### `CHANGELOG.md`
Documents all changes, additions, and fixes for each version following [Keep a Changelog](https://keepachangelog.com/) format.

#### `hacs.json`
HACS metadata file that tells HACS how to handle this integration:
- Minimum Home Assistant version required
- Integration domain
- Whether to render the README in HACS

#### `info.md`
Brief description displayed in the HACS store interface.

#### `INSTALL.md`
Comprehensive installation guide covering:
- HACS installation
- Manual installation
- Finding your Frame ID
- Configuration steps
- Troubleshooting

#### `LICENSE`
MIT License granting permission to use, modify, and distribute the software.

#### `README.md`
Main documentation including:
- Features overview
- Installation methods
- Configuration instructions
- Usage examples
- Service parameters
- Troubleshooting tips

#### `STRUCTURE.md`
This file - explains the repository layout and purpose of each file.

### `.github/` Directory

Contains GitHub-specific configuration and templates.

#### `ISSUE_TEMPLATE/bug_report.md`
Template for users to report bugs with structured information:
- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Logs

#### `ISSUE_TEMPLATE/feature_request.md`
Template for feature requests with:
- Problem description
- Proposed solution
- Alternative considerations
- Example usage

### `custom_components/skylight/` Directory

The main integration code following Home Assistant's structure.

#### `__init__.py`
Main integration file:
- **`async_setup()`**: Registers the `skylight.create_chore` service
- **`async_setup_entry()`**: Sets up a config entry (creates API client)
- **`async_unload_entry()`**: Cleans up when integration is removed
- **Service handler**: Handles `create_chore` service calls

#### `client.py`
Skylight API client implementation:
- **`SkylightClient`**: Main API client class
  - `async_login()`: Authenticates with Skylight API
  - `async_create_chore()`: Creates a chore via API
  - `_get_auth_token()`: Generates Base64 auth token
- **Custom exceptions**:
  - `SkylightAuthError`: Authentication failures
  - `SkylightConnectionError`: Connection issues

#### `config_flow.py`
Configuration flow for UI-based setup:
- **`SkylightConfigFlow`**: Handles user input
  - `async_step_user()`: Main configuration step
  - Input validation
  - Duplicate prevention
- **Custom exceptions**:
  - `CannotConnect`: Connection errors
  - `InvalidAuth`: Authentication errors

#### `const.py`
Constants used throughout the integration:
- Domain name (`skylight`)
- Configuration keys (`CONF_FRAME_ID`)
- Service names (`SERVICE_CREATE_CHORE`)
- Attribute names (`ATTR_SUMMARY`, `ATTR_EMOJI_ICON`, etc.)
- API URL (`API_BASE_URL`)
- Logger instance

#### `manifest.json`
Integration metadata for Home Assistant:
- Domain and display name
- Codeowners
- Version number
- Documentation links
- Integration type and IoT class
- Dependencies/requirements

#### `services.yaml`
Service definitions for the Home Assistant UI:
- Service name and description
- Field definitions with:
  - Names and descriptions
  - Required/optional flags
  - Example values
  - UI selectors

#### `strings.json`
Localization strings for:
- **Config flow**: Step descriptions, field labels, error messages
- **Services**: Service and field descriptions

## Integration Flow

### Setup Flow
1. User adds integration via UI
2. `config_flow.py` presents configuration form
3. User enters username, password, and Frame ID
4. `validate_input()` tests connection
5. Config entry created and stored
6. `__init__.py:async_setup_entry()` creates API client
7. Client stored in `entry.runtime_data`

### Service Call Flow
1. User calls `skylight.create_chore` service
2. `async_handle_create_chore()` receives call
3. Config entry retrieved (or auto-selected)
4. API client retrieved from runtime data
5. Client calls `async_create_chore()`
6. If auth fails, client re-authenticates automatically
7. Chore created via API
8. Success/error logged

## Dependencies

The integration uses only Home Assistant's built-in dependencies:
- `aiohttp`: For async HTTP requests (built into Home Assistant)
- `voluptuous`: For schema validation (built into Home Assistant)
- Standard library: `base64`, `datetime`, `typing`

## HACS Compatibility

This integration is designed to be HACS-compatible:
- ✅ Proper directory structure (`custom_components/skylight/`)
- ✅ `hacs.json` with required metadata
- ✅ `info.md` for store display
- ✅ Comprehensive `README.md`
- ✅ Proper versioning in `manifest.json`
- ✅ GitHub issue templates

## Development

To modify this integration:

1. **Edit integration code**: Modify files in `custom_components/skylight/`
2. **Test changes**: Copy to Home Assistant's `custom_components` folder
3. **Restart HA**: Reload the integration
4. **Check logs**: Monitor for errors
5. **Update version**: Increment version in `manifest.json`
6. **Update CHANGELOG**: Document changes in `CHANGELOG.md`

## Future Enhancements

Potential additions (not yet implemented):
- Support for updating/deleting chores
- Support for marking chores as complete
- Support for recurring chores
- Sensors for chore status
- Events for chore completion
- Support for rewards/points

See `CHANGELOG.md` for actual implemented features by version.

