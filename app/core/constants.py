from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class ToolType(Enum):
    COMPUTER = "computer"
    TERMINAL = "terminal"
    EDITOR = "editor"

class ActionType(Enum):
    MOUSE = "mouse_action"
    KEYBOARD = "keyboard_action"
    SYSTEM = "system_action"

@dataclass
class Coordinates:
    x:int
    y:int

@dataclass
class Region:
    x:int
    y:int
    width:int
    height:int

@dataclass
class Screenshot:
    id:str
    timestamp:datetime
    data:str
    format:str = "png"