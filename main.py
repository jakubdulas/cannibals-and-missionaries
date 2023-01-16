"""
Missionaries and Cannibals by Jakub Dulas
"""
import pygame
from constants import *
from Cannibal import Cannibal
from Missionary import Missionary
from Boat import Boat
import time
import sys


def is_boat_on_right_side(boat, character):
    """
    checks if the boat is on the right side of the river. Returns True or False
    """
    side = boat.get_side()

    if character in right.values() and side == 1:
        return True
    elif character in left.values() and side == -1:
        return True
    return False


def set_position(side, character, is_getting_on_boat):
    """
    sets a position on the riverside of a given character
    """
    global right, left

    if is_getting_on_boat:
        for key, value in right.items():
            if value == character:
                right[key] = None
                return
        for key, value in left.items():
            if value == character:
                left[key] = None
                return
    else:
        if side == 1:
            for key, value in right.items():
                if value is None:
                    right[key] = character
                    character.set_position(key)
                    return
        elif side == -1:
            for key, value in left.items():
                if value is None:
                    left[key] = character
                    character.set_position(key)
                    return


def handle_events():
    """
    handle events for game
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        character_clicked = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            clicked_sprites = [ch for ch in characters
                               if ch.rect.collidepoint(pos)]
            clicked_sprites.reverse()

            for character in clicked_sprites:
                l, top = character.rect.topleft
                x, y = pos
                pixel = character.image.get_at((x-l, y-top))
                if pixel[3] != 0:
                    character_clicked = True
                    if character.is_on_boat(boat) and not boat.sailing:
                        character.get_off_boat(boat)
                        set_position(boat.get_side(), character, False)
                    elif (is_boat_on_right_side(boat, character)
                          and not boat.sailing):
                        is_sailor_added = boat.add_sailor(character)
                        if is_sailor_added:
                            set_position(boat.get_side(), character, True)
                    break

            if boat.rect.collidepoint(pos) and not character_clicked:
                boat.sail()


def check_game_result(current_time):
    """
    announces a result of a game
    """
    global result, game_state, best_time
    characters_on_left = sum(map(lambda obj: obj.side == -1
                             if obj else 0, characters))
    if characters_on_left == 6:
        game_state = "result"
        result = "win"
        last_best_time = read_best_time()

        with open('best_time.txt', 'w') as f:
            if not last_best_time:
                f.write(str(current_time))
                best_time = current_time
            elif current_time < float(last_best_time):
                f.write(str(current_time))
                best_time = current_time
            else:
                f.write(str(last_best_time))

    cannibals_on_right = sum(map(lambda obj: obj.side == 1 if obj else 0,
                                 filter(lambda obj: type(obj) == Cannibal,
                                        characters)))
    missionaries_on_right = sum(map(lambda obj: obj.side == 1 if obj else 0,
                                filter(lambda obj: type(obj) == Missionary,
                                       characters)))
    cannibals_on_left = COUNT_CANNIBALS - cannibals_on_right
    missionaries_on_left = COUNT_MISSIONARIES - missionaries_on_right

    if cannibals_on_right > missionaries_on_right and \
       missionaries_on_right != 0:
        game_state = "result"
        result = "loss"
    elif cannibals_on_left > missionaries_on_left and \
            missionaries_on_left != 0:
        game_state = "result"
        result = "loss"


def game():
    """
    main function of game
    """
    current_time = time.time()-t
    handle_events()
    check_game_result(current_time)

    scr.blit(background, (0, 0))

    for character in left.values():
        if character is not None:
            character.show(scr, boat)

    boat.show(scr, current_time)

    for sailor in boat.sailors:
        sailor.show(scr, boat)

    for character in right.values():
        if character is not None:
            character.show(scr, boat)

    timer = timer_font.render(f"Time: {round(current_time, 2)}s",
                              False, (0, 0, 0))
    scr.blit(timer, (10, 10))

    if best_time:
        bt = timer_font.render(f"Best time: {round(best_time, 2)}",
                               False, (0, 0, 0))
        scr.blit(bt, (10, 30))


def show_rules():
    """
    displays rules
    """
    global game_state, t
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_state = "game"
                t = time.time()
    scr.blit(background, (0, 0))

    for idx, line in enumerate(RULES.split('\n')):
        text = rules_font.render(line, False, (0, 255, 0))
        scr.blit(text, (100, 100+idx*28))


def center_text(text):
    """
    centers given text
    """
    x, y = WINDOW_SIZE[0]/2-text.get_width()/2, \
        WINDOW_SIZE[1]/2-text.get_height()/2
    return x, y


def show_result(result):
    """
    displays a result
    """
    global game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                reset_game()
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    if result == 'loss':
        text = result_font.render('You lost!', False, (255, 0, 0))
        x, y = center_text(text)
        scr.blit(text, (x, y))

        for idx, line in enumerate(PLAY_AGAIN_TEXT.split('\n')):
            text = result_font.render(line, False, (0, 255, 0))
            x, y = center_text(text)
            scr.blit(text, (x+30, y+50*(idx+1)))

    elif result == 'win':
        text = result_font.render('You lost!', False, (255, 0, 0))
        x, y = center_text(text)
        scr.blit(text, (x, y))

        for idx, line in enumerate(PLAY_AGAIN_TEXT.split('\n')):
            text = result_font.render(line, False, (0, 255, 0))
            x, y = center_text(text)
            scr.blit(text, (x+30, y+50*(idx+1)))


def reset_timer():
    """
    resets timer
    """
    global t
    t = time.time()


def render_objects():
    """
    render game objects
    """
    right = {}
    left = {}

    for position in RIGHT_POSITIONS:
        right[position] = None

    for position in LEFT_POSITIONS:
        left[position] = None

    for position in RIGHT_POSITIONS:
        right[position] = None

    for position in LEFT_POSITIONS:
        left[position] = None

    characters = pygame.sprite.Group()

    # adding characters to group
    for cls in [Cannibal, Missionary]:
        for _ in range(3):
            obj = cls()
            characters.add(obj)

    # setting initial positions
    for character, pos in zip(characters, right.keys()):
        character.set_position(pos)
        right[pos] = character

    boat = Boat()
    return characters, right, left, boat


def reset_game():
    """
    sets initial game settings
    """
    global characters, right, left, game_state, boat, result, best_time
    game_state = "game"
    result = ""
    characters, right, left, boat = render_objects()
    best_time = read_best_time()
    reset_timer()


def read_best_time():
    """
    reads best time
    """
    with open('best_time.txt', 'r') as file:
        line = file.readline()
        if line:
            return float(line)
        return ''


if __name__ == '__main__':
    pygame.init()
    game_state = "main_screen"

    # setting up screen and background
    scr = pygame.display.set_mode(WINDOW_SIZE)
    background = pygame.image.load('images/background.png')

    timer_font = pygame.font.SysFont("Comic Sans MS", 18)
    rules_font = pygame.font.SysFont("Comic Sans MS", 32)
    result_font = pygame.font.SysFont("Comic Sans MS", 48)

    result = ""
    t = 0
    characters, right, left, boat = render_objects()

    best_time = read_best_time()

    while True:
        if game_state == "main_screen":
            show_rules()
        elif game_state == "game":
            game()
        elif game_state == "result":
            show_result(result)

        pygame.display.flip()
