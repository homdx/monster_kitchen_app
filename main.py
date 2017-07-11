#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from monster_kitchen import *
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from text_handling import *


class ZeroScreen(Screen):

    def on_enter(self, *args):
        KL.restart()


class TestScreen(Screen):

    def on_enter(self, *args):
        # TODO: clear all marked buttons
        pass


class IntroScreen(Screen):

    def on_enter(self, *args):
        # TODO: talk
        pass

class MonsterKitchenApp(App):
    game_screen = None

    def build(self):
        self.init_communication()

        TTS.start()

        self.sm = ScreenManager()

        screen = ZeroScreen()
        screen.ids['subject_id'].bind(text=screen.ids['subject_id'].on_text_change)
        self.sm.add_widget(screen)

        screen = IntroScreen(name='intro_screen')
        self.sm.add_widget(screen)

        screen = TestScreen()
        self.sm.add_widget(screen)

        self.game_screen = GameScreen(name='the_game')
        self.game_screen.start(self)
        self.game_screen.add_widget(self.game_screen.curiosity_game.the_widget)
        self.sm.add_widget(self.game_screen)

        # self.sm.current = 'zero_screen'
        # self.sm.current = 'test_screen'
        self.sm.current = 'intro_screen'
        return self.sm

    def init_communication(self):
        KC.start(the_ip='192.168.1.254', the_parents=[self])  # 127.0.0.1
        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir,
                 the_ip='192.168.1.254')

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='FreeExplorationApp', comment='start')

    def press_start(self, pre_post):
        self.game_screen.curiosity_game.filename = 'items.json'
        self.sm.current = 'the_game'

    def test_monster(self, monster):
        self.sm.current = 'test_screen'
        self.sm.current_screen.monster_id.source = items_path + monster.img['neutral']

    def next_monster(self):
        self.sm.current = 'the_game'


if __name__ == '__main__':
    MonsterKitchenApp().run()
