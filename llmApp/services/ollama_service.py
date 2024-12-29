# llmApp/services/ollama_service.py
import requests
import time

class OllamaService:
    def __init__(self, model_name="gemma2:2b"):
        self.base_url = "http://localhost:11434/api/generate"
        self.model_name = model_name

    def generate_text(self, prompt):
        try:
            response = requests.post(
                self.base_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            response.raise_for_status()
            time.sleep(1)  # Prevent overwhelming the API
            return response.json().get('response', '').strip()
        except Exception as e:
            print(f"Error generating text: {str(e)}")
            return None

    def generate_property_description(self, property_data):
        prompt = f"""Generate an engaging hotel description for this property:
        Hotel Name: {property_data['property_title']}
        Location: {property_data['city_name']}
        Room Type: {property_data['room_type']}
        Rating: {property_data['rating']}/5
        Price: ${property_data['price']} per night

        Instructions:
        1. Write 2-3 paragraphs
        2. Highlight the location and surroundings
        3. Mention the room types and amenities
        4. Include the price point and value proposition
        5. Keep it professional but engaging
        
        Generate only the description without any additional text or formatting."""

        description = self.generate_text(prompt)
        return description if description else "Description not available"