from flask import Flask, render_template, request, jsonify
import chatbot  # Assuming you have a separate chatbot module
import re
import json

app = Flask(__name__)

intents = json.loads(open('intents.json').read())

# Function to evaluate mathematical expression
def evaluate_expression(expression):
    try:
        cleaned_input = re.sub(r'[=^0-9+\-*/(). ]', '', expression)  # Allow digits and math symbols only
        print("This is cleaned input:", cleaned_input)
        result = eval(cleaned_input)  # Safely evaluate the expression
        print("This is expression result:", result)
        return cleaned_input, result
    except ZeroDivisionError:
        return "Cannot divide by zero!"
    except Exception as e:
        return str(e)  # Handle any other errors

# Chatbot response function for non-math queries
def chatbot_response(user_input):
    # Example basic responses or call external chatbot logic
    if "hello" in user_input.lower():
        return "Hello! How can I assist you today?"
    elif "bye" in user_input.lower():
        return "Goodbye! Have a nice day!"
    else:
        return chatbot.output(user_input)  # Use your chatbot module for complex responses

# Route for the main page
@app.route("/")
def index():
    return render_template("index.html")

# Route to handle chatbot or math requests
@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form.get("message")
    
    # Check if the message contains a math expression
    if any(op in user_message for op in ['+', '-', '*', '/']):
        # Try to evaluate the expression
        try:
            expression, result = evaluate_expression(user_message)
            return jsonify({"reply": f"{expression} = {result}"})
        except Exception as e:
            return jsonify({"reply": f"Error: {str(e)}"})
    
    # Otherwise, treat it as a general chatbot query
    else:
        bot_reply = chatbot_response(user_message)
        return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)











# from fastapi import FastAPI, Request, Form
# from fastapi.responses import JSONResponse
# import chatbot  # Assuming you have a separate chatbot module
# import re
# import json

# app = FastAPI()

# # Load intents
# with open('intents.json') as file:
#     intents = json.load(file)

# # Function to evaluate mathematical expression
# def evaluate_expression(expression):
#     try:
#         # Clean input to allow digits and basic math symbols only
#         cleaned_input = re.sub(r'[^0-9+\-*/(). ]', '', expression)
#         result = eval(cleaned_input)  # Evaluate the expression
#         return cleaned_input, result
#     except ZeroDivisionError:
#         return "Cannot divide by zero!"
#     except Exception as e:
#         return str(e)  # Handle other errors

# # Chatbot response function for non-math queries
# def chatbot_response(user_input):
#     if "hello" in user_input.lower():
#         return "Hello! How can I assist you today?"
#     elif "bye" in user_input.lower():
#         return "Goodbye! Have a nice day!"
#     else:
#         return chatbot.output(user_input)  # Use your chatbot module for complex responses

# # Route for the main page
# @app.get("/")
# async def index():
#     return {"message": "Welcome to the chatbot and math evaluator API"}

# # Route to handle chatbot or math requests
# @app.post("/get_response")
# async def get_response(message: str = Form(...)):
#     # Check if the message contains a math expression
#     if any(op in message for op in ['+', '-', '*', '/']):
#         # Try to evaluate the expression
#         try:
#             expression, result = evaluate_expression(message)
#             return JSONResponse({"reply": f"{expression} = {result}"})
#         except Exception as e:
#             return JSONResponse({"reply": f"Error: {str(e)}"})

#     # Otherwise, treat it as a general chatbot query
#     else:
#         bot_reply = chatbot_response(message)
#         return JSONResponse({"reply": bot_reply})

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

