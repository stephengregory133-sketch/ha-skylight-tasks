# Skylight-Tasks Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A custom Home Assistant integration for [Skylight Frame](https://www.ourskylight.com/) that allows you to create chores via actions/services.

## Features

- 🔐 Secure authentication with your Skylight account
- ✨ Create chores with custom emoji icons
- 🏷️ Assign chores to specific categories
- 📅 Automatically sets today's date for new chores
- 🔄 Auto-reauthentication on token expiry

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/riyadchowdhury/ha-skylight-tasks`
6. Select category "Integration"
7. Click "Add"
8. Search for "Skylight-Tasks" in HACS
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Download the latest release from this repository
2. Copy the `custom_components/skylight` folder to your Home Assistant's `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Skylight-Tasks**
4. Enter your credentials:
   - **Username**: Your Skylight account email
   - **Password**: Your Skylight account password
   - **Frame ID**: Your Skylight Frame ID

### Finding Your Frame ID

You can find your Frame ID by:

1. Opening the Skylight mobile app
2. Looking at network requests (using a proxy like Charles or mitmproxy)
3. The Frame ID appears in API calls to `https://app.ourskylight.com/api/frames/{FRAME_ID}/`

Alternatively, you can use the provided `skylight_scrape.py` script from the [Skylight API documentation](https://github.com/mightybandito/Skylight) to retrieve your Frame ID.

## Usage

### Service: `skylight.create_chore`

Creates a new chore in your Skylight Frame.

#### Service Parameters

| Parameter         | Required | Description                                                | Example                 |
| ----------------- | -------- | ---------------------------------------------------------- | ----------------------- |
| `config_entry_id` | No       | Config entry ID to use (auto-selected if only one account) | `abc123def456`          |
| `summary`         | Yes      | The chore title/description                                | `"Load the dishwasher"` |
| `emoji_icon`      | No       | Emoji icon for the chore                                   | `"🧺"`                  |
| `category_id`     | No       | Category ID to assign the chore                            | `"12812432"`            |

#### Examples

**Simple Usage (Single Account):**

```yaml
service: skylight.create_chore
data:
  summary: "Load the dishwasher"
  emoji_icon: "🧺"
```

**With Category:**

```yaml
service: skylight.create_chore
data:
  summary: "Take out the trash"
  emoji_icon: "🗑️"
  category_id: "12812432"
```

**Multiple Accounts:**

```yaml
service: skylight.create_chore
data:
  config_entry_id: "abc123def456..."
  summary: "Clean the kitchen"
  emoji_icon: "🧽"
  category_id: "12812432"
```

**In an Automation:**

```yaml
automation:
  - alias: "Create evening chores"
    trigger:
      - platform: time
        at: "18:00:00"
    action:
      - service: skylight.create_chore
        data:
          summary: "Prepare dinner"
          emoji_icon: "🍳"
```

**Using a Script:**

```yaml
script:
  create_weekly_chore:
    alias: "Create Weekly Chore"
    sequence:
      - service: skylight.create_chore
        data:
          summary: "{{ chore_name }}"
          emoji_icon: "{{ chore_emoji }}"
          category_id: "{{ category }}"
    fields:
      chore_name:
        description: "Name of the chore"
        example: "Vacuum the house"
      chore_emoji:
        description: "Emoji for the chore"
        example: "🧹"
      category:
        description: "Category ID"
        example: "12812432"
```

## Finding Category IDs

To find category IDs for your Skylight Frame:

1. Use the Skylight mobile app
2. Capture network traffic to see the category IDs
3. Look for API calls to `/api/frames/{FRAME_ID}/categories`

Or use a script to query the API (similar to the login process in `skylight_scrape.py`).

## Troubleshooting

### Authentication Errors

If you receive authentication errors:

- Verify your username and password are correct
- Make sure your Frame ID is accurate
- Try removing and re-adding the integration

### Connection Errors

If you receive connection errors:

- Check your internet connection
- Verify that `https://app.ourskylight.com` is accessible
- Check Home Assistant logs for detailed error messages

### Debug Logging

To enable debug logging, add this to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.skylight: debug
```

## Credits

This integration is based on reverse-engineered API endpoints from the Skylight Frame service. Special thanks to:

- [Skylight API Documentation](https://github.com/mightybandito/Skylight) by @ramseys1990 and contributors
- Home Assistant community

## Disclaimer

This is an unofficial integration and is not affiliated with, endorsed by, or connected to Skylight or their parent company. Use at your own risk.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter issues or have questions:

1. Check the [Issues](https://github.com/riyadchowdhury/ha-skylight-tasks/issues) page
2. Create a new issue with detailed information about your problem
3. Include relevant logs (with sensitive information removed)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
