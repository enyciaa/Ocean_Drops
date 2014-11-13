'''
Added
-UI layout
-Graphics

To Do
-Touch up graphics
-Make it so clicking mini app title takes you back to first page of mini app
-Create transition between main menu and mini apps
-Investigate whether this cna be achieved easily with a screen manager

Future
-Make sm widget do a for loop of adding buttons for each mini_app in the file to shorten code
-folderise as a package to help organisation

Widget Tree
-App
  -MainMenu
    -TitleBar
      -TitleDrop
    -Container
      -menu_sm
          -ScreenOne
          -ScreenTwo
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
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.modules import inspector
import json
import Three
import Utility

app = None  

#settings drop down logic
class TitleDrop(DropDown):
    pass
    
    
#this bar is always displayed providing a route to settings and the mainmenu
class TitleBar(Widget):
    title_drop = ObjectProperty(None)
    
    app_title = StringProperty()
    
    def variable_definition(self):
        self.app_title = app.layout["title_bar"]["app_title"]
        
    #changes the title text when a mini app is opened
    def mini_app_title(self, title_text):
        self.app_title = title_text
    
    #changes title back to main title
    def main_title(self):
        self.app_title = app.layout["title_bar"]["app_title"]
    
    #returns to home screen
    def home_press(self):
        container = app.main_menu.container
        container.add_menu_sm()
     
    #opens drop down for right hand button (opposite home button)    
    def open_drop_down(self, main_button):
        self.title_drop = TitleDrop()
        self.title_drop.open(main_button)    
       

#contains the first four miniapp buttons      
class ButtonsOne(Screen):   
    #changes the title bar text to the mini_app title
    def change_title(self, mini_app):
        title_text = mini_app.title
        title = app.main_menu.title_bar
        title.mini_app_title(title_text)         
    
    #three_Drops mini app opening functions
    def three_drops(self):
        three_drops = app.three_drops
        container = app.main_menu.container
        
        self.change_title(three_drops)                #passes three_drops() class reference to the title class
        three_drops.open()                              #creates the mini_app object
        container.mini_app_box = three_drops.mini_app     #takes the mini_app object variable from the mini_app
        container.add_mini_app()                          #adds the mini_app to the container        


class MenuBackground(Screen): 
    menu_sm = ObjectProperty(None)
    menu_buttons = ObjectProperty(None)
    
    #button classes allowing access to their functions
    #don't know how to do this directly from within screen manager
    buttons_one = ObjectProperty(None)
    
    #sets up the menu screen manager
    #when >4 mini apps can add second button screen here
    def screen_manager(self):
        self.buttons_one = ButtonsOne(name = 'ButtonsOne')
        self.menu_sm = ScreenManager(transition = FadeTransition()) 
        self.menu_sm.add_widget(self.buttons_one)
        
    def add_menu_buttons(self):
        self.menu_buttons.add_widget(self.menu_sm)


#any new screens are added to the container widget
class Container(RelativeLayout):  
    menu = ObjectProperty(None)
    mini_app_box = ObjectProperty(None)
    
    menu_displayed = BooleanProperty(False)
        
    #on start up adds the menu_sm to the container
    def start_menu(self):
        self.menu = MenuBackground()
        self.add_widget(self.menu)
        self.menu.screen_manager() 
        self.menu.add_menu_buttons()
        self.change_title()
        self.menu_displayed = True
    
    #adds mini_app to container
    def add_mini_app(self):
        self.remove_widget(self.menu)  
        self.add_widget(self.mini_app_box)  
        self.menu_displayed = False
    
    #removes the mini_app and adds the menu_sm to the container
    def add_menu_sm(self):
        if self.menu_displayed == False:
            self.remove_widget(self.mini_app_box)  
            self.add_widget(self.menu)
            self.change_title()
            self.menu_displayed = True   
    
    #changes title text to main app title text (from mini_app title text)     
    def change_title(self):
        title = app.main_menu.title_bar
        title.main_title() 
            

#main screen class contains the title bar and the container widget
class MainMenu(Widget):
    container = ObjectProperty(None)
    title_bar = ObjectProperty(None)
    

#singleton main class
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
           
    #runs straight after build
    def on_start(self):
        container = self.main_menu.container 
        container.start_menu()     #Adds menu to container on start up  
        self.variable_definition()     
    
    #defines all the start up variables that need calculated or grabbed from json    
    def variable_definition(self):
        title = self.main_menu.title_bar
        title.variable_definition()   
            
    
if __name__ == '__main__':
    OceanDropsApp().run()