'''
Utility file with chunks of code used in whole package
Contains all the text templates

Added
-checked code
-finished typography

To Do

'''

from kivy.app import Builder
from kivy.uix.label import Label
from kivy.properties import ListProperty, NumericProperty, ObjectProperty, \
    BooleanProperty, ReferenceListProperty, StringProperty

Builder.load_file('Library/lib_Text.kv') 

app = None

class Heading(Label):
    pass


class SubHeading(Label):
    pass


class NormalText(Label):
    pass


class MiniAppDescription(Label):
    pass


class Footer(Label):
    pass
