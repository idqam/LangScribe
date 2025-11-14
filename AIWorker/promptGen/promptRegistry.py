from typing import Dict, List
from AIWorker.promptGen.promptEnums import PromptCategory, PromptDifficulty


class PromptRegistry:
    def __init__(self):
        self.cache: Dict[str, Dict[str, Dict[str, str]]] = {}

    def get_cached_prompt(self, user_id: str, lang: str, level: str) -> str | None:
        user_map = self.cache.get(user_id)
        if not user_map:
            return None
        lang_map = user_map.get(lang)
        if not lang_map:
            return None
        return lang_map.get(level)

    def store_prompt(self, user_id: str, lang: str, level: str, prompt: str):
        if user_id not in self.cache:
            self.cache[user_id] = {}
        if lang not in self.cache[user_id]:
            self.cache[user_id][lang] = {}
        self.cache[user_id][lang][level] = prompt

    def clear_user(self, user_id: str):
        if user_id in self.cache:
            del self.cache[user_id]

    def clear_all(self):
        self.cache.clear()
