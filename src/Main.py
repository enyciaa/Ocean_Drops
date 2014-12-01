'''
Main entry point for app
Contains the main screen manager and main menu
-use same basic mini_app layout across mini_apps for user continuity
    -Header, description, quote, read more, links to next page
    
Added


To Do
-Make it so clicking dropdown doesn't highlight the whole screen
-Add a reading section with condensed overcoming depression book
-Set notifications that the user can modify

Future
-text may struggle on small screens.  Maybe a function to check for certain screen size and make all text smaller if so?
-when you press app icon (top left) have a drop down list of all the other miniapps OR 
    make it change to a back button which goes back to the main menu
-Make ButtonSwitcher widget do a for loop of adding buttons for each mini_app in the file to shorten code
-Some kind of progress bar, that makes it so the more you invest (repeat exercises) the more you gain (unlock more exercises?)
-Could make the json function better, tried using arrays and for loops, but ran into trouble with using object strings

Widget Tree
-App
  -OceanDrops
    -TitleBar
      -TitleDrop
    -Appswitcher
        -MainMenu
            -ButtonSwitcher
                -Buttons1
        -Also contains links to all mini app managers
       
'''

__version__ = '1.1.2'

import kivy
kivy.require('1.8.0')

'hide on compile'
#code to set window size on desktop
from kivy.config import Config
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '35')
Config.set('graphics', 'left', '5')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.modules import inspector
import json
from misc import misc
from three_drops import three
from library import lib_button
from library import lib_text

app = None  

#settings drop down logic
class TitleDrop(DropDown):
    button_height = NumericProperty(0)
    button_width = NumericProperty(0)
    
    #sizes the drop down buttons
    def button_size(self):
        self.button_height = app.ocean_drops.title_bar.height * app.layout["title_drop"]["button_height_factor"]
        self.button_width = self.button_height * app.layout["title_drop"]["button_size_ratio"]  #ensures the ratio always matches the image ratio for the button background
        
#this bar is always displayed providing a route to settings and the mainmenu
class TitleBar(Widget):
    title_drop = ObjectProperty(None)
    
    app_title = StringProperty()
     
    #changes title back to main title
    def set_main_title(self):
        self.app_title = app.layout["title_bar"]["app_title"]
            
    #changes the title text when a mini app is opened
    def mini_app_title(self, mini_title):
        self.app_title = mini_title
     
    #opens drop down for three dots button    
    def open_drop_down(self, parent_button):
        self.title_drop = TitleDrop()
        self.title_drop.button_size()
        self.title_drop.open(parent_button)   
       

#contains the first four mini app buttons      
class ButtonsOne(Screen):   
    pass


#contains all the button grids to the mini apps
#when there are more button grids try to make screen change happen on swipes
class ButtonSwitcher(ScreenManager):
    buttons_one = ObjectProperty(None)
    
    #adds each button grid
    def add_button_grids(self):
        self.buttons_one = ButtonsOne(name = 'ButtonsOne')
        self.add_widget(self.buttons_one)
        
        
#the main menu which is the first screen seen and is linked to all the mini apps      
class MainMenu(Screen): 
    button_switcher = ObjectProperty(None)


#any new mini apps are added to the app switcher
class AppSwitcher(ScreenManager):  
    main_menu = ObjectProperty(None)
    
    app_switcher_pos = ListProperty([])
    
    #adds each mini app
    def add_mini_apps(self):
        self.main_menu = MainMenu(name = 'MainMenu')
        self.add_widget(self.main_menu)
        
        self.add_widget(app.misc)           #adds three dots menu to screen manager
        self.add_widget(app.three_drops)     #adds mini app to screen manager 
    
    'Implement properly when kivy 1.9.0 is released'
    #remember 1.9.0 method won't work on kivy launcher until the launcher is updated to kivy 1.9.0
    #could implement as its own text_input utility file?
    #text input will always move to align to top of keyboard if keyboard covers it on screen
    #called when the keyboard is displayed in three_drops app    
    def keyboard_up(self, txt_input):
        self.app_switcher_pos = self.pos
        y_shift = app.ocean_drops.height * 0.3
        self.pos = [0, y_shift]
    
    'Implement when kivy 1.9.0 is released'
    #called when the keyboard is dropped in three_drops app
    def keyboard_down(self): 
        self.pos = self.app_switcher_pos
               
               
#main screen class contains the title bar and the app_switcher widget
class OceanDrops(Widget):
    app_switcher = ObjectProperty(None)
    title_bar = ObjectProperty(None)
    

#singleton main class
class MainApp(App):
    ocean_drops = ObjectProperty(None)
    misc = ObjectProperty(None)
    three_drops = ObjectProperty(None)

    #json files
    layout = ObjectProperty(None)
    misc_layout = ObjectProperty(None)
    td_layout = ObjectProperty(None)
    lib_text_layout = ObjectProperty(None)
    lib_button_layout = ObjectProperty(None)
    
    def build(self): 
        ##definitions
        lib_button.app = self
        lib_text.app = self
        
        self.load_json_files()
        
        #main app
        global app
        app = self
        self.ocean_drops = OceanDrops()
        #three dots extras loading
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
        json_data = open('main.json')
        self.layout = json.load(json_data)
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
           
    #runs straight after build
    def on_start(self):
        self.ocean_drops.app_switcher.add_mini_apps()      #creates app switcher screen manager
        self.ocean_drops.app_switcher.main_menu.button_switcher.add_button_grids()  #creates button switcher screen manager
        self.ocean_drops.title_bar.set_main_title()     #sets title bar text
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