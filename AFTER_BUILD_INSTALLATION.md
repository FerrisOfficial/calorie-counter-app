# iOS Installation Guide - After Successful Build

## 🎯 What You Get After Build

After a successful iOS build, you'll have:
- `Licznik Kalorii.app` - The iOS application
- `Licznik Kalorii.xcodeproj` - Xcode project for signing/deployment
- Build logs and artifacts

## 📱 Installation Options

### Option 1: iOS Simulator (✅ Works Immediately)

**What you can do:**
- Install and test immediately
- No Apple Developer account needed
- No code signing required

**How to install:**
```bash
# If using kivy-ios
cd "Licznik Kalorii-ios"
open "Licznik Kalorii.xcodeproj"
# Select iOS Simulator and click Run

# If using buildozer
buildozer ios debug
# The app will launch in simulator automatically
```

**Limitations:**
- Only works on Mac with Xcode
- Can't test real device features (camera, GPS, etc.)
- Performance may differ from real device

### Option 2: Real iOS Device (⚠️ Requires Additional Setup)

**What you need:**
1. **Apple Developer Account** ($99/year)
2. **Mac with Xcode**
3. **Your iOS device**
4. **Code signing setup**

**Step-by-step process:**

#### Step 1: Get Apple Developer Account
```
1. Go to https://developer.apple.com
2. Sign up for Developer Program ($99/year)
3. Wait for approval (usually 24-48 hours)
```

#### Step 2: Setup Code Signing in Xcode
```
1. Open "Licznik Kalorii.xcodeproj" in Xcode
2. Select project in navigator
3. Go to "Signing & Capabilities" tab
4. Enable "Automatically manage signing"
5. Select your development team
6. Xcode will create certificates automatically
```

#### Step 3: Register Your Device
```
1. Connect iPhone/iPad to Mac
2. In Xcode: Window → Devices and Simulators
3. Select your device
4. Click "Use for Development"
5. Trust the computer on your device
```

#### Step 4: Install on Device
```
1. Select your device in Xcode
2. Click Run (▶️) button
3. App will install and launch on device
```

### Option 3: TestFlight Distribution (📤 For Beta Testing)

**What it's for:**
- Share app with testers (up to 100 people)
- No need for testers to have Xcode
- Apple handles distribution

**Requirements:**
- Apple Developer Account
- App Store Connect access
- Archive build (not debug)

**Process:**
```
1. Archive app in Xcode (Product → Archive)
2. Upload to App Store Connect
3. Create TestFlight build
4. Invite testers via email
5. Testers install via TestFlight app
```

### Option 4: App Store Release (🏪 Public Distribution)

**What it's for:**
- Public distribution via App Store
- Monetization options
- Widest reach

**Requirements:**
- Apple Developer Account
- App Store review approval
- App Store guidelines compliance

## 🔧 Quick Setup for Device Testing

If you want to test on your own device quickly:

### Update buildozer.spec for device builds:

```ini
# Enable code signing
ios.codesign.allowed = true

# Xcode will auto-manage signing if you don't specify these
# ios.codesign.debug = "iPhone Developer"
# ios.codesign.release = "iPhone Developer"
```

### Alternative: Manual Xcode Setup

1. Build with current settings (simulator)
2. Open `.xcodeproj` in Xcode
3. Enable "Automatically manage signing"
4. Select your Apple ID team
5. Build and run on device

## 💰 Cost Breakdown

| Method | Cost | What You Get |
|--------|------|--------------|
| Simulator Only | Free | Testing on Mac only |
| Device Testing | $99/year | Install on your devices |
| TestFlight | $99/year | Beta testing with others |
| App Store | $99/year + review | Public distribution |

## 🚨 Common Issues

### "No developer certificate found"
- Solution: Join Apple Developer Program
- Alternative: Use iOS Simulator for free testing

### "Device not recognized"
- Solution: Enable Developer Mode in iOS Settings
- Update Xcode and iOS to latest versions

### "App installation failed"
- Solution: Check code signing settings
- Ensure device is registered in developer account

## 📋 Summary

**If you just want to see your app running:**
- iOS Simulator works immediately after build ✅

**If you want to install on your iPhone/iPad:**
- You need Apple Developer Account ($99/year) ⚠️

**If you want to share with others:**
- TestFlight or App Store (both require developer account) 📤

The GitHub Actions build will create a working app, but installing it on real devices requires the additional Apple Developer setup.
