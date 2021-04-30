import pygame_menu
import pygame
import game
import json
import threading


DEFAULT = 'Ivan'


class Menu:
    def start_game(self):
        user_name = self.text_input.get_value()
        with open('save.json', 'w') as file:
            json.dump(user_name, file)
        game.main(user_name)

    def __init__(self, name, width, height):
        try:
            with open('save.json', 'r') as file:
                user_name = json.load(file)
        except FileNotFoundError:
            print('File not found!')
            user_name = DEFAULT
        surface = pygame.display.set_mode((750, 500))
        menu = pygame_menu.Menu(name, width, height,
                                theme=pygame_menu.themes.THEME_BLUE)
        self.text_input = menu.add.text_input('Name: ', default=str(user_name))
        menu.add.button('Play', self.start_game)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(surface)


def main():
    pygame.init()
    Menu('Welcome', 300, 400)
    pygame.exit()


if __name__ == '__main__':
    main()
