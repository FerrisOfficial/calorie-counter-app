[app]

title = Licznik Kalorii
package.name = caloriecounter
package.domain = org.dudek.caloriecounter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = tests, bin, venv, __pycache__, .git, .github
version = 1.0
requirements = python3,kivy==2.1.0,kivymd,pillow,setuptools
orientation = portrait
fullscreen = 1

android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = True
android.release_artifact = apk
android.archs = arm64-v8a
android.allow_backup = True
android.logcat_filters = *:S python:D

android.skip_update = False
android.numeric_version = 1
android.bootstrap = sdl2

p4a.branch = master

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0
ios.codesign.allowed = false

# iOS app configuration
ios.bundle_identifier = org.dudek.caloriecounter
ios.bundle_name = Licznik Kalorii
ios.bundle_version = 1.0
ios.bundle_display_name = Licznik Kalorii
ios.version = 1.0
ios.deployment_target = 11.0
ios.arch = arm64
ios.orientation = portrait

[buildozer]

log_level = 2
warn_on_root = 1
