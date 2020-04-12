# from libdw import sm

from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.label import CoreLabel, Label
from kivy.uix.button import Button
from kivy.graphics import Rectangle
import random

# Before the window starts
# Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'width', '412')
Config.set('graphics', 'height', '732')
# Window.size = (412, 732)

# Create the manager
manager = ScreenManager(transition=FadeTransition())

# Initialize list of states
states = ["HOME", "LEVELS", "INSTRUCTIONS", "LEVEL1", "LEVEL2", "LEVEL3", "ADVANCE", "WIN", "LOSE"]

# class TimeWidget(Widget):
#     def __init__(self, **kwargs):
#         super(TimeWidget, self).__init__(**kwargs)

#         with self.canvas:
#             self.fullbar = Rectangle(pos=(10,10), size=(10,Window.width-20))
#             self.timebar = Rectangle(color=(1,0,0,1),pos=(10,10), size=(10.Window.width-20))
#             self.bind(pos = self.update_fullbar, size = self.update_fullbar)
#             self.bind(pos = self.update_timebar, size = self.update_timebar)

#     def update_timebar(self, *args):
#         self.fullbar.pos = self.pos
#         self.fullbar.size = self.size

#     def update_timebar(self, *args):
#         pass


############################################################

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super(GameWidget,self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        self._score_label = CoreLabel(text="Score: 0", font_size=50, font_name='./fonts/absolutepink.otf')
        self._score_label.refresh()
        self._score = 0
        # self._time = 30

        self.register_event_type("on_frame")

        with self.canvas:
            # Rectangle(source="./images/galaxybackground.jpg", pos=self.pos,
            #           size=(Window.width, Window.height))
            self._score_instruction = Rectangle(texture=self._score_label.texture, pos=(
                0, Window.height - 50), size=self._score_label.texture.size)
        
        self.keysPressed = set()
        self._entities = set()

        Clock.schedule_interval(self._on_frame, 0)
        # self.num_stars = 5
        # self.spawn_player()
        # self.spawn_stars(self.num_stars)

        # Clock.schedule_interval(self.spawn_enemies, 2)

    # Create Star objects from Star class
    def spawn_stars(self, num_stars):
        for i in range(num_stars):
            random_x = random.randint(Window.width*0.15, Window.width*0.85)     # randomize x-coordinate
            random_y = random.randint(Window.height*0.5, Window.height*0.85)    # randomize y-coordinate
            rand_size = random.randint(70,100)                                  # randomize size of stars
            star = Star(random_x, random_y, rand_size)
            self.add_entity(star)

    def _on_frame(self, dt):
        self.dispatch("on_frame", dt)

    def on_frame(self, dt):
        pass

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self._score_label.text = "Score: " + str(value)
        self._score_label.refresh()
        self._score_instruction.texture = self._score_label.texture
        self._score_instruction.size = self._score_label.texture.size

    def add_entity(self, entity):
        self._entities.add(entity)
        self.canvas.add(entity._instruction)

    def remove_entity(self, entity):
        if entity in self._entities:
            self._entities.remove(entity)
            self.canvas.remove(entity._instruction)

    def collides(self, e1, e2):
        r1x = e1.pos[0]
        r1y = e1.pos[1]
        r2x = e2.pos[0]
        r2y = e2.pos[1]
        r1w = e1.size[0]
        r1h = e1.size[1]
        r2w = e2.size[0]
        r2h = e2.size[1] - e2.size[0]   # takes only the top of the arrow

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else:
            return False

    def colliding_entities(self, entity):
        result = set()
        for e in self._entities:
            if self.collides(e, entity) and e != entity:
                result.add(e)
        return result

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(keycode[1])

    #print (keycode[1]) double check what is keycode tuple

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

class Star:
    def __init__(self, pos_x, pos_y, length):
        self.pos = (pos_x, pos_y)
        self.size = (length, length)
        self.source = "./images/star1.png"
        self._instruction = Rectangle(pos=self.pos, size=self.size, source=self.source)

class Entity(object):
    def __init__(self):
        self._pos = (0, 0)
        self._size = (100, 100)
        self._source = "RANDOM.png"
        self._instruction = Rectangle(
            pos=self._pos, size=self._size, source=self._source)

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._instruction.pos = self._pos

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._instruction.size = self._size

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
        self._instruction.source = self._source


class Hook(Entity):
    def __init__(self, pos, speed=300):
        super(Hook,self).__init__()
        sound = SoundLoader.load('./music/pres_plop2.wav')
        sound.play()
        self._speed = speed
        self.pos = pos
        self.source = './images/arrow.png'
        self.size = (45, Window.height)
        game.bind(on_frame=self.move_step)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)

    def move_step(self, sender, dt):
        # check for collision/out of bounds
        if self.pos[1] > Window.height:
            self.stop_callbacks()
            game.remove_entity(self)
            return
        for e in game.colliding_entities(self):
            if isinstance(e, Star):
                game.add_entity(Explosion((e.pos[0]-50, e.pos[1]-50)))    # Depends on size of explosion
                self.stop_callbacks()
                game.remove_entity(self)
                # e.stop_callbacks()
                game.remove_entity(e)
                game.score += 1
                return

        # move
        step_size = self._speed * dt
        new_x = self.pos[0]
        new_y = self.pos[1] + step_size
        self.pos = (new_x, new_y)


# class Enemy(Entity):
#     def __init__(self, pos, speed=100):
#         super(Enemy,self).__init__()
#         self._speed = speed
#         self.pos = pos
#         self.source = './images/blackhole.png'
#         game.bind(on_frame=self.move_step)

#     def stop_callbacks(self):
#         game.unbind(on_frame=self.move_step)

#     def move_step(self, sender, dt):
#         # check for collision/out of bounds
#         if self.pos[1] < 0:
#             self.stop_callbacks()
#             game.remove_entity(self)
#             game.score -= 1
#             return
#         for e in game.colliding_entities(self):
#             if e == game.player:
#                 game.add_entity(Explosion(self.pos))
#                 self.stop_callbacks()
#                 game.remove_entity(self)
#                 game.score -= 1
#                 return

#         # move
#         step_size = self._speed * dt
#         new_x = self.pos[0]
#         new_y = self.pos[1] - step_size
#         self.pos = (new_x, new_y)


class Explosion(Entity):
    def __init__(self, pos):
        super(Explosion,self).__init__()
        self.pos = pos
        sound = SoundLoader.load('./music/star3.wav')
        self.source = './images/sparkle.png'
        sound.play()
        Clock.schedule_once(self._remove_me, 0.1)

    def _remove_me(self, dt):
        game.remove_entity(self)

class Player(Entity):
    def __init__(self):
        super(Player,self).__init__()
        self.source = './images/astro.png'
        game.bind(on_frame=self.move_step)
        self._shoot_event = Clock.schedule_interval(self.shoot_step, 0.3)
        self.pos = (400, 0)

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)
        self._shoot_event.cancel()

    def shoot_step(self, dt):
        # shoot
        if "spacebar" in game.keysPressed:
            x = self.pos[0] + self.size[0]/2
            y = -Window.height
            game.add_entity(Hook((x, y)))

    def move_step(self, sender, dt):
        # move
        step_size = 350 * dt
        newx = self.pos[0]
        newy = self.pos[1]
        if "a" in game.keysPressed:
            newx -= step_size
        if "d" in game.keysPressed:
            newx += step_size
        self.pos = (newx, newy)

#############################################################

# Inheritance - Screen is the Super Class
class HomeScreen(Screen):
    pass

class LevelsScreen(Screen):
    pass

class InstructionsScreen(Screen):
    pass

class Level1Screen(Screen):
    astronaut_killed = False
    num_stars = 5
    num_stars_collected = 0
    num_blackholes = 0
    num_animals = 0
    pass

class Level2Screen(Screen):
    astronaut_killed = False
    num_stars = 8
    num_stars_collected = 0
    num_blackholes = 3
    num_animals = 0
    pass

class Level3Screen(Screen):
    astronaut_killed = False
    num_stars = 12
    num_stars_collected = 0
    num_blackholes = 5
    num_animals = 3
    pass

class AdvanceScreen(Screen):
    pass

class WinScreen(Screen):
    pass

class LoseScreen(Screen):
    pass

game = GameWidget()
game.player = Player()
game.player.pos = (Window.width/2, 0)
game.add_entity(game.player)

# player2 = Player()
# player2.pos = (Window.width/3, 0)
# player2.source = './images/porcupine.png'
# game.add_entity(player2)

# Build the Astronaut App
class MyApp(App):
    # Initialize when app starts
    def on_start(self):
        # Load all the relevant sound tracks
        self.plop_sound = SoundLoader.load("./music/pres_plop3.wav")
        self.star_sound = SoundLoader.load("./music/star3.wav")
        self.blackhole_sound = SoundLoader.load("./music/bh1.wav")
        self.main_bg_music = SoundLoader.load("./music/song1.wav")

        # Plays background music when game starts
        self.main_bg_music.loop = True
        self.main_bg_music.play()

    # Play star sound when star is clicked in Levels Screen
    def play_star_sound(self, screenName):
        self.star_sound.play()
        manager.current = screenName

    def play_plop_sound(self, screenName):
        self.plop_sound.play()
        manager.current = screenName

    def screen_on_enter(self, screenNum):
        game.score = 0
        game.spawn_stars(screenNum * 5)

        curr_screen = self.root.screens[screenNum]
        curr_screen.ids['layout_lvl'+str(screenNum)].add_widget(game)

    def screen_on_leave(self, screenNum):

        curr_screen = self.root.screens[screenNum]
        curr_screen.ids['layout_lvl'+str(screenNum)].remove_widget(game)

    def build(self):
        # Load KV file
        Builder.load_file("astronaut.kv")

        # Add Screen widgets to Screen Manager
        manager.add_widget(HomeScreen(name="HOME"))
        manager.add_widget(Level1Screen(name="LEVEL1"))
        manager.add_widget(Level2Screen(name="LEVEL2"))
        manager.add_widget(Level3Screen(name="LEVEL3"))
        manager.add_widget(LevelsScreen(name="LEVELS"))
        manager.add_widget(InstructionsScreen(name="INSTRUCTIONS"))
        manager.add_widget(AdvanceScreen(name="ADVANCE"))
        manager.add_widget(WinScreen(name="WIN"))
        manager.add_widget(LoseScreen(name="LOSE"))

        # Display the Home Screen
        manager.current = "HOME"
        return manager

if __name__ == '__main__':
    MyApp().run()





# Use State Machines to transition to different screens
# class Astronaut(sm.SM):
    
#     def __init__(self):
#         self.start_state = "LEVELS"