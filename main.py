__version__ = "1.0"

import time
from os import path
from kivy.app import App
from kivy.utils import platform
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.context_instructions import PopMatrix, PushMatrix, Rotate

class Recognition(App):
    def build(self):
        self.floatLayout = FloatLayout()
        self.floatLayout.orientation = 'vertical'

        self.button = Button()
        self.button.text = 'Capture'
        self.button.size_hint = (1, .1)
        self.button.disabled = False
        self.button.bind(on_press = self.capture)
        self.floatLayout.add_widget(self.button)

        if not self.check_permissions_granted():
            self.button.disabled = True
            from kivy.uix.label import Label
            label = Label()
            label.text = 'The app needs camera and\nstorage access to work.\nRestart the app\nand grant access.'
            label.halign = 'center'
            self.floatLayout.add_widget(label)
            return self.floatLayout

        self.camera = Camera()
        self.camera.resolution = (640, 480)
        self.camera.size = (Window.height, Window.width)
        self.camera.allow_stretch = True
        self.camera.keep_ratio = True
        self.camera.play = True
        
        with self.camera.canvas.before:
            PushMatrix()
            self.rot = Rotate()
            self.rot.angle = -90
            self.rot.origin = (self.camera.center_y, self.camera.center_x)
        with self.camera.canvas.after:
            PopMatrix()

        self.floatLayout.add_widget(self.camera)

        return self.floatLayout

    def check_permissions_granted(self):
        nChecks = 10   #number of checks until giving up
        timeSleep = 1  #sleep time between checks
        check = False
        if platform == 'android':
            from android.permissions import request_permissions, Permission, check_permission
            if check_permission(Permission.CAMERA) and check_permission(Permission.WRITE_EXTERNAL_STORAGE):
                check = True
            else:
               request_permissions([Permission.CAMERA, Permission.WRITE_EXTERNAL_STORAGE])
               time.sleep(timeSleep)
               check = True
               count = 0
               while not (check_permission(Permission.CAMERA) and check_permission(Permission.WRITE_EXTERNAL_STORAGE)):
                   if count > nChecks:
                       check = False
                       break
                   count+=1
                   time.sleep(timeSleep)
        return check
        
    def capture(self, args):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        if platform == 'android':
            from android.storage import primary_external_storage_path
            dir = primary_external_storage_path()
            save_dir_path = path.join(dir, 'DCIM/Camera/')
            self.camera.export_to_png("{}IMG_{}.png".format(save_dir_path, timestr))

if __name__ == '__main__':
    Recognition().run()