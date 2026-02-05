#!/bin/bash
# CanaryDrop CLI Installation Script

set -e

echo "================================"
echo "  CanaryDrop CLI Installer"
echo "================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Check minimum version (3.7)
if [ "$(printf '%s\n' "3.7" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.7" ]; then
    echo "❌ Error: Python 3.7 or higher is required"
    exit 1
fi

# Make executable
chmod +x canarydrop.py
echo "✓ Made canarydrop.py executable"

# Test run
if python3 canarydrop.py --help &> /dev/null; then
    echo "✓ Tool is working correctly"
else
    echo "❌ Error: Tool failed to run"
    exit 1
fi

# Create alias option
echo ""
echo "Installation complete! 🎉"
echo ""
echo "You can run the tool with:"
echo "  ./canarydrop.py --help"
echo "  python3 canarydrop.py --help"
echo ""
echo "Optional: Add to PATH for global access"
echo "  sudo ln -s $(pwd)/canarydrop.py /usr/local/bin/canarydrop"
echo ""
echo "Then you can run: canarydrop --help"
echo ""
echo "Get started:"
echo "  1. Read QUICKSTART.md for a 5-minute tutorial"
echo "  2. Check DEPLOYMENT_EXAMPLES.md for real-world scenarios"
echo "  3. See README.md for complete documentation"
echo ""
echo "Create your first canary:"
echo "  python3 canarydrop.py create --type aws-key --name 'my-first-canary'"
echo ""
