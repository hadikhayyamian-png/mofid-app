[app]
# (User-defined parameters)
title = Mofid Tracker
package.name = mofidtracker
package.domain = org.mofid
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,kivy.garden.graph
orientation = portrait
osx.kivy_version = 2.3.1
android.archs = arm64-v8a
fullscreen = 1

# (MANDATORY CRITICAL SECTIONS FOR ANDROID PACKAGING)
android.api = 34
android.minapi = 21
android.ndk_api = 21
android.private_storage = True
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1

