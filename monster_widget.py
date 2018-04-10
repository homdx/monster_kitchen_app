from kivy.properties import StringProperty, ObjectProperty

from kivy_communication import *
from kivy.uix.image import *


class MonsterWidget(WidgetLogger):
    image_id = ObjectProperty(None)
    button_id = ObjectProperty(None)
    cg = None

    base_pos = None
    base_size = None
    likes = None
    name = ''
    img = None

    items_path = ''

    def change_img(self, im='neutral', sequence=0):
        if im in self.img:
            if im == 'eating':
                self.image_id.source = self.items_path + self.img[im][sequence]
            else:
                self.image_id.source = self.items_path + self.img[im]

    def on_size(self, *args):
        base_size = self.cg.size
        true_pos = (int(float(base_size[0]) * self.base_pos[0]), int(float(base_size[1]) * self.base_pos[1]))
        true_size = (int(float(base_size[0]) * self.base_size[0]), int(float(base_size[1]) * self.base_size[1]))

        if self.pos != true_pos and self.size != true_size:
            self.change_pos(true_pos, true_size)

    def change_pos(self, true_pos, true_size):
        self.pos = true_pos
        self.size = true_size
        self.image_id.pos = true_pos
        self.image_id.size = true_size
        self.button_id.pos = true_pos
        self.button_id.size = true_size

    def log(self):
        KL.log.insert(action=LogAction.data, obj=self.name, comment=json.dumps(self.likes))

    def __init__(self, curisoity_game=None):
        super(MonsterWidget, self).__init__()
        self.cg = curisoity_game

    def monster_pressed(self):
        self.cg.monster_pressed()
