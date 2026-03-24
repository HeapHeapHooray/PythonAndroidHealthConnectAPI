import os
import glob

def before_apk_build(toolchain):
    print("Running custom p4a hook to inject activities!")
    
    # Try to find AndroidManifest.xml starting from current directory
    cwd = os.getcwd()
    manifest_path = None
    
    for root, dirs, files in os.walk(cwd):
        if 'AndroidManifest.xml' in files and 'src/main' in root.replace('\\', '/'):
            manifest_path = os.path.join(root, 'AndroidManifest.xml')
            break
            
    if not manifest_path:
        print("Could not find AndroidManifest.xml!")
        return
        
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    extra_xml = """
        <activity android:name="com.health.PermissionsActivity" android:theme="@android:style/Theme.Translucent.NoTitleBar" />
        <activity android:name="com.health.PermissionsRationaleActivity" android:exported="true">
            <intent-filter>
                <action android:name="androidx.health.ACTION_SHOW_PERMISSIONS_RATIONALE" />
            </intent-filter>
        </activity>
        <activity-alias
            android:name="com.health.ViewPermissionUsageActivity"
            android:exported="true"
            android:targetActivity="com.health.PermissionsRationaleActivity"
            android:permission="android.permission.START_VIEW_PERMISSION_USAGE">
            <intent-filter>
                <action android:name="android.intent.action.VIEW_PERMISSION_USAGE" />
                <category android:name="android.intent.category.HEALTH_PERMISSIONS" />
            </intent-filter>
        </activity-alias>
    """
    
    if '</application>' in content and 'com.health.PermissionsActivity' not in content:
        content = content.replace('</application>', extra_xml + '\n    </application>')
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully injected activities into AndroidManifest.xml at " + manifest_path)
    else:
        print("Activities already injected or </application> tag not found.")
