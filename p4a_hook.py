import os

def before_apk_assemble(toolchain):
    print("Running custom p4a hook to inject activities right before assemble!")
    
    cwd = os.getcwd()
    
    for root, dirs, files in os.walk(cwd):
        if 'AndroidManifest.xml' in files and 'src/main' in root.replace('\\', '/'):
            manifest_path = os.path.join(root, 'AndroidManifest.xml')
            
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
            queries_xml = """
    <queries>
        <package android:name="com.google.android.apps.healthdata" />
        <intent>
            <action android:name="androidx.health.ACTION_REQUEST_PERMISSIONS" />
        </intent>
    </queries>
    """
            
            modified = False
            if '</application>' in content and 'com.health.PermissionsActivity' not in content:
                content = content.replace('</application>', extra_xml + '\n    </application>')
                modified = True
                print("Injected activities into AndroidManifest.xml at " + manifest_path)
            
            if '<queries>' not in content and '<application' in content:
                content = content.replace('<application', queries_xml + '<application')
                modified = True
                print("Injected queries into AndroidManifest.xml at " + manifest_path)
                
            if modified:
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    f.write(content)

