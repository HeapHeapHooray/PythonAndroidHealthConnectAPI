package com.health

import android.app.Activity
import androidx.health.connect.client.HealthConnectClient
import androidx.health.connect.client.records.StepsRecord
import androidx.health.connect.client.request.ReadRecordsRequest
import androidx.health.connect.client.time.TimeRangeFilter
import kotlinx.coroutines.MainScope
import kotlinx.coroutines.launch
import java.time.Instant
import kotlin.reflect.KClass

class HealthConnectWrapper {
    interface Callback {
        fun onResult(result: String)
        fun onError(error: String)
    }

    private val scope = MainScope()

    fun readSteps(activity: Activity, startTimeMillis: Long, endTimeMillis: Long, callback: Callback) {
        val client = HealthConnectClient.getOrCreate(activity)
        scope.launch {
            try {
                val response = client.readRecords(
                    ReadRecordsRequest(
                        recordType = StepsRecord::class,
                        timeRangeFilter = TimeRangeFilter.between(
                            Instant.ofEpochMilli(startTimeMillis),
                            Instant.ofEpochMilli(endTimeMillis)
                        )
                    )
                )
                var totalSteps = 0L
                for (record in response.records) {
                    totalSteps += record.count
                }
                callback.onResult(totalSteps.toString())
            } catch (e: Exception) {
                callback.onError(e.message ?: "Unknown error")
            }
        }
    }
}
