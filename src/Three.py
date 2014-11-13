'''
Added
-UI Layout

To Do
-Graphics

Future
-have quote change every day

Widget Tree
-Three_Drops
  -mini_app
    -sm
      -StartScreen
      -Three
      -Sent
  -read_more
    -ReadMore    
'''
from kivy.core.window import Window
from kivy.app import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, BooleanProperty, ReferenceListProperty
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


class ThreeDrops(Widget):
    read_more = ObjectProperty(None)
    mini_app = ObjectProperty(None)
    sm = ObjectProperty(None)
    
    title = 'Three Good Drops'   #has to be here rather than json as title is changed before mini app object is made
    
    back_x = NumericProperty(0)
    back_y = NumericProperty(0)
    next_x = NumericProperty(0)
    next_y = NumericProperty(0)
    
    #defines variables and does initial build for mini app
    def start(self):
        global three_drops
        three_drops = self
        self.button_position()
    
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
        self.sm = ScreenManager(transition = FadeTransition()) 
        self.sm.add_widget(start_screen)
        self.sm.add_widget(three)
        self.sm.add_widget(sent)
        self.sm.add_widget(read_more)
        self.mini_app = self.sm
        
        