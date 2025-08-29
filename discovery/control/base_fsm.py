from __future__ import annotations #python 3.7
from typing import Optional
from abc import ABC, abstractmethod

class Context:

    _state: Optional[State] = None

    def __init__(self, initial_state: State):
        self._state = initial_state
        self._state.context = self
    
    def start(self):
        while self._state is not None:
            self._state.run()

    def set_state(self, state: State):
        self._state = state
        self._state.context = self 


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context
    
    @context.setter
    def context(self, context) -> None:
        self._context = context

    @abstractmethod
    def run(self):
        pass