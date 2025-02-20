import webbrowser
from enum import Enum
from dataclasses import dataclass
from typing import NamedTuple, cast
from itertools import product
from random import choice

import pygame as pg
from rich.text import Text
from rich.segment import Segment
from rich.style import Style
from textual import on
from textual.binding import Binding
from textual.events import DescendantFocus
from textual.message import Message
from textual.app import App, ComposeResult
from textual.strip import Strip
from textual.widgets import Button, Static, Select, Digits, Label
from textual.containers import Center, Widget, Grid, VerticalScroll
from textual.screen import Screen, ModalScreen

SPACE_ASCII = """\
  
  
  
  
  
  
  
"""
A_ASCII = """\
██████████
██      ██
██      ██
██████████
██      ██
██      ██
██      ██
"""
B_ASCII = """\
████████  
██    ██  
██    ██  
██████████
██      ██
██      ██
██████████
"""
C_ASCII = """\
██████████
██      ██
██      
██
██        
██      ██  
██████████
"""
D_ASCII = """\
████████  
██     ██ 
██      ██
██      ██
██      ██
██     ██ 
████████  
"""
E_ASCII = """\
██████████
██        
██        
██████████
██        
██        
██████████
"""
F_ASCII = """\
██████████
██        
██        
██████████
██        
██        
██
"""
G_ASCII = """\
██████████
██      ██
██
██    ████
██      ██
██      ██
██████████
"""
H_ASCII = """\
██      ██
██      ██
██      ██
██████████
██      ██
██      ██
██      ██
"""
I_ASCII = """\
██████████
    ██    
    ██
    ██
    ██
    ██
██████████
"""
J_ASCII = """\
██████████
        ██
        ██
        ██
██      ██
██      ██
██████████
"""
K_ASCII = """\
██      ██
██     ██ 
██   ██   
██████    
██   ██   
██     ██ 
██      ██
"""
L_ASCII = """\
██
██
██
██
██
██
██████████
"""
M_ASCII = """\
████    ████
██ ██  ██ ██
██  ████  ██
██   ██   ██
██        ██
██        ██
██        ██
"""
N_ASCII = """\
██████████
██      ██
██      ██
██      ██
██      ██
██      ██
██      ██
"""
O_ASCII = """\
██████████
██      ██
██      ██
██      ██
██      ██
██      ██
██████████
"""
P_ASCII = """\
██████████
██      ██
██      ██
██████████
██        
██        
██        
"""
Q_ASCII = """\
"""
R_ASCII = """\
██████████
██      ██
██      ██
██████████
██  ██    
██    ██  
██      ██
"""
S_ASCII = """\
 ████████ 
██      ██
  ██      
    ██    
      ██  
██      ██
 ████████ 
"""
T_ASCII = """\
"""
U_ASCII = """\
██      ██
██      ██
██      ██
██      ██
██      ██
██      ██
██████████
"""
V_ASCII = """\
██      ██
██      ██
██      ██
██      ██
 ██    ██ 
  ██  ██  
   ████  
"""
W_ASCII = """\
"""
X_ASCII = """\
"""
Y_ASCII = """\
"""
Z_ASCII = """\
"""

WALL_HIT_WAV = "src/audio/wall_hit.wav"
TAIL_BITE_WAV = "src/audio/tail_bite.wav"
CORN_BITE_WAV = "src/audio/corn_bite.wav"


class SingleMode(Enum):
    SINGLE = 0
    LOCAL = 1
    LAN = 2


class Coord2D(NamedTuple):
    x: int
    y: int


@dataclass(frozen=True)
class BoardSizeData:
    name_str: str
    width: int
    height: int


class BoardSize(BoardSizeData, Enum):
    SMALL = "Small", 30, 20
    MEDIUM = "Medium", 60, 40
    BIG = "Big", 90, 60


@dataclass(frozen=True)
class SnakeSpeedData:
    name_str: str
    speed: float


class SnakeSpeed(SnakeSpeedData, Enum):
    SLOW = "Slow", 0.08
    NORMAL = "Normal", 0.05
    FAST = "Fast", 0.03
    TEXTUALIZE = "Textualize™", 0.01


