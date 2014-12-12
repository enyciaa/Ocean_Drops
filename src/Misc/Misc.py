'''
Extra pages that are reached via the top right three dots

Added
-reminders screen

To Do
-add time setter

Future


Widget Tree
-Reminders
-About  
 
'''
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty
from library.lib_settime import SetTimePop

Builder.load_file('misc/misc.kv') 

app = None
misc = None  


class Reminders(Screen):
    td_time = StringProperty('22:30')
    
    def time_popup(self):
        SetTimePop().open()


class About(Screen):
    pass
 

class MiscScreens(Screen):
    misc_manager = ObjectProperty(None)
    reminders = ObjectProperty(None)
    
    #defines variables and does initial build for mini app
    def start(self):
        global misc
        misc = self 
        self.create_sm()
    
    #opens three drops miniapp
    def create_sm(self):
        self.reminders = Reminders(name = 'Reminders')
        about = About(name = 'About')
        self.misc_manager = ScreenManager(transition = FadeTransition()) 
        self.misc_manager.add_widget(self.reminders)
        self.misc_manager.add_widget(about)
        self.add_widget(self.misc_manager)