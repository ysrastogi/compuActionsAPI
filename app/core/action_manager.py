from typing import List
from datetime import datetime

from core.constants import ActionType, ToolType, Screenshot

class Action:
    def __init__(self, action_type: ActionType, action_name:str, **params):
        self.type = action_type
        self.name = action_name
        self.params = params
        self.timestamp = datetime.now()

    def to_dict(self) -> dict:
        return{
            "type": self.type.value,
            "action":self.name,
            "parameters":self.params,
            "timestamp": self.timestamp
        }
    
class ActionSequence:
    def __init__(self, tool_id: str):
        self.sequence_id = f"seq_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.tool_id = tool_id
        self.actions: List[Action] = []
        self.screenshots: List[Screenshot] = []

    def add_action(self, action: Action):
        self.actions.append(action)

    def add_screenshot(self, screenshot: Screenshot):
        self.screenshots.append(screenshot)

    def to_dict(self) -> dict:
        return {
            "sequence_id": self.sequence_id,
            "tool_id": self.tool_id,
            "actions": [action.to_dict() for action in self.actions],
            "screenshots": [
                {
                    "id": ss.id,
                    "timestamp": ss.timestamp.isoformat(),
                    "format": ss.format,
                    "data": ss.data
                } for ss in self.screenshots
            ]
        }