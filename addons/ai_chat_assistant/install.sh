#!/bin/bash

# AI Chat Assistant Module - Installation Script

echo "🤖 AI Chat Assistant Module Installation"
echo "=========================================="
echo ""

# Step 1: Check Python version
echo "✓ Step 1: Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Step 2: Install Python dependencies
echo ""
echo "✓ Step 2: Installing Python dependencies..."
pip install --upgrade pip
pip install transformers>=4.30.0
pip install torch>=2.0.0
pip install bitsandbytes>=0.40.0
pip install numpy>=1.24.0
pip install underthesea>=1.3.3

if [ $? -ne 0 ]; then
    echo "⚠️  Some packages failed to install. Check your internet connection."
else
    echo "✅ All packages installed successfully"
fi

# Step 3: Check GPU availability
echo ""
echo "✓ Step 3: Checking GPU availability..."
python3 << 'EOF'
import torch
if torch.cuda.is_available():
    print(f"✅ GPU Available: {torch.cuda.get_device_name(0)}")
    print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
else:
    print("⚠️  GPU not available. LLM will run on CPU (slower)")
EOF

# Step 4: Verify module structure
echo ""
echo "✓ Step 4: Verifying module structure..."
if [ -f "__manifest__.py" ] && [ -f "models/chat_log.py" ] && [ -f "controllers/main.py" ]; then
    echo "✅ Module structure is correct"
else
    echo "❌ Module structure is incomplete"
    exit 1
fi

# Step 5: Check Odoo installation
echo ""
echo "✓ Step 5: Checking Odoo installation..."
ODOO_PATH=$(find / -name "odoo-bin" -type f 2>/dev/null | head -1)
if [ -n "$ODOO_PATH" ]; then
    echo "✅ Odoo found at: $ODOO_PATH"
else
    echo "⚠️  Odoo not found in standard paths"
fi

# Step 6: Display module info
echo ""
echo "✓ Step 6: Module Information"
echo "=========================================="
grep -E "'^[[:space:]]*\"name\"|\"version\"|\"category\"'" __manifest__.py | head -3
echo "=========================================="

echo ""
echo "✅ Installation check complete!"
echo ""
echo "Next steps:"
echo "1. Place this module in your Odoo addons directory"
echo "2. Restart Odoo service"
echo "3. Go to Apps menu and search for 'AI Chat Assistant'"
echo "4. Click Install button"
echo "5. Chat widget should appear in the bottom-right corner"
echo ""
echo "For more information, read README.md"
