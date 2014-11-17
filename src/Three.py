'''
Added
-UI Layout

To Do
-Graphics
-Cloud text box positioning

Future
-have quote change every day

Widget Tree
-Three_Drops
    -sm
        -StartScreen
        -Three
        -Sent
        -ReadMore    
'''
from kivy.core.window import Window
from kivy.app import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty, StringProperty
import Utility

Builder.load_file('three.kv') 

app = None
three_drops = None  

class StartScreen(Screen):
    pass

        
class Three(Screen):  
    pass   


class Sent(Screen):   
    pass
            
        
class ReadMore(Screen): 
    pass


class ThreeDrops(Screen):
    td_manager = ObjectProperty(None)
    
    title = StringProperty()
    
    back_x = NumericProperty(0)
    back_y = NumericProperty(0)
    next_x = NumericProperty(0)
    next_y = NumericProperty(0)
    
    #defines variables and does initial build for mini app
    def start(self):
        global three_drops
        three_drops = self
        self.title = app.td_layout["whole_section"]["app_title"] 
        self.button_position()
        self.open()
    
    def button_position(self):
        self.back_x = Window.width / app.td_layout["button_layout"]["pos_horizontal_factor"] 
        self.back_y = Window.height / app.td_layout["button_layout"]["pos_vertical_factor"] 
        self.next_x = Window.width - self.back_x
        self.next_y = self.back_y
    
    #opens three drops miniapp
    def open(self):
        start_screen = StartScreen(name = 'StartScreen')
        three = Three(name = 'Three')
        sent = Sent(name = 'Sent')   
        read_more = ReadMore(name = 'ReadMore')  
        self.td_manager = ScreenManager(transition = FadeTransition()) 
        self.td_manager.add_widget(start_screen)
        self.td_manager.add_widget(three)
        self.td_manager.add_widget(sent)
        self.td_manager.add_widget(read_more)
        self.add_widget(self.td_manager)
        
        