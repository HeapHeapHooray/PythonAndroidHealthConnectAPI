from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform
from datetime import datetime, timedelta
import time

class AndroidApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.label = Label(
            text="Health Connect Example",
            font_size='24sp',
            size_hint=(1, 0.4),
            halign='center',
            valign='middle'
        )
        self.label.bind(width=lambda *x: self.label.setter('text_size')(self.label, (self.label.width - 40, None)))
        
        btn_status = Button(
            text="1. Check Status",
            font_size='20sp',
            size_hint=(1, 0.2)
        )
        btn_status.bind(on_press=self.check_health_connect)
        
        btn_request = Button(
            text="1.5. Request Permissions",
            font_size='20sp',
            size_hint=(1, 0.2)
        )
        btn_request.bind(on_press=self.request_permissions)

        btn_read = Button(
            text="2. Read Steps (Today)",
            font_size='20sp',
            size_hint=(1, 0.2)
        )
        btn_read.bind(on_press=self.read_steps)
        
        btn_sleep = Button(
            text="3. Read Sleep (Today)",
            font_size='20sp',
            size_hint=(1, 0.2)
        )
        btn_sleep.bind(on_press=self.read_sleep)
        
        btn_hr = Button(
            text="4. Read Heart Rate (Today)",
            font_size='20sp',
            size_hint=(1, 0.2)
        )
        btn_hr.bind(on_press=self.read_heart_rate)
        
        layout.add_widget(self.label)
        layout.add_widget(btn_status)
        layout.add_widget(btn_request)
        layout.add_widget(btn_read)
        layout.add_widget(btn_sleep)
        layout.add_widget(btn_hr)
        
        return layout

    def check_health_connect(self, instance):
        if platform != 'android':
            self.label.text = "Error: Not running on Android!"
            return

        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            HealthConnectClient = autoclass('androidx.health.connect.client.HealthConnectClient')
            
            context = PythonActivity.mActivity
            status = HealthConnectClient.getSdkStatus(context)
            
            if status == HealthConnectClient.SDK_AVAILABLE:
                self.label.text = "Health Connect is Available!"
            elif status == HealthConnectClient.SDK_UNAVAILABLE:
                self.label.text = "Health Connect is Unsupported."
            else:
                self.label.text = f"Status Code: {status}"
        except Exception as e:
            self.label.text = f"Error: {str(e)}"

    def request_permissions(self, instance):
        if platform != 'android':
            self.label.text = "Error: Not running on Android!"
            return

        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            PackageManager = autoclass('android.content.pm.PackageManager')
            
            context = PythonActivity.mActivity
            pm = context.getPackageManager()
            
            # Diagnostic check: Let's see if the system actually sees our Activity!
            info = pm.getPackageInfo(context.getPackageName(), PackageManager.GET_ACTIVITIES)
            activities = info.activities
            
            found = False
            if activities:
                for act in activities:
                    if act.name == "com.health.PermissionsActivity":
                        found = True
                        break
            
            if not found:
                self.label.text = "Error: PermissionsActivity not found in installed APK! Please uninstall the old app completely and reinstall the new APK."
                return

            intent = Intent()
            intent.setClassName(context.getPackageName(), "com.health.PermissionsActivity")
            
            context.startActivity(intent)
            self.label.text = "Requesting permissions..."
        except Exception as e:
            self.label.text = f"Permission Error: {str(e)}"

    def read_steps(self, instance):
        if platform != 'android':
            self.label.text = "Error: Not running on Android!"
            return

        try:
            from jnius import autoclass, PythonJavaClass, java_method
            
            # Load our custom Kotlin wrapper
            HealthConnectWrapper = autoclass('com.health.HealthConnectWrapper')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            # Define Callback for the wrapper
            class HealthCallback(PythonJavaClass):
                __javainterfaces__ = ['com/health/HealthConnectWrapper$Callback']
                __javacontext__ = 'app'

                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer

                @java_method('(Ljava/lang/String;)V')
                def onResult(self, result):
                    self.outer.label.text = f"Total Steps: {result}"

                @java_method('(Ljava/lang/String;)V')
                def onError(self, error):
                    self.outer.label.text = f"Read Error: {error}"

            # Calculate time range for today
            now = int(time.time() * 1000)
            start_of_day = int((time.time() - (time.time() % 86400)) * 1000)
            
            wrapper = HealthConnectWrapper()
            wrapper.readSteps(
                PythonActivity.mActivity,
                start_of_day,
                now,
                HealthCallback(self)
            )
            self.label.text = "Reading steps..."
            
        except Exception as e:
            self.label.text = f"Wrapper Error: {str(e)}"

    def read_sleep(self, instance):
        if platform != 'android':
            self.label.text = "Error: Not running on Android!"
            return

        try:
            from jnius import autoclass, PythonJavaClass, java_method
            
            HealthConnectWrapper = autoclass('com.health.HealthConnectWrapper')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            class SleepCallback(PythonJavaClass):
                __javainterfaces__ = ['com/health/HealthConnectWrapper$Callback']
                __javacontext__ = 'app'

                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer

                @java_method('(Ljava/lang/String;)V')
                def onResult(self, result):
                    try:
                        millis = int(result)
                        hours = millis // 3600000
                        minutes = (millis % 3600000) // 60000
                        self.outer.label.text = f"Time Slept: {hours}h {minutes}m"
                    except ValueError:
                        self.outer.label.text = f"Invalid result: {result}"

                @java_method('(Ljava/lang/String;)V')
                def onError(self, error):
                    self.outer.label.text = f"Read Error: {error}"

            # Calculate time range for today
            now = int(time.time() * 1000)
            start_of_day = int((time.time() - (time.time() % 86400)) * 1000)
            
            wrapper = HealthConnectWrapper()
            wrapper.readSleep(
                PythonActivity.mActivity,
                start_of_day,
                now,
                SleepCallback(self)
            )
            self.label.text = "Reading sleep data..."
            
        except Exception as e:
            self.label.text = f"Wrapper Error: {str(e)}"

    def read_heart_rate(self, instance):
        if platform != 'android':
            self.label.text = "Error: Not running on Android!"
            return

        try:
            from jnius import autoclass, PythonJavaClass, java_method
            
            HealthConnectWrapper = autoclass('com.health.HealthConnectWrapper')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            class HRCallback(PythonJavaClass):
                __javainterfaces__ = ['com/health/HealthConnectWrapper$Callback']
                __javacontext__ = 'app'

                def __init__(self, outer):
                    super().__init__()
                    self.outer = outer

                @java_method('(Ljava/lang/String;)V')
                def onResult(self, result):
                    if result == "No data":
                        self.outer.label.text = "Average Heart Rate: No data"
                    else:
                        self.outer.label.text = f"Average Heart Rate: {result} BPM"

                @java_method('(Ljava/lang/String;)V')
                def onError(self, error):
                    self.outer.label.text = f"Read Error: {error}"

            # Calculate time range for today
            now = int(time.time() * 1000)
            start_of_day = int((time.time() - (time.time() % 86400)) * 1000)
            
            wrapper = HealthConnectWrapper()
            wrapper.readHeartRate(
                PythonActivity.mActivity,
                start_of_day,
                now,
                HRCallback(self)
            )
            self.label.text = "Reading heart rate..."
            
        except Exception as e:
            self.label.text = f"Wrapper Error: {str(e)}"

if __name__ == '__main__':
    AndroidApp().run()