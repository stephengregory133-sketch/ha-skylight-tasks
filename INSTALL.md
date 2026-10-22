# Installation Guide

This guide will walk you through installing the Skylight integration for Home Assistant.

## Prerequisites

- Home Assistant 2024.1.0 or newer
- A Skylight Frame account
- Your Skylight Frame ID (see below for how to find it)

## Method 1: HACS Installation (Recommended)

### Step 1: Install HACS

If you don't have HACS installed:

1. Visit [HACS Installation Guide](https://hacs.xyz/docs/setup/download)
2. Follow the installation instructions

### Step 2: Add Custom Repository

1. Open Home Assistant
2. Go to **HACS** → **Integrations**
3. Click the **three dots menu** (⋮) in the top right
4. Select **Custom repositories**
5. Enter repository URL: `https://github.com/riyadchowdhury/ha-skylight-tasks`
6. Select category: **Integration**
7. Click **Add**

### Step 3: Install Integration

1. In HACS, search for **"Skylight-Tasks"**
2. Click on the integration
3. Click **Download**
4. Restart Home Assistant

### Step 4: Configure Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Skylight-Tasks**
4. Enter your credentials:
   - **Username**: Your Skylight email address
   - **Password**: Your Skylight password
   - **Frame ID**: Your Skylight Frame ID (see below)

## Method 2: Manual Installation

### Step 1: Download Files

Download the latest release from:

```
https://github.com/riyadchowdhury/ha-skylight-tasks/releases/latest
```

### Step 2: Copy Files

1. Extract the downloaded ZIP file
2. Copy the `custom_components/skylight` folder to your Home Assistant configuration directory:
   ```
   /config/custom_components/skylight/
   ```

### Step 3: Restart Home Assistant

Restart Home Assistant to load the new integration.

### Step 4: Configure Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **Skylight**
4. Enter your credentials

## Finding Your Frame ID

There are several ways to find your Skylight Frame ID:

### Method 1: Using Browser Developer Tools

1. Log into [app.ourskylight.com](https://app.ourskylight.com) in your browser
2. Open Developer Tools (F12)
3. Go to the **Network** tab
4. Refresh the page or navigate to your chores
5. Look for API calls to `/api/frames/{FRAME_ID}/`
6. The Frame ID is the numeric value in the URL

### Method 2: Using the Skylight Scrape Script

If you have the [Skylight API repository](https://github.com/mightybandito/Skylight) scripts:

```python
# Run the skylight_scrape.py script
python3 skylight_scrape.py
# Enter your email and password when prompted
# The script will display your Frame ID(s)
```

### Method 3: Using a Proxy (Advanced)

1. Install a proxy tool like [Charles Proxy](https://www.charlesproxy.com/) or [mitmproxy](https://mitmproxy.org/)
2. Configure your mobile device to use the proxy
3. Open the Skylight mobile app
4. Observe the network traffic
5. Look for requests to `https://app.ourskylight.com/api/frames/`
6. Note the Frame ID from the URL

## Verifying Installation

After configuration, you should see:

1. **In Integrations**: A new Skylight-Tasks entry with your Frame ID
2. **In Services**: A new `skylight.create_chore` service available

To test the integration:

1. Go to **Developer Tools** → **Services**
2. Select `skylight.create_chore`
3. Enter test data:
   ```yaml
   summary: Test Chore
   emoji_icon: ✅
   ```
4. Click **Call Service**
5. Check your Skylight Frame - the chore should appear!

## Troubleshooting

### Integration Not Appearing

- Ensure you restarted Home Assistant after copying files
- Check the logs: **Settings** → **System** → **Logs**
- Look for errors related to `skylight` or `custom_components`

### Authentication Failed

- Double-check your email and password
- Ensure your Skylight account is active
- Try logging into [app.ourskylight.com](https://app.ourskylight.com) directly

### Cannot Find Frame ID

- Try all methods above
- Contact support if you need assistance

### Service Not Working

- Check Home Assistant logs for detailed error messages
- Verify your Frame ID is correct
- Ensure you have an active internet connection

## Updating

### Via HACS

1. Go to HACS → Integrations
2. Find Skylight-Tasks integration
3. Click **Update** if available
4. Restart Home Assistant

### Manual Update

1. Download the latest release
2. Replace the files in `custom_components/skylight/`
3. Restart Home Assistant

## Uninstalling

1. Go to **Settings** → **Devices & Services**
2. Find the Skylight-Tasks integration
3. Click the **three dots** (⋮)
4. Select **Delete**
5. Optionally, remove the `custom_components/skylight` folder
6. Restart Home Assistant

## Support

If you need help:

- Check the [README](README.md) for usage examples
- Review [open issues](https://github.com/riyadchowdhury/ha-skylight-tasks/issues)
- Create a [new issue](https://github.com/riyadchowdhury/ha-skylight-tasks/issues/new) with:
  - Your Home Assistant version
  - Integration version
  - Relevant log entries
  - Steps to reproduce the issue
