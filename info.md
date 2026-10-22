# Skylight-Tasks Integration

Integrate your Skylight Frame with Home Assistant to create chores programmatically.

## Features

- Create chores with custom titles and emoji icons
- Assign chores to specific categories
- Automatic authentication handling
- Support for multiple Skylight accounts

## Quick Start

After installation:

1. Add the Skylight-Tasks integration via **Settings** → **Devices & Services**
2. Enter your Skylight credentials and Frame ID
3. Use the `skylight.create_chore` service to create chores

## Example

```yaml
service: skylight.create_chore
data:
  summary: "Load the dishwasher"
  emoji_icon: "🧺"
```

For more examples and detailed documentation, see the [README](https://github.com/riyadchowdhury/ha-skylight-tasks).

