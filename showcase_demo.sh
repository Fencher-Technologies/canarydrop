#!/bin/bash
# CanaryDrop CLI - Visual Showcase Demo

echo "════════════════════════════════════════════════════════════════════════════"
echo "              🎬 CanaryDrop CLI - Interactive Demo"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

# Show banner
echo "1️⃣  Displaying beautiful startup banner..."
echo ""
python3 canarydrop.py --help | head -15
echo ""
read -p "Press Enter to continue..."
clear

# Create tokens
echo "2️⃣  Creating various canary tokens..."
echo ""
python3 canarydrop.py create --type aws-key --name "prod-backup-key" --memo "Demo canary"
echo ""
read -p "Press Enter to continue..."
clear

echo "3️⃣  Creating more tokens..."
echo ""
python3 canarydrop.py create --type sql --name "customer-database"
python3 canarydrop.py create --type http --name "admin-panel"
python3 canarydrop.py create --type email --name "info-contact"
echo ""
read -p "Press Enter to continue..."
clear

# List all
echo "4️⃣  Viewing all canary tokens..."
echo ""
python3 canarydrop.py list
echo ""
read -p "Press Enter to continue..."
clear

# Show stats
echo "5️⃣  Viewing statistics dashboard..."
echo ""
python3 canarydrop.py stats
echo ""
read -p "Press Enter to continue..."
clear

# Trigger one
echo "6️⃣  Simulating an attack (triggering a canary)..."
echo ""
TOKEN=$(python3 canarydrop.py list --json | grep -o 'aws_[a-f0-9]*' | head -1)
python3 canarydrop.py trigger "$TOKEN" --ip "45.77.123.45" --user-agent "aws-cli/2.13.0"
echo ""
read -p "Press Enter to continue..."
clear

# Show history
echo "7️⃣  Viewing access logs (ALERT!)..."
echo ""
python3 canarydrop.py history
echo ""
read -p "Press Enter to continue..."
clear

# Show final stats
echo "8️⃣  Final statistics..."
echo ""
python3 canarydrop.py stats
echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "              ✅ Demo Complete! Your canaries are ready."
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  • Check README.md for full documentation"
echo "  • Read QUICKSTART.md to deploy your first real canary"
echo "  • See DEPLOYMENT_EXAMPLES.md for production scenarios"
echo ""
