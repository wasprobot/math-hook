import datetime
import importlib
from transitions import Machine

# Validate user input based on the current state validation rules
def validate_input(state, user_input, context):
    validation = state.get("validation")
    if not validation:
        return True, None

    input_type = validation.get("type")
    if input_type == "number":
        try:
            user_input = int(user_input)
        except ValueError:
            return False, "Please enter a valid number."
        if "min" in validation and user_input < validation["min"]:
            return False, f"The number must be at least {validation['min']}."
        if "max" in validation:
            if isinstance(validation["max"], dict) and "from" in validation["max"]:
                max_value = int(context.get(validation["max"]["from"]))
            else:
                max_value = int(validation["max"])
            if user_input > max_value:
                return False, f"The number cannot exceed {max_value}."
    elif input_type == "date":
        try:            
            dt = datetime.strptime(user_input, "%m/%d/%Y")
        except ValueError:
            return False, "Please enter a valid date in the format MM/DD/YYYY."

    return True, None

# Match user input with the current state's expected input
def match_input(state, user_input, context):
    match = state.get("match")

    if not match:
        return True, None

    if match.get("type") == "function":
        c = importlib.import_module(f"workflows.library.{match['class']}")
        function = getattr(c, match["function"])
        return function(context, user_input)
    
    return True, None

class WorkflowEngine():
    def __init__(self, workflow_data):
        self.workflow_data = workflow_data
        self.states = workflow_data['states']
        self.transitions = workflow_data['transitions']
        self._class = workflow_data.get('class')
        self._function = workflow_data.get('function')

        self.prompts = {name: self.states[name]['prompt'] for name in list(self.states.keys())}
        self.context = {}  # Store user responses for validation
        self.machine = Machine(model=self, states=list(self.states.keys()), transitions=self.transitions, initial='start')

    def call_action(self):
        if not self._class or not self._function:
            return ""
        
        c = importlib.import_module(f"workflows.library.{self._class}")
        function = getattr(c, self._function)
        return function(self.context)
    
    def to_state(self, state):
        self.state = state

    def get_prompt(self):
        return self.prompts[self.state]

    # def get_state_validation(self):
    #     for state in self.states:
    #         if state['name'] == self.state:
    #             return state

    def validate_and_next(self, user_input):
        current_state_data = self.workflow_data['states'][self.state]

        # Validate input
        is_valid, error_message = validate_input(current_state_data, user_input, self.context)
        if not is_valid:
            return error_message, False

        # Match input
        is_match, error_message = match_input(current_state_data, user_input, self.context)
        if not is_match:
            return error_message, False

        # Store valid user input in context
        self.context[self.state] = user_input

        # Trigger next state if valid
        if self.state != 'end':
            self.next()
            return self.get_prompt(), True
        else:
            return "You've completed the workflow!", True