from __future__ import annotations #python 3.7
from abc import ABC, abstractmethod

class Context:

    _state = None

    def __init__(self, initial_state: State):
        self._state = initial_state
        self._state.context = self
    
    def run(self):
        while self._state is not None:
            self._state.run()

    def set_state(self, state: State):
        self._state = state
        self._state.context = self #the self reference is necessary because sometimes the state wants to change the context state.


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