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
            size_hint=(1, 0.4)
        )
        
        btn_status = Button(
            text="1. Check Status",
            font_size='20sp',
            size_hint=(1, 0.2)
        )
        btn_status.bind(on_press=self.check_health_connect)
        
        btn_read = Button(
            text="2. Read Steps (Today)",
            font_size='20sp',
            size_hint=(1, 0.2)
        )
        btn_read.bind(on_press=self.read_steps)
        
        layout.add_widget(self.label)
        layout.add_widget(btn_status)
        layout.add_widget(btn_read)
        
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

if __name__ == '__main__':
    AndroidApp().run()