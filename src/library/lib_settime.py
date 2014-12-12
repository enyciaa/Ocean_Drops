'''
Popup to set time

Added
-new feature

To Do
-do logic for setting notification time
-design notification time pop up

Future


Widget Tree
-SetTimePop 
 
'''
from kivy.app import Builder
from kivy.uix.modalview import ModalView
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty   

Builder.load_file('library/lib_settime.kv') 

app = None


class SetTimePop(ModalView):    
    pass