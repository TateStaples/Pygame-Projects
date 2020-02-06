from random import shuffle

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (135, 206, 235)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Game:
    bg_color = LIGHT_BLUE

    def __init__(self, players):
        self.pile = Pile()
        self.sets = []
        self.hands = [Rack(self.pile) for i in range(players)]
        self.in_progress = True
        self.game_loop()

    def game_loop(self):
        while self.in_progress:
            for hand in self.hands:
                self.play_round(hand)
                if hand.get_length() == 0:  # if the player has gotten rid of all the tiles
                    self.in_progress = False
                    break

    def play_round(self, hand):
        pass

    def valid_gamestate(self):
        for set in self.sets:
            if not set.is_valid():
                return False
        return True


class Tile:
    width = None
    height = None
    bg_color = WHITE

    def __init__(self, val, color):
        self.val = val
        self.color = color

    def draw(self, x, y):
        pass


class Rack:
    start_amount = 13

    def __init__(self, pile):
        self.the_pile = pile
        self.tiles = [pile.retrieve_tile() for i in range(self.start_amount)]

    def draw(self):
        pass

    def get_tile(self):
        pass

    def get_length(self):
        return len(self.tiles)

    def score(self):
        return sum([tile.val for tile in self.tiles])


class Set:
    def __init__(self, tiles):
        self.tiles = tiles

    def is_valid(self):
        if len(self.tiles) < 2:  # must be at least 3 long
            return False
        colors = set([tile.color for tile in self.tiles])
        vals = sorted([tile.val for tile in self.tiles])
        if len(colors) != len(self.tiles) and len(colors) != 1: # must have all dif or all same color
            return False
        all_same_color = len(colors) == 1
        if len(set(vals)) == 1:  # if they share one number
            ascending = False
        elif [i for i in range(vals[0], vals[-1])] == [vals]:
            ascending = True
        else:
            return False
        return ascending == all_same_color

    def split(self, index):
        set1 = Set(self.tiles[:index])
        set2 = Set(self.tiles[index:])
        del self
        return set1, set2

    def fuse(self):
        pass

    def draw(self):
        pass

    def get_open_location(self):
        pass


class Pile:
    def __init__(self):
        self.pile = []
        for iteration in range(2):
            for val in range(1, 14):
                for color in [RED, BLUE, BLACK, YELLOW]:
                    self.pile.append(Tile(val, color))
        shuffle(self.pile)

    def retrieve_tile(self):
        return self.pile.pop()

    def draw(self):
        pass
