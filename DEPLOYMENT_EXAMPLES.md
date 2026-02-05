# Real-World Deployment Examples

This document provides copy-paste ready examples for common canary deployment scenarios.

## 1. AWS Credentials in Config Files

### Create the Canary
```bash
python3 canarydrop.py create \
  --type aws-key \
  --name "legacy-backup-service" \
  --memo "Deployed in /var/backups/old-configs/"
```

### Deploy: ~/.aws/credentials (old backup)
```ini
# Old backup service credentials - DEPRECATED
[backup-service]
aws_access_key_id = AKIA[YOUR_CANARY_KEY]
aws_secret_access_key = [YOUR_CANARY_SECRET]
region = us-east-1
```

### Deploy: .env file
```bash
# Legacy environment variables
AWS_ACCESS_KEY_ID=AKIA[YOUR_CANARY_KEY]
AWS_SECRET_ACCESS_KEY=[YOUR_CANARY_SECRET]
AWS_DEFAULT_REGION=us-east-1
```

### Deploy: Commented in Code
```python
# Old AWS configuration - DO NOT USE
# aws_key = "AKIA[YOUR_CANARY_KEY]"
# aws_secret = "[YOUR_CANARY_SECRET]"
```

---

## 2. Database Connection Strings

### Create the Canary
```bash
python3 canarydrop.py create \
  --type sql \
  --name "legacy-customer-database" \
  --memo "Deployed in old app configs"
```

### Deploy: .env File
```bash
# Legacy database connection
DATABASE_URL=mysql://canary_abc123:password@db-old.internal:3306/customers
DB_HOST=db-old.internal
DB_USER=canary_abc123
DB_PASS=[YOUR_CANARY_PASSWORD]
DB_NAME=customers
```

### Deploy: Django settings.py (commented)
```python
# Old database configuration - DEPRECATED
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'customers',
#         'USER': 'canary_abc123',
#         'PASSWORD': '[YOUR_CANARY_PASSWORD]',
#         'HOST': 'db-old.internal',
#         'PORT': '3306',
#     }
# }
```

### Deploy: Connection String in README
```markdown
## Database Setup (DEPRECATED)

Old connection string (do not use):
`mysql://canary_abc123:[PASSWORD]@db-old.internal:3306/customers`
```

---

## 3. API Keys in Documentation

### Create the Canary
```bash
python3 canarydrop.py create \
  --type api-key \
  --name "stripe-test-key" \
  --memo "In API documentation examples"
```

### Deploy: API Documentation
```markdown
## Authentication

Example API call:
```bash
curl -X POST https://api.example.com/charge \
  -H "Authorization: Bearer sk_[YOUR_CANARY_KEY]" \
  -d amount=1000
```

### Deploy: Code Comments
```javascript
// Example API key - DO NOT USE IN PRODUCTION
// const API_KEY = 'sk_[YOUR_CANARY_KEY]';
```

### Deploy: .gitignore'd Config (that got committed anyway)
```json
{
  "api_keys": {
    "stripe_test": "sk_[YOUR_CANARY_KEY]",
    "stripe_live": "sk_[YOUR_CANARY_KEY]"
  }
}
```

---

## 4. Fake Documents with Tracking

### Create the Canary
```bash
python3 canarydrop.py create \
  --type document \
  --name "Executive_Compensation_2024.docx" \
  --memo "Shared drive HR folder"
```

### Deploy: In Microsoft Word

1. Insert → Online Pictures
2. Paste the callback URL
3. Make image 1x1 pixel
4. Save as "Executive_Compensation_2024.docx"
5. Place in shared drive

### Deploy: In HTML Email Signature
```html
<!-- Tracking pixel -->
<img src="https://canarytokens.local/doc/[TOKEN_ID]/track.gif" 
     width="1" height="1" border="0" style="display:none;">
```

### Deploy: In PDF (HTML method)
```html
<!DOCTYPE html>
<html>
<head><title>Confidential Report</title></head>
<body>
    <h1>Q4 Financial Results - CONFIDENTIAL</h1>
    <p>Revenue: $5.2M</p>
    <img src="https://canarytokens.local/doc/[TOKEN_ID]/track.gif" 
         width="1" height="1" style="position:absolute;left:-9999px;">
</body>
</html>
```

Then: Print to PDF or use wkhtmltopdf

---

## 5. DNS Tokens in Configurations

### Create the Canary
```bash
python3 canarydrop.py create \
  --type dns \
  --name "internal-api-hostname" \
  --memo "In service discovery configs"
```

### Deploy: /etc/hosts (backup file)
```bash
# Old internal services
10.0.1.100  api.internal.company.com
10.0.1.101  db.internal.company.com
10.0.1.102  [YOUR_CANARY_HOSTNAME]
```

### Deploy: In Code (commented)
```python
# Legacy service endpoints
# API_ENDPOINT = "https://[YOUR_CANARY_HOSTNAME]/api/v1"
# DB_ENDPOINT = "https://[YOUR_CANARY_HOSTNAME]:5432"
```

### Deploy: Docker Compose
```yaml
# Old service configuration
services:
  api:
    image: company/api:old
    environment:
      - SERVICE_URL=https://[YOUR_CANARY_HOSTNAME]
```

---

## 6. Email Canaries in Contact Lists

