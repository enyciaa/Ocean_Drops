'''
Added


To Do


Future


Widget Tree
-About  
 
'''
from kivy.app import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty, StringProperty
import Utility

Builder.load_file('misc.kv') 

app = None
misc = None  

class About(Screen):
    pass
 

class MiscScreens(Screen):
    misc_manager = ObjectProperty(None)
    
    #defines variables and does initial build for mini app
    def start(self):
        global misc
        misc = self
        self.title = app.misc_layout["whole_section"]["app_title"] 
        self.open()
    
    #opens three drops miniapp
    def open(self):
        about = About(name = 'About')
        self.misc_manager = ScreenManager(transition = FadeTransition()) 
        self.misc_manager.add_widget(about)
        self.add_widget(self.misc_manager)