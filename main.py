import google.generativeai as genai
import os
from dotenv import load_dotenv

class ViolenceDetector:

    def __init__(self, generation_config = None, model = None) -> None:

        if not generation_config:
            self.generation_config = self._create_generation_config() 
        if not model:
            self.model = self._create_model(self.generation_config)

    def _post_process_reponse(self, response:str)->bool:
        return "true" in response.lower()
    
    def _create_generation_config(self):
        #configure model generation parameters:
        generation_config = genai.types.GenerationConfig(
            temperature = 0, #lower temperature = less randomness & less "creativity"
            top_k = 1,
            max_output_tokens = 24,
        )
        return generation_config

    def _create_model(self, generation_config):
        model = genai.GenerativeModel(
            model_name = "gemini-pro",
            generation_config = generation_config
        )
        return model

    def detect_violence_in_text(self, text:str)->bool:
        instructions = """
            Your task is to detect violence in text. You are provided with a query represented as a string containing\
            a piece of text. Your objective is to determine whether or not the given text contains violent language.\
            Finally, please respond with 'True' if you believe there is violence in the text, otherwise respond with \
            'False'. Here's the input:\n"""
        
        input_prompt = instructions + text
        
        response = self.model.generate_content(
            input_prompt,
            generation_config = self.generation_config
        )
        
        is_violent = self._post_process_reponse(response.text)
        return is_violent
    
#load and set up api key, you must have your api_key in seperate .env file: API_KEY=...
load_dotenv()
gemini_api_key = os.getenv("API_KEY")
genai.configure(api_key=gemini_api_key)

#Example of text with violence:
text = """
The sound of gunfire echoed through the deserted streets as the gang members clashed with rival factions.\
Blood splattered against the walls as screams filled the air. Bodies lay motionless on the ground,\
their lives taken in a brutal display of violence. The city descended into chaos as law enforcement \
struggled to regain control, but the cycle of brutality seemed endless.
"""

text = input("Enter any text:\n\n")
violence_detector = ViolenceDetector()
is_violent = violence_detector.detect_violence_in_text(text)
print(f'\nResult: {is_violent}')