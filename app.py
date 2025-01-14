from dotenv import load_dotenv
import os
from openai import OpenAI
from lib.dog_repository import DogRepository
from lib.dog import Dog
import json
from lib.database_connection import DatabaseConnection
import csv
from colorama import init, Fore, Style

load_dotenv()  # Load environment variables from the .env file
api_key = os.getenv("OPENAI_API_KEY")

# seed_file_path = './Dogs_seed.csv'

client = OpenAI(api_key=api_key) 

connection = DatabaseConnection()
connection.connect()

def is_valid_dog_entry(dog_data):
    required_fields = {
        "Name": str,
        "Breed": str,
        "Purebreed": bool,
        "Mix": bool,
        "Sex": str,
        "Location": str,
        "Personality": str,
        "Likes": (int, float),
        "Comments": (int, float),
        "Link_to_post": str
    }
    
    for field, expected_type in required_fields.items():
        value = dog_data.get(field)
        # Check if value is None, "None", empty string, or not of expected type
        if value is None or value == "None" or value == "" or not isinstance(value, expected_type):
            return False, field
        if "Age" in dog_data and dog_data["Age"] is not None:
            if not isinstance(dog_data["Age"], (int, float)):
                return False, "Age (invalid type)"
    return True, None

def extract_and_save_dog_data(description):
    dog_repository = DogRepository(connection)
    print("Welcome to The Dogist!\nWhat would you like to do? \n1 - Add a new dog \n2 - View rankings by breed \n3 - Viewing rankings by name \n4 - Search by breed \n5 - Search by name \n6 - Import dogs by CSV file")
    selection = input()
    if selection == str(1):
        description = input('Please enter a brief description of the dog here: \n')
        try:
            prompt = f"""
            Extract the following fields from the description of a dog. Please capitalise the name and breed, and if shorthand has been used (e.g. 'lab'for labrador
            or 'rottie' for rottweiler) please change to the full name. Please also correct any spelling errors. Be careful when determining the age of the dog as it may be presented as for example 'almost 5', which means the dog is in fact 4!
            If the age is unknown please record it as Null.
            - Name
            - Breed
            - Age (in years)

            Description: "{description}"

            Provide the output as a JSON object.
            """

            # Call OpenAI's API with the correct parameters
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Use the chat model instead of completions
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts dog information from text descriptions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )

            name = json.loads(response.choices[0].message.content.strip())["Name"]
            breed = json.loads(response.choices[0].message.content.strip())["Breed"]
            age = json.loads(response.choices[0].message.content.strip())["Age"]

            dog_repository.create(Dog(None, name, breed, age))

            # repository = DogRepository(connection)
            # repository.create(Dog(None, name, breed, age))

            # Parse and return the AI's response
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error: {e}")
            return None
    elif selection == str(2):
        return "\n".join(dog_repository.get_breed_popularity())
    
    elif selection == str(3):
        return "\n".join(dog_repository.get_name_popularity())
    
    elif selection == str(4):
        print("Please enter the breed you wish to search")
        breed = input()
        return dog_repository.find_by_breed(breed)
    
    elif selection == str(5):
        print("Please enter the name you wish to search")
        name = input()
        return dog_repository.find_by_name(name)
    
    elif selection == str(6):
        print("Enter the path to the CSV file")
        seed_file_path = input()
        print("Processing file...")
    
        dogs_data = []
        with open(seed_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Use DictReader if the file has headers
            for row in reader:
                dogs_data.append(row)
        descriptions = []
        for row in dogs_data:
            description_2 = row["Caption"]
            descriptions.append(description_2)
        
        total_descriptions = len(descriptions)
        
        for idx, single_description in enumerate(descriptions, start=1):
            try:
                prompt = f"""
                    Extract dog information from the description below and return ONLY a raw JSON object with no markdown formatting, no code blocks, and no additional text.
                    Multiple dogs should be returned in an array format. Even for a single dog, use the array format.
                    Required JSON structure:
                    {{
                        "dogs": [
                            {{
                                "Name": "Dog's name",
                                "Breed": "Dog's breed",
                                "Age": age_number,
                                "Purebreed": true or false,
                                "Mix": true or fale,
                                "Sex": "Boy" or "Girl",
                                "Location": "Dog's location",
                                "Personality": "Dog's personality traits / quirks",
                                "Likes": likes_number,
                                "Comments": comments_number,
                                "Link_to_post": "URL link to instagram post",
                                "Photo": null
                            }}
                        ]
                    }}

                    Rules:
                    - Return ONLY the JSON object with no decorators or markdown
                    - Output "Breed" as "Mix" if no other breed is mentioned in the description
                    - Purebreed is true if words 'mix' or 'mixed' are absent
                    - Mix is the inverse value of Purebreed
                    - All boolean values must be lowercase (true/false)
                    - Capitalize first letter of name and breed
                    - Convert breed shorthand (e.g., 'lab' to 'Labrador')
                    - Correct spelling errors
                    - For 'almost X years', use X-1 as the age
                    - Use null for unknown age or breed
                    - Set photo to null

                    Description: "{single_description}"
                    """

            
                # Call OpenAI's API with the correct parameters
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Use the chat model instead of completions
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that extracts dog information from text descriptions."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=800,
                    temperature=0.5
                )   

                try:
                    # Parse the JSON response
                    content = json.loads(response.choices[0].message.content.strip())
                    # Process dogs array (will work for both single and multiple dogs)
                    for dog in content["dogs"]:
                            name = dog["Name"]
                            breed = dog["Breed"]
                            age = dog["Age"]
                            purebreed = dog["Purebreed"]
                            mix = dog["Mix"]
                            sex = dog["Sex"]
                            location = dog["Location"]
                            personality = dog["Personality"]
                            likes = dog["Likes"]
                            comments = dog["Comments"]
                            link_to_post = dog["Link_to_post"]
                            photo = dog["Photo"]

                            is_valid, missing_field = is_valid_dog_entry(dog)

                            if is_valid:
                                print(f"Name: {name}")
                                print(f"Breed: {breed}")
                                print(f"Age: {age} years old")
                                print(f"Purebreed: {purebreed}")
                                print(f"Mix: {mix}")
                                print(f"Sex: {sex}")
                                print(f"Hometown: {location}")
                                print(f"Personality / quirks: {personality}")
                                print(f"{likes} likes")
                                print(f"{comments} comments")
                                print(link_to_post)

                                dog_repository.create(Dog(None, name, breed, age, purebreed, mix, sex, location, personality, likes, comments, link_to_post, photo))
                                print(f"{Fore.GREEN}New dog added successfully!{Style.RESET_ALL}")

                            else:
                                print(f"{Fore.RED}Invalid dog entry in row {idx}. Missing or invalid {missing_field}{Style.RESET_ALL}")
                                with open('invalid_entries.csv', 'a', newline='') as file:
                                    writer = csv.writer(file)
                                    writer.writerow([idx, single_description, missing_field])
                                print(f"{Fore.YELLOW}Entry added to invalid_entries.csv for manual review{Style.RESET_ALL}")

                except json.JSONDecodeError as e:
                    print(f"JSON Parsing Error: {e}")
                    print("Response content:", response.choices[0].message.content.strip())
                except KeyError as e:
                    print(f"Missing Key Error: {e}")
                    print("Content structure:", content)
                except Exception as e:
                        print(f"Other Error: {e}")
                
                progress = (idx / total_descriptions) * 100
                print(f"{Fore.YELLOW}Progress: {progress:.2f}% ({idx}/{total_descriptions}){Style.RESET_ALL}")

            except Exception as e:
                    print(f"API Error: {e}")
    
        return f"{Style.BRIGHT}{Fore.GREEN}Processing complete{Style.RESET_ALL}"

# Example usage
if __name__ == "__main__":

    # app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
    description = (
        "A very passive and friendly soul, Munchkin has been around for 5 years and is a collie "
        "and whippet cross who likes to curl up next to you on the sofa and does spins when she sees you."
    )
    result = extract_and_save_dog_data(description)
    print(result)