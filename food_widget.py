from kivy.properties import StringProperty, ObjectProperty

from kivy_communication import *
from kivy.uix.image import *


class FoodWidget(WidgetLogger):
    image_id = ObjectProperty(None)
    button_id = ObjectProperty(None)
    cg = None

    def __init__(self, curisoity_game=None):
        super(FoodWidget, self).__init__()
        self.cg = curisoity_game

    def food_pressed(self):
        self.cg.food_pressed(self)

