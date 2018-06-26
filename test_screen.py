from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader
from category_widget import *
import json
from monster_widget import MonsterWidget
from monster_kitchen import *


class TestScreen(Screen):
    the_app = None
    monster = None
    first_monster = True

    def play_next(self, *args):
        if self.intro_counter < len(self.introduction):
            wav_filename = sounds_path + self.introduction[self.intro_counter]
            print(wav_filename)
            sl = SoundLoader.load(wav_filename)
            sl.bind(on_stop=self.play_next)
            self.intro_counter += 1
            sl.play()

    def start(self):
        self.introduction = [
                        "Intro_3_Categories.wav",
                        "Intro_4_Mission.wav",
                        "categories_1_what.wav",
                        "categories_2_choose.wav"
            ]

        self.intro_counter = 0

        with self.canvas.before:
            self.bind(size=self.update_pos, pos=self.update_pos)
        self.the_widget = self.ids['the_widget']

        attributes = json.load(open('items/items.json', 'r')).get('attributes')
        att_types = ['color', 'type', 'size']
        for at_i, att_type in enumerate(att_types):
            for i, att in enumerate(attributes[att_type]):
                cw = CategoryWidget()
                cw.image_id.source = att_path + att + '.png'
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
        done_button.image_id.color = (0, 0, 0, 0)
        done_button.image_id.base_pos = done_button.base_pos
        done_button.image_id.base_size = done_button.base_size
        done_button.button_id.base_pos = done_button.base_pos
        done_button.button_id.base_size = done_button.base_size
        done_button.button_id.name = 'done_button'
        done_button.button_id.bind(on_press=self.press_finish)
        self.the_widget.add_widget(done_button)

        self.monster = MonsterWidget()
        self.monster.base_pos = (0.6, 0.5)
        self.monster.base_size = (0.4, 0.4)
        self.the_widget.add_widget(self.monster)

    def update_monster(self, monster):
        monster.change_img()
        self.monster.image_id.source = monster.image_id.source
        self.monster.likes = monster.likes

    def on_enter(self, *args):
        KL.log.insert(action=LogAction.data, obj='TestScreen', comment='entered')
        self.update_pos(instance=self, value=None)
        for cw in self.the_widget.children:
            try:
                if cw.image_id is None: pass
                if cw.button_id.name is None: pass
                if 'done' not in cw.button_id.name:
                    cw.button_id.value = False
                    cw.image_id.source = att_path + cw.button_id.name.split(',')[1] + '.png'
            except:
                pass

        if self.first_monster:
            self.intro_counter = 0
            self.first_monster = False
        else:
            self.intro_counter = 2
        self.play_next()
        # self.speak_1()

    def speak_1(self):
        wav_filename = sounds_path + 'categories_1_what.wav'
        sl = SoundLoader.load(wav_filename)
        sl.bind(on_stop=self.speak_2)
        sl.play()

    def speak_2(self, *args):
        wav_filename = sounds_path + 'categories_2_choose.wav'
        sl = SoundLoader.load(wav_filename)
        sl.play()

    def speak_3(self, *args):
        wav_filename = sounds_path + 'categories_1_what.wav'
        sl = SoundLoader.load(wav_filename)
        sl.bind(on_stop=self.end_screen)
        sl.play()

    def speak_correct(self, *args):
        wav_filename = sounds_path + 'categories_correct.wav'
        sl = SoundLoader.load(wav_filename)
        sl.bind(on_stop=self.delay_end)
        sl.play()

    def delay_end(self, *args):
        Clock.schedule_once(self.end_screen, 1.0)

    def att_pressed(self, *args):
        the_button = args[0]
        the_button.value = not the_button.value
        att = the_button.name.split(',')
        if the_button.value:
            filename = att_path + att[1] + '_off.png'
        else:
            filename = att_path + att[1] + '.png'
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

    def log_answer(self):
        selected_att = []
        for cw in self.the_widget.children:
            if type(cw) == CategoryWidget:
                if cw.button_id.value:
                    selected_att.append(cw.button_id.name)
        KL.log.insert(action=LogAction.data, obj=self.name, comment='selected_atttributes' + str(selected_att),
                      sync=True)
        KL.log.insert(action=LogAction.data, obj=self.name, comment='correct_atttributes' + str(self.monster.likes),
                      sync=True)

    def press_finish(self, *args):
        self.log_answer()
        self.show_answer()
        self.speak_3()

    def end_screen(self, *args):
        self.the_app.next_monster()

    def show_answer(self):
        for likes_cat, likes_atts in self.monster.likes.items():
            for likes_att in likes_atts:
                for cw in self.the_widget.children:
                    try:
                        if cw.image_id is None: pass
                        if cw.button_id.name is None: pass
                        if 'done' not in cw.button_id.name:
                            if likes_cat in cw.button_id.name and likes_att in cw.button_id.name:
                                cw.image_id.color = (0.5, 0.8, 0.7, 0.5)
                    except:
                        pass