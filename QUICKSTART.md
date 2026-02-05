# CanaryDrop CLI - Quick Start Guide

## 5-Minute Setup

### 1. Create Your First Canary (30 seconds)

```bash
# Create a fake AWS credential
python3 canarydrop.py create \
  --type aws-key \
  --name "backup-service-key"
```

You'll get output like:
```
✓ Canary token created successfully!

Access Key ID: AKIA7F8E9D0C1B2A3456
Secret Access Key: xY9zW8vU7tS6rQ5pO4nM3lK2jI1hG0fE9dC8bA7
```

### 2. Deploy It (2 minutes)

Create a file called `old-config.env`:
```bash
# Legacy backup configuration
AWS_ACCESS_KEY_ID=AKIA7F8E9D0C1B2A3456
AWS_SECRET_ACCESS_KEY=xY9zW8vU7tS6rQ5pO4nM3lK2jI1hG0fE9dC8bA7
AWS_REGION=us-east-1
```

Place this file somewhere an attacker might look:
- `/var/backups/config/`
- `~/old-configs/`
- In a commented section of your code

### 3. Simulate an Attack (30 seconds)

Test that it works:
```bash
# Get your token ID from the creation output
python3 canarydrop.py trigger aws_YOUR_TOKEN_ID \
  --ip "192.168.1.100" \
  --user-agent "aws-cli/2.13.0"
```

### 4. Check for Alerts (30 seconds)

```bash
python3 canarydrop.py history
```

You should see:
```
🚨 ALERT - 2024-02-05 14:23:45
Token: aws_...
Name: backup-service-key
Type: aws-key
IP Address: 192.168.1.100
User Agent: aws-cli/2.13.0
```

## Common Use Cases

### Detect Config File Theft

```bash
# Create fake database credentials
python3 canarydrop.py create --type sql --name "production-db"

# Add to .env file
DATABASE_URL=mysql://canary_abc123:password@db-fake.local:3306/prod
```

### Detect Unauthorized File Access

```bash
# Create document tracker
python3 canarydrop.py create --type document --name "Confidential_Report.docx"

# Embed the tracking URL in a real document
```

### Detect Email List Scraping

```bash
# Create email canary
python3 canarydrop.py create --type email --name "Newsletter_Contact"

# Add to your contact database
contact_email_f1a2b3c4d5@canarytokens.local
```

## Essential Commands

```bash
# List all canaries
python3 canarydrop.py list

# View statistics
python3 canarydrop.py stats

# Get details on specific token
python3 canarydrop.py info TOKEN_ID

# Export everything
python3 canarydrop.py export

# Delete a canary
python3 canarydrop.py delete TOKEN_ID
```

## Tips

1. **Name canaries descriptively** - You'll thank yourself later
2. **Add memos** - Note where you deployed each canary
3. **Check regularly** - Run `history` daily or weekly
4. **Respond to alerts** - Every trigger deserves investigation
5. **Rotate periodically** - Refresh canaries every 6-12 months

## Next Steps

Read the full README.md for:
- Advanced deployment strategies
- Real-world scenarios
- Best practices
- Troubleshooting
- Integration options

## Getting Help

```bash
# General help
python3 canarydrop.py --help

# Command-specific help
python3 canarydrop.py create --help
python3 canarydrop.py list --help
```

---

**You're now ready to deploy your first canary tokens! 🐤🔒**
