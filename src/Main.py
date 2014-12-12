'''
Main entry point for app
Does everything needed before the app starts up
Handles a lot of the behind the scene stuff, setting up app, acting as singleton, setting up services etc.

logic is that the this entry point opens ocean drops (UI manager) which creates title bar, main menu and adds mini app sms to overall sm.
But this main entry point still acts as the singleton.  (not entirely logical, but any way of seperating this creates complexity)

-use same basic mini_app layout across mini_apps for user continuity
    
Added
-moved ocean drops portion to a seperate file

To Do
-Set notifications that the user can modify

Future
-different text sizes for different dpi screens?
-Add a reading section with condensed overcoming depression book
-when you press app icon (top left) have a drop down list of all the other miniapps OR 
    make it change to a back button which goes back to the main menu
-Could make the json function better, tried using arrays and for loops, but ran into trouble with using object strings

Widget Tree
-App
  -ocean drops
  -misc
  -three drops
       
'''

__version__ = '1.1.5'

import kivy
kivy.require('1.8.0')

#code to set window size on desktop
from kivy.config import Config
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '35')
Config.set('graphics', 'left', '1045')

from kivy.utils import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.modules import inspector
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty
import json
from ocean_drops import ocean_drops 
from misc import misc
from three_drops import three
from library import lib_button
from library import lib_text
from library import lib_settime

app = None  


#app entry point, setting everything up, handling services and acting as singleton
class MainApp(App):
    ocean_drops = ObjectProperty(None)
    misc = ObjectProperty(None)
    three_drops = ObjectProperty(None)
    service = ObjectProperty(None)

    #json files
    od_layout = ObjectProperty(None)
    misc_layout = ObjectProperty(None)
    td_layout = ObjectProperty(None)
    lib_text_layout = ObjectProperty(None)
    lib_button_layout = ObjectProperty(None)
    lib_settime_layout = ObjectProperty(None)
    
    def build(self):         
        self.load_json_files()
        self.android_integration()
        
        #app entry point
        global app
        app = self
        lib_button.app = self
        lib_text.app = self
        lib_settime.app = self
        
        #ocean drops loading (includes app_switcher - the overall screen manager)
        ocean_drops.app = self
        self.ocean_drops = ocean_drops.OceanDrops()
        self.ocean_drops.start()
        #settings screens loading
        misc.app = self
        self.misc = misc.MiscScreens(name = 'Misc')
        self.misc.start()
        #mini app loading
        three.app = self
        self.three_drops = three.ThreeDrops(name = 'ThreeDrops')
        self.three_drops.start()
        
        #disable on compile
        inspector.create_inspector(Window, self.ocean_drops)
        
        return self.ocean_drops
        
    
    #loads json files
    #can make this more sexy somehow
    def load_json_files(self):
        json_data = open('ocean_drops/ocean_drops.json')
        self.od_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('misc/misc.json')
        self.misc_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('three_drops/three.json')
        self.td_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('library/lib_button.json')
        self.lib_button_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('library/lib_text.json')
        self.lib_text_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('library/lib_settime.json')
        self.lib_settime_layout = json.load(json_data)
        json_data.close()
    
    def android_integration(self):
        if platform == 'android':
            from android_integration import notificaitons
            scheduler = notificaitons.Scheduler()
            scheduler.create_alarm()
            
           
    #runs straight after build
    def on_start(self):
        self.ocean_drops.after_build()
        Window.bind(on_keyboard = self.android_back)   
    
    #keeps the app open if the phone sleeps or switches app
    def on_pause(self):
        return True     #disable when testing on kivy launcher or airdroid screws up
        
    #when app resumes put any data that needs reloaded here (if any)
    def on_resume(self):
        pass
    
    #code to run when android back button (or keyboard escape button) is pressed
    def android_back(self, window, key, *args):
        if key == 27:        #key 27 is the esc key or back button on android
            self.ocean_drops.app_switcher.current = 'MainMenu'
            return True
        
        
if __name__ == '__main__':
    MainApp().run()