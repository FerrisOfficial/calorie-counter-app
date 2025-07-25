# iOS Build Guide for Licznik Kalorii

This guide will help you build the Licznik Kalorii app for iOS devices.

## Prerequisites

- **macOS** (iOS development requires macOS)
- **Xcode** installed from the App Store
- **Command Line Tools** for Xcode
- **Python 3.11+**
- **Homebrew** (package manager for macOS)

## Method 1: Using kivy-ios (Recommended)

### Step 1: Install Dependencies

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install system dependencies
brew install autoconf automake libtool pkg-config libffi openssl cmake

# Install Python dependencies
pip3 install --upgrade pip setuptools wheel
pip3 install cython==0.29.33 kivy-ios
```

### Step 2: Build iOS Dependencies

```bash
# This will take 15-30 minutes
kivy-ios build python3 kivy pillow
```

### Step 3: Create iOS Project

```bash
# Create the iOS project
kivy-ios create "Licznik Kalorii" org.dudek.caloriecounter

# Copy your app files
cp main.py "Licznik Kalorii-ios/"
cp calorie_counter_app.py "Licznik Kalorii-ios/"
```

### Step 4: Open in Xcode

```bash
cd "Licznik Kalorii-ios"
open "Licznik Kalorii.xcodeproj"
```

### Step 5: Build and Run

1. In Xcode, select your target device or simulator
2. Click the play button (▶️) to build and run
3. For real devices, you'll need:
   - Apple Developer Account
   - Code signing certificate
   - Provisioning profile

## Method 2: Using Buildozer

### Step 1: Install Buildozer

```bash
pip3 install buildozer
```

### Step 2: Build iOS App

```bash
buildozer ios debug
```

## Method 3: Automatic Build (GitHub Actions)

This repository includes two GitHub Actions workflows for iOS:

1. **build-ios.yml** - Uses kivy-ios directly
2. **build-ios-buildozer.yml** - Uses buildozer

These will automatically build iOS apps when you push to the main branch.

## Troubleshooting

### "xcrun: error: invalid active developer path"

```bash
sudo xcode-select --install
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

### "Command Line Tools not found"

1. Open Xcode
2. Go to Preferences → Locations
3. Select Command Line Tools version

### "No developer certificate found"

1. Sign up for Apple Developer Program ($99/year)
2. Create certificates in Xcode or Apple Developer portal
3. Add your device to provisioning profile

### Build fails with "recipe not found"

```bash
# Clean and rebuild dependencies
rm -rf ~/.kivy-ios
kivy-ios build python3 kivy pillow
```

## App Store Distribution

To distribute on the App Store:

1. Join Apple Developer Program
2. Create App Store Connect record
3. Archive the app in Xcode
4. Upload to App Store Connect
5. Submit for review

## Local Testing

### iOS Simulator

- No developer account needed
- Faster testing
- Available CPU architectures: x86_64, arm64

### Real iOS Device

- Requires Apple Developer account
- Enable "Developer Mode" in iOS Settings
- Trust the developer certificate

## Configuration

The iOS configuration is in `buildozer.spec`:

```ini
ios.bundle_identifier = org.dudek.caloriecounter
ios.bundle_name = Licznik Kalorii
ios.deployment_target = 11.0
ios.arch = arm64
```

You can modify these settings as needed.
