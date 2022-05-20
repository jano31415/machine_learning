import arcade
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class AbaloneGame(arcade.Window):
    """Main application class."""

    def __init__(self, width, height):
        super().__init__(width, height)
        self.board_width = SCREEN_WIDTH - 100
        self.board_height = SCREEN_HEIGHT - 100
        self.empty = " "
        self.black = "B"
        self.white = "W"
        self.state = self.create_default_state()
        self.print_state()

        self.color_map = {
            self.black: arcade.color.BLACK,
            self.white: arcade.color.WHITE,
            "A": arcade.color.ALMOND,
        }

        arcade.set_background_color(arcade.color.AMAZON)
        self.active = []

    def create_default_state(self):
        state = [[" "] * x for x in [5, 6, 7, 8, 9, 8, 7, 6, 5]]
        for row in range(2):
            for j in range(len(state[row])):
                state[row][j] = self.black
        state[2][2:5] = [self.black] * 3
        for row in range(7, 9):
            for j in range(len(state[row])):
                state[row][j] = self.white
        state[6][2:5] = [self.white] * 3
        return state

    def print_state(self):
        print("\n".join([" ".join(row).rjust(9, " ") for row in self.state]))

    def draw_ball(self, x, y, color):
        radius = 20
        arcade.draw_circle_filled(x, y, radius, self.color_map[color])

    def get_draw_pos(self, rownr, colnr):
        y = 100 + rownr * (self.board_height // len(self.state))
        x = int(100 + (colnr + 0.5 * (abs(4 - rownr))) * (self.board_height // 9))
        return x, y

    def draw_state(self):
        for rownr, row in enumerate(self.state):
            for colnr, b in enumerate(row):
                x, y = self.get_draw_pos(rownr, colnr)
                arcade.draw_rectangle_outline(x, y, 50, 50, arcade.color.BLACK)
                if b != self.empty:
                    if (rownr, colnr) in self.active:
                        b = "A"
                        print(b)
                    self.draw_ball(x, y, b)
                else:
                    arcade.draw_rectangle_outline(x, y, 50, 50, arcade.color.BLACK)
                    arcade.draw_rectangle_filled(x, y, 50, 50, arcade.color.ASH_GREY)
        arcade.finish_render()

    def setup(self):
        arcade.set_background_color(arcade.color.ASH_GREY)
        arcade.start_render()
        self.draw_state()
        # arcade.draw_polygon_outline([[0, 300], [100, 0], [400, 0], [500, 300], [400, 600], [100, 600]], arcade.color.BLACK)
        # arcade.finish_render()

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        # Your drawing code goes here

    def update(self, delta_time):
        """All the logic to move, and the game logic goes here."""
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        print("mouse press")
        for rownr, row in enumerate(self.state):
            for colnr, b in enumerate(row):
                xb, yb = self.get_draw_pos(rownr, colnr)
                if abs(xb - x) + abs(yb - y) < 30:
                    rowa, cola = self.get_row_col(xb, yb)
                    print((rowa, cola))
                    if (xb, yb) in self.active:
                        self.active.remove((rowa, cola))
                    else:
                        if self.state[rowa][cola] in [self.black, self.white]:

                            if len(self.active) == 0:
                                self.active.append((rowa, cola))
                            elif len(self.active) == 1:
                                self.add_if_adjacent(rowa, cola)
                            elif len(self.active) == 2:
                                rowa1, cola1 = self.active[0]
                                rowa2, cola2 = self.active[1]

                                dir = self.get_dir(rowa1, cola1, rowa2, cola2)
                                if rowa == rowa2 + dir[0] and cola == cola2 + dir[1]:
                                    self.active.append((rowa, cola))

                        else:
                            self.move(rowa, cola)
                    self.draw_state()
                    return

    def move(self, rowa, cola):
        direction = self.get_dir(*self.active[0], rowa, cola)
        active_color = self.state[self.active[0][0]][self.active[0][1]]

        for row, col in self.active:
            self.state[row][col] = self.empty
        self.move_dir(direction, active_color)
        self.active = []

    def get_dir(self, rowold, colold, rownew, colnew):
        return ((rownew - rowold), (colnew - colold))

    def move_ball(self, rownew, colnew, color):
        self.state[rownew][colnew] = color

    def move_dir(self, direction, color):
        for row, col in self.active:
            print(direction)
            print((row, col))
            newrow = np.clip(row + direction[0], 0, 9)
            newcol = np.clip(col + direction[1], 0, 9)
            print((newrow, newcol))
            self.move_ball(newrow, newcol, color)

    def get_row_col(self, xb: int, yb: int):
        rownr = (yb - 100) // (self.board_height // len(self.state))
        colnr = round((xb - 100) / (self.board_height // 9) - abs(4 - rownr) * 0.5)
        return rownr, colnr

    def on_key_press(self, key, modifiers):
        pass

    def add_if_adjacent(self, row, col):
        rowact, colact = self.active[0]
        if abs(rowact - row) <= 1 and abs(colact - col) <= 1:
            self.active.append((row, col))


def main():
    game = AbaloneGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


def test_get_row_col():
    game = AbaloneGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    for rownr, row in enumerate(game.state):
        for colnr in range(len(row)):
            xb, yb = game.get_draw_pos(rownr, colnr)
            print(xb)
            print(yb)
            rownew, colnew = game.get_row_col(xb, yb)
            assert rownew == rownr
            assert colnew == colnr


if __name__ == "__main__":
    main()
