from kivy.properties import StringProperty, ObjectProperty
from kivy_communication import *


class CategoryWidget(WidgetLogger):
    image_id = ObjectProperty(None)
    button_id = ObjectProperty(None)
    cg = None


    def __init__(self):
        super(CategoryWidget, self).__init__()
        # self.cg = curisoity_game
        self.button_id.value = False

    def category_pressed(self):
        pass

