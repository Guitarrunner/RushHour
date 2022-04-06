# Car Class
import pygame
carTags = {'X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K'}
truckTags = {'O', 'P', 'Q', 'R'}

class Cars(object):

    def __init__(self, id, x, y, orientation,algorithm):

        if id in carTags:
            self.id = id
            self.length = 2
        elif id in truckTags:
            self.id = id
            self.length = 3
        else:
            raise ValueError('Invalid id {0}'.format(id))

        if 0 <= x <= 5:
            self.x = x
        else:
            raise ValueError('Invalid x {0}'.format(x))

        if 0 <= y <= 5:
            self.y = y
        else:
            raise ValueError('Invalid y {0}'.format(y))

        if self.id == "X":
            self.img = "./img/x.png"
        elif self.id == "A":
            self.img = "./img/a.png"
        elif self.id == "B":
            self.img = "./img/b.png"
        elif self.id == "C":
            self.img = "./img/c.png"
        elif self.id == "D":
            self.img = "./img/d.png"
        elif self.id == "E":
            self.img = "./img/e.png"
        elif self.id == "F":
            self.img = "./img/f.png"
        elif self.id == "G":
            self.img = "./img/g.png"
        elif self.id == "H":
            self.img = "./img/h.png"
        elif self.id == "I":
            self.img = "./img/i.png"
        elif self.id == "J":
            self.img = "./img/j.png"
        elif self.id == "K":
            self.img = "./img/k.png"
        elif self.id == "O":
            self.img = "./img/o.png"
        elif self.id == "P":
            self.img = "./img/p.png"
        elif self.id == "Q":
            self.img = "./img/q.png"
        elif self.id == "R":
            self.img = "./img/r.png"

        if orientation == 'H':
            self.orientation = orientation
            x_end = self.x + (self.length - 1)
            y_end = self.y
        elif orientation == 'V':
            self.orientation = orientation
            x_end = self.x
            y_end = self.y + (self.length - 1)
        else:
            raise ValueError('Invalid orientation {0}'.format(orientation))

        if x_end > 5 or y_end > 5:
            raise ValueError('Invalid configuration')
        
        if not algorithm:
            self.image = pygame.image.load(self.img)
            self.image = pygame.transform.scale(self.image, (self.length * 100, 100))
            if self.orientation == 'V':
                self.image = pygame.transform.rotate(self.image, 90)

    #Comparing functions

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "Vehicle({0}, {1}, {2}, {3})".format(self.id, self.x, self.y,
                                                    self.orientation)
    
    