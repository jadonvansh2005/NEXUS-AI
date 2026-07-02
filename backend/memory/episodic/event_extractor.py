import json
from llm.providers.gemini.gemini_client import GeminiClient


class EventExtractor:

    def __init__(self):

        self.llm = GeminiClient()

    def extract(

        self,

        text: str

    ):

        prompt = (
            "Analyze this user message to see if it represents a meaningful event, decision, milestone, action, or technical problem "
            "(e.g., uploading files, choosing a database, crashing errors like CUDA, starting a new module/project, changing plans/roadmap, debugging issues). "
            "If it is not a meaningful event (e.g. greetings like 'hi', small talk, polite remarks like 'thanks', simple yes/no, general questions), output 'None'.\n\n"
            "Otherwise, summarize the event cleanly as a short past-tense phrase (e.g., 'Uploaded blockchain proposal PDF', 'Encountered CUDA crashing issue', 'Started building memory router') "
            "and classify the event_type as one of: 'milestone', 'technology_decision', 'roadmap_change', 'issue_encountered', or 'event'.\n\n"
            f"User Message: \"{text}\"\n\n"
            "Output your classification as JSON in this format: {\"event_type\": \"...\", \"summary\": \"...\"}. "
            "Output ONLY the JSON, nothing else."
        )

        try:
            response = self.llm.generate(prompt).strip()
            if response.lower() == "none" or not response:
                return []
            
            # Clean up potential markdown code block backticks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
                
            data = json.loads(response)
            if "event_type" in data and "summary" in data:
                return [(data["event_type"], data["summary"])]
        except Exception as e:
            print(f"[EventExtractor Error] {e}")
        return []