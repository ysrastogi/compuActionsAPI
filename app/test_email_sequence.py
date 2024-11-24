from core.tools.computer import ComputerTool
from core.action_manager import Action
from core.constants import ActionType,Coordinates

import json
from typing import Optional, Dict


def create_email_sequence():
    computer = ComputerTool()
    computer.start_sequence()

    # Create sequence of actions
    actions = [
        Action(
            ActionType.KEYBOARD
        )
        Action(
            ActionType.MOUSE,
            "left_button_press",
            coordinates=Coordinates(100, 200)
        ),
        Action(
            ActionType.KEYBOARD,
            "type_text",
            text="recipient@example.com"
        ),
        Action(
            ActionType.SYSTEM,
            "screenshot"
        )
    ]

    # Execute actions
    for action in actions:
        computer.execute(action)
        if computer.current_sequence:
            computer.current_sequence.add_action(action)

    # End sequence and get results
    sequence_data = computer.end_sequence()
    return sequence_data

# Error handling class
class ToolError(Exception):
    def __init__(self, code: str, message: str, details: Dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details
            }
        }
    

if __name__ == "__main__":
    # Example usage
    try:
        # Create and execute an email sequence
        sequence_data = create_email_sequence()
        print(json.dumps(sequence_data, indent=2))

    except ToolError as e:
        print(json.dumps(e.to_dict(), indent=2))
    except Exception as e:
        print(json.dumps({
            "error": {
                "code": "internal_error",
                "message": str(e)
            }
        }, indent=2))