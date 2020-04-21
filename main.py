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
# Config.set('graphics', 'width', '412')
# Config.set('graphics', 'height', '732')
Window.size = (900,600)

# Create the manager
manager = ScreenManager(transition=FadeTransition())
# Load KV file
Builder.load_file("astronaut.kv")

# Inheritance - Screen is the Super Class
class HomeScreen(Screen):
    pass

class LevelsScreen(Screen):
    pass

class InstructionsScreen(Screen):
    pass

class Level1Screen(Screen):
    # astronaut_killed = False
    # num_stars = 5
    # num_stars_collected = 0
    # num_blackholes = 0
    # num_animals = 0
    pass

class Level2Screen(Screen):
    # astronaut_killed = False
    # num_stars = 8
    # num_stars_collected = 0
    # num_blackholes = 3
    # num_animals = 0
    pass

class Level3Screen(Screen):
    # astronaut_killed = False
    # num_stars = 12
    # num_stars_collected = 0
    # num_blackholes = 5
    # num_animals = 3
    pass

class AdvanceScreen(Screen):
    pass

class WinScreen(Screen):
    pass

class LoseScreen(Screen):
    pass

# Add Screen widgets to Screen Manager, goes in order i.e. 0 = "HOME", 1 = "LEVEL1"
manager.add_widget(HomeScreen(name="HOME"))
manager.add_widget(Level1Screen(name="LEVEL1"))
manager.add_widget(Level2Screen(name="LEVEL2"))
manager.add_widget(Level3Screen(name="LEVEL3"))
manager.add_widget(LevelsScreen(name="LEVELS"))
manager.add_widget(InstructionsScreen(name="INSTRUCTIONS"))
manager.add_widget(AdvanceScreen(name="ADVANCE"))
manager.add_widget(WinScreen(name="WIN"))
manager.add_widget(LoseScreen(name="LOSE"))


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super(GameWidget,self).__init__(**kwargs)

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        # self._score_label = CoreLabel(text="Score: 0", font_size=50, font_name='./fonts/absolutepink.otf')
        # self._score_label.refresh()
        # self._score = 0
        self._lives_label = CoreLabel(text="Lives: 0", font_size=100, font_name='./fonts/absolutepink.otf')
        self._lives_label.refresh()
        self._lives = 3

        self._stars = -1 #to initialise, however will never get this value 
        self._levels = 0 #initialise 
        self._num_portals = 0
        self.register_event_type("on_frame")

        with self.canvas:
            self._lives_instruction = Rectangle(texture=self._lives_label.texture, pos=(7, Window.height *0.93), size=self._lives_label.texture.size)
        
        self.keysPressed = set()
        self._entities = set()

        Clock.schedule_interval(self._on_frame, 0)
        Clock.schedule_interval(self.checks_win_lose, 0)

    def checks_win_lose(self, dt):
        if self.lives == 0:
            manager.current = "LOSE"
            self.lives = 3
        elif self.stars == 0:
            if self.levels == 3:  #won at level 3
                manager.current = "WIN"
                self.stars = -1
            else: 
                #portal appears
                self.spawn_portal()
             
    def spawn_animal(self):
        animal = Animal()
        self.add_entity(animal)


    def spawn_portal(self):
        #appears as canvas widget
        if self._num_portals == 0:
            self._portal = Portal()
            self.add_entity(self._portal)
            self._num_portals += 1 #ensures that it only appears once
        #if position of player within pos of portal, advance to nxt lvl + remove canvas widget 
        # for entity in self._entities:
        #     if isinstance(entity, Portal):
        #         portal = entity 

        if (self.player.pos[0] + self.player.size[0]/2) >= (self._portal.pos[0] + self._portal.size[0]/2):
            self.stars = -1 #to ensure constant looping 
            self._num_portals -= 1    
            manager.current = "LEVEL{}".format(self.levels + 1)


    # Create instance objects from Star class
    def spawn_stars(self, num_stars):
        self.stars = num_stars
        for i in range(num_stars):
            star = Star()
            self.add_entity(star)

    # Create instance objects from Blackhole class
    def spawn_blackhole(self, num_blackhole):
        for i in range(num_blackhole):
            random_x = random.uniform(Window.width*0.15, Window.width*0.85)     # randomize x-coordinate
            random_y = random.uniform(Window.height*0.5, Window.height*0.85)    # randomize y-coordinate
            rand_pos = (random_x, random_y)
            rand_length = random.uniform(110,150)                                  # randomize size of stars
            blackhole = Blackhole(rand_pos, rand_length) #called the class Blackhole
            self.add_entity(blackhole)
    
    def remove_all(self):
        for entity in self._entities.copy(): #.copy() to allow iteration through all elements while elements in original list is being romved 
            if isinstance(entity, Star) or isinstance(entity, Blackhole) or isinstance(entity, Hook) or isinstance(entity, Portal):
                self.remove_entity(entity)

    def _on_frame(self, dt):
        self.dispatch("on_frame", dt)

    def on_frame(self, dt):
        pass
    
    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self,value):
        self._lives = value
        self._lives_label.text = "Lives = " + str(value)
        self._lives_label.refresh()
        self._lives_instruction.texture = self._lives_label.texture
        self._lives_instruction.size = self._lives_label.texture.size
    
    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self,value):
        self._stars = value 

    @property
    def levels(self):
        return self._levels

    @levels.setter
    def levels(self, value):
        self._levels = value  



    # @property
    # def score(self):
    #     return self._score

    # @score.setter
    # def score(self, value):
    #     self._score = value
    #     self._score_label.text = "Score: " + str(value)
    #     self._score_label.refresh()
    #     self._score_instruction.texture = self._score_label.texture
    #     self._score_instruction.size = self._score_label.texture.size

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
        r2h = e2.size[1]

        # Center coordinates of the tip of arrow
        x = r2x + r2w/2
        y = r2y + r2h - r2w/2

        # Check if tip of arrow is within the target boundary
        if (r1x < x < r1x + r1w and r1y < y < r1y + r1h):
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

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

class Entity(object):
    def __init__(self):
        self._pos = (0, 0)
        self._size = (200, 200)
        self._source = "RANDOM.png"
        self._instruction = Rectangle(
            pos=self._pos, size=self._size, source=self._source)

#to access the private attribute, need to create getter and setter
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._instruction.pos = self._pos   # changes the position of entity

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

class Portal(Entity):
    def __init__(self):
        super(Portal,self).__init__()
        self.pos = (Window.width - 1.5*self.size[0], 0)
        self.source = "./images/portal.png"

class Animal(Entity):
    def __init__(self):
        super(Animal,self).__init__()
        self.size = (100,100)
        self.pos = (0,0)
        self.source = "./images/porcupine.png"
        self.direction = "right"
        Clock.schedule_interval(self.move_step, 0)


    def change_direction(self):
        if self.direction == "right":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "right"


    #if player pushes it, both player and animal move together but in a slower motion 
    def move_step(self, dt):
        self.stepsize = 200 * dt
        newx = self.pos[0]
        newy = self.pos[1]
        command = game.player.push_animal(self)

        if command == True:
            self.change_direction()
        
        if self.direction == "right":
            newx += self.stepsize
            if newx >= Window.width: #return from the left side of window
                newx = 0 - self.size[0]
        
        if self.direction == "left":
            newx -= self.stepsize
            if newx <= 0 - self.size[0]: #return from the right side of window
                newx = Window.width

        step = game.player.with_animal(self)
        newx += step  #net speed of the animal slows down and moves in opp direction cuz player's speed is faster than animal 

        self.pos = (newx, newy)
        pass    
    
    # def entering_from

class Blackhole(Entity):
    def __init__(self, pos, length):
        super(Blackhole,self).__init__()
        self.pos = pos
        self.size = (length, length)
        self.source = "./images/blackhole.png"

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
            if isinstance(e, Blackhole): # (object, class) checks whether collided object is an instance of Blackhole
                game.add_entity(Explosion((e.pos[0]-150, e.pos[1]-150)))    # Depends on size of explosion
                self.stop_callbacks()
                game.remove_entity(self)
                # e.stop_callbacks()
                game.remove_entity(e)
                # game.score -= 100 
                game.lives -= 1
                return
                
            elif isinstance(e, Star):  # checks whether collided object is an instance Star
                game.add_entity(Explosion((e.pos[0]-150, e.pos[1]-150)))
                self.stop_callbacks()
                game.remove_entity(self)
                game.remove_entity(e)
                # game.score += 10000
                game.stars -= 1

        # move
        step_size = self._speed * dt
        new_x = self.pos[0]
        new_y = self.pos[1] + step_size
        self.pos = (new_x, new_y)

class Explosion(Entity):
    def __init__(self, pos):
        super(Explosion,self).__init__()
        self.size = (300, 300)
        self.pos = pos
        self.source = './images/sparkle.png'

        sound = SoundLoader.load('./music/star3.wav')
        sound.play()
        Clock.schedule_once(self._remove_me, 0.1)

    def _remove_me(self, dt):
        game.remove_entity(self)

class Star(Entity):
    def __init__(self):
        super(Star,self).__init__()
        self.source = './images/star1.png'
        self.size = (150, 150)
        self.pos = (Window.width/2, Window.height/2)
        self.new_x, self.new_y = self.rand_side(False) #Boolean by default false, to initialise first point

        Clock.schedule_interval(self.change_dir, 0)

    def rand_side(self, new_dir):
        # Selects a random point within the side boundaries
        left = (random.uniform(Window.width* 0.05, Window.width*0.3), random.uniform(Window.height*0.3,Window.height*0.7))
        right = (random.uniform(Window.width*0.7, Window.width*0.90), random.uniform(Window.height*0.3,Window.height*0.7))
        top = (random.uniform(Window.width*0.05, Window.width* 0.90), random.uniform(Window.height*0.7, Window.height*0.90))
        bottom = (random.uniform(Window.width*0.05, Window.width*0.90), random.uniform(Window.height*0.3, Window.height*0.4))
        
        # Selects the coordinates that the star will move towards
        if (not new_dir):
            # Initializing the first random point
            self.new_x, self.new_y = random.choice([left,right,top,bottom])
        else:
            # Star is at the left
            if (self.new_x <= Window.width*0.3):
                self.new_x, self.new_y = random.choice([right, top, bottom])
            # Star is at the right
            elif (self.new_x >= Window.width*0.7):
                self.new_x, self.new_y = random.choice([left, top, bottom])
            # Star is at the top
            elif (self.new_y <= Window.height*0.4):
                self.new_x, self.new_y = random.choice([top, left, right])
            # Star is at the bottom
            elif (self.new_y >= Window.height*0.7):
                self.new_x, self.new_y = random.choice([bottom, left, right])
        
        return self.new_x, self.new_y

    def change_dir(self, dt):
        # Controls the speed of the star
        step_size = 300 * dt

        # Move towards the direction of the new position
        if (self.pos[0] < self.new_x):
            new_x = self.pos[0] + step_size
        elif (self.pos[0] > self.new_x):
            new_x = self.pos[0] - step_size
        if (self.pos[1] < self.new_y):
            new_y = self.pos[1] + step_size
        elif (self.pos[1] > self.new_y):
            new_y = self.pos[1] - step_size

        # Assigns new position of star after moving
        self.pos = (new_x, new_y)
        
        # Checks if it's within the range of target point. Signifies that star changes direction
        if (abs(self.new_x - self.pos[0]) <= step_size/2 or abs(self.new_y - self.pos[1]) <= step_size/2):
            self.rand_side(True)

class Player(Entity):
    def __init__(self):
        super(Player,self).__init__()
        self.source = './images/astro.png'
        game.bind(on_frame=self.move_step)
        self._shoot_event = Clock.schedule_interval(self.shoot_step, 0.3)
        self.pos = (400,0)
        self.dist_moved = 0
        # self.jumping = True

    def stop_callbacks(self):
        game.unbind(on_frame=self.move_step)
        self._shoot_event.cancel()

    def shoot_step(self, dt):
        # shoot
        if "spacebar" in game.keysPressed:
            x = self.pos[0] + self.size[0]/2
            y = -Window.height
            game.add_entity(Hook((x, y))) #(x,y) position of Hook follows player, no speed hence by default = 300

    def with_animal(self, animal):
        newx = self.pos[0]
        newy = self.pos[1]
        step_size = 0      #if no force exerted, animal does not feel anything 

        if self.pos[0] <= animal.pos[0] + animal.size[0] < self.pos[0] + self.size[0]/2: #animal on left, within the range of player on right
            newx += animal.stepsize #player slows down => net step size, and moves with the animal 
            if "a" in game.keysPressed: #player exerts force on animal, a stepsize onto the animal
                step_size = -self.step_size 
        if self.pos[0] + self.size[0]/2 < animal.pos[0] <= self.pos[0] + self.size[0]: #animal on right, within the range of player on the left
            newx -= animal.stepsize #player slows down => net step size 
            if "d" in game.keysPressed:
                step_size = self.step_size

        if "w" in game.keysPressed:
                step_size = 0
        
        self.pos = (newx, newy)
        return step_size  #used to change speed of animal 
    
    def push_animal(self, animal):
        command = False

        #when in contact with animal, set a distance counter whereby if reached, the animal will change its direction
        if self.pos[0] <= animal.pos[0] + animal.size[0] < self.pos[0] + self.size[0]/2:  #animal on left
            if "a" in game.keysPressed:
                self.dist_moved += self.step_size - animal.stepsize #net speed of both player and animal
                if self.dist_moved >= self.size[0]:
                    command = True
                    self.dist_moved = 0 #to reset 
                    
        if self.pos[0] + self.size[0]/2 < animal.pos[0] <= self.pos[0] + self.size[0]: #animal on right
            if "d" in game.keysPressed:
                self.dist_moved += self.step_size - animal.stepsize
                if self.dist_moved >= self.size[0]:
                    command = True
                    self.dist_moved = 0 #to reset 

        return command 



    def move_step(self, sender, dt):
        # move
        self.step_size = 350 * dt
        newx = self.pos[0]
        newy = self.pos[1]
        # Window boundary = [0,Window.width-self.size[0]]
        if "a" in game.keysPressed and newx > 0:
            newx -= self.step_size
        if "d" in game.keysPressed and newx < Window.width-self.size[0]:
            newx += self.step_size

        #ensuring natural jump motion => gradual decrease in step size as player moves up, gradual increase as player moves down
        if "w" in game.keysPressed and newy == 0:
            self.jumpup = True
            newy += self.step_size*3
        elif 0 < newy <= self.size[1]/2 and self.jumpup:
            newy += self.step_size*3
        elif self.size[1]/2 < newy <= self.size[1]*3/4 and self.jumpup:
            newy += self.step_size*2
        elif self.size[1]*3/4 < newy <= self.size[1] and self.jumpup:
            newy += self.step_size
        elif newy > self.size[1]:
            self.jumpup = False
            newy -= self.step_size
        elif self.size[1]*3/4 < newy <= self.size[1] and not self.jumpup:
            newy -= self.step_size
        elif self.size[1]/2 < newy <= self.size[1]*3/4 and not self.jumpup:
            newy -= self.step_size*2
        elif 0 < newy <= self.size[1]/2 and not self.jumpup:
            newy -= self.step_size*3
            if (newy < 0):
                newy = 0
        
        self.pos = (newx, newy)


#############################################################

# # Inheritance - Screen is the Super Class
# class HomeScreen(Screen):
#     pass

# class LevelsScreen(Screen):
#     pass

# class InstructionsScreen(Screen):
#     pass

# class Level1Screen(Screen):
#     # astronaut_killed = False
#     # num_stars = 5
#     # num_stars_collected = 0
#     # num_blackholes = 0
#     # num_animals = 0
#     pass

# class Level2Screen(Screen):
#     # astronaut_killed = False
#     # num_stars = 8
#     # num_stars_collected = 0
#     # num_blackholes = 3
#     # num_animals = 0
#     pass

# class Level3Screen(Screen):
#     # astronaut_killed = False
#     # num_stars = 12
#     # num_stars_collected = 0
#     # num_blackholes = 5
#     # num_animals = 3
#     pass

# class AdvanceScreen(Screen):
#     pass

# class WinScreen(Screen):
#     pass

# class LoseScreen(Screen):
#     pass

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
        # Load all the relevant sound tracks to be used for each buttons
        self.plop_sound = SoundLoader.load("./music/pres_plop3.wav")
        self.star_sound = SoundLoader.load("./music/star3.wav")
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
        # game.score = 0 #initialise score to be 0
        game.levels = screenNum
        game.lives = 3
        game.remove_all()
        game.spawn_blackhole((screenNum-1) * 5) #num of blackholes = each level multiply 5 
        game.spawn_stars(screenNum) #according to the level, i.e. screenNUM = 1 (LEVEL1) = 1
        if screenNum == 3:
            game.spawn_animal()
        curr_screen = self.root.screens[screenNum] 
        #in documentation: ids to call the layouts for each screen, add_widget to transport the game into the screen
        curr_screen.ids['layout_lvl'+str(screenNum)].add_widget(game) 



    def screen_on_leave(self, screenNum):

        curr_screen = self.root.screens[screenNum]
        curr_screen.ids['layout_lvl'+str(screenNum)].remove_widget(game)

    def build(self):
        # # Load KV file
        # Builder.load_file("astronaut.kv")

        # # Add Screen widgets to Screen Manager, goes in order i.e. 0 = "HOME", 1 = "LEVEL1"
        # manager.add_widget(HomeScreen(name="HOME"))
        # manager.add_widget(Level1Screen(name="LEVEL1"))
        # manager.add_widget(Level2Screen(name="LEVEL2"))
        # manager.add_widget(Level3Screen(name="LEVEL3"))
        # manager.add_widget(LevelsScreen(name="LEVELS"))
        # manager.add_widget(InstructionsScreen(name="INSTRUCTIONS"))
        # manager.add_widget(AdvanceScreen(name="ADVANCE"))
        # manager.add_widget(WinScreen(name="WIN"))
        # manager.add_widget(LoseScreen(name="LOSE"))

        # Display the Home Screen as the first screen when entered
        manager.current = "HOME"
        return manager

if __name__ == '__main__':
    MyApp().run()


