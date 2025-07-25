[app]

title = Licznik Kalorii
package.name = caloriecounter
package.domain = org.dudek.caloriecounter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_dirs = tests, bin, venv, __pycache__, .git, .github
version = 1.0
requirements = python3,kivy==2.1.0,kivymd==1.1.1,pillow
orientation = portrait
fullscreen = 1

# Improved build settings
android.gradle_dependencies = 
android.add_jars = 
android.add_src = 
android.add_aars = 

android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = True
android.release_artifact = apk
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.logcat_filters = *:S python:D

# Additional settings to fix build issues
android.skip_update = False
android.numeric_version = 1

[buildozer]

log_level = 2
warn_on_root = 1
