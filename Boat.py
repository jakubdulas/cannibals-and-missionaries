"""
Boat class
"""
import pygame
import math
import copy


class Boat(pygame.sprite.Sprite):
    A = 10  # amplitude of harmonic motion of a boat
    omega = 3  # angular frequency of harmonic motion of a boat
    STARTING_POINT = (450, 200)
    ENDING_POINT = (150, 180)

    def __init__(self) -> None:
        super(Boat, self).__init__()
        self.image = pygame.image.load('images/raft.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = self.STARTING_POINT
        self.sailors_seats = [None, None]
        self.sailing = False
        self.last_position = self.ENDING_POINT
        self.seats = [(self.rect.w/5, self.rect.h*4/5),
                      (self.rect.h*3/5, self.rect.h*3/5)]

    @property
    def sailors(self):
        """
        return list of sailors which are not None
        """
        return list(filter(lambda x: x is not None, self.sailors_seats))

    def add_sailor(self, sailor):
        if None in self.sailors_seats and not self.sailing:
            idx = self.sailors_seats.index(None)
            x, y = self.get_seat_position(idx)

            self.sailors_seats[idx] = sailor

            sailor.get_on_boat(x, y, self.get_side())
            return True
        return False

    def remove_sailor(self, sailor):
        """
        removes sailor from a boat
        """
        idx = self.sailors_seats.index(sailor)
        self.sailors_seats[idx] = None

    def show(self, scr, t):
        """
        displays a boat
        """
        self.t = t
        self.displacement = self.A*math.sin(self.omega*t)
        rect = copy.copy(self.rect)
        rect.move_ip(0, self.displacement)

        if self.sailing:
            dystance_x = abs(self.STARTING_POINT[0]-self.ENDING_POINT[0])
            dystance_y = abs(self.STARTING_POINT[1]-self.ENDING_POINT[1])

            if self.last_position == self.ENDING_POINT:
                direction = -1
            else:
                direction = 1

            step_x = direction * dystance_x / 100
            step_y = direction * dystance_y / 20

            self.rect.move_ip(step_x, step_y)

            if self.rect.x > self.STARTING_POINT[0] and \
               self.rect.y > self.STARTING_POINT[1]:
                self.last_position = self.ENDING_POINT
                self.sailing = False
                for sailor in self.sailors:
                    sailor.side = self.get_side()
            elif self.rect.x < self.ENDING_POINT[0] and \
                    self.rect.y < self.ENDING_POINT[1]:
                self.last_position = self.STARTING_POINT
                self.sailing = False
                for sailor in self.sailors:
                    sailor.side = self.get_side()

            for sailor in self.sailors:
                sailor.move(step_x, step_y)

        scr.blit(self.image, rect)

    def sail(self):
        """
        sets status of boat to sailing
        """
        if not self.sailing and len(self.sailors):
            self.sailing = True

    def get_seat_position(self, seat):
        """
        returns free position on a boat
        """
        x, y = self.rect.topleft
        return (self.seats[seat][0] + x, self.seats[seat][1] + y)

    def get_side(self):
        """
        return on which side is a boat located
        """
        return 1 if self.last_position == self.ENDING_POINT else -1
