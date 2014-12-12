'''
Contains the overall screen manager, main menu and title bar
    
Added
-Made footer sizing into pixels, calculated as a percentage of total screen size
-Made it so clicking dropdown doesn't highlight whole screen

To Do


Future
-Some kind of progress bar, that makes it so the more you invest (repeat exercises) the more you gain (unlock more exercises?)

Widget Tree
-OceanDrops
    -TitleBar
        -TitleDrop
    -AppSwitcher
        -MainMenu
            -ButtonSwitcher
                ButtonsOne
        -misc
        -three_drops

       
'''

__version__ = '1.1.5'

import kivy
kivy.require('1.8.0')

'hide on compile'
#code to set window size on desktop
from kivy.config import Config
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'top', '35')
Config.set('graphics', 'left', '1045')

from kivy.app import Builder
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.modules import inspector
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty

Builder.load_file('ocean_drops/ocean_drops.kv')

app = None  
ocean_drops = None


#settings drop down logic
class TitleDrop(DropDown):
    button_height = NumericProperty(0)
    button_width = NumericProperty(0)
    
    #sizes the drop down buttons
    def button_size(self):
        self.button_height = app.ocean_drops.title_bar.height * app.od_layout["title_drop"]["button_height_factor"]
        self.button_width = self.button_height * app.od_layout["title_drop"]["button_size_ratio"]  #ensures the ratio always matches the image ratio for the button background
        
        
#this bar is always displayed providing a route to settings and the mainmenu
class TitleBar(Widget):
    title_drop = ObjectProperty(None)
    
    app_title = StringProperty()
     
    #changes title back to main title
    def set_main_title(self):
        self.app_title = app.od_layout["title_bar"]["app_title"]
            
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
    
    footer_height = NumericProperty(0)
    
    def start(self):
        global ocean_drops
        ocean_drops = self
        self.footer_sizing()
    
    def after_build(self):
        self.app_switcher.add_mini_apps()      #creates app switcher screen manager
        self.app_switcher.main_menu.button_switcher.add_button_grids()  #creates button switcher screen manager
        self.title_bar.set_main_title()     #sets title bar text 
    
    def footer_sizing(self):
        self.footer_height = Window.height * app.od_layout["menu_background"]["footer_factor"]
        
        