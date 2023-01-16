"""
Character class which is a parrent class for Missionary and Cannibal
"""
import pygame
import copy
import math


class Character(pygame.sprite.Sprite):
    def __init__(self, image) -> None:
        super(Character, self).__init__()
        self.initial_image = pygame.image.load(f'images/{image}')
        self.image = copy.copy(self.initial_image)
        self.rect = self.image.get_rect()
        self.side = 1

    def get_on_boat(self, x, y, side):
        """
        adds a character to a boat
        """
        if side == 1:
            self.image = pygame.transform.scale(self.image,
                                                (self.rect.w/2, self.rect.h/2))
            self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

    def get_off_boat(self, boat):
        """
        removes a character from a boat
        """
        boat.remove_sailor(self)
        if boat.get_side() == 1:
            self.image = copy.copy(self.initial_image)
            self.rect = self.image.get_rect()

    def show(self, scr, boat):
        """
        displays a character
        """
        rect = copy.copy(self.rect)
        if self.is_on_boat(boat):
            displacement = boat.A*math.sin(boat.omega*boat.t)
            rect.move_ip(0, displacement)
        scr.blit(self.image, rect)

    def move(self, x, y):
        """
        moves a character
        """
        self.rect.move_ip(x, y)

    def is_on_boat(self, boat):
        """
        checks if a character is on a boat
        """
        return self in boat.sailors

    def set_position(self, position):
        """
        sets a postion of a character
        """
        self.rect.x, self.rect.y = position
