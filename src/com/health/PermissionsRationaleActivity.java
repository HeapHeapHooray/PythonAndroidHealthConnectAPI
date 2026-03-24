package com.health;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Toast;

public class PermissionsRationaleActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Toast.makeText(this, "Health Connect permissions are required to display your step count.", Toast.LENGTH_LONG).show();
        finish();
    }
}
