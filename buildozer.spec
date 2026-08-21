[app]
title = Mofid Tracker
package.name = mofidtracker
package.domain = org.mofid
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivy_garden.graph
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

# Critical SDK parameters for modern Android devices
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.private_storage = True
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
