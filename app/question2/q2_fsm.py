from typing import List, Dict, Any
from pydantic import BaseModel

class StateTransitions(BaseModel):
    "Pydantic model for State Transitions"
    trigger: str
    source: str
    destination: str

class State:
    """
    A class to represent a state in a finite state machine (FSM).

    Attributes:
    name (str): The name of the state.
    transitions (dict): A dictionary mapping input symbols to next states.

    Methods:
    get_next_state(self, input_symbol: str) -> Any:

    """
    def __init__(self, name: str) -> None:
        """
        Initialize the state with a name

        Parameters:
        name (str): The name of the state.
        """
        self.name = name.upper()
        self.transitions = {}

    def get_next_state(self, input_symbol: str) -> Any:
        """
        Retrieve the next state based on the input symbol.

        Parameters:
        input_symbol (str): The input symbol to check for the next state transition.

        Returns:
        State: The next state corresponding to the input symbol, or None if no transition exists.
        """
        if input_symbol.upper() in self.transitions:
            return self.transitions.get(input_symbol.upper())
        else:
            raise Exception("State name does not exist in transition dictionary")

class FSM():
    """
    A class to represent a finite state machine (FSM).

    Attributes:
    states (dict): A dictionary mapping state names to State objects.
    start_state (State): The starting state of the FSM.
    current_state (State): The current state of the FSM.

    Methods:
    add_transition(self, transitions: List[StateTransitions]) -> None:
    set_start_state(self, state_name: str) -> None:
    reset(self) -> None:
    process_input(self, input_string: str) -> None:
    get_current_state(self) -> str:
    _check_transition_dict(self, state_name: str) -> None:
    """

    def __init__(self, stateNames: List[str]) -> None:
        """
        Initialize the FSM with a list of state names.

        Parameters:
        stateNames (List[str]): A list of state names to initialize the FSM with.
        """

        if not isinstance(stateNames, List):
            raise Exception("Incorrect data type for stateNames parameter") 

        self.states = {}
        for single_state in stateNames:
            if not isinstance(single_state, str):
                raise Exception("Incorrect data type for stateNames List values. Should be str") 

            self.states[single_state] = State(name=single_state)
            
        self.start_state = None
        self.current_state = None

    def add_transition(self, transitions: List[StateTransitions]) -> None:
        """
        Add transitions to the FSM.

        Parameters:
        transitions (List[StateTransitions]): A list of StateTransitions to add to the FSM.

        Return:
        None
        """
        for single_transition in transitions:
            if not isinstance(single_transition, StateTransitions):
                raise Exception("Incorrect data type for transitions List values. Should be StateTransitions pydantic model") 

            state_cls: State = self.states[single_transition.source.upper()]
            state_cls.transitions[single_transition.trigger.upper()] = self.states[single_transition.destination.upper()]

    def set_start_state(self, state_name: str) -> None:
        """
        Set the starting state of the FSM.

        Parameters:
        state_name (str): The name of the state to set as the start state.

        Return:
        None
        """
        if state_name.upper() in self.states:
            self.start_state = self.states.get(state_name.upper())
            self.current_state = self.start_state
        else:
            raise Exception("State name does not exist in states dictionary")

    def reset(self) -> None:
        """
        Reset the FSM to the starting state.
        """
        self.current_state = self.start_state

    def process_input(self, input_string: str) -> None:
        """
        Process an input string through the FSM.

        Parameters:
        input_string (str): The input string to process.

        Return:
        None
        """
        self.reset()
        for symbol in input_string:
            self.current_state = self.current_state.get_next_state(symbol)

    def get_current_state(self) -> str:
        """
        Get the name of the current state.

        Returns:
        str: The name of the current state, or None if no current state is set.
        """
        return self.current_state.name if self.current_state else None
    
    def _check_transition_dict(self, state_name: str) -> None:
        """
        Print the transitions dictionary for a given state.

        Parameters:
        state_name (str): The name of the state to check transitions for.

        Return:
        None
        """
        state_cls: State = self.states[state_name.upper()]
        print(f"state class is: {state_cls.name}")
        print(state_cls.transitions)

