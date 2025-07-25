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

[buildozer]

log_level = 2
warn_on_root = 1
