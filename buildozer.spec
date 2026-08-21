[app]

title = Mofid Tracker
package.name = mofidtracker
package.domain = org.mofid

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 0.1

requirements = python3,kivy,kivy-garden

orientation = portrait
fullscreen = 1

android.archs = arm64-v8a
android.api = 34
android.minapi = 24
android.ndk_api = 24

android.permissions = INTERNET

# Don't package build artifacts
source.exclude_dirs = .git,.github,.buildozer,bin,venv

[buildozer]

log_level = 2
warn_on_root = 1
