from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from core.constants import ToolType
from core.action_manager import Action, ActionSequence

class BaseTool(ABC):
    def __init__(self, tool_id: str, tool_type: ToolType):
        self.tool_id = tool_id
        self.tool_type = tool_type
        self.current_sequence: Optional[ActionSequence] = None

    @abstractmethod
    def execute(self, action: Action) -> bool:
        pass

    def start_sequence(self):
        self.current_sequence = ActionSequence(self.tool_id)

    def end_sequence(self) -> Dict:
        if self.current_sequence:
            sequence_data = self.current_sequence.to_dict()
            self.current_sequence = None
            return sequence_data
        return {}