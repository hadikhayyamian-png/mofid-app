[app]
title = Mofid Tracker
package.name = mofidtracker
package.domain = org.mofid

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# Android API/target settings â€” leave at defaults unless you need a specific SDK level
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
