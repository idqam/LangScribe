from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

class OpenAIClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        openai_token = os.getenv("OPEN_AI_TOKEN")
        self.client = OpenAI(api_key=openai_token)
        self.temperature = 0.3
        self.model = 'gpt-4o-mini'
        self._initialized = True
    
    def _define_sys_prompt(self, user_language: str, prompt: str, user_proficiency: str, user_text: str):

        format_example = """
        {
            "Overview": {"message": "string", "rate": 1},
            "Grammar": {"message": "string", "rate": 1},
            "Readability": {"message": "string", "rate": 1},
            "Coherence": {"message": "string", "rate": 1},
            "Vocab": {"message": "string", "rate": 1},
            "Strengths": {"message": "string"},
            "Improvement": {"message": "string"},
            "ActualLevel": {"level": "A1-C2"},
            "FinalRating": {"rate": 1}
        }
        """
        
        language_instruction = f"Respond in user's preferred language: {user_language}" if user_language else "Respond in the same language as the user's text"
        proficiency = user_proficiency if user_proficiency else "B1"
        
        self.sys_prompt = f"""You are a professional language teacher.
        Your job is to review a student's message that responds to a prompt.
        Don't be overly harsh with your student but don't be too lenient.

        You must:
        - Create a JSON response and don't respond outside that JSON or add/delete sections
        - {language_instruction}
        - Current user proficiency level: {proficiency}

        Sections:
        - Overview: Summarize clarity and overall message quality [rate 1-5]
        - Grammar: Summarize grammar, point out concrete errors and suggestions [rate 1-5]
        - Readability: Is the text readable? Point out concrete examples of unclear phrases or ideas [rate 1-5]
        - Coherence: Does the text follow logical steps or deviate from argument? [rate 1-5]
        - Vocab: Does the text have rich vocabulary for user's proficiency? Suggest new words and point out overused ones [rate 1-5]
        - Strengths: Point out your student's strengths
        - Improvement: Point out opportunities to grow based on errors made
        - ActualLevel: Assess the actual language level demonstrated (A1, A2, B1, B2, C1, C2)
        - FinalRating: Overall rating [1-5]

        Format of response:
        {format_example}

        Prompt:
        {prompt}

        User's Text:
        {user_text}
"""
    
    def review_user_text(self, user_language: str, prompt: str, user_proficiency: str, user_text: str):
        self._define_sys_prompt(
            user_language=user_language,
            prompt=prompt,
            user_text=user_text,
            user_proficiency=user_proficiency
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": self.sys_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=self.temperature
            )
            
            model_response = response.choices[0].message.content
            return json.loads(model_response)
            
        except Exception as e:
            print(f"Error: {e}")
            raise

