"""
Show how to use lights.

.. note:: This uses features from the upcoming version 2.4. The API for these
          functions may still change. To use, you will need to install one of the
          pre-release packages, or install via GitHub.

Artwork from http://kenney.nl

"""
import arcade
from arcade.experimental.lights import Light, LightLayer

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Lighting Demo"
VIEWPORT_MARGIN = 200
MOVEMENT_SPEED = 5

# Это цвет, используемый для обозначения "рассеянного света". Если ты ничего не хочешь
# рассеянный свет, установите его на черный.
AMBIENT_COLOR = (10, 10, 10)

class MyGame(arcade.Window):
    """ Main Game Window """

    def __init__(self, width, height, title):
        """ Set up the class. """
        super().__init__(width, height, title, resizable=True)

        # Sprite lists
        self.background_sprite_list = None
        self.player_list = None
        self.wall_list = None
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Used for scrolling
        self.view_left = 0
        self.view_bottom = 0

        # --- Light related ---
        # List of all the lights
        self.light_layer = None
        # Individual light we move with player, and turn on/off
        self.player_light = None

    def setup(self):
        """ Create everything """

        # Создание списков спрайтов
        self.background_sprite_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Создать спрайт игрока
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.4)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 270
        self.player_list.append(self.player_sprite)

        # --- Light related ---
        # Свет должен на что-то падать. Если нет фонового спрайта или цвета,
        # вы увидите только черный цвет. Поэтому мы используем цикл для создания целой кучи кирпичных плиток, которые будут помещены в
        # background.
        for x in range(-128, 2000, 128):
            for y in range(-128, 1000, 128):
                sprite = arcade.Sprite(":resources:images/tiles/brickTextureWhite.png")
                sprite.position = x, y
                self.background_sprite_list.append(sprite)

        # Создайте световой слой, используемый для рендеринга объектов, затем выполните постобработку и
        # добавьте подсветку. Это должно соответствовать размеру экрана.
        self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
        # Мы также можем установить цвет фона, который будет подсвечиваться лампочками,
        # но в данном случае нам нужен просто черный фон
        self.light_layer.set_background_color(arcade.color.BLACK)

        # Здесь мы создаем пучок огней.

        # Создайте небольшой белый свет
        x = 100
        y = 200
        radius = 100
        mode = 'soft'
        color = arcade.csscolor.WHITE
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        # Создайте перекрывающий друг друга большой белый свет
        x = 300
        y = 150
        radius = 200
        color = arcade.csscolor.WHITE
        mode = 'soft'
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        # Создайте три неперекрывающихся RGB-источника света
        x = 50
        y = 450
        radius = 100
        mode = 'soft'
        color = arcade.csscolor.RED
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        x = 250
        y = 450
        radius = 100
        mode = 'soft'
        color = arcade.csscolor.GREEN
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        x = 450
        y = 450
        radius = 100
        mode = 'soft'
        color = arcade.csscolor.BLUE
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        # Создайте три перекрывающихся RGB-источника света
        x = 650
        y = 450
        radius = 100
        mode = 'soft'
        color = arcade.csscolor.RED
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        x = 750
        y = 450
        radius = 100
        mode = 'soft'
        color = arcade.csscolor.GREEN
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        x = 850
        y = 450
        radius = 100
        mode = 'soft'
        color = arcade.csscolor.BLUE
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        # создайте три перекрывающихся RGB-источника света
        #  Но "жесткий" свет, который не гаснет.
        x = 650
        y = 150
        radius = 100
        mode = 'hard'
        color = arcade.csscolor.RED
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        x = 750
        y = 150
        radius = 100
        mode = 'hard'
        color = arcade.csscolor.GREEN
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        x = 850
        y = 150
        radius = 100
        mode = 'hard'
        color = arcade.csscolor.BLUE
        light = Light(x, y, radius, color, mode)
        self.light_layer.add(light)

        # Создайте свет, который будет сопровождать игрока повсюду.
        #  Мы расположим его позже, когда игрок сделает ход.
        #  Мы добавим его к световому слою только тогда, когда проигрыватель включит свет
        #  Мы начинаем с выключенного света.
        radius = 150
        mode = 'soft'
        color = arcade.csscolor.WHITE
        self.player_light = Light(0, 0, radius, color, mode)

        # Создайте физический движок
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Установите границы видового экрана
        #  Эти цифры указывают, куда мы "прокрутили".
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """ Draw everything. """
        self.clear()

        # --- Light related ---
        # Все, на что должно влиять освещение, визуализируется внутри этого
        # оператора 'with'. На экране пока ничего не отображается, только свет
        # слой
        with self.light_layer:
            self.background_sprite_list.draw()
            self.player_list.draw()

        # Нарисуйте светлый слой на экране.
        # Это заполнит весь экран освещенной версией
        # того, что мы нарисовали на световом слое выше.
        self.light_layer.draw(ambient_color=AMBIENT_COLOR)

        # Now draw anything that should NOT be affected by lighting.
        arcade.draw_text("Press SPACE to turn character light on/off.",
                         10 + self.view_left, 10 + self.view_bottom,
                         arcade.color.WHITE, 20)

    def on_resize(self, width, height):
        """ User resizes the screen. """

        # --- Light related ---
        # Нам нужно изменить размер светового слоя таким образом, чтобы
        self.light_layer.resize(width, height)

        # Прокрутите экран так, чтобы пользователь был виден
        self.scroll_screen()

    def on_key_press(self, key, _):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            # --- Light related ---
            # Мы можем добавлять/ удалять источники света из слоя light. Если их нет
            # в световом слое, то свет выключен.
            if self.player_light in self.light_layer:
                self.light_layer.remove(self.player_light)
            else:
                self.light_layer.add(self.player_light)

    def on_key_release(self, key, _):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def scroll_screen(self):
        """ Manage Scrolling """

        # Прокрутите влево
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left

        # Прокрутите вправо
        right_boundary = self.view_left + self.width - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary

        # Прокрутите вверх
        top_boundary = self.view_bottom + self.height - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary

        # Прокрутите вниз
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom

        # Убедитесь, что наши границы представляют собой целочисленные значения. Хотя окно просмотра
        # поддерживает числа с плавающей запятой, для этого приложения мы хотим, чтобы каждый пиксель
        # в окне просмотра отображался непосредственно на пиксель на экране. Нам не нужны
        # какие-либо ошибки округления.
        self.view_left = int(self.view_left)
        self.view_bottom = int(self.view_bottom)

        arcade.set_viewport(self.view_left,
                            self.width + self.view_left,
                            self.view_bottom,
                            self.height + self.view_bottom)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Вызовите обновление для всех спрайтов (хотя в этом примере спрайты мало что делают
        # ).
        self.physics_engine.update()

        # --- Light related ---
        # Мы можем легко переместить светильник, установив положение,
        # или с помощью center_x, center_y.
        self.player_light.position = self.player_sprite.position

        # Прокрутите экран, чтобы мы могли видеть игрока
        self.scroll_screen()


if __name__ == "__main__":
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()
