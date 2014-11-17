'''
Utility file with chunks of code used in whole package
Contains all the text templates
'''

from kivy.app import Builder
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty, StringProperty

Builder.load_file('Utility.kv') 

app = None

class Heading(Label):
    pass

class SubHeading(Label):
    pass

class MiniAppDescription(Label):
    pass

class Footer(Label):
    pass

class NormalText(Label):
    pass

#Template class for all button labels
class ButtonLabel(Label, ButtonBehavior):
    pressed_label = ObjectProperty(None, allownone = True)
    pressed_down = BooleanProperty(False)
    
    #when button is clicked text becomes translucent        
    def click_down(self, label):
        self.pressed_down = True
        self.pressed_label = label
        label.color = app.utility_layout["button_label"]["pressed_color"]
    
    #when touch moves off text, text returns to normal color    
    def click_moved(self, label):
        if self.pressed_down:
            self.pressed_label = None
            self.pressed_down = False
            label.color = app.utility_layout["button_label"]["normal_color"]
            
    #on button click start the game           
    def click_up(self, label):
        self.pressed_down = False
        if label == self.pressed_label:
            self.pressed_label = None
            label.color = app.utility_layout["button_label"]["normal_color"]


#Template class for all buttons to give them desired clicking behaviour
class ButtonClicks(Image, ButtonBehavior):  
    pressed_button = ObjectProperty(None, allownone = True)
    pressed_down = BooleanProperty(False)
    
    button_functions = {
            "but_001": "self.but_001()",
            "but_002": 'app.ocean_drops.title_bar.open_drop_down(button)',
            "but_003": "self.but_003()",
            "but_004": "app.three_drops.td_manager.current = 'ReadMore'",
            "but_005": "self.but_005()",
            "but_006": "app.three_drops.td_manager.current = 'Three'",
            "but_007": "app.three_drops.td_manager.current = 'StartScreen'",
            "but_008": "app.three_drops.td_manager.current = 'Sent'",
            "but_009": "app.three_drops.td_manager.current = 'Three'",
            "but_010": "self.but_010()",
            "but_011": "app.three_drops.td_manager.current = 'StartScreen'",
            "but_012": "app.misc.misc_manager.current = 'About'"
        }
    
    #if multiple functions are run
    #the library directs the button press to one of these functions
    
    #home button
    def but_001(self):
        app.ocean_drops.app_switcher.current = 'MainMenu'
        app.ocean_drops.title_bar.set_main_title()
    
    #menu button to enter three drops mini app
    def but_003(self):
        app.ocean_drops.app_switcher.current = 'ThreeDrops'
        mini_title = app.td_layout["whole_section"]["app_title"] 
        app.ocean_drops.title_bar.mini_app_title(mini_title)
        
    #back button on first screen of three drops
    def but_005(self):
        app.ocean_drops.app_switcher.current = 'MainMenu'
        app.ocean_drops.title_bar.set_main_title()
    
    #main menu button at the end of three drops
    def but_010(self):
        app.ocean_drops.app_switcher.current = 'MainMenu'
        app.three_drops.td_manager.current = 'StartScreen'
        app.ocean_drops.title_bar.set_main_title()
    
    #when button is clicked text becomes translucent        
    def click_down(self, button):
        self.pressed_down = True
        self.pressed_button = button
        button.color = app.utility_layout["button_clicks"]["pressed_color"]
    
    #when touch moves off text, text returns to normal color    
    def click_moved(self, button):
        if self.pressed_down:
            self.pressed_button = None
            self.pressed_down = False
            button.color = app.utility_layout["button_clicks"]["normal_color"]
            
    #on button click start the game           
    def click_up(self, button, button_identifier):
        self.pressed_down = False
        if button == self.pressed_button:
            self.pressed_button = None
            button.color = app.utility_layout["button_clicks"]["normal_color"]
            run_function = self.button_functions[button_identifier]
            exec run_function