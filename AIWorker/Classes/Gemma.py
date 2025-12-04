from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import torch
from CustomExceptions import GemmaGenerationError, GemmaError

class GemmaReviewer:
    _instance = None 
    
    def __new__(cls):
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 

        return cls._instance

    def __init__(self):
        try:
            print('logging into hugging face!')
            login(token='')
            print('logged!')

            self.model_name = "google/gemma-2-2b-it"
            self.max_tokens= 1000
            self.tokenizer: AutoTokenizer = AutoTokenizer.from_pretrained(self.model_name)
            print('about to download llm model :(')
            self.model: AutoModelForCausalLM = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                dtype=torch.float16,
                device_map="cpu",
                low_cpu_mem_usage= True

            )
            print('Gemma downloaded!')
        except Exception:
            raise GemmaError
        

    def infere_basic_text(self, txt: str, lvl: str, user_lan: str, prompt: str)->str:
        prompt= f"""
        Review the following text as if you were a teacher of that language, check for gramatical errors, syntax, readability and clarity as if it was 'your student' had {lvl} level.
        In your corrections shadow cite that shit and point the error and how to correct, add at least two options better than your student did.
        Dont over explain yourself that much.
        At the end of your report do a list of things your student did a great job and do another list of things he should study. 
        Dont be too harsh but not too lenient.

        **FORMAT IN WHICH YOU SHOULD RESPOND**

        ** SCORES **

        1. OVER ALL: Summarize the clarity, readiblity and quality of the text. At the end conclude with X/10 on your jugde, i.e 8/10 (HAVE IN MIND YOUR STUDENT LEVEL)
        2. GRAMMAR: summarize grammar and conclude with X/10 (HAVE IN MIND THE LEVEL OF YOUR STUDENT)
        3. READABILITY: how clear is the text? ~ does it get to the point? ~ is it cohesive? ~ conclude with X/10 (HAVE IN MIND THE LEVEL OF YOUR STUDENT)
        4. COHERENCE: Is the text really coherent? ~ Is it logically sound? ~ conclude with X/10 (HAVE IN MIND THE LEVEL OF YOUR STUDENT)
        5. VOCABULARY: Do your student overuse some words? should they/them use a more appropiate word in that case? If so give examples shadow citing your student. ~ conclude with X/10 (HAVE IN MIND THE LEVEL OF YOUR STUDENT)
        6. NATURAL PHRASING: Is your student just translating from their native language? how natural is his message? ~ conclude with X/10 (HAVE IN MIND THE LEVEL OF YOUR STUDENT)
        
        ** WHAT YOUR STUDENT GOT RIGHT **

        Explain what he got right, 3-5 lines

        ** WHAT YOUR STUDENT GOT WRONG **

        Explain what he got wrong, 3-5 lines

        ** IMPROVEMENTS

        detail here the way your student can improve 3-5 lines

        *** NO MORE TEXT MORE THAN ABOVE ** 

        ** LANGUAGE **
        Always respond in your student's main language, which is {user_lan}

        ** USER PROMPT **
        This is what We asked the student to write about: {prompt}

        ** USER MESSAGE **
        {txt}
        --------------------------------------------
        """
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
            with torch.no_grad():
                outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_tokens,
                do_sample= True,
                pad_token_id=self.tokenizer.eos_token_id
                )
            
            llm_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            llm_response = llm_response.split('--------------------------------------------') #TODO: find a better/deterministic way to always split input and output
            return llm_response
        except Exception:
            raise GemmaGenerationError
        
tin = GemmaReviewer()

print(tin.infere_basic_text(
    txt="HEEEEEEEEEEEEEEEEEEEEEY PLEASE WORK FOR THE LOVE OF GOOOOOOOOOOOOOOOOOOOOOD",
    lvl= "A2",
    user_lan="Spanish",
    prompt="does this work?"
))


