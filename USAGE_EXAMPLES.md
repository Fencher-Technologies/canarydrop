# CanaryDrop CLI - Complete Usage Examples

## Table of Contents
1. [Basic Operations](#basic-operations)
2. [Creating Different Token Types](#creating-different-token-types)
3. [Monitoring and Alerts](#monitoring-and-alerts)
4. [Advanced Scenarios](#advanced-scenarios)
5. [Integration Examples](#integration-examples)

---

## Basic Operations

### Installation & Setup
```bash
# Make executable
chmod +x canarydrop.py

# Test installation
python3 canarydrop.py --help

# Check version
python3 canarydrop.py stats
```

### View All Commands
```bash
python3 canarydrop.py --help
```

Output:
```
Commands:
  create    Create a new canary token
  list      List all canary tokens
  history   Show access history
  delete    Delete a canary token
  info      Show token details
  trigger   Manually trigger a token (testing)
  stats     Show statistics
  export    Export all data to JSON
```

---

## Creating Different Token Types

### 1. AWS Credentials
```bash
# Basic AWS key
python3 canarydrop.py create \
  --type aws-key \
  --name "backup-service-key"

# With full metadata
python3 canarydrop.py create \
  --type aws-key \
  --name "production-s3-access" \
  --memo "Planted in /opt/legacy/aws-credentials.conf" \
  --alert email \
  --destination "security@company.com"
```

**Output:**
```
✓ Canary token created successfully!

Token ID: aws_a1b2c3d4e5f6g7h8...
Access Key ID: AKIA7F8E9D0C1B2A3456
Secret Access Key: xY9zW8vU7tS6rQ5pO4nM3lK2jI1hG0fE9dC8bA7

Example AWS config:
  [profile backup-service-key]
  aws_access_key_id = AKIA7F8E9D0C1B2A3456
  aws_secret_access_key = xY9zW8vU7tS6rQ5pO4nM3lK2jI1hG0fE9dC8bA7
  region = us-east-1
```

### 2. SQL Connection Strings
```bash
# MySQL connection
python3 canarydrop.py create \
  --type sql \
  --name "customer-database-replica"

# With context
python3 canarydrop.py create \
  --type sql \
  --name "analytics-db" \
  --memo "In docker-compose.yml.backup"
```

**Output:**
```
Connection String: mysql://canary_abc123:xY9zW@db-host.local:3306/customers

Example .env entry:
  DATABASE_URL=mysql://canary_abc123:xY9zW@db-host.local:3306/customers
```

### 3. HTTP URLs
```bash
# Simple URL canary
python3 canarydrop.py create \
  --type http \
  --name "admin-dashboard-link"

# With tracking context
python3 canarydrop.py create \
  --type http \
  --name "password-reset-form" \
  --memo "Shared in phishing test"
```

**Output:**
```
URL: https://canarytokens.local/http_1a2b3c4d5e6f...

Usage: Share this URL or embed in web pages
```

### 4. DNS Hostnames
```bash
# Internal API hostname
python3 canarydrop.py create \
  --type dns \
  --name "legacy-api-endpoint"

# Service discovery
python3 canarydrop.py create \
  --type dns \
  --name "microservice-registry" \
  --memo "In old Kubernetes configs"
```

**Output:**
```
Hostname: dns_a1b2c3d4e5f6g7h8.canarytokens.local

Usage: Embed this hostname in configs or scripts
```

### 5. Email Addresses
```bash
# Contact form canary
python3 canarydrop.py create \
  --type email \
  --name "support-inbox"

# Mailing list entry
python3 canarydrop.py create \
  --type email \
  --name "newsletter-subscriber-1247" \
  --memo "Added to MailChimp list"
```

**Output:**
```
Email: email_f1a2b3c4d5e6f7g8@canarytokens.local

Usage: Use as contact email in documents or configs
```

### 6. API Keys
```bash
# Generic API key
python3 canarydrop.py create \
  --type api-key \
  --name "stripe-test-key"

# Third-party service
python3 canarydrop.py create \
  --type api-key \
  --name "sendgrid-api" \
  --memo "In CI/CD pipeline config"
```

**Output:**
```
API Key: sk_LeLPMo5dEf3eSYB3VfW7inTFxH3job7hHrRYFamv5Vo

Usage: Plant in scripts or configuration files
```

### 7. QR Codes
```bash
# WiFi credentials QR
python3 canarydrop.py create \
  --type qr-code \
  --name "server-room-wifi"

# Custom URL QR
python3 canarydrop.py create \
  --type qr-code \
  --name "equipment-checkout" \
  --url "https://internal.company.com/checkout"
```

**Output:**
```
URL: https://canarytokens.local/qr/a1b2c3d4e5f6g7h8

To create QR code:
  Visit: https://www.qr-code-generator.com/
  Enter URL: [above URL]
```

### 8. Document Trackers
```bash
# Word document
python3 canarydrop.py create \
  --type document \
  --name "Q4_Financial_Report.docx"

# PDF file
python3 canarydrop.py create \
  --type document \
  --name "Employee_Handbook_2024.pdf" \
  --memo "On shared HR drive"
```

**Output:**
```
Callback URL: https://canarytokens.local/doc/a1b2c3d4/track.gif

Usage: Create a document and embed this URL as a hidden image
```

---

## Monitoring and Alerts

### List All Canaries
```bash
# View all
python3 canarydrop.py list

# Filter by type
python3 canarydrop.py list --type aws-key
python3 canarydrop.py list --type sql

# JSON output for parsing
python3 canarydrop.py list --json | jq '.'
```

**Sample Output:**
```
================================================================================
                                 CANARY TOKENS
================================================================================

🟢 ACTIVE | AWS-KEY
Name: prod-backup-key
Token ID: aws_5a977c2c9e515f498877bce410c0be50
Created: 2026-02-05T11:48:41

🔴 TRIGGERED | SQL
Name: legacy-database
Token ID: sql_64333eb261c5a6e1e946ddb195dffdfe
Created: 2026-02-05T11:48:44
⚠ Accessed: 3 times
Last access: 2026-02-05T14:23:45

Total: 6 canaries
```

### View Access History
```bash
# All access events
python3 canarydrop.py history

# Specific token
python3 canarydrop.py history --token aws_5a977c2c...

# Limit results
python3 canarydrop.py history --limit 50

# JSON output
python3 canarydrop.py history --json
```

**Sample Output:**
```
================================================================================
                               CANARY ACCESS LOGS
================================================================================

🚨 ALERT - 2026-02-05T14:23:45
Token: sql_64333eb261c5a6e1e946ddb195dffdfe
Name: legacy-database
Type: sql
IP Address: 185.220.101.45
User Agent: python-requests/2.28.0
Additional Info:
  method: connection_attempt
  database: customers
  error: authentication_failed
--------------------------------------------------------------------------------

Total: 1 access events
```

### Get Token Details
```bash
# Detailed information
python3 canarydrop.py info aws_5a977c2c9e515f498877bce410c0be50
```

**Sample Output:**
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
Alert Destination: 

Access Count: 1
Last Accessed: 2026-02-05T11:48:50

Token-Specific Data:
  access_key_id: AKIA0B7F498397DE55E331F0
  secret_access_key: JqlSs9PcZjeMTGXI3ApyWoxNsRU-BpOUcSzhhq8R
  region: us-east-1
```

### View Statistics
```bash
python3 canarydrop.py stats
```

**Sample Output:**
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

### Manual Testing
```bash
# Basic trigger
python3 canarydrop.py trigger aws_5a977c2c... \
  --ip "192.168.1.100"

# With full context
python3 canarydrop.py trigger sql_64333eb... \
  --ip "45.77.123.45" \
  --user-agent "mysql-connector-python/8.0.23" \
  --metadata '{"attempt": "connection", "database": "customers"}'
```

---

## Advanced Scenarios

### Scenario 1: Complete Breach Detection Setup

```bash
# Step 1: Create multiple canary types
python3 canarydrop.py create --type aws-key --name "s3-backup-creds" \
  --memo "Deployed: /opt/backup/aws.conf"

python3 canarydrop.py create --type sql --name "user-database" \
  --memo "Deployed: /etc/app/database.yml.old"

python3 canarydrop.py create --type api-key --name "stripe-live-key" \
  --memo "Deployed: Commented in payment.py"

python3 canarydrop.py create --type email --name "admin-contact" \
  --memo "Deployed: About Us page footer"

# Step 2: Check deployment status
python3 canarydrop.py list

# Step 3: Daily monitoring (add to cron)
python3 canarydrop.py history --limit 20
python3 canarydrop.py stats
```

### Scenario 2: Insider Threat Detection

```bash
# Create canaries for sensitive documents
python3 canarydrop.py create --type document \
  --name "Executive_Salaries_2024.xlsx" \
  --memo "Shared drive: HR/Confidential/"

python3 canarydrop.py create --type document \
  --name "Merger_Plans_CONFIDENTIAL.pdf" \
  --memo "Shared drive: Finance/Strategic/"

python3 canarydrop.py create --type document \
  --name "Employee_Performance_Reviews.docx" \
  --memo "Shared drive: HR/Reviews/"

# Monitor who opens them
python3 canarydrop.py history --json | \
  jq '.[] | select(.token_id | startswith("doc_"))'
```

### Scenario 3: Supply Chain Monitoring

```bash
# Create canaries for code shared externally
python3 canarydrop.py create --type api-key \
  --name "vendor-integration-key" \
  --memo "Shared with: ThirdPartyVendor Inc, 2024-02-05"

python3 canarydrop.py create --type sql \
  --name "demo-database-credentials" \
  --memo "In SDK example code"

# Check if leaked
python3 canarydrop.py history --token api_...
```

---

## Integration Examples

### Export to JSON
```bash
# Export everything
python3 canarydrop.py export

# Export to specific file
python3 canarydrop.py export --output backup-2024-02-05.json
```

### Parse with jq
```bash
# List only triggered canaries
python3 canarydrop.py list --json | \
  jq '.[] | select(.accessed_count > 0)'

# Get all AWS keys
python3 canarydrop.py list --json | \
  jq '.[] | select(.type == "aws-key")'

# Count by type
python3 canarydrop.py list --json | \
  jq 'group_by(.type) | map({type: .[0].type, count: length})'
```

### Monitoring Script
```bash
#!/bin/bash
# monitor-canaries.sh

# Check for new triggers
ALERTS=$(python3 canarydrop.py history --json | \
  jq '[.[] | select(.accessed_at > "'$(date -d '1 hour ago' -Iseconds)'")]')

ALERT_COUNT=$(echo $ALERTS | jq 'length')

if [ $ALERT_COUNT -gt 0 ]; then
    echo "🚨 $ALERT_COUNT new canary alerts!"
    echo "$ALERTS" | jq '.'
    
    # Send to Slack (example)
    # curl -X POST -H 'Content-type: application/json' \
    #   --data "{\"text\":\"Canary Alert: $ALERT_COUNT new triggers\"}" \
    #   $SLACK_WEBHOOK_URL
else
    echo "✓ No new canary triggers"
fi
```

### Daily Report Script
```bash
#!/bin/bash
# daily-canary-report.sh

DATE=$(date +%Y-%m-%d)
REPORT_FILE="canary_report_$DATE.txt"

{
  echo "==================================="
  echo "  Canary Token Daily Report"
  echo "  Date: $DATE"
  echo "==================================="
  echo ""
  
  echo "STATISTICS:"
  python3 canarydrop.py stats
  
  echo ""
  echo "RECENT ALERTS (Last 24 hours):"
  python3 canarydrop.py history --limit 50 | \
    grep -A 10 "$(date -d '1 day ago' +%Y-%m-%d)"
  
  echo ""
  echo "ACTIVE CANARIES:"
  python3 canarydrop.py list | grep "🟢 ACTIVE" | wc -l
  
  echo ""
  echo "TRIGGERED CANARIES:"
  python3 canarydrop.py list | grep "🔴 TRIGGERED" | wc -l
  
} > $REPORT_FILE

# Email report
mail -s "Canary Token Report - $DATE" security@company.com < $REPORT_FILE

echo "Report generated: $REPORT_FILE"
```

### Cleanup Old Canaries
```bash
#!/bin/bash
# cleanup-old-canaries.sh

# Delete canaries older than 6 months that were never triggered
python3 canarydrop.py list --json | \
  jq -r '.[] | select(.accessed_count == 0 and 
    (.created_at | strptime("%Y-%m-%dT%H:%M:%S") | 
    mktime < (now - 15552000))) | .token_id' | \
while read token; do
    echo "Deleting old canary: $token"
    python3 canarydrop.py delete $token --yes
done

echo "✓ Cleanup complete"
```

---

## Delete Operations

### Delete Single Canary
```bash
# With confirmation prompt
python3 canarydrop.py delete aws_5a977c2c...

# Skip confirmation
python3 canarydrop.py delete aws_5a977c2c... --yes
```

### Batch Delete
```bash
# Delete all email canaries
python3 canarydrop.py list --json | \
  jq -r '.[] | select(.type == "email") | .token_id' | \
while read token; do
    python3 canarydrop.py delete $token --yes
done
```

---

## Best Practices

### Naming Convention
```bash
# ✅ Good: Descriptive and location-aware
python3 canarydrop.py create --type aws-key \
  --name "aws-s3-backup-prod-2024" \
  --memo "File: /opt/backup/aws-credentials.conf, Line 47"

# ❌ Bad: Generic and unmemorable
python3 canarydrop.py create --type aws-key \
  --name "canary1"
```

### Regular Monitoring
```bash
# Add to crontab (daily at 9 AM)
0 9 * * * cd /path/to/canarydrop-cli && ./daily-canary-report.sh

# Add to crontab (check every hour)
0 * * * * cd /path/to/canarydrop-cli && ./monitor-canaries.sh
```

### Documentation
```bash
# Always use --memo to document deployment
python3 canarydrop.py create --type sql \
  --name "analytics-db" \
  --memo "Location: docker-compose.yml.backup, Server: prod-app-01, Deployed: 2024-02-05"
```

---

## Troubleshooting

### Database Issues
```bash
# Check database location
ls -la ~/.canarydrop/

# Backup database
cp ~/.canarydrop/canaries.db ~/.canarydrop/canaries.db.backup

# Reset database (WARNING: Deletes all data)
rm ~/.canarydrop/canaries.db
python3 canarydrop.py stats  # Recreates database
```

### Permission Issues
```bash
# Fix executable permission
chmod +x canarydrop.py

# Fix database permissions
chmod 600 ~/.canarydrop/canaries.db
```

### Color Output Issues
```bash
# If colors don't work, use JSON output
python3 canarydrop.py list --json | jq '.'
```

---

**Created with ❤️ for cybersecurity professionals**

For more information, see:
- README.md - Complete documentation
- QUICKSTART.md - 5-minute getting started guide
- DEPLOYMENT_EXAMPLES.md - Real-world deployment scenarios
