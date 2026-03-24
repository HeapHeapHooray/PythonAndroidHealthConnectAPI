# Python Android Health Connect Example

This project demonstrates how to successfully integrate **Android Health Connect** into a Python (Kivy) Android application built with Buildozer. 

Integrating modern Android APIs (like Health Connect) into a Python framework poses several unique challenges. This document outlines the journey of how we overcame them!

## The Challenges & Solutions

### 1. The Permissions & Rationale Activity Requirement
Health Connect handles highly sensitive data. Unlike standard permissions, it requires the app to declare a "Rationale Activity" in the `AndroidManifest.xml` with specific intent filters (`ACTION_SHOW_PERMISSIONS_RATIONALE`). Without this, the Android system flat-out refuses to show your app in the Health Connect settings.
* **Solution:** We created a `PermissionsRationaleActivity.java` and a `ViewPermissionUsageActivity` alias to satisfy the OS requirements.

### 2. PyJnius vs. Modern Android APIs
Health Connect relies heavily on modern Kotlin Coroutines and `ActivityResultContracts` to request permissions. PyJnius (the bridge between Python and Java in Kivy) struggles to implement these complex asynchronous Java/Kotlin interfaces directly from Python.
* **Solution:** We bypassed PyJnius for the heavy lifting. We wrote native Java wrappers:
  * `PermissionsActivity.java`: A transparent Activity that cleanly launches the Health Connect permission contract.
  * `HealthConnectWrapper.java`: A background worker that uses the `HealthConnectClient` to query data (Steps and Sleep) and passes the results back to Python via a simple callback interface.

### 3. The Buildozer Manifest Bug
To register our new Java Activities, we needed to inject them into the `AndroidManifest.xml`. However, Buildozer's `android.extra_manifest_xml` configuration option currently has a bug where it improperly escapes quotes when passing the XML block to the Android Manifest Merger, resulting in a corrupted manifest.
* **Solution:** We abandoned `android.extra_manifest_xml` and wrote a custom Python-for-Android hook (`p4a_hook.py`).

### 4. Hook Timing & The Overwrite Issue
Initially, our `p4a_hook.py` ran during the `before_apk_build` stage. We discovered that the toolchain completely regenerates the manifest *after* this stage, wiping out our injected activities!
* **Solution:** We moved the hook to trigger on `before_apk_assemble`. This runs milliseconds before Gradle packages the APK, ensuring our injected XML survives the build process.

### 5. Android 11+ Package Visibility (The "Blindfold")
Even with the activities properly registered, requesting permissions threw an `ActivityNotFoundException`. Why? Android 11 introduced Package Visibility rules. By default, apps are "sandboxed" and cannot see other apps installed on the device—including the official Google Health Connect app.
* **Solution:** We updated `p4a_hook.py` to also inject a `<queries>` block into the manifest. This explicitly tells the OS that our app needs to interact with `com.google.android.apps.healthdata`, lifting the blindfold and allowing the intent to route successfully!

## Features

* **Check Status:** Verifies if Health Connect is available on the device.
* **Request Permissions:** Requests read access for Steps and Sleep data using the official Health Connect UI.
* **Read Steps:** Retrieves the total step count for the current day.
* **Read Sleep:** Retrieves the total time slept (in hours and minutes) for the current day.
* **Read Heart Rate:** Retrieves the average heart rate (BPM) for the current day.

## How to Build

To build the debug APK, ensure you have Buildozer installed and run:

```bash
buildozer android debug
```

*(Built autonomously by Gemini! 🚀)*
