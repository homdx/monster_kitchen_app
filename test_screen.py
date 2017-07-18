from kivy.uix.screenmanager import Screen
from category_widget import *
import json


class TestScreen(Screen):
    the_app = None

    def on_enter(self, *args):
        with self.canvas.before:
            self.bind(size=self.update_pos, pos=self.update_pos)
        self.the_widget = self.ids['the_widget']

        attributes = json.load(open('items/items.json', 'r')).get('attributes')
        att_types = ['color', 'type', 'size']
        for at_i, att_type in enumerate(att_types):
            for i, att in enumerate(attributes[att_type]):
                cw = CategoryWidget()
                cw.image_id.source = 'items/' + att + '.png'
                cw.base_pos = (0.05 + i * 0.15, 0.8 - at_i * 0.3)
                cw.base_size = (0.15, 0.15)
                cw.image_id.base_pos = cw.base_pos
                cw.image_id.base_size = cw.base_size
                cw.button_id.base_pos = cw.base_pos
                cw.button_id.base_size = cw.base_size
                cw.button_id.name = att_type + ',' + att
                cw.button_id.bind(on_press=self.att_pressed)
                self.the_widget.add_widget(cw)

        done_button = CategoryWidget()
        done_button.image_id.source = ''
        done_button.base_pos = (0.6, 0.0)
        done_button.base_size = (0.4, 0.4)
        done_button.image_id.color = (0,0,0,0)
        done_button.image_id.base_pos = done_button.base_pos
        done_button.image_id.base_size = done_button.base_size
        done_button.button_id.base_pos = done_button.base_pos
        done_button.button_id.base_size = done_button.base_size
        done_button.button_id.name = 'done_button'
        done_button.button_id.bind(on_press=self.the_app.next_monster)
        self.the_widget.add_widget(done_button)

        self.update_pos(instance=self, value=None)

    def att_pressed(self, *args):
        the_button = args[0]
        the_button.value = not the_button.value
        att = the_button.name.split(',')
        if the_button.value:
            filename = 'items/' + att[1] + '_off.png'
        else:
            filename = 'items/' + att[1] + '.png'
        the_button.parent.children[0].source = filename
        KL.log.insert(action=LogAction.press, obj=self.name, comment='value=' + str(the_button.value), sync=False)

    def update_pos(self, instance, value):
        if instance:
            for cw in self.the_widget.children:
                try:
                    if cw.image_id is None: pass
                    cw.pos = (cw.base_pos[0] * instance.size[0], cw.base_pos[1] * instance.size[1])
                    cw.size = (cw.base_size[0] * instance.size[0], cw.base_size[1] * instance.size[1])
                    cw.image_id.pos = cw.pos
                    cw.image_id.size = cw.size
                    cw.button_id.pos = cw.pos
                    cw.button_id.size = cw.size
                except:
                    pass
