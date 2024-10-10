import json
import os

from flask import Flask, request, jsonify
from datetime import datetime
from workflows.WorkflowEngine import WorkflowEngine

app = Flask(__name__)

WORKFLOW_PATH = './workflows'

# Load workflow from a JSON file
def load_workflow(workflow_name):
    workflow_file = os.path.join(WORKFLOW_PATH, f"{workflow_name.lower()}_workflow.json")
    if os.path.exists(workflow_file):
        with open(workflow_file) as f:
            return json.load(f)
    return None

# List available workflows
def list_available_workflows():
    workflows = []
    for file in os.listdir(WORKFLOW_PATH):
        if file.endswith('_workflow.json'):
            workflow_name = file.replace('_workflow.json', '')
            workflows.append(workflow_name.capitalize())
    return workflows

# Flask route for webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    session_id = req.get('session')
    queryResult = req.get('queryResult')

    # Extract session and query parameters    
    current_state = queryResult.get('outputContexts', [{}])[0].get('parameters', {}).get('current_state', 'start')
    context_data = queryResult.get('outputContexts', [{}])[0].get('parameters', {}).get('context_data', {})
    workflow_name = queryResult.get('outputContexts', [{}])[0].get('parameters', {}).get('workflow', '')

    # print(f"Session ID: {session_id}")
    # parameters = queryResult.get('parameters')

    user_input = queryResult['queryText'].strip().lower()

    # The menu command to select a workflow
    if user_input == 'menu':
        return menu(session_id)

    # Check if this is the first interaction
    is_first = not workflow_name
    if is_first:
        workflow_name = user_input.lower()

    # Load workflow data
    workflow_data = load_workflow(workflow_name)

    if not workflow_data:
        return menu(session_id)

    # Create the workflow engine and set its state
    engine = WorkflowEngine(workflow_data)
    engine.context = context_data
    engine.to_state(current_state)

    # print(f"Current state: {current_state}")

    # The first interaction
    if is_first:
        prompt = engine.call_action()
    else:
        # Validate user input and move to next state
        message, success = engine.validate_and_next(user_input)
        current_state = engine.state
        prompt = message

    # Prepare response with updated state and output context
    response = {
        "fulfillmentText": prompt,
        "outputContexts": [
            {
                "name": f"{session_id}/contexts/session_info",
                "lifespanCount": 5,
                "parameters": {
                    "workflow": workflow_name,
                    "current_state": current_state,
                    "context_data": engine.context
                }
            }
        ]
    }

    return jsonify(response)

# Menu to select a workflow 
def menu(session_id, last_workflow_success=False):
    workflows = list_available_workflows()
    return jsonify({
        "fulfillmentText": ("Yay! You've completed the workflow!" if last_workflow_success else "") + "Choose a workflow. Some examples are DOW, QUAD, and FIB.",
        "fulfillmentMessages": [
            # {
            #     "image": {
            #         "imageUri": "https://latex.codecogs.com/svg.image?\\bg{white}\\frac{-b\\pm\\sqrt{b^2-4ac}}{2a}",
            #         "accessibilityText": "Sample image description"
            #     }
            # },
            {
                "quickReplies": {
                    "title": "Choose a workflow:",
                    "quickReplies": workflows
                }
            }
        ],
        "outputContexts": [
            {
                "name": f"{session_id}/contexts/session_info",
                "lifespanCount": 5,
                "parameters": None,
                "current_state": None,
                "workflow": None
            }
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)
