[app]
title = Action & Verite
package.name = actionverite
package.domain = org.orpheun
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas
version = 1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.allow_backup = True
android.debug_artifact = apk
