'''
Utility file with chunks of code used in whole package
'''

from kivy.app import Builder
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty, StringProperty

Builder.load_file('Utility.kv') 

app = None

#Template class for all buttons to give them desired clicking behaviour
class ButtonClicks(Image, ButtonBehavior):  
    pressed_button = ObjectProperty(None, allownone = True)
    pressed_down = BooleanProperty(False)
    
    button_functions = {
            "but_001": 'app.main_menu.title_bar.home_press()',
            "but_002": 'app.main_menu.title_bar.open_drop_down(button)',
            "but_003": 'app.main_menu.container.scroll_menu.three_drops()',
            "but_004": 'app.main_menu.container.scroll_menu.three_drops_read()',
            "but_005": 'app.main_menu.container.add_scroll_menu()',
            "but_006": "app.three_drops.sm.current = 'Three'",
            "but_007": "app.three_drops.sm.current = 'StartScreen'",
            "but_008": "app.three_drops.sm.current = 'Sent'",
            "but_009": "app.three_drops.sm.current = 'Three'",
            "but_010": 'app.main_menu.container.add_scroll_menu()',
            "but_011": 'app.main_menu.container.add_scroll_menu()'
        }
    
    #when button is clicked text becomes translucent        
    def click_down(self, button):
        self.pressed_down = True
        self.pressed_button = button
        button.color = app.utility_layout["button_clicks"]["pressed_text_color"]
    
    #when touch moves off text, text returns to normal color    
    def click_moved(self, button):
        if self.pressed_down:
            self.pressed_button = None
            self.pressed_down = False
            button.color = app.utility_layout["button_clicks"]["normal_text_color"]
            
    #on button click start the game           
    def click_up(self, button, button_identifier):
        self.pressed_down = False
        if button == self.pressed_button:
            self.pressed_button = None
            button.color = app.utility_layout["button_clicks"]["normal_text_color"]
            run_function = self.button_functions[button_identifier]
            exec run_function