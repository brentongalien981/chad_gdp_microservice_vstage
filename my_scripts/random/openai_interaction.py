import os
from openai import OpenAI
from dotenv import load_dotenv
import ast

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI()


# Parse the string to a dictionary
def parse_dict_string(dict_string):
    try:
        parsed_dict = ast.literal_eval(dict_string)
        return parsed_dict
    except (ValueError, SyntaxError) as e:
        print("Error parsing string dictionary:", e)


def count_tokens(messages):
    """Estimate the number of tokens in the messages."""
    return sum(len(msg["content"].split()) for msg in messages)


def generate_response(messages):
    try:
        # Use the OpenAI API to generate a response
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )

        # DEBUG
        print("\n\n\n##############################################")
        print("completion ==> ...")
        print(completion)
        print("##############################################\n\n\n")

        # Print tokens info.
        print("\n\n\n##############################################")
        print("Tokens info ==> ...")
        print(f"prompt_tokens: {completion.usage.prompt_tokens}")
        print(f"completion_tokens: {completion.usage.completion_tokens}")
        print(f"total_tokens: {completion.usage.total_tokens}")
        print("##############################################\n\n\n")

        response = completion.choices[0].message.content
        return response

    except Exception as e:
        return f"An error occurred: {str(e)}"


# Initialize the chat with a system message
system_message1 = os.getenv("INITIAL_INSTRUCTION")
messages = [{"role": "system", "content": system_message1}]


# Start the chat with the user
print("Welcome to OpenAI ChatBot!")

while True:

    # Generate and print the response from OpenAI
    response = generate_response(messages)

    # Append the AI's response to the messages list
    messages.append({"role": "assistant", "content": response})

    # Print the AI's response
    print(f"AI: {response}")

    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chat. Goodbye!")
        break

    # Append the user's message to the messages list
    messages.append({"role": "user", "content": user_input})

    # Check the token count and truncate if necessary
    while count_tokens(messages) > 3500:  # Set slightly below the 4096 limit
        # Only pop messages that are not the system message.
        # So start from index 1 instead of 0.
        messages.pop(1)


# Format the chad's profile in a python dictionary.

# Append the AI's response to the messages list
final_instruction = "Finally, present the answers in python dictionary with these format: {'nationality':  nationality, 'income': income, 'physiqueType': physiqueType}"
messages.append({"role": "assistant", "content": final_instruction})

# Generate and print the response from OpenAI
response = generate_response(messages)

# Print the AI's response
print(f"AI: {response}")


print("\n\n\n################################################")
print("Extracting the dictionary literal from the python code...")
print("################################################\n\n\n")
new_messages = [
    {
        "role": "user",
        "content": f"Extract just the dictionary literal from this python code: {response}... No extra comments and variable names. No backticks and anything else.",
    }
]

response = generate_response(new_messages)
chad_profile = parse_dict_string(response)

# Print Chad's Profile
print("Chad's Profile:")
print(chad_profile)
# Loop through the dictionary and print the key-value pairs
for key, value in chad_profile.items():
    print(f"{key}: {value}")

print("\n\n\n################################################")
print("Chat ended.")
print("################################################\n\n\n")
