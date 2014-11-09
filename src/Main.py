'''
Added

To Do
-UI layout
-Graphics

Future
-Make scroll widget do a for loop of adding buttons for each mini_app in the file to shorten code
-folderise as a package to help organisation

Widget Tree
-App
  -MainMenu
    -TitleBar
      -TitleDrop
    -Container
      -ScrollMenu
      -mini_app_box
       
'''
__version__ = "1.0.2"

import kivy
kivy.require('1.8.0')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.dropdown import DropDown
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty, StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.modules import inspector
import json
import Three
import Utility

app = None                       

class ButtonClicks(Utility.ButtonClicks):
    pass


#Settings drop down logic
class TitleDrop(DropDown):
    pass
    
    
#This bar is always displayed providing a route to settings and the mainmenu
class TitleBar(Widget):
    title_drop = ObjectProperty(None)
    
    app_title = StringProperty()
    
    def variable_definition(self):
        self.app_title = app.layout["title_bar"]["app_title"]
        
    #Changes the title text when a mini app is opened
    def mini_app_title(self, title_text):
        self.app_title = title_text
    
    #Changes title back to main title
    def main_title(self):
        self.app_title = app.layout["title_bar"]["app_title"]
    
    #Returns to home screen
    def home_press(self):
        container = app.main_menu.container
        container.add_scroll_menu()
     
    #Opens drop down for right hand button (opposite home button)    
    def open_drop_down(self, main_button):
        self.title_drop = TitleDrop()
        self.title_drop.open(main_button)    
       

#Contains all the miniapp buttons      
class ScrollMenu(ScrollView):  
    scroll_height = NumericProperty(0)
    
    #Calculates the height of the scroll menu portion of the main menu
    #Will need to alter this calculation when there are lots of mini_apps buttons
    def variable_definition(self):
        main = app.main_menu
        self.scroll_height = (main.height + 50)   #50 makes it bigger than the space available so its scrollable  
    
    #Changes the title bar text to the mini_app title
    def change_title(self, mini_app):
        title_text = mini_app.title
        title = app.main_menu.title_bar
        title.mini_app_title(title_text)         
    
    #Three_Drops mini app opening functions
    def three_drops(self):
        three_drops = app.three_drops
        container = app.main_menu.container
        
        self.change_title(three_drops)                #passes three_drops() class reference to the title class
        three_drops.open()                              #creates the mini_app object
        container.mini_app_box = three_drops.mini_app     #takes the mini_app object variable from the mini_app
        container.add_mini_app()                          #adds the mini_app to the container
        

#Any new screens are added to the container widget
class Container(RelativeLayout):  
    scroll_menu = ObjectProperty(None)
    mini_app_box = ObjectProperty(None)
    
    scroll_displayed = BooleanProperty(False)
    
    #On start up adds the ScrollMenu to the container
    def start_menu(self):
        self.scroll_menu = ScrollMenu()
        self.add_widget(self.scroll_menu)
        self.change_title()
        self.scroll_displayed = True
    
    #Adds mini_app to container
    def add_mini_app(self):
        self.remove_widget(self.scroll_menu)  
        self.add_widget(self.mini_app_box)  
        self.scroll_displayed = False
    
    #Removes the mini_app and adds the ScrollMenu to the container
    def add_scroll_menu(self):
        if self.scroll_displayed == False:
            self.remove_widget(self.mini_app_box)  
            self.add_widget(self.scroll_menu) 
            self.change_title()
            self.scroll_displayed = True   
    
    #Changes title text to main app title text (from mini_app title text)     
    def change_title(self):
        title = app.main_menu.title_bar
        title.main_title() 
            

#Main screen class contains the title bar and the container widget
class MainMenu(Widget):
    container = ObjectProperty(None)
    title_bar = ObjectProperty(None)
    

#Singleton main class
class OceanDropsApp(App):
    main_menu = ObjectProperty(None)
    three_drops = ObjectProperty(None)
    
    #json files
    layout = ObjectProperty(None)
    td_layout = ObjectProperty(None)
    utility_layout = ObjectProperty(None)
    
    def build(self): 
        ##definitions
        global app
        app = self
        Three.app = self
        Utility.app = self
        
        #main app loading
        self.load_json()
        self.main_menu = MainMenu()
        
        #mini app loading
        self.three_drops = Three.ThreeDrops()
        self.three_drops.start()
        
        inspector.create_inspector(Window, self.main_menu)
        
        return self.main_menu
    
    def load_json(self):
        json_data = open('OceanDrops.json')
        self.layout = json.load(json_data)
        json_data.close()
        
        json_data = open('Three.json')
        self.td_layout = json.load(json_data)
        json_data.close()
        
        json_data = open('Utility.json')
        self.utility_layout = json.load(json_data)
        json_data.close()
           
    #Runs straight after build
    def on_start(self):
        container = self.main_menu.container
        container.start_menu()     #Adds scroll menu to container on start up  
        self.variable_definition()      
    
    #Defines all the start up variables that need calculated or grabbed from json    
    def variable_definition(self):
        title = self.main_menu.title_bar
        title.variable_definition()   
        container = self.main_menu.container 
        scroll = container.scroll_menu
        scroll.variable_definition()   #Changes height of scroll
    
    
if __name__ == '__main__':
    OceanDropsApp().run()