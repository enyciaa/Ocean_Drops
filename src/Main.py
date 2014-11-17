'''
Added
-UI layout
-Graphics
-Changed logic for switching to miniapps to another screen manager, aids loading time, shortens code and allows transition setting

To Do
-Touch up graphics
-Make button labels highlight when buttons are clicked

Future
-when you press app icon (top left) have a drop down list of all the other miniapps OR 
    make it change to a back button which goes back to the main menu
-Make ButtonSwitcher widget do a for loop of adding buttons for each mini_app in the file to shorten code
-folderise as a package to help organisation

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
__version__ = "1.0.2"

import kivy
kivy.require('1.8.0')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.modules import inspector
import json
import Three
import Misc
import Utility

app = None  

#settings drop down logic
class TitleDrop(DropDown):
    pass
    
    
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
     
    #opens drop down for right hand button (opposite home button)    
    def open_drop_down(self, main_button):
        self.title_drop = TitleDrop()
        self.title_drop.open(main_button)    
       

#contains the first four mini app buttons      
class ButtonsOne(Screen):   
    pass


#contains all the button grids to the mini apps
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
    
    #adds each mini app
    def add_mini_apps(self):
        self.main_menu = MainMenu(name = 'MainMenu')
        self.add_widget(self.main_menu)
        
        self.add_widget(app.misc)
        self.add_widget(app.three_drops)     #adds mini app to screen manager 
            
            
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
    utility_layout = ObjectProperty(None)
    
    def build(self): 
        ##definitions
        global app
        app = self
        Three.app = self
        Misc.app = self
        Utility.app = self
        
        self.load_json()
        
        #main app
        self.ocean_drops = OceanDrops()
        self.misc = Misc.MiscScreens(name = 'Misc')
        self.misc.start()
        #mini app loading
        self.three_drops = Three.ThreeDrops(name = 'ThreeDrops')
        self.three_drops.start()
        
        inspector.create_inspector(Window, self.ocean_drops)
        
        return self.ocean_drops
    
    def load_json(self):
        json_data = open('Main.json')
        self.layout = json.load(json_data)
        json_data.close()
        
        json_data = open('Misc.json')
        self.misc_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('Three.json')
        self.td_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('Utility.json')
        self.utility_layout = json.load(json_data)
        json_data.close()
           
    #runs straight after build
    def on_start(self):
        self.ocean_drops.app_switcher.add_mini_apps()      #creates app switcher screen manager
        self.ocean_drops.app_switcher.main_menu.button_switcher.add_button_grids()      #creates button switcher screen manager
        self.ocean_drops.title_bar.set_main_title()     #sets title bar text
        Window.bind(on_keyboard = self.android_back)    
    
    #code to run when android back button (or keyboard escape button) is pressed
    def android_back(self, window, key, *args):
        if key == 27:        #key 27 is the esc key or back button on android
            self.ocean_drops.app_switcher.current = 'MainMenu'
            return True
        
        
if __name__ == '__main__':
    MainApp().run()