'''
Extra pages that are reached via the top right three dots

Added
-Design and content
-touched up layout
-checked code

To Do


Future


Widget Tree
-About  
 
'''
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty

Builder.load_file('Misc/Misc.kv') 

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
        self.open()
    
    #opens three drops miniapp
    def open(self):
        about = About(name = 'About')
        self.misc_manager = ScreenManager(transition = FadeTransition()) 
        self.misc_manager.add_widget(about)
        self.add_widget(self.misc_manager)