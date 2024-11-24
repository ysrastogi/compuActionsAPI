from core.tools.base import BaseTool
from core.action_manager import Action
from core.constants import ToolType, ActionType, Coordinates, Region, Screenshot

from datetime import datetime
from mss import mss
from typing import Optional
import logging

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController

mouse = MouseController()
keyboard = KeyboardController()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_screen_dimensions():
    with mss() as sct:
        monitor = sct.monitors[1]
        return monitor['width'], monitor['height']
    

def get_ai_scaled_screen_dimensions():
    widht, height = get_screen_dimensions()
    aspect_ratio = widht/height

    if aspect_ratio > 1280/800:
        scaled_width = 1280
        scaled_height = round(1280/aspect_ratio)

    else:
        scaled_height = 800
        scaled_width = round(800*aspect_ratio)
    
    return scaled_width, scaled_height



class ComputerTool(BaseTool):
    def __init__(self):
        super().__init__("computer_20241022", ToolType.COMPUTER)

    def execute(self, action: Action) -> bool:
        try:
            if action.type == ActionType.MOUSE:
                return self._handle_mouse_action(action)
            elif action.type == ActionType.KEYBOARD:
                return self._handle_keyboard_action(action)
            elif action.type == ActionType.SYSTEM:
                return self._handle_system_action(action)
            return False
        except Exception as e:
            logger.error(f"Error executing action: {str(e)}")
            return False
        
    def _map_to_ai_space(x,y):
        widht, height = get_screen_dimensions()
        scaled_width, scaled_height = get_ai_scaled_screen_dimensions()
        return (x*scaled_width)/widht, (y*scaled_height)/height

    def _map_from_ai_space(x,y):
        width, height = get_screen_dimensions()
        scaled_width, scaled_height = get_ai_scaled_screen_dimensions()
        return (x*width)/scaled_width, (y*height)/scaled_height

    def _handle_mouse_action(self, action: Action) -> bool:
        if action.name == "left_button_press":
            return self._left_click()
        elif action.name == "right_button_press":
            return self._right_click()
        elif action.name == "double_left_button_press":
            return self._double_click()
        elif action.name == "mouse_move":
            return self._mouse_move(Action.get("coordinates"))
        elif action.name =="left_click_drag":
            return self._left_click_drag(Action.get("coordinates"))
        # Add other mouse actions
        return False

    def _handle_keyboard_action(self, action: Action) -> bool:
        if action.name == "type_text":
            return self._type_text(action.params.get("text", ""))
        if action.name == "key_combination":
            return self._
        return False

    def _handle_system_action(self, action: Action) -> bool:
        if action.name == "screenshot":
            screenshot = self._take_screenshot(action.params.get("region"))
            if screenshot and self.current_sequence:
                self.current_sequence.add_screenshot(screenshot)
            return bool(screenshot)
        return False

    def _left_click(self, coordinates: Coordinates) -> bool:
        mouse.click(Button.left)
        logger.info(f"Clicking at coordinates: ({coordinates.x}, {coordinates.y})")
        return True
    
    def _right_click(self, coordinates: Coordinates) -> bool:
        mouse.click(Button.right)
        logger.info(f"Clicking at coordinates: ({coordinates.x}, {coordinates.y})")
        return True
    
    def _double_click(self, coordinates: Coordinates) -> bool:
        mouse.click(Button.left, 2)
        logger.info(f"Clicking at coordinates: ({coordinates.x}, {coordinates.y})")
        return True

    def _mouse_move(self, coordinates: Coordinates) -> bool:
        x,y = self._map_from_ai_space(coordinates.x, coordinates.y)
        mouse.position(x,y)
        logger.info(f"Mouse moved to {x} and {y} coordinates")
        return True
    
    def _get_mouse_position(self):
        x,y = mouse.position
        ai_x, ai_y = self._map_to_ai_space(x,y)
        return ai_x, ai_y
    
    def _left_click_drag(self, coordinates:Coordinates) -> bool:
        x_initial , y_initial = self._get_mouse_position()
        x,y = self._map_from_ai_space(coordinates.x, coordinates.y)
        mouse.press(Button.left)
        mouse.move(x,y)
        mouse.release(Button.left)
        logger.info(f"Drag from ({x_initial},{y_initial}) to ({x}, {y})")
        return True

    def _scroll(self, direction: str, amount: int) -> bool:
        # Implement scroll logic
        logger.info(f"Scrolling {direction} by {amount}")
        return True

    def _type_text(self, text: str) -> bool:
        # Implement typing logic
        logger.info(f"Typing text: {text}")
        return True
    
    def _key_combination(self, keys: list[str]) -> bool:
        #Implement key combination logic
        logger.info(f"Typing text: {text}")
        return True

    def _take_screenshot(self, region: Optional[Region] = None) -> Optional[Screenshot]:
        with mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
            scaled_width, scaled_height = get_ai_scaled_screen_dimensions()
            img = img.resize((scaled_width, scaled_height))
        try:
            # Simulate screenshot capture
            screenshot_data = img
            return Screenshot(
                id=f"shot_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                timestamp=datetime.now(),
                data=screenshot_data
            )
        except Exception as e:
            logger.error(f"Screenshot failed: {str(e)}")
            return None