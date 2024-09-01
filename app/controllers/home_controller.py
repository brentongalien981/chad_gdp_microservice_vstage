from typing import Tuple
from flask import jsonify, request
import os
from openai import OpenAI

#
client = OpenAI()


# Initialize chat messages
system_message1 = os.getenv("INITIAL_INSTRUCTION_V2")
initial_messages = [{"role": "system", "content": system_message1}]


class HomeController:

    @staticmethod
    def home() -> Tuple[dict, int]:

        return (
            jsonify(
                {
                    "message": "Welcome to the Home Page!",
                }
            ),
            200,
        )

    @staticmethod
    def get_my_info() -> Tuple[dict, int]:
        return jsonify({"name": "John Doe", "bull": "rider"}), 200

    @staticmethod
    def chat() -> Tuple[dict, int]:
        try:
            # Extract the currentMessages array from the request body.
            current_messages = request.json.get("currentMessages", [])

            # Set the completion_messages to contain the system message and the current messages.
            completion_messages = initial_messages + current_messages

            # Generate and print the response from OpenAI
            response = generate_response(completion_messages)

            # Flag to check if all the main questions have been answered.
            is_session_done = response.endswith("{{YES}}")
            # The dictionary to hold the chad's profile.
            chad_profile = None

            if is_session_done:
                # Append the response to the completion_messages.
                completion_messages.append({"role": "assistant", "content": response})

                # Remove the flag from the response.
                response = response.replace("{{YES}}", "").strip()

                # Make another call to the OpenAI API to get the guy's profile
                # in a python dictionary format.
                final_instruction = os.getenv("LAST_INSTRUCTION_V2")

                completion_messages.append(
                    {"role": "system", "content": final_instruction}
                )

                # Make the request.
                chad_profile_dict_str = generate_response(completion_messages)
                # Convert the string to a python dictionary.
                chad_profile = eval(chad_profile_dict_str)

            # Set the chat_obj to contain the response.
            chat_obj = {"role": "assistant", "content": response}

            return (
                jsonify(
                    {
                        "chat_obj": chat_obj,
                        "isSessionDone": is_session_done,
                        "chad_profile": chad_profile,
                    }
                ),
                200,
            )
        except Exception as e:
            raise e

    @staticmethod
    def generate_image() -> Tuple[dict, int]:
        try:
            # Extract the chadProfile from the request body with a POST request.
            chad_profile = request.json.get("chadProfile", {})

            instructions = get_image_instructions(chad_profile)

            # Generate the image
            response = client.images.generate(
                model="dall-e-3",
                prompt=instructions,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_url = response.data[0].url
            revised_prompt = response.data[0].revised_prompt

            return (
                jsonify(
                    {
                        "message": "Image generated successfully!",
                        "instructions": instructions,
                        "image_url": image_url,
                        "revised_prompt": revised_prompt,
                    }
                ),
                200,
            )
        except Exception as e:
            raise e


def count_tokens(messages):
    """Estimate the number of tokens in the messages."""
    return sum(len(msg["content"].split()) for msg in messages)


def generate_response(messages):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages, max_tokens=8192
        )

        response = completion.choices[0].message.content
        return response

    except Exception as e:
        raise e


def get_image_instructions(chad_profile: dict) -> str:
    instructions = os.getenv("THE_IMAGE_GENERATION_STARTING_INSTRUCTION_V2")

    for key, value in chad_profile.items():
        instructions += f"{key}: {value}\n"

    instructions += os.getenv("THE_IMAGE_GENERATION_ENDING_INSTRUCTION_V2")
    return instructions
