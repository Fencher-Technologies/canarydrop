# CanaryDrop CLI - Visual Interface Showcase 🎨

## Beautiful Startup Banner

When you run `python3 canarydrop.py` or `python3 canarydrop.py --help`, you see:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║          🐤  CanaryDrop CLI 🔒                                               ║
║          ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                         ║
║                                                                              ║
║          Advanced Canary Token Management System                            ║
║          Detect unauthorized access before it's too late                    ║
║                                                                              ║
║          Version 1.0.0 | MIT License | Pure Python 3                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

💡 Tip: Use --help with any command for detailed usage information
📚 Docs: Check README.md, QUICKSTART.md, and USAGE_EXAMPLES.md
🔐 Database: ~/.canarydrop/canaries.db
```

## Creating a Canary Token

```bash
$ python3 canarydrop.py create --type aws-key --name "prod-backup"
```

Output:
```
✓ Canary token created successfully!

Token ID: aws_790cf3b890e43d45bfe7f0c7a3bd07d5
Type: aws-key
Name: prod-backup

Access Key ID: AKIA29236173107B92FEAF07
Secret Access Key: ItfSRx-kwm6w1WBRTcbS6ZNTC5VK4w74R-B_KsfW

Usage: Plant in config files, .env files, or scripts

Example AWS config:
  [profile prod-backup]
  aws_access_key_id = AKIA29236173107B92FEAF07
  aws_secret_access_key = ItfSRx-kwm6w1WBRTcbS6ZNTC5VK4w74R-B_KsfW
  region = us-east-1

⚠  Monitor with: python canarydrop.py history --token aws_790cf3b890e43d45bfe7f0c7a3bd07d5
```

## Listing All Canaries

```bash
$ python3 canarydrop.py list
```

Output:
```
================================================================================
                                 CANARY TOKENS
================================================================================

🟢 ACTIVE | API-KEY
Name: stripe-production
Token ID: api_60b68c2dd57fd7fe1e322c30b1eb50e5
Created: 2026-02-05T11:50:39
--------------------------------------------------------------------------------

🟢 ACTIVE | DNS
Name: internal-api
Token ID: dns_69ae4cf1c38366cb2e9f3788f9a2b120
Created: 2026-02-05T11:50:39
--------------------------------------------------------------------------------

🟢 ACTIVE | EMAIL
Name: contact-form
Token ID: email_f6fdedf2fcf690457d8ae6a3ac2ac0bf
Created: 2026-02-05T11:48:45
--------------------------------------------------------------------------------

🔴 TRIGGERED | AWS-KEY
Name: prod-backup-key
Token ID: aws_5a977c2c9e515f498877bce410c0be50
Created: 2026-02-05T11:48:41
⚠ Accessed: 1 times
Last access: 2026-02-05T11:48:50
Memo: Test canary for demo
--------------------------------------------------------------------------------

Total: 6 canaries
```

## Viewing Statistics

```bash
$ python3 canarydrop.py stats
```

Output:
```
================================================================================
                            CANARY TOKEN STATISTICS
================================================================================

Total Canaries: 15
🟢 Active (Never Triggered): 12
🔴 Triggered: 3

Canaries by Type:
  aws-key: 5
  sql: 4
  http: 3
  email: 2
  dns: 1

Total Access Events: 8
Most Recent Access: 2026-02-05T14:23:45
```

## Viewing Access History (ALERT!)

```bash
$ python3 canarydrop.py history
```

Output:
```
================================================================================
                               CANARY ACCESS LOGS
================================================================================

🚨 ALERT - 2026-02-05T14:23:45
Token: aws_5a977c2c9e515f498877bce410c0be50
Name: prod-backup-key
Type: aws-key
IP Address: 45.77.123.45
User Agent: aws-cli/2.13.0
Additional Info:
  attempt: authentication
  region: us-east-1
--------------------------------------------------------------------------------

🚨 ALERT - 2026-02-05T12:15:33
Token: sql_64333eb261c5a6e1e946ddb195dffdfe
Name: legacy-database
Type: sql
IP Address: 192.168.1.100
User Agent: mysql-connector/8.0
--------------------------------------------------------------------------------

