import pygame as pg
from engine.colors import BLACK
from engine.config import WND_SIZE, FPS, SIZE, ROWS, COLS
from engine.shapes import RectangleShape
from engine.tilemap import MAP_SCHEME
from engine.groups import DeathWall
from engine.player import Snake
from engine.bonuses import Apple
from engine.text import Text, FNT_SIZE
from engine.enumerations import MousePressed
from engine.gui import Button
from engine.tools import SaveLoad
from paths import FONT, SCORE, FOOD_MUS, OVER_MUS


pg.init()
TITLE: str = 'Snake'
pg.display.set_caption(TITLE)



def make_wall(wall: DeathWall) -> None:
    sizes: tuple[int, int] = SIZE, SIZE
    for row_index, row in enumerate(MAP_SCHEME):
        for col_index, col in enumerate(row):
            if col == 'B':
                pos: tuple[int, int] = row_index * SIZE, col_index * SIZE
                rect: RectangleShape = RectangleShape(sizes, pos)
                wall.group.append(rect)


class Game:
    def __init__(self) -> None:

        # Common game objects

        self.wnd: pg.Surface = pg.display.set_mode(WND_SIZE, pg.HWSURFACE)
        self.clock: pg.time.Clock = pg.time.Clock()
        self.running: bool = True
        self.started: bool = False

        # Game loop objects

        self.snake: Snake = Snake(FONT)
        self.apple: Apple = Apple(FOOD_MUS)
        self.wall_group: DeathWall = DeathWall()
        make_wall(self.wall_group)

        # Game over objects

        text_over: str = 'Game over'
        fnt_size1: int = FNT_SIZE * 3
        fnt_size2: int = FNT_SIZE * 2
        pos_over: tuple[int, int] = int(SIZE * COLS * .12), int(SIZE * ROWS * .3)
        self.txt_over: Text = Text(text_over, FONT, pos_over, fnt_size1, fill_color=None)
        button1_text: str = 'Try again?'
        button1_pos: tuple[int, int] = SIZE * 7, pos_over[1] + SIZE * 6
        self.button_try: Button = Button(button1_text, FONT, button1_pos, fnt_size2)
        button2_text: str = 'Quit'
        button2_pos: tuple[int, int] = button1_pos[0] + SIZE * 4, button1_pos[1] + SIZE * 5
        self.button_quit: Button = Button(button2_text, FONT, button2_pos, fnt_size2)
        self.over_mus: pg.mixer.Sound = pg.mixer.Sound(OVER_MUS)
        self.mus_played: bool = False

        # Game start objects

        button3_text: str = 'Start'
        button3_pos: tuple[int, int] = SIZE * 11, WND_SIZE[1] - SIZE * 12
        self.button_start: Button = Button(button3_text, FONT, button3_pos, fnt_size2)
        best_score: str = SaveLoad.load(SCORE)
        self.best_score: int = int(best_score)
        self.score_rewritten: bool = False
        text_score: str = f'Best score: {best_score}'
        pos_score: tuple[int, int] = SIZE * 4, button3_pos[1] + SIZE * 5
        self.txt_score: Text = Text(text_score, FONT, pos_score, fnt_size2, fill_color=None)
        pos_title: tuple[int, int] = SIZE * 9, SIZE * 7
        self.txt_title: Text = Text(TITLE, FONT, pos_title, fnt_size1, fill_color=None)

    def rewrite_score(self) -> None:
        if self.snake.apples > self.best_score and not self.score_rewritten:
            SaveLoad.save(SCORE, self.snake.apples)
            self.score_rewritten = True

    def play_death_sound(self) -> None:
        if not self.mus_played:
            self.over_mus.play()
            self.mus_played = True

    def death_loop(self) -> None:
        self.rewrite_score()
        self.play_death_sound()
        self.txt_over.draw(self.wnd)
        self.button_try.draw(self.wnd)
        self.button_try.update()
        self.button_quit.draw(self.wnd)
        self.button_quit.update()
        if self.button_try.mouse == MousePressed.LEFT:
            self.snake.respawn()
        elif self.button_quit.mouse == MousePressed.LEFT:
            self.running = False

    def live_loop(self) -> None:
        self.wall_group.update(self.wnd, self.snake)
        self.snake.draw(self.wnd)
        self.apple.draw(self.wnd)
        self.score_rewritten = False
        self.mus_played = False
        if self.started:
            self.snake.update()
            self.apple.interact(self.snake)
            self.apple.respawn()
        else:
            self.txt_title.draw(self.wnd)
            self.button_start.draw(self.wnd)
            self.txt_score.draw(self.wnd)
            self.button_start.update()
            if self.button_start.mouse == MousePressed.LEFT:
                self.started = True

    def game_loop(self) -> None:
        self.wnd.fill(BLACK)
        if self.snake.alive:
            self.live_loop()
        else:
            self.death_loop()
        pg.display.flip()

    def main(self) -> None:
        while self.running:
            self.game_loop()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                elif not self.running:
                    pg.quit()
                    break
                else:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            self.running = False
                            pg.quit()


if __name__ == '__main__':
    game: Game = Game()
    game.main()
