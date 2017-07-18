#!/usr/bin/kivy
# -*- coding: utf-8 -*-
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy_communication import *
from hebrew_management import HebrewManagement
from text_handling import *
from kivy.uix.screenmanager import Screen
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.animation import Animation
from food_widget import FoodWidget

from functools import partial
from copy import deepcopy

LANGUAGE = 'English'  # 'Hebrew'
items_path = 'items/'
number_of_tries = 1


class Monster(Image):
    cg = None
    base_pos = None
    base_size = None
    likes = None
    name = ''
    img = None

    def change_img(self, im='neutral', sequence=0):
        if im in self.img:
            if im == 'eating':
                self.source = items_path + self.img[im][sequence]
            else:
                self.source = items_path + self.img[im]

    def on_size(self, *args):
        base_size = self.cg.size
        true_pos = (int(float(base_size[0]) * self.base_pos[0]), int(float(base_size[1]) * self.base_pos[1]))
        true_size = (int(float(base_size[0]) * self.base_size[0]), int(float(base_size[1]) * self.base_size[1]))

        if self.pos != true_pos and self.size != true_size:
            self.pos = true_pos
            self.size = true_size

    def log(self):
        KL.log.insert(action=LogAction.data, obj=self.name, comment=json.dumps(self.likes))


class GameScreen(Screen):
    the_app = None
    curiosity_game = None
    current_monster = 0

    def start(self, the_app):
        self.the_app = the_app
        self.curiosity_game = CuriosityGame(the_app)
        self.current_monster = -1

    def on_enter(self, *args):
        self.current_monster += 1
        self.curiosity_game.current_monster = self.current_monster
        if self.current_monster == 0:
            self.curiosity_game.load(self.the_app.root.size)
            Clock.schedule_once(self.introduction, 0.1)
        elif self.current_monster >= len(self.curiosity_game.monsters['list']):
            self.end_game()
        else:
            self.curiosity_game.start()

    def introduction(self, dt):
        self.curiosity_game.start()

    def end_game(self):
        wav_filename = 'items/sounds/the_end.wav'
        sl = SoundLoader.load(wav_filename)
        sl.bind(on_stop=self.next_subject)
        sl.play()

    def next_subject(self, *args):
        self.the_app.sm.current = 'zero_screen'


class CuriosityGame:
    items = {}
    current = 0
    the_widget = None
    the_end = False
    game_duration = 120
    filename = 'items.json'

    current_monster = -1

    attribute_images = []

    def __init__(self, the_app):
        self.the_widget = CuriosityWidget(self)
        self.size = [100,100]
        self.tries = 0
        self.the_app = the_app

    def load(self, size=None):
        self.size = size
        items_json = JsonStore(items_path + self.filename)
        self.the_widget.update_background(items_path + items_json.get('background'))
        self.test = items_json.get('test')

        # initialize items
        food_json = JsonStore(items_path + 'food.json')

        items_list = food_json.get('data')
        self.items = {}
        for name, value in items_list.items():
            self.items[name] = FoodWidget(self)
            self.items[name].name = name

            if 'pos' in value:
                self.items[name].base_pos = [float(x) for x in value['pos']]
                self.items[name].base_size = [float(x) for x in value['size']]

            self.items[name].image_id.source = items_path + name + '.png'

            if 'attributes' in value:
                self.items[name].attributes = {
                    'type': value['attributes'][0],
                    'color': value['attributes'][1],
                    'size': value['attributes'][2]
                }

        self.monsters = items_json.get('monsters')
        self.monster = Monster()
        self.monster.cg = self
        self.monster.base_pos = [float(x) for x in self.monsters['pos'].split(',')]
        self.monster.base_size = [float(x) for x in self.monsters['size'].split(',')]
        self.change_monster(self.current_monster)

        self.attribute_images = {
            'type': FoodWidget(self),
            'color': FoodWidget(self),
            'size': FoodWidget(self),
        }
        descriptors = ['color', 'type', 'size']
        for i, ai in enumerate(self.attribute_images.values()):
            ai.base_pos = (0.01 + 0.1 * i, 0.80)
            ai.base_size = (0.15, 0.15)
            ai.image_id.source = 'items/' + descriptors[i] + '.png'
            ai.disabled = True

        # set widgets
        self.the_widget.clear_widgets()
        self.the_widget.add_widget(self.monster)
        for key, value in self.items.items():
            self.the_widget.add_widget(value)

        for ai in self.attribute_images.values():
            self.the_widget.add_widget(ai)

        self.update_pos_size(self.size)

    def update_pos_size(self, app_size):
        self.size = app_size
        if self.items:
            for i_name, i in self.items.items():
                pos = i.base_pos
                size = i.base_size
                i.pos = (int(pos[0] * self.size[0]), int(pos[1] * self.size[1]))
                i.size = (int(size[0] * self.size[0]), int(size[1] * self.size[1]))
                i.image_id.pos = (int(pos[0] * self.size[0]), int(pos[1] * self.size[1]))
                i.image_id.size = (int(size[0] * self.size[0]), int(size[1] * self.size[1]))
                i.button_id.pos = i.image_id.pos
                i.button_id.size = i.image_id.size
        if self.attribute_images:
            for i_name, i in self.attribute_images.items():
                pos = i.base_pos
                size = i.base_size
                i.pos = (int(pos[0] * self.size[0]), int(pos[1] * self.size[1]))
                i.size = (int(size[0] * self.size[0]), int(size[1] * self.size[1]))
                i.image_id.pos = (int(pos[0] * self.size[0]), int(pos[1] * self.size[1]))
                i.image_id.size = (int(size[0] * self.size[0]), int(size[1] * self.size[1]))
                i.button_id.pos = i.image_id.pos
                i.button_id.size = i.image_id.size

    def start(self):
        self.update_pos_size(self.size)
        self.next_monster()


    def reset_pos(self):
        for i in self.items.values():
            base_size = self.size
            true_pos = (int(float(base_size[0]) * i.base_pos[0]), int(float(base_size[1]) * i.base_pos[1]))
            i.pos = true_pos
            true_size = (int(float(base_size[0]) * i.base_size[0]), int(float(base_size[1]) * i.base_size[1]))
            i.size = true_size

    def change_monster(self, monster_num):
        self.monster.name = self.monsters['list'][monster_num]['name']
        self.monster.img = self.monsters['list'][monster_num]['image']
        self.monster.change_img('neutral')
        self.monster.likes = self.monsters['list'][monster_num]['likes']
        self.monster.log()
        self.selected_item = None
        self.the_end = False
        self.unlock_tablet()

    def food_pressed(self, item):
        self.lock_tablet()
        self.selected_item = item
        print(item.name, item.pos, item.attributes)
        # set attributes
        for a_name, a in item.attributes.items():
            ai = self.attribute_images[a_name]
            the_source = 'items/' + a + '.png'
            ai.color = (1, 1, 1, 1)
            ai.image_id.source = the_source

        Clock.schedule_once(self.food_animation, 0.1)

    def lock_tablet(self):
        for w in self.the_widget.children:
            w.disabled = True

    def unlock_tablet(self):
        for w in self.the_widget.children:
            w.disabled = False

    def food_animation(self, dt):
        anim = Animation(x=self.monster.pos[0] + self.monster.size[0] / 2,
                         y=self.monster.pos[1] + self.monster.size[1] / 4,
                         duration=1)
        anim.bind(on_complete=self.finished_animation)
        anim.start(self.selected_item.image_id)

    def finished_animation(self, *args):
        item = args[1]
        item.size = (1, 1)
        self.feed_monster(self.selected_item)

    def feed_monster(self, item, anim=6, dt=0):
        if anim == 0:
            self.check_likes(item)
        else:
            sequence = int(anim % len(self.monster.img['eating']))

            self.monster.change_img('eating', sequence)
            Clock.schedule_once(partial(self.feed_monster, item, anim-1), 0.5)

    def check_likes(self, item):
        # check how many attributes the monster likes
        print(item.name)
        likes_item = 0
        total_likes = 0
        for att_name, att_list in self.monster.likes.items():
            for a in att_list:
                total_likes += 1
                if a in item.attributes[att_name]:
                    likes_item += 1
        monster_likes = float(likes_item) / float(total_likes)
        KL.log.insert(action=LogAction.data, obj=self.monster.name,
                      comment=json.dumps(item.attributes) + ' likes ' + str(monster_likes))

        # change monster image to correct one
        if monster_likes < 0.3:
            self.food_bad()
        elif monster_likes < 0.7:
            self.food_ok()
        else:
            self.food_tasty()

        self.tries -= 1
        print('tries', self.tries)
        if self.tries == 0:
            Clock.schedule_once(self.test_monster, 2)
            return
        self.selected_item = None
        self.unlock_tablet()

    def food_tasty(self):
        self.monster.change_img('good')
        if self.monsters['list'][self.current_monster]['wav'] is not '':
            wav_filename = 'items/sounds/' + self.monsters['list'][self.current_monster]['wav'] + '_2_tasty.wav'
            SoundLoader.load(wav_filename).play()

    def food_ok(self):
        self.monster.change_img('neutral')
        if self.monsters['list'][self.current_monster]['wav'] is not '':
            wav_filename = 'items/sounds/' + self.monsters['list'][self.current_monster]['wav'] + '_3_ok.wav'
            SoundLoader.load(wav_filename).play()

    def food_bad(self):
        self.monster.change_img('bad')
        if self.monsters['list'][self.current_monster]['wav'] is not '':
            wav_filename = 'items/sounds/' + self.monsters['list'][self.current_monster]['wav'] + '_4_bad.wav'
            SoundLoader.load(wav_filename).play()

    def test_monster(self, dt):
        self.the_app.test_monster(self.monster)

    def next_monster(self):
        self.tries = number_of_tries
        # set the timer of the game
        print('Starting clock...')
        self.change_monster(self.current_monster)

        for k, v in self.items.items():
            v.current = 1
            # v.pos = v.base_pos
        self.reset_pos()
        self.the_end = False
        Clock.schedule_once(self.meet_monster, 0.05)

    def meet_monster(self, dt):
        if self.monsters['list'][self.current_monster]['wav'] is not '':
            wav_filename = 'items/sounds/' + self.monsters['list'][self.current_monster]['wav'] + '_1_opening.wav'
            SoundLoader.load(wav_filename).play()
        else:
            TTS.speak(['I am ', self.monsters['list'][self.current_monster]['name'], ' and i am hungry.'])

    def change_item(self, item, tool):
        item.attributes['process'] = tool.attributes['process']



class CuriosityWidget(FloatLayout):
    cg_lbl = None
    the_game = None

    def __init__(self, the_game=None):
        super(CuriosityWidget, self).__init__()
        self.the_game = the_game
        with self.canvas.before:
            self.rect = Rectangle(source='')
            self.bind(size=self._update_rect, pos=self._update_rect)

    def update_background(self, filename):
        with self.canvas.before:
            self.rect = Rectangle(source=filename, size=self.size)

            self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        self.the_game.update_pos_size(instance.size)
