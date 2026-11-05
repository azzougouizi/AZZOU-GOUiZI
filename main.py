from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0, 0, 0, 1)

class AzzouApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=15)

        title = Label(
            text="[b]AZZOU GOUiZI[/b]",
            markup=True,
            color=(0, 1, 0.3, 1),
            font_size=30
        )

        self.url = TextInput(
            hint_text="Enter URL",
            multiline=False,
            size_hint_y=None,
            height=50
        )

        button = Button(
            text="SCAN URL",
            background_color=(0, 0.8, 0.2, 1),
            size_hint_y=None,
            height=55
        )
        button.bind(on_press=self.scan)

        self.result = Label(
            text="Ready to scan",
            color=(0, 1, 0.3, 1)
        )

        layout.add_widget(title)
        layout.add_widget(self.url)
        layout.add_widget(button)
        layout.add_widget(self.result)

        return layout

    def scan(self, instance):
        import socket
        from urllib.parse import urlparse

        url = self.url.text.strip()

        if not url:
            self.result.text = "Enter a URL first!"
            return

        if "://" not in url:
            url = "https://" + url

        try:
            host = urlparse(url).hostname
            if not host:
                self.result.text = "Invalid URL"
                return

            socket.getaddrinfo(host, None)
            self.result.text = "Domain resolved: " + host

        except Exception:
            self.result.text = "Could not resolve domain"

AzzouApp().run()
