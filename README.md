# CanaryDrop CLI 

A lightweight, professional cybersecurity terminal tool for creating and managing **canary tokens** - tripwires that alert you when attackers access them.

## What Are Canary Tokens?

Canary tokens are fake digital assets that look valuable but exist solely to alert you when accessed. They're like burglar alarms for your infrastructure - they don't prevent intrusion, but they immediately tell you when someone's snooping around.

**Traditional Security**: Look for known bad things (malware signatures, attack patterns)  
**Canary Tokens**: Detect unauthorized access to things that should never be touched (high signal, low noise)

## Features

### Token Types Supported

1. **DNS Tokens** - Unique hostnames that alert when resolved
2. **HTTP Tokens** - URLs that trigger alerts when visited
3. **AWS Credentials** - Fake AWS keys that alert when used
4. **SQL Connection Strings** - Fake database credentials
5. **Email Addresses** - Unique emails that alert when mail is received
6. **API Keys** - Fake API credentials
7. **QR Codes** - Generate QR codes that trigger alerts when scanned
8. **Document Trackers** - Tracking pixels for documents

### Core Capabilities

- ✅ Create multiple token types
- ✅ Track access attempts with full metadata
- ✅ SQLite database for persistent storage
- ✅ Color-coded terminal output
- ✅ JSON export for integration
- ✅ Manual trigger testing
- ✅ Statistics and reporting
- ✅ Zero external dependencies (pure Python 3)

## 📦 Installation

### Requirements

- Python 3.7 or higher (built-in libraries only!)
- No external dependencies required

### Setup

```bash
# Clone or download the tool
cd canarydrop-cli

# Make executable
chmod +x canarydrop.py

# Run directly
./canarydrop.py --help

# Or with Python
python3 canarydrop.py --help
```

### Database Location

All data is stored in: `~/.canarydrop/canaries.db`

## 📖 Usage Guide

### Basic Commands

```bash
# View all commands
python3 canarydrop.py --help

# Create a canary
python3 canarydrop.py create --type <TYPE> --name <NAME>

# List all canaries
python3 canarydrop.py list

# View access history
python3 canarydrop.py history

# View statistics
python3 canarydrop.py stats

# Get token details
python3 canarydrop.py info <TOKEN_ID>

# Delete a token
python3 canarydrop.py delete <TOKEN_ID>

# Export all data
python3 canarydrop.py export
```

## Examples & Use Cases

### 1. Internal Threat Detection

**Scenario**: Detect if employees are snooping in unauthorized directories

```bash
# Create fake "confidential" files
python3 canarydrop.py create \
  --type document \
  --name "Executive_Salaries_2024.docx" \
  --memo "Planted in shared HR folder"

python3 canarydrop.py create \
  --type document \
  --name "Merger_Plans_CONFIDENTIAL.pdf" \
  --memo "Planted in finance shared drive"
```

**Deploy**: Place the tracking URLs in actual documents in accessible locations.

### 2. Breach Detection

**Scenario**: Know immediately if attackers exfiltrate config files

```bash
# Create fake AWS credentials
python3 canarydrop.py create \
  --type aws-key \
  --name "prod-backup-service" \
  --memo "Planted in old config files" \
  --alert email \
  --destination security@company.com

# Create fake database credentials
python3 canarydrop.py create \
  --type sql \
  --name "legacy-customer-db" \
  --memo "Embedded in deprecated codebase"
```

**Deploy**: Scatter these in old config files, commented-out code, or backup directories.

### 3. Supply Chain Monitoring

**Scenario**: Know if code you share with vendors leaks

```bash
# Create API key canary
python3 canarydrop.py create \
  --type api-key \
  --name "vendor-api-key-v2" \
  --memo "Shared with ThirdPartyVendor Inc"
```

**Deploy**: Include this in code or docs you share externally.

### 4. Physical Security

**Scenario**: Know if someone scans a QR code on a poster

```bash
# Create QR code token
python3 canarydrop.py create \
  --type qr-code \
  --name "Server Room Access" \
  --url "https://mycompany.com/access-restricted"

# The tool provides URL - create QR at qr-code-generator.com
```

**Deploy**: Print QR code on fake "Wi-Fi credentials" posters in restricted areas.

### 5. Email Leak Detection

**Scenario**: Know if your contact list is scraped or leaked

```bash
# Create email canary
python3 canarydrop.py create \
  --type email \
  --name "Contact List Entry #47" \
  --memo "Added to customer database"
```

**Deploy**: Add this email to customer lists, CRMs, or mailing lists.

## Monitoring & Alerts

### Check for Triggers

```bash
# View all access attempts
python3 canarydrop.py history

# View specific token history
python3 canarydrop.py history --token aws_a1b2c3d4...

# Get JSON output for parsing
python3 canarydrop.py history --json > alerts.json
```

### Manual Testing

```bash
# Test if alerts work correctly
python3 canarydrop.py trigger <TOKEN_ID> \
  --ip "192.168.1.100" \
  --user-agent "Mozilla/5.0..." \
  --metadata '{"location": "office-network"}'
```

### View Statistics

```bash
# See overview of all tokens
python3 canarydrop.py stats
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
Most Recent Access: 2024-02-05 14:23:45
```

##  Advanced Usage

### JSON Export for Integration

```bash
# Export everything
python3 canarydrop.py export --output canaries_backup.json

# Parse with jq
python3 canarydrop.py list --json | jq '.[] | select(.accessed_count > 0)'
```

### Filtering by Type

```bash
# List only AWS keys
python3 canarydrop.py list --type aws-key

# Export only triggered tokens
python3 canarydrop.py history --json | jq 'select(.accessed_count > 0)'
```

### Alert Integration (Future Enhancement)

Currently, the tool supports `--alert` and `--destination` flags for future webhook/email integration:

```bash
python3 canarydrop.py create \
  --type aws-key \
  --name "production-db" \
  --alert webhook \
  --destination "https://hooks.slack.com/services/YOUR/WEBHOOK"
```

##  Output Examples

### Creating a Token

```
✓ Canary token created successfully!

Token ID: aws_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Type: aws-key
Name: prod-backup-service

Access Key ID: AKIA7F8E9D0C1B2A3456
Secret Access Key: xY9zW8vU7tS6rQ5pO4nM3lK2jI1hG0fE9dC8bA7

Usage: Plant in config files, .env files, or scripts

Example AWS config:
  [profile prod-backup-service]
  aws_access_key_id = AKIA7F8E9D0C1B2A3456
  aws_secret_access_key = xY9zW8vU7tS6rQ5pO4nM3lK2jI1hG0fE9dC8bA7
  region = us-east-1

⚠  Monitor with: python canarydrop.py history --token aws_a1b2c3d4...
```

### Viewing History (Alert!)

```
================================================================================
                         CANARY ACCESS LOGS
================================================================================

 ALERT - 2024-02-05 14:23:45
Token: aws_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
Name: prod-backup-service
Type: aws-key
IP Address: 45.77.123.45
User Agent: aws-cli/2.13.0 Python/3.11.0
--------------------------------------------------------------------------------

Total: 1 access events
```

##  Security Best Practices

### Deployment Strategy

1. **Scatter Broadly**: Place canaries in multiple locations
2. **Make Them Realistic**: Use naming that looks valuable
3. **Document Internally**: Track where you planted tokens
4. **Rotate Periodically**: Refresh tokens every 6-12 months
5. **Respond Quickly**: Investigate all triggers immediately

### What NOT To Do

❌ Don't use real credentials as canaries  
❌ Don't place canaries in active codebases  
❌ Don't ignore alerts (defeats the purpose)  
❌ Don't tell everyone where canaries are  
❌ Don't use predictable naming patterns

### Incident Response

When a canary is triggered:

1. **Verify** - Check the access log details
2. **Investigate** - Determine if legitimate or malicious
3. **Contain** - If breach confirmed, begin containment
4. **Analyze** - Review other canaries for additional access
5. **Improve** - Update security based on findings

##  Project Structure

```
canarydrop-cli/
├── canarydrop.py         # Main application
├── README.md             # This file
├── requirements.txt      # Dependencies (none!)
└── ~/.canarydrop/        # User data directory
    └── canaries.db       # SQLite database
```

##  Technical Details

### Database Schema

**canaries table**:
- token_id (unique identifier)
- type (token type)
- name (user-provided name)
- memo (notes)
- alert_method (console/email/webhook)
- alert_destination (where to send alerts)
- created_at (timestamp)
- accessed_count (number of accesses)
- last_accessed (last access timestamp)
- metadata (JSON blob with token-specific data)

**access_logs table**:
- token_id (foreign key)
- accessed_at (timestamp)
- ip_address (source IP)
- user_agent (client info)
- metadata (additional context)

### Token ID Format

All tokens follow the pattern: `{type}_{32_hex_chars}`

Examples:
- `dns_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6`
- `aws_1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6`

##  Real-World Deployment Scenarios

### Scenario 1: Ransomware Early Warning

**Problem**: You want to know if attackers are exploring your network before encryption begins.

**Solution**: Plant SQL and AWS canaries in:
- Old database backup directories
- Decommissioned server configs
- Archive folders labeled "2020_backups"

**Result**: When attackers scan for credentials, they'll try the fake ones first, giving you warning before the actual attack.

### Scenario 2: Insider Threat Detection

**Problem**: Concerned about employees accessing files they shouldn't.

**Solution**: Create document canaries named:
- "Board_Meeting_Minutes_CONFIDENTIAL.docx"
- "Layoff_List_2024.xlsx"
- "CEO_Compensation.pdf"

Place in shared drives with restrictive permissions.

**Result**: Anyone opening these files triggers an alert with their identity.

### Scenario 3: Supply Chain Attack Detection

**Problem**: You share code with multiple third-party vendors.

**Solution**: Embed API key and HTTP canaries in:
- Example code snippets
- SDK documentation
- Reference implementations

**Result**: If your code leaks to unauthorized parties, you'll know immediately.

##  Troubleshooting

### Database Locked Error

```bash
# If you get "database is locked" error
# Close all other instances of the tool
pkill -f canarydrop.py

# Or reset database (WARNING: deletes all data)
rm ~/.canarydrop/canaries.db
```

### Colors Not Showing

```bash
# If terminal colors don't work, use JSON output
python3 canarydrop.py list --json
```

### Permission Issues

```bash
# Ensure script is executable
chmod +x canarydrop.py

# Check database directory permissions
ls -la ~/.canarydrop/
```

##  Future Enhancements

Planned features:

- [ ] Email alert integration (SMTP)
- [ ] Webhook alert support (Slack, Discord, etc.)
- [ ] Web dashboard for monitoring
- [ ] Geolocation of access attempts
- [ ] Integration with SIEM systems
- [ ] Docker container deployment
- [ ] Multi-user support
- [ ] Automated canary rotation
- [ ] Machine learning anomaly detection
- [ ] Cloud storage integration

##  License

MIT License - Free to use and modify for personal and commercial use.

##  Contributing

Contributions welcome! Areas for improvement:
- Additional token types
- Alert integrations
- Better documentation
- Test cases
- Performance optimizations

##  Disclaimer

This tool is for **defensive security purposes only**. Use responsibly and only on systems you own or have permission to monitor. The authors are not responsible for misuse.

##  Additional Resources

- [Canary Tokens Concept](https://canarytokens.org/)
- [MITRE ATT&CK - Deception](https://attack.mitre.org/techniques/T1562/001/)
- [Honeypots and Canaries](https://www.sans.org/white-papers/)

---

**Built with ❤️ for the cybersecurity community**

Questions? Issues? Open a GitHub issue or contribute!
