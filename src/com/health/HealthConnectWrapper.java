package com.health;

import android.app.Activity;
import androidx.health.connect.client.HealthConnectClient;
import androidx.health.connect.client.records.StepsRecord;
import androidx.health.connect.client.request.ReadRecordsRequest;
import androidx.health.connect.client.time.TimeRangeFilter;
import androidx.health.connect.client.response.ReadRecordsResponse;
import androidx.health.connect.client.records.metadata.DataOrigin;
import java.time.Instant;
import java.util.HashSet;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.CoroutineContext;
import kotlin.coroutines.EmptyCoroutineContext;
import kotlin.jvm.JvmClassMappingKt;

public class HealthConnectWrapper {
    public interface Callback {
        void onResult(String result);
        void onError(String error);
    }

    public void readSteps(final Activity activity, final long startTimeMillis, final long endTimeMillis, final Callback callback) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    HealthConnectClient client = HealthConnectClient.getOrCreate(activity);
                    TimeRangeFilter filter = TimeRangeFilter.between(
                        Instant.ofEpochMilli(startTimeMillis),
                        Instant.ofEpochMilli(endTimeMillis)
                    );
                    
                    ReadRecordsRequest<StepsRecord> request = new ReadRecordsRequest<>(
                        JvmClassMappingKt.getKotlinClass(StepsRecord.class), 
                        filter, new HashSet<DataOrigin>(), true, 1000, null
                    );
                    
                    client.readRecords(request, new Continuation<ReadRecordsResponse<StepsRecord>>() {
                        @Override
                        public CoroutineContext getContext() {
                            return EmptyCoroutineContext.INSTANCE;
                        }

                        @Override
                        public void resumeWith(Object result) {
                            try {
                                ReadRecordsResponse<StepsRecord> response = (ReadRecordsResponse<StepsRecord>) result;
                                long totalSteps = 0;
                                for (StepsRecord record : response.getRecords()) {
                                    totalSteps += record.getCount();
                                }
                                callback.onResult(String.valueOf(totalSteps));
                            } catch (Exception e) {
                                callback.onError("Read failed: " + result.toString() + " | " + e.getMessage());
                            }
                        }
                    });
                } catch (Exception e) {
                    callback.onError(e.getMessage() != null ? e.getMessage() : "Unknown error");
                }
            }
        }).start();
    }
}