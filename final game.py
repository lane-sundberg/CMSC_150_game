import os
import arcade
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Catch me if you can"


file_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(file_path)


class IntroView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Welcome to TAG ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Don't let the Baker catch you. ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("The longer you last, the higher the score ", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 225,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Mygame()
        game_view.setup()
        self.window.show_view(game_view)


class Enemy(arcade.Sprite):
    def __init__(self, image):
        super().__init__(image)
        self.speed = 2.5
    def follow_sprite(self, player_sprite):
        print(f"self.speed {self.speed}")
        if self.center_y < player_sprite.center_y:
            self.center_y += min(self.speed, player_sprite.center_y - self.center_y)
        elif self.center_y > player_sprite.center_y:
            self.center_y -= min(self.speed, self.center_y - player_sprite.center_y)

        if self.center_x < player_sprite.center_x:
            self.center_x += min(self.speed, player_sprite.center_x - self.center_x)
        elif self.center_x > player_sprite.center_x:
            self.center_x -= min(self.speed, self.center_x - player_sprite.center_x)





class Mygame(arcade.View,Enemy):
    def __init__(self):
        super().__init__()
        self.background = None
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.player_list = None

        self.player_sprite = None

        self.enemy_list = None

        self.score = 0
        arcade.set_background_color(arcade.color.BLACK)
        self.window.set_mouse_visible(False)
    def setup(self):
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        self.score = 0

        self.player_sprite = arcade.Sprite("cake.png")
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.enemy = Enemy("chef.bmp")
        self.enemy.center_x = 750
        self.enemy.center_y = 550
        self.enemy_list.append(self.enemy)

        self.frame_count = 100

    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.enemy_list.draw()

        output = f"Time: {self.score}"
        arcade.draw_text(output, 713.5, 550, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        self.frame_count-=1
        global enemy
        self.player_list.update()
        self.enemy_list.update()
        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player_sprite)


        self.score += delta_time
        print(self.frame_count)
        if self.frame_count <0:
            enemy.speed += .5
            self.frame_count = 100



        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        for collision in hit_list:
            self.player_sprite.kill()
            self.enemy.kill()
            end_game_view = Endgame(self.score)
            self.window.show_view(end_game_view)


class Endgame(arcade.View,):
    def __init__(self, score):
        super().__init__()
        self.text = "Oops, Looks like you have been caught by the Baker!!"
        self.score = score
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text(self.text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        score = f"{round(self.score, 2)} seconds"
        arcade.draw_text(f"your time is: {score}",
                         SCREEN_WIDTH / 2,
                         200,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Mygame()
        game_view.setup()
        self.window.show_view(game_view)


def main():
    """ Main method """
    # window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    # window.setup()
    # arcade.run()
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    intro_view = IntroView()
    window.show_view(intro_view)
    arcade.run()


main()
