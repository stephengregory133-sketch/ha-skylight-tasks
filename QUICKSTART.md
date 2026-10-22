# Quick Start Guide

Get up and running with the Skylight integration in minutes!

## 1️⃣ Install via HACS (2 minutes)

1. **HACS** → **Integrations** → **⋮** → **Custom repositories**
2. Add: `https://github.com/riyadchowdhury/ha-skylight-tasks`
3. Category: **Integration**
4. Search **"Skylight-Tasks"** → **Download**
5. **Restart Home Assistant**

## 2️⃣ Configure (1 minute)

1. **Settings** → **Devices & Services** → **+ Add Integration**
2. Search **"Skylight-Tasks"**
3. Enter:
   - **Username**: your.email@example.com
   - **Password**: your password
   - **Frame ID**: 1234567 (see below)

### Finding Frame ID

**Quick Method:**
1. Go to [app.ourskylight.com](https://app.ourskylight.com)
2. Open browser DevTools (F12) → **Network** tab
3. Look for requests to `/api/frames/`
4. Your Frame ID is the number in the URL

## 3️⃣ Create Your First Chore (30 seconds)

### Via UI
1. **Developer Tools** → **Services**
2. Service: `skylight.create_chore`
3. Fill in:
   ```yaml
   summary: Test Chore
   emoji_icon: ✅
   ```
4. **Call Service**

### Via Automation
```yaml
service: skylight.create_chore
data:
  summary: "Load the dishwasher"
  emoji_icon: "🧺"
```

## Common Use Cases

### Morning Chores Reminder
```yaml
automation:
  - alias: "Morning chores"
    trigger:
      - platform: time
        at: "08:00:00"
    action:
      - service: skylight.create_chore
        data:
          summary: "Make bed"
          emoji_icon: "🛏️"
```

### Laundry Notification
```yaml
automation:
  - alias: "Laundry done"
    trigger:
      - platform: state
        entity_id: binary_sensor.washing_machine
        to: "off"
        for: "00:02:00"
    action:
      - service: skylight.create_chore
        data:
          summary: "Move laundry to dryer"
          emoji_icon: "🧺"
          category_id: "12812432"
```

### Weekly Cleaning Tasks
```yaml
automation:
  - alias: "Sunday cleaning"
    trigger:
      - platform: time
        at: "10:00:00"
    condition:
      - condition: time
        weekday:
          - sun
    action:
      - service: skylight.create_chore
        data:
          summary: "Vacuum the house"
          emoji_icon: "🧹"
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Authentication failed** | Double-check email/password, verify Frame ID |
| **Service not found** | Restart Home Assistant after installation |
| **Chore not appearing** | Check logs, verify Frame ID is correct |
| **Multiple accounts** | Add `config_entry_id` to service call |

## Next Steps

- 📖 Read the [full documentation](README.md)
- 📋 Check [installation guide](INSTALL.md) for advanced options
- 🐛 [Report issues](https://github.com/riyadchowdhury/ha-skylight-tasks/issues)
- ⭐ Star the repo if you find it useful!

## Need Help?

- **Detailed docs**: See [README.md](README.md)
- **Installation help**: See [INSTALL.md](INSTALL.md)
- **Report bugs**: [Create an issue](https://github.com/riyadchowdhury/ha-skylight-tasks/issues/new/choose)

---

**That's it!** 🎉 You're now creating Skylight chores from Home Assistant!

