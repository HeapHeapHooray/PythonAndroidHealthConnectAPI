[app]
title = My Application
package.name = myapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,pyjnius

orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1

fullscreen = 0
android.permissions = INTERNET, android.permission.health.READ_STEPS, android.permission.health.READ_HEART_RATE
android.api = 35
android.minapi = 26
android.sdk = 35
android.ndk = 25b
android.enable_androidx = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.debug_artifact = apk

android.add_src = src
android.gradle_dependencies = androidx.health.connect:connect-client:1.1.0-alpha11, org.jetbrains.kotlinx:kotlinx-coroutines-android:1.7.3, org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3

p4a.hook = p4a_hook.py

[buildozer]
build_dir = /tmp/python-android-buildozer
log_level = 2
warn_on_root = 1