Total: 2 access events
```

## Token Details View

```bash
$ python3 canarydrop.py info aws_5a977c2c9e515f498877bce410c0be50
```

Output:
```
================================================================================
🔴 TRIGGERED CANARY TOKEN DETAILS
================================================================================

Token ID: aws_5a977c2c9e515f498877bce410c0be50
Type: aws-key
Name: prod-backup-key
Created: 2026-02-05T11:48:41
Memo: Test canary for demo

Alert Method: console
Alert Destination: security@company.com

Access Count: 3
Last Accessed: 2026-02-05T14:23:45

Token-Specific Data:
  access_key_id: AKIA0B7F498397DE55E331F0
  secret_access_key: JqlSs9PcZjeMTGXI3ApyWoxNsRU-BpOUcSzhhq8R
  region: us-east-1
```

## Color Coding System

The tool uses intelligent color coding:

- 🟢 **GREEN** - Active/Safe status, successful operations
- 🔴 **RED** - Triggered/Alert status, critical warnings
- 🟡 **YELLOW** - Highlights, important information, tips
- 🔵 **CYAN** - Token IDs, section headers, primary UI elements
- 🔷 **BLUE** - Separators, secondary information

## Special Features

### Emojis for Quick Recognition
- 🐤 Canary bird - Main logo
- 🔒 Lock - Security focus
- ✓ Checkmark - Success
- ⚠ Warning - Monitoring needed
- 🚨 Alert - Triggered canary
- 💡 Lightbulb - Tips
- 📚 Books - Documentation
- 🔐 Padlock - Database location

### Visual Separators
```
================================================================================
                                 SECTION TITLE
================================================================================
```

```
--------------------------------------------------------------------------------
```

### Box Drawing
```
╔══════════════════════════════════════════════════════════════╗
║                    Boxed Content                             ║
╚══════════════════════════════════════════════════════════════╝
```

## Interactive Demo

Run the interactive showcase:

```bash
chmod +x showcase_demo.sh
./showcase_demo.sh
```

This will walk you through:
1. Viewing the banner
2. Creating tokens
3. Listing tokens
4. Viewing statistics
5. Simulating an attack
6. Viewing alerts
7. Checking final stats

## Terminal Compatibility

The interface works perfectly in:
- ✅ Linux terminals (GNOME Terminal, Konsole, etc.)
- ✅ macOS Terminal
- ✅ Windows Terminal
- ✅ iTerm2
- ✅ VS Code integrated terminal
- ✅ SSH sessions

For terminals without color support, use `--json` flag for clean output.

## Screenshots (Text-Based)

### Creating Multiple Token Types
```
$ python3 canarydrop.py create --type dns --name "api-endpoint"
✓ Canary token created successfully!
Hostname: dns_a1b2c3d4e5f6g7h8.canarytokens.local

$ python3 canarydrop.py create --type sql --name "customer-db"
✓ Canary token created successfully!
Connection String: mysql://canary_abc123:pass@db-host.local:3306/customers

$ python3 canarydrop.py create --type email --name "support"
✓ Canary token created successfully!
Email: email_f1a2b3c4d5e6f7g8@canarytokens.local
```

### Dashboard Overview
```
$ python3 canarydrop.py list

🟢 ACTIVE | DNS         - api-endpoint
🟢 ACTIVE | SQL         - customer-db
🟢 ACTIVE | EMAIL       - support
🔴 TRIGGERED | AWS-KEY  - backup-service (⚠ 3 accesses)
🔴 TRIGGERED | HTTP     - admin-panel (⚠ 1 access)

Total: 5 canaries (3 active, 2 triggered)
```

## Why This Interface?

1. **Quick Recognition** - Colors and emojis let you spot issues instantly
2. **Professional** - Clean, organized output suitable for security teams
3. **Informative** - Every screen tells you what you need to know
4. **Accessible** - Works in all terminals, degrades gracefully
5. **Memorable** - The canary emoji makes it instantly recognizable

## Customization

The interface uses ANSI color codes. Colors are defined in the `Colors` class:

```python
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    # ... and more
```

You can modify these in the code if you want different colors!

---

**The interface is already beautiful and ready to use!** 🎨✨

Just run `python3 canarydrop.py` to see the gorgeous banner.