class SnakeHeadRotation(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


@dataclass
class SnakeHead:
    last_rotation: SnakeHeadRotation
    current_rotation: SnakeHeadRotation
    coords: Coord2D | None = None


@dataclass(frozen=True)
class SnakeColorsDt:
    name_str: str
    bg: Style
    fg: Style


class SnakeColor(SnakeColorsDt, Enum):
    ORANGE = "Orange", Style.parse("on #f54900"), Style.parse("#f54900")
    AMBER = "Amber", Style.parse("on #e07000"), Style.parse("#e07000")
    YELLOW = "Yellow", Style.parse("on #d08600"), Style.parse("#d08600")
    LIME = "Lime", Style.parse("on #5ea400"), Style.parse("#5ea400")
    GREEN = "Green", Style.parse("on #00a53e"), Style.parse("#00a53e")
    TEAL = "Teal", Style.parse("on #009688"), Style.parse("#009688")
    CYAN = "Cyan", Style.parse("on #0092b8"), Style.parse("#0092b8")
    SKY = "Sky", Style.parse("on #0083d1"), Style.parse("#0083d1")
    BLUE = "Teal", Style.parse("on #145dfc"), Style.parse("#145dfc")
    INDIGO = "Indigo", Style.parse("on #4f38f6"), Style.parse("#4f38f6")
    VIOLET = "Violet", Style.parse("on #7f21fe"), Style.parse("#7f21fe")
    PURPLE = "Purple", Style.parse("on #980ffa"), Style.parse("#980ffa")
    FUCHSIA = "Fuchsia", Style.parse("on #c700de"), Style.parse("#c700de")
    PINK = "Pink", Style.parse("on #e50075"), Style.parse("#e50075")
    ROSE = "Rose", Style.parse("on #eb003f"), Style.parse("#eb003f")
    SLATE = "Slate", Style.parse("on #44546c"), Style.parse("#44546c")
    GRAY = "Gray", Style.parse("on #4a5464"), Style.parse("#4a5464")
    ZINC = "Zinc", Style.parse("on #51515c"), Style.parse("#51515c")
    NEUTRAL = "Neutral", Style.parse("on #515151"), Style.parse("#515151")
    STONE = "Stone", Style.parse("on #56524d"), Style.parse("#56524d")
    WHITE = "White", Style.parse("on #FFFFFF"), Style.parse("#FFFFFF")



class BoardObjectType(Enum):
    NULL = 0
    WALL = 1
    BODY = 3
    FOOD = 4


@dataclass
class BoardObject:
    type: BoardObjectType
    style: Style | None = None


class GameState2:
    def __init__(self, width: int, height: int, snake_speed: float, snake_color: SnakeColor):
        self.width = width
        self.height = height
        self.snake_speed = snake_speed
        self.null_object = BoardObject(BoardObjectType.NULL)
        self.body_object = BoardObject(BoardObjectType.BODY, snake_color.bg)
        self.food_object = BoardObject(BoardObjectType.FOOD, Style.parse("on #2f6620"))
        self.wall_object = BoardObject(BoardObjectType.WALL, Style.parse("on #330000"))
        self.game_board = self.generate_game_board()
        self.snake_body: list[Coord2D] = []
        self.snake_head = SnakeHead(
            last_rotation=SnakeHeadRotation.RIGHT,
            current_rotation=SnakeHeadRotation.RIGHT,
        )
        self.not_occupied = {
            Coord2D(x, y) for x, y in product(range(self.width), range(self.height))
        }
        self.points: int = 0

        # Init game
        self.turn_cells_into_walls()
        self.turn_cells_into_snake()
        self.turn_cell_into_food()

    def generate_game_board(self) -> list[list[BoardObject]]:
        return [
            [self.null_object for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def turn_cells_into_walls(self) -> None:
        for x, y in product(range(self.width), range(1)):
            self.game_board[y][x] = self.wall_object
            self.not_occupied.remove(Coord2D(x, y))
        for x, y in product(range(self.width), range(self.height - 1, self.height)):
            self.game_board[y][x] = self.wall_object
            self.not_occupied.remove(Coord2D(x, y))
        for x, y in product(range(1), range(1, self.height - 1)):
            self.game_board[y][x] = self.wall_object
            self.not_occupied.remove(Coord2D(x, y))
        for x, y in product(range(self.width - 1, self.width), range(1, self.height - 1)):
            self.game_board[y][x] = self.wall_object
            self.not_occupied.remove(Coord2D(x, y))

    def turn_cells_into_snake(self) -> None:
        for i in range(3):
            c = Coord2D(self.width // 2 - i, self.height // 2)
            self.game_board[c.y][c.x] = self.body_object
            self.not_occupied.remove(c)
            self.snake_body.append(c)

    def turn_cell_into_food(self) -> None:
        cell: Coord2D = choice(tuple(self.not_occupied))
        self.game_board[cell.y][cell.x] = self.food_object


class FoodEaten(Message):
    pass


class PauseScreen(ModalScreen):
    BINDINGS = [Binding("space", "resume", show=False)]

    def action_resume(self):
        self.dismiss()

    def __init__(self, game_loop, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.game_loop = game_loop
        self.styles.height = "100%"
        self.styles.width = "100%"

    def compose(self) -> ComposeResult:
        with Static(id="Wrapper"):
            yield Static(P_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(A_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(U_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(S_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(E_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(D_ASCII)


class SnakeBoard(Widget, can_focus=True):
    BINDINGS = [
        # WASD Controls
        Binding("w", "head_up", show=False),
        Binding("s", "head_down", show=False),
        Binding("a", "head_left", show=False),
        Binding("d", "head_right", show=False),

        # Arrow Key Controls
        Binding("up", "head_up", show=False),
        Binding("down", "head_down", show=False),
        Binding("left", "head_left", show=False),
        Binding("right", "head_right", show=False),

        # Vim-style (hjkl) Controls
        Binding("k", "head_up", show=False),
        Binding("j", "head_down", show=False),
        Binding("h", "head_left", show=False),
        Binding("l", "head_right", show=False),

        # Game settings
        Binding("space", "stop_game", show=False),
        Binding("enter", "new_game", show=False),
        Binding("escape", "main_menu", show=False),
    ]

    def action_head_up(self) -> None:
        if self.gs.snake_head.last_rotation != SnakeHeadRotation.DOWN:
            self.gs.snake_head.current_rotation = SnakeHeadRotation.UP

    def action_head_down(self) -> None:
        if self.gs.snake_head.last_rotation != SnakeHeadRotation.UP:
            self.gs.snake_head.current_rotation = SnakeHeadRotation.DOWN

    def action_head_left(self) -> None:
        if self.gs.snake_head.last_rotation != SnakeHeadRotation.RIGHT:
            self.gs.snake_head.current_rotation = SnakeHeadRotation.LEFT

    def action_head_right(self) -> None:
        if self.gs.snake_head.last_rotation != SnakeHeadRotation.LEFT:
            self.gs.snake_head.current_rotation = SnakeHeadRotation.RIGHT

    def action_stop_game(self) -> None:
        self.game_loop.pause()
        self.app.push_screen(
            PauseScreen(self.game_loop),
            lambda x: self.game_loop.resume()
        )

    async def action_new_game(self) -> None:
        if not self.game_loop_active:
            await cast(GamePlayScreen, self.screen).new_game()

    def action_main_menu(self) -> None:
        if not self.game_loop_active:
            self.screen.dismiss()

    def __init__(self, game_state: GameState2, snake_color: SnakeColor, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.gs = game_state
        self.styles.width = self.gs.width * 2
        self.styles.height = self.gs.height
        self.snake_color = snake_color

        self.game_loop_active = True
        self.game_loop = self.set_interval(self.gs.snake_speed, self.move_snake)
        self.controller_support = self.set_interval(self.gs.snake_speed, self.pg_controller)

    def render_line(self, y: int) -> Strip:
        segments = []

        if y >= self.gs.game_board.__len__():
            return Strip.blank(self.gs.height)

        for segment in self.gs.game_board[y]:
            segments.append(Segment("  ", segment.style))
        return Strip(segments, cell_length=2)

    def move_snake(self):
        snake_head = self.gs.snake_body[0]
        snake_head_rotation = self.gs.snake_head

        if snake_head_rotation.current_rotation == SnakeHeadRotation.UP:
            new_head = Coord2D(snake_head.x, snake_head.y - 1)
        elif snake_head_rotation.current_rotation == SnakeHeadRotation.DOWN:
            new_head = Coord2D(snake_head.x, snake_head.y + 1)
        elif snake_head_rotation.current_rotation == SnakeHeadRotation.LEFT:
            new_head = Coord2D(snake_head.x - 1, snake_head.y)
        else:
            new_head = Coord2D(snake_head.x + 1, snake_head.y)

        if self.gs.game_board[new_head.y][new_head.x].type \
                in [BoardObjectType.WALL, BoardObjectType.BODY]:
            self.game_loop.stop()
            self.game_loop_active = False
            if self.gs.game_board[new_head.y][new_head.x].type == BoardObjectType.WALL:
                pg.mixer.Sound(WALL_HIT_WAV).play()
            else:
                pg.mixer.Sound(TAIL_BITE_WAV).play()
        else:
            self.gs.not_occupied.remove(new_head)

        tail = self.gs.snake_body[-1]

        for i, snake_part in enumerate(self.gs.snake_body[:-1], 1):
            self.gs.snake_body[i] = snake_part
        self.gs.snake_body[0] = new_head

        if self.gs.game_board[new_head.y][new_head.x].type != BoardObjectType.FOOD:
            self.gs.game_board[tail.y][tail.x] = self.gs.null_object
            self.gs.not_occupied.add(tail)
        else:
            self.gs.snake_body.append(tail)
            self.gs.turn_cell_into_food()
            self.gs.points += 1
            self.post_message(FoodEaten())
            pg.mixer.Sound(CORN_BITE_WAV).play()

        self.gs.game_board[new_head.y][new_head.x] = self.gs.body_object
        self.gs.snake_head.coords = new_head

        snake_head_rotation.last_rotation = snake_head_rotation.current_rotation
        self.refresh()

    def pg_controller(self) -> None:
        for event in pg.event.get(pg.JOYBUTTONDOWN):
            if event.button == 12:
                self.action_head_down()
            elif event.button == 13:
                self.action_head_left()
            elif event.button == 11:
                self.action_head_up()
            elif event.button == 14:
                self.action_head_right()


class GameStats(Static):
    def __init__(self, game_state: GameState2, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.game_state = game_state
        self.styles.width = self.game_state.width * 2
        self.points = Digits(str(self.game_state.points))

    def compose(self) -> ComposeResult:
        yield Static("")
        yield self.points
        yield Static("")

    def update_points(self):
        self.points.update(str(self.game_state.points))


class GamePlayScreen(Screen):
    def __init__(
        self,
        board_size: BoardSize,
        snake_speed: SnakeSpeed,
        snake_color: SnakeColor,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.board_size = board_size
        self.snake_speed = snake_speed
        self.snake_color = snake_color

        self.game_state = GameState2(
            width=board_size.width,
            height=board_size.height,
            snake_speed=snake_speed.speed,
            snake_color=snake_color,
        )

    def compose(self) -> ComposeResult:
        yield GameStats(self.game_state)
        yield SnakeBoard(self.game_state, self.snake_color)

    def on_food_eaten(self):
        self.query_one(GameStats).update_points()

    async def new_game(self) -> None:
        self.game_state = GameState2(
            width=self.board_size.width,
            height=self.board_size.height,
            snake_speed=self.snake_speed.speed,
            snake_color=self.snake_color
        )
        await self.recompose()
        self.query_one(SnakeBoard).focus()


class SingleGameSettingsScreen(Screen):
    """Screen that allows user to choose game specs."""
    BINDINGS = [
        Binding("escape", "exit_screen"),
    ]

    SELECT_BOARD = Select(
        ((size.name_str, size) for size in BoardSize),
        value=BoardSize.MEDIUM,
        allow_blank=False,
        id="Board"
    )
    SELECT_SPEED = Select(
        ((speed.name_str, speed) for speed in SnakeSpeed),
        value=SnakeSpeed.NORMAL,
        allow_blank=False,
        id="Speed"
    )

    SELECT_SNAKE_COLOR = Select(
        ((Text(color.name_str, style=color.fg), color) for color in SnakeColor),
        value=SnakeColor.WHITE,
        allow_blank=False,
        id="Color"
    )

    def action_exit_screen(self) -> None:
        self.dismiss()

    def compose(self) -> ComposeResult:
        with Static(id="Wrapper"):
            with Center():
                yield Static("Gameplay Settings", id="Title")
            with Grid(id="Grid"):
                yield Label("Board Size")
                yield self.SELECT_BOARD
                yield Label("Snake Speed")
                yield self.SELECT_SPEED
                yield Label("Snake Color")
                yield self.SELECT_SNAKE_COLOR
            with Center():
                yield Button("Play", variant="success")

    @on(Button.Pressed)
    def play_button(self) -> None:
        self.app.push_screen(GamePlayScreen(
            board_size=self.SELECT_BOARD.value,
            snake_speed=self.SELECT_SPEED.value,
            snake_color=self.SELECT_SNAKE_COLOR.value,
        ))


class AboutSettings(Static):
    def compose(self) -> ComposeResult:
        yield Static("Check out our media!")
        with Grid():
            yield Button("Discord", id="discord")
            yield Button("Github", id="github")
            yield Button("X", id="x")

    @on(Button.Pressed, "#discord")
    def discord_pressed(self) -> None:
        webbrowser.open("https://discord.gg/JF44rr67Ng")

    @on(Button.Pressed, "#github")
    def github_pressed(self) -> None:
        webbrowser.open("")

    @on(Button.Pressed, "#x")
    def x_pressed(self) -> None:
        webbrowser.open("https://x.com/zimzozaur")


class LocalGameSettingsScreen(Screen):
    pass


class LanGameSettingsScreen(Screen):
    pass


class GameSettingsScreen(Screen):
    BINDINGS = [
        Binding("escape", "exit_screen"),
    ]

    def action_exit_screen(self) -> None:
        self.dismiss()

    def __init__(self) -> None:
        super().__init__()
        self.sound_settings_border = Static(classes="Section_Wrapper")
        self.sound_settings_border.border_title = "Sound"

        self.about = Static(classes="Section_Wrapper")
        self.about.border_title = "About"

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            with Static(id="Body"):
                with self.about:
                    yield AboutSettings()


class GameModeScreen(Screen):
    app: "SnakeApp"
    BINDINGS = [Binding("t", "title_screen")]

    def action_title_screen(self):
        self.app.title_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "Single":
            self.app.push_screen(SingleGameSettingsScreen())
        elif event.button.id == "Multi":
            self.notify("Not implemented")
        elif event.button.id == "LAN":
            self.notify("Not implemented")
        elif event.button.id == "Settings":
            self.app.push_screen(GameSettingsScreen())

    @on(DescendantFocus, "Button")
    def change_variant(self, event: DescendantFocus):
        bts = self.query(Button)
        for bt in bts:
            bt.variant = "default"
        event.widget.variant = "primary"

    def compose(self) -> ComposeResult:
        with Static(id="Wrapper"):
            with Center():
                yield Static("Game Modes", id="Title")
            with Center():
                yield Button("Single Player", id="Single")
            with Center():
                yield Button("Local Multiplayer", id="Multi")
            with Center():
                yield Button("LAN Party", id="LAN")
            with Center():
                yield Button("Settings", id="Settings")


class TitleScreen(Screen):
    def compose(self) -> ComposeResult:
        with Center():
            yield Static(S_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(N_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(A_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(K_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(E_ASCII)
        with Center():
            yield Static(G_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(A_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(M_ASCII)
            yield Static(SPACE_ASCII)
            yield Static(E_ASCII)
        with Center(id="Author"):
            yield Static("Developed by Simon Piechutowski")


class SnakeApp(App):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = ["styles/snake.tcss"]

    def __init__(self, *args, borders=False, debugging=False, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        pg.init()
        pg.mixer.init()
        pg.joystick.init()
        self.joysticks: list[pg.joystick.JoystickType] = []

        for event in pg.event.get():
            if event.type == pg.JOYDEVICEADDED:
                self.joysticks.append(pg.joystick.Joystick(event.device_index))

        # Debugging
        self.debugging = debugging
        self.borders = borders
        if self.borders:
            with open("styles/borders.tcss") as f:
                self.stylesheet.add_source("".join(f.readlines()))

    def on_mount(self):
        self.push_screen(TitleScreen())
        self.set_timer(
            0.01 if self.debugging else 2,
            lambda: self.switch_screen(GameModeScreen()),
        )

    def title_screen(self):
        self.push_screen(TitleScreen())
        self.set_timer(2, lambda: self.pop_screen())


if __name__ == "__main__":
    SnakeApp(borders=False, debugging=True).run()
