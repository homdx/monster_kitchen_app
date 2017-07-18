#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.app import App
from monster_kitchen import *
from kivy_communication import *
from kivy.uix.screenmanager import ScreenManager, Screen
from text_handling import *
from test_screen import *

class ZeroScreen(Screen):

    def on_enter(self, *args):
        KL.restart()
        KL.log.insert(action=LogAction.data, obj='subject', comment='the_end', sync=True)

    def start(self):
        self.ids['subject_id'].bind(text=self.ids['subject_id'].on_text_change)


class IntroScreen(Screen):
    the_app = None

    def on_enter(self, *args):
        self.introduction = [
                            "Intro_1_Welcome.wav",
                            "Intro_2_Monsters_are_coming.wav",
                            "Intro_3_Categories.wav",
                            "Intro_4_Mission.wav",
                            "Intro_5_How.wav",
                            "Intro_6_after.wav",
                            "Intro_7_bonappetit.wav"
                        ]
        self.intro_counter = 0
        self.play_next()

    def play_next(self, *args):
        if self.intro_counter < len(self.introduction):
            wav_filename = 'items/sounds/' + self.introduction[self.intro_counter]
            sl = SoundLoader.load(wav_filename)
            sl.bind(on_stop=self.play_next)
            self.intro_counter += 1
            sl.play()
        else:
            self.the_app.sm.current = "the_game"


class EndScreen(Screen):
    the_app = None

    def on_enter(self, *args):
        TTS.speak(["thank you for feed the monsters"], self.next_screen)

    def next_screen(self, *args):
        self.the_app.sm.current = "zero_screen"


class MonsterKitchenApp(App):
    game_screen = None

    def build(self):
        self.init_communication()

        TTS.start()

        self.sm = ScreenManager()

        screen = ZeroScreen()
        screen.start()
        screen.ids['subject_id'].bind(text=screen.ids['subject_id'].on_text_change)
        self.sm.add_widget(screen)

        screen = IntroScreen(name='intro_screen')
        screen.the_app = self
        self.sm.add_widget(screen)

        self.game_screen = GameScreen(name='the_game')
        self.game_screen.start(self)
        self.game_screen.add_widget(self.game_screen.curiosity_game.the_widget)
        self.sm.add_widget(self.game_screen)

        screen = TestScreen()
        screen.the_app = self
        screen.start()
        self.sm.add_widget(screen)

        screen = EndScreen(name='end_screen')
        screen.the_app = self
        self.sm.add_widget(screen)

        self.sm.current = 'zero_screen'
        # self.sm.current = 'test_screen'
        # self.sm.current = 'intro_screen'
        # self.sm.current = 'the_game'
        return self.sm

    def init_communication(self):
        KC.start(the_ip='192.168.1.254', the_parents=[self])  # 127.0.0.1
        KL.start(mode=[DataMode.file, DataMode.communication, DataMode.ros], pathname=self.user_data_dir,
                 the_ip='192.168.1.254')

    def on_connection(self):
        KL.log.insert(action=LogAction.data, obj='FreeExplorationApp', comment='start')

    def press_start(self, pre_post):
        self.game_screen.curiosity_game.filename = 'items.json'
        self.sm.current = 'intro_screen'

    def test_monster(self, monster):
        self.sm.current = 'test_screen'
        self.sm.current_screen.monster.source = items_path + monster.img['neutral']

    def next_monster(self, *args):
        self.sm.current = 'the_game'

    def on_stop(self):
        KL.log.insert(action=LogAction.data, obj='game', comment='the_end', sync=True)


if __name__ == '__main__':
    MonsterKitchenApp().run()
