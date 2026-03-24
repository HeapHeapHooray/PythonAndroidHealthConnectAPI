from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import platform

class AndroidApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        self.label = Label(
            text="Health Connect Example",
            font_size='24sp',
            size_hint=(1, 0.6)
        )
        
        button = Button(
            text="Check Health Connect Status",
            font_size='20sp',
            size_hint=(1, 0.4)
        )
        button.bind(on_press=self.check_health_connect)
        
        layout.add_widget(self.label)
        layout.add_widget(button)
        
        return layout

    def check_health_connect(self, instance):
        if platform != 'android':
            self.label.text = "Error: Not running on Android!"
            return

        try:
            from jnius import autoclass
            
            # Load Android Activity and Health Connect Client
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            HealthConnectClient = autoclass('androidx.health.connect.client.HealthConnectClient')
            
            context = PythonActivity.mActivity
            
            # Check SDK availability
            status = HealthConnectClient.getSdkStatus(context)
            
            if status == HealthConnectClient.SDK_AVAILABLE:
                self.label.text = "Health Connect is Available!\nReady to request permissions."
                # client = HealthConnectClient.getOrCreate(context)
                # Next steps: Request permissions and read data
            elif status == HealthConnectClient.SDK_UNAVAILABLE:
                self.label.text = "Health Connect is not supported\non this device."
            elif status == HealthConnectClient.SDK_UNAVAILABLE_PROVIDER_UPDATE_REQUIRED:
                self.label.text = "Health Connect needs an update.\nPlease check the Play Store."
            else:
                self.label.text = f"Unknown Health Connect Status: {status}"
                
        except Exception as e:
            self.label.text = f"Pyjnius Error:\n{str(e)}"

if __name__ == '__main__':
    AndroidApp().run()