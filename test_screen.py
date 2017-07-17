from kivy.uix.screenmanager import Screen
from category_widget import *


class TestScreen(Screen):

    def on_enter(self, *args):
        the_widget = self.ids['the_widget']



        cw = CategoryWidget()
        cw.image_id.source = 'items/fruit_vegetable.png'
        the_widget.add_widget(cw)