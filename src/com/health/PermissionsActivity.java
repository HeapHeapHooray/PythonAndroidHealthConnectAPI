package com.health;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.Toast;
import androidx.health.connect.client.PermissionController;
import androidx.health.connect.client.permission.HealthPermission;
import androidx.health.connect.client.records.StepsRecord;
import androidx.health.connect.client.records.SleepSessionRecord;
import androidx.health.connect.client.records.HeartRateRecord;
import androidx.activity.result.contract.ActivityResultContract;
import java.util.HashSet;
import java.util.Set;
import kotlin.jvm.JvmClassMappingKt;

public class PermissionsActivity extends Activity {
    private static final int REQUEST_CODE = 1001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        try {
            ActivityResultContract<Set<String>, Set<String>> contract = PermissionController.createRequestPermissionResultContract();
            Set<String> permissions = new HashSet<>();
            permissions.add(HealthPermission.getReadPermission(JvmClassMappingKt.getKotlinClass(StepsRecord.class)));
            permissions.add(HealthPermission.getReadPermission(JvmClassMappingKt.getKotlinClass(SleepSessionRecord.class)));
            permissions.add(HealthPermission.getReadPermission(JvmClassMappingKt.getKotlinClass(HeartRateRecord.class)));
            
            Intent intent = contract.createIntent(this, permissions);
            startActivityForResult(intent, REQUEST_CODE);
        } catch (Throwable e) {
            e.printStackTrace();
            Toast.makeText(this, "Perms Error: " + e.toString(), Toast.LENGTH_LONG).show();
            finish();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQUEST_CODE) {
            finish();
        }
    }
}