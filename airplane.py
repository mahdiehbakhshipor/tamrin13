import random
import arcade
import time 
import math
import threading

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


class StarShip(arcade.sprite):
    def __init__(self):
        super().init__(":resources:images/space_shooter/playerShip1_green.png")
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 35
        self.width = 50
        self.height= 50
        self.angle = 0
        self.change_angle = 0
        self.speed = 5
        self.bulelt_list = []
        self.score = 10
        self.heart = 3
        self.hert_image = arcade.load_texture("heart.png")
        self.fire_sound = arcade.loud_sound(":resources:sounds/laser2.wav")
    def fire(self):
        self.bullet_list.append(Bullet(self))

    def rotate(self):
        self.angle += self.speed * self.change_angle
    
    def fire(self):
        self.bullet_list.append(Bullet(self))
        arcade.play_sound(self.fire_sound)


class Enemy(arcade.sprite):
    def __init__(self):
        super().init__(":resources:images/space_shooter/playerShip3_orange.png")
        self.center_x = random.randint(0, SCREEN_WIDTH)
        self.center_y = SCREEN_HEIGHT + 25
        self.change_y = 0
        self.width = 50
        self.height= 50
        self.speed = 5
        self.bullet_list = []

    def move(self):
        self.center_y -= self.speed       
    

class Bullet(arcade.sprit):
    def __init__(self, host):
        super().__init__(":resources:images/space_shooter/laserRed01.png")
        self.speed = 6
        self.angle = host.angle
        self.center_x = host.center_x
        self.center_y = host.center_y

    def move (self):
        a = math.radians(self.angle)
        self.center_x += self.speed * math.sin(a)
        self.center_y += self.speed * math.cos(a)

class Explosion(arcade.Sprite):
    def __init__(self, x, y, st):
        super().__init__("explosion.png")
        self.width = 60
        self.height = 60
        self.center_x = x
        self.center_y = y
        self.show_time = 4
        self.start_time = st

class Game(arcade.window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,"Interstellar game 🚀")
        arcade.set_background_color(arcade.color.BLACK)
        self.background_image = arcade.load_texture(":resources:images/backgrounds/abstract_2.jpg")
        self.me = StarShip()
        #self.enemy = Enemy()
        self.enemy_list = []
        self.start_time = time.time()
        self.gameover_image = arcade.load_texture("gameovver.jpg")
        self.difficulty = 0.2
        self.enemy_interval = random.randint(1, 5)
        self.game_status = True
        self.destroy_sound = arcade.load_sound(":resources:sounds/lose3.wav")
        self.explosion_list = []
        self.start_thread=True
        self.end_thread=False
        self.my_thread=threading.Thread(target=self.add_enemy)
        self.my_thread.start()


    def add_enemy(self):
        while not self.game_over:
            time.sleep(5)
            speed=4
            if not self.game_over:
                self.enemy_list.append(Enemy())
            




    def on_draw(self):
        arcade.start_render()

        if self.me.health <=0 :
            arcade.draw_text("GAME OVER!! ", self.w//2-200, self.h//2, arcade.color.RED,20, width=400, align="center")

        else:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.w, self.h, self.background_image)  
            self.me.draw()
            for i in range(len(self.me.bullet_list)):
                self.me.bullet_list[i].draw()

            for i in range(len(self.enemy_list)):
                self.enemy_list[i].draw()

            for i in range(self.me.health):
                arcade.draw_lrwh_rectangle_textured(10+i*35 ,10 ,30 ,30 ,self.health_image)
            arcade.draw_text("Score: %i"%self.me.score, self.w-130, 10, arcade.color.LIGHT_HOT_PINK, 20, width=200, align='left')
     

    def on_update(self, delta_time: float):
        self.end_time = time.time()

        if self.end_time - self.start_time > self.next_enemy_time:
           self.next_enemy_time = random.randint(3, 5)
           self.enemy_list.append(Enemy(self.w, self.h, int(3+(self.end_time-self.game_start_time)//24)))
           self.start_time = time.time()

        self.me.rotate()
        for i in range(len(self.me.bullet_list)):
            self.me.bullet_list[i].move()
        for i in range(len(self.enemy_list)):
            self.enemy_list[i].move()
        for enemy in self.enemy_list:
            for bullet in self.me.bullet_list:
                if arcade.check_for_collision(bullet, enemy):
                    enemy.hit_sound()
                    self.me.bullet_list.remove(bullet)
                    self.enemy_list.remove(enemy)
                    self.me.score += 1
        for enemy in self.enemy_list:
            if enemy.center_y < 0:
                self.me.health -= 1
                self.enemy_list.remove(enemy)
        for bullet in self.me.bullet_list:
            if bullet.center_y > self.height or bullet.center_x < 0 or bullet.center_x > self.width:
                self.me.bullet_list.remove(bullet)
        

    def on_key_press(self, symbol: int, modifiers: int):
       
        if symbol == arcade.key.SPACE:
           self.me.fire() 
           self.me.bullet_list[-1].lunch()

        elif symbol == arcade.key.RIGHT:
            self.me.change_angle=-1

        elif symbol == arcade.key.LEFT:
            self.me.change_angle=+1

        elif symbol == arcade.key.UP:
            self.me.change_y = 1

        elif symbol == arcade.key.DOWN:
            self.me.change_y = -1

    def on_key_release(self, symbol, modifiers):
        self.me.change_angle = 0
        self.me.change_x = 0
        self.me.change_y = 0

game = Game()
arcade.ran()