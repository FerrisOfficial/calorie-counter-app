#!/bin/bash

# iOS Build Setup Script for Licznik Kalorii
# Run this on macOS to set up iOS development environment

echo "🍎 Setting up iOS build environment for Licznik Kalorii..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script must be run on macOS for iOS development"
    exit 1
fi

# Install Homebrew if not present
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install system dependencies
echo "🔧 Installing system dependencies..."
brew install python@3.11 autoconf automake libtool pkg-config libffi openssl cmake

# Set up Python environment
echo "🐍 Setting up Python environment..."
python3 -m pip install --upgrade pip setuptools wheel
pip3 install cython==0.29.33

# Install kivy-ios
echo "📱 Installing kivy-ios..."
pip3 install kivy-ios

# Build iOS dependencies
echo "🏗️ Building iOS dependencies (this may take a while)..."
kivy-ios build python3 kivy pillow

# Create iOS project
echo "📲 Creating iOS project..."
kivy-ios create "Licznik Kalorii" org.dudek.caloriecounter

# Copy app files
echo "📋 Copying application files..."
cp main.py "Licznik Kalorii-ios/"
cp calorie_counter_app.py "Licznik Kalorii-ios/"

echo "✅ iOS setup complete!"
echo ""
echo "Next steps:"
echo "1. cd 'Licznik Kalorii-ios'"
echo "2. Open 'Licznik Kalorii.xcodeproj' in Xcode"
echo "3. Select your target device/simulator"
echo "4. Click the play button to build and run"
echo ""
echo "Note: You may need to:"
echo "- Sign the app with your Apple Developer account"
echo "- Add your device to the provisioning profile"
echo "- Enable Developer Mode on your iOS device"