### Create the Canary
```bash
python3 canarydrop.py create \
  --type email \
  --name "marketing-list-entry-47" \
  --memo "Added to customer CRM"
```

### Deploy: In CRM/Database
```sql
INSERT INTO customers (name, email, segment) VALUES
('John Doe', 'john@example.com', 'premium'),
('Test User', '[YOUR_CANARY_EMAIL]', 'standard'),
('Jane Smith', 'jane@example.com', 'premium');
```

### Deploy: In Newsletter Signup Form
Add as a hidden test subscriber

### Deploy: In Contact Management Spreadsheet
```csv
Name,Email,Status,Notes
John Doe,john@example.com,Active,VIP Customer
Test Account,[YOUR_CANARY_EMAIL],Active,Internal Test
Jane Smith,jane@example.com,Active,Regular
```

---

## 7. QR Codes for Physical Security

### Create the Canary
```bash
python3 canarydrop.py create \
  --type qr-code \
  --name "wifi-credentials-poster" \
  --url "https://mycompany.com/network/access" \
  --memo "Server room poster"
```

### Deploy: Generate QR Code

Visit https://www.qr-code-generator.com/ and paste your canary URL

### Use Cases:
- **Fake WiFi credentials** poster in restricted areas
- **Equipment checkout** forms in secure locations  
- **Access instructions** in data centers
- **Training materials** with sensitive info

Print and laminate the QR code poster:

```
╔═══════════════════════════════════╗
║    RESTRICTED AREA WIFI ACCESS    ║
║                                   ║
║    [QR CODE HERE]                 ║
║                                   ║
║    Scan for network credentials   ║
║    Authorized personnel only      ║
╚═══════════════════════════════════╝
```

---

## 8. Multi-Layered Defense Example

Deploy multiple canaries in different locations to create defense-in-depth:

```bash
# Layer 1: Code repository
python3 canarydrop.py create --type aws-key --name "repo-config"
# Deploy in: .github/workflows/deploy.yml.old

# Layer 2: File servers  
python3 canarydrop.py create --type document --name "HR-Salaries.xlsx"
# Deploy in: \\fileserver\hr\archive\2020\

# Layer 3: Database backups
python3 canarydrop.py create --type sql --name "backup-db-connection"
# Deploy in: /var/backups/database/credentials.txt

# Layer 4: Email system
python3 canarydrop.py create --type email --name "info-mailbox"
# Deploy in: Public contact database

# Layer 5: API documentation
python3 canarydrop.py create --type api-key --name "docs-example"
# Deploy in: README.md examples
```

Check all layers weekly:
```bash
python3 canarydrop.py list
python3 canarydrop.py history
```

---

## Best Practices for Deployment

### Naming Convention
Use descriptive names that tell you WHERE it's deployed:
- ✅ `aws-key-github-actions-old`
- ✅ `sql-backup-server-2020`
- ✅ `email-crm-test-account`
- ❌ `canary1`
- ❌ `test`

### Memo Field
Always document the exact location:
```bash
python3 canarydrop.py create \
  --type aws-key \
  --name "backup-service" \
  --memo "File: /var/backups/configs/2020-aws.conf, Line 47"
```

### Rotation Schedule
```bash
# Create rotation script
#!/bin/bash
# rotate-canaries.sh

# Delete old canaries (6+ months)
for token in $(python3 canarydrop.py list --json | jq -r '.[] | select(.created_at < "'$(date -d '6 months ago' +%Y-%m-%d)'") | .token_id'); do
    python3 canarydrop.py delete $token --yes
done

# Create fresh canaries
python3 canarydrop.py create --type aws-key --name "q1-backup-key"
python3 canarydrop.py create --type sql --name "q1-db-connection"
```

### Alert Integration (Coming Soon)
```bash
# When webhook support is added:
python3 canarydrop.py create \
  --type aws-key \
  --name "production-key" \
  --alert webhook \
  --destination "https://hooks.slack.com/services/YOUR/WEBHOOK"
```

---

## Monitoring Script

Create a daily monitoring script:

```bash
#!/bin/bash
# check-canaries.sh

echo "=== Canary Status Report ==="
echo "Date: $(date)"
echo ""

# Show statistics
python3 canarydrop.py stats

echo ""
echo "=== Recent Alerts ==="
python3 canarydrop.py history --limit 10

# Send to security team (example)
# python3 canarydrop.py history --json | \
#   mail -s "Daily Canary Report" security@company.com
```

Run daily with cron:
```bash
0 9 * * * /path/to/check-canaries.sh | mail -s "Canary Report" security@company.com
```

---

## Response Playbook

When a canary is triggered:

1. **Immediate Actions** (0-5 minutes)
   ```bash
   # Get details
   python3 canarydrop.py info [TOKEN_ID]
   
   # Check for other triggers
   python3 canarydrop.py history
   ```

2. **Investigation** (5-30 minutes)
   - Identify source IP/user
   - Check other logs for related activity
   - Determine if test or real incident

3. **Containment** (if real incident)
   - Isolate affected systems
   - Reset actual credentials
   - Block attacker IP
   
4. **Documentation**
   - Record incident details
   - Update security procedures
   - Create new canaries in different locations

---

**Remember**: The goal is detection, not prevention. Canaries give you early warning!
