import pytest
from app.question2.q2_fsm import StateTransitions, FSM

# Assuming the `State` and `FSM` classes are defined in a module named `fsm_module`
# from fsm_module import State, FSM, StateTransitions

def create_mod_three_fsm():
    # Create FSM instance
    fsm = FSM(['S0', 'S1', 'S2'])

    # Add transitions
    transitions = [
        StateTransitions(trigger='0', source='S0', destination='S0'),
        StateTransitions(trigger='1', source='S0', destination='S1'),
        StateTransitions(trigger='0', source='S1', destination='S2'),
        StateTransitions(trigger='1', source='S1', destination='S0'),
        StateTransitions(trigger='0', source='S2', destination='S1'),
        StateTransitions(trigger='1', source='S2', destination='S2')
    ]
    fsm.add_transition(transitions)
    fsm.set_start_state('S0')
    
    return fsm

def test_mod_three_fsm():
    fsm = create_mod_three_fsm()

    # Test binary string "1101" which should have a remainder of 1 when divided by 3
    resp = fsm.process_input("1101")
    assert resp == "1", "Expected remainder 1"

    # Test binary string "1010" which should have a remainder of 2 when divided by 3
    resp = fsm.process_input("1110")
    assert resp == "2", "Expected remainder 2"

    # Test binary string "111" which should have a remainder of 0 when divided by 3
    resp = fsm.process_input("1111")
    assert resp == "0", "Expected remainder 0"

def test_incorrect_state_name():
    fsm = create_mod_three_fsm()

    with pytest.raises(Exception) as err:
        fsm.set_start_state('A1')

    assert str(err.value) == "State name does not exist in states dictionary"



if __name__ == "__main__":
    pytest.main()
