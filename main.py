import cv2
import os
import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from plyer import notification
import threading

kivy.require('2.0.0')

class VideoRecorder:
    def __init__(self):
        self.is_recording = False
        self.filename = 'video.avi'

    def start_recording(self):
        self.is_recording = True
        threading.Thread(target=self.record_video).start()

    def stop_recording(self):
        self.is_recording = False

    def record_video(self):
        cap = cv2.VideoCapture(0)  # 0 para a câmera padrão
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.filename, fourcc, 20.0, (640, 480))

        # Notificação de início de gravação
        notification.notify(
            title='Gravação de Vídeo',
            message='Gravação em andamento...',
            timeout=5
        )

        while self.is_recording:
            ret, frame = cap.read()
            if ret:
                out.write(frame)

        cap.release()
        out.release()

class VideoApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.recorder = VideoRecorder()

        start_button = Button(text='Iniciar Gravação')
        start_button.bind(on_press=self.start_recording)

        stop_button = Button(text='Parar Gravação')
        stop_button.bind(on_press=self.stop_recording)

        layout.add_widget(start_button)
        layout.add_widget(stop_button)

        return layout

    def start_recording(self, instance):
        self.recorder.start_recording()

    def stop_recording(self, instance):
        self.recorder.stop_recording()

if __name__ == '__main__':
    VideoApp().run()
