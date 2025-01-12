from lib.data_trimmer import Data
import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from the .env file
api_key = os.getenv("OPENAI_API_KEY")

class DataRepository:
    def __init__(self, connection):
        self._connection = connection

# Example data (string)

# Dipper, Pit Bull (13 y/o), Red Bank, NJ. 
# "He loves to chew our socks and sleep on the couch,
# when he was a puppy he was very energetic but now
# he's kinda goofy and sleeps all day".

from openai import OpenAI

client = OpenAI(api_key="your_api_key_here")

# Configure your OpenAI API key

def extract_dog_data(description):
    try:
        # Define the prompt for the AI
        prompt = f"""
        Extract the following fields from the description of a dog:
        - Name
        - Breed
        - Age (in years)
        - Quirks/Personality traits

        Description: "{description}"

        Provide the output as a JSON object.
        """

        # Call OpenAI's API
        response = client.completions.create(engine="text-davinci-003",  # Use GPT-3.5 or GPT-4
        prompt=prompt,
        max_tokens=100,
        temperature=0.5)

        # Parse and return the AI's response
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage
description = (
    "A very passive and friendly soul, Munchkin has been around for 5 years and is a collie "
    "and whippet cross who likes to curl up next to you on the sofa and does spins when she sees you."
)
result = extract_dog_data(description)
print(result)

