# llmApp/services/ollama_service.py
import requests
import json
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

    def rewrite_property_title(self, hotel):
        prompt = f"""Rewrite this hotel property title to be more engaging and descriptive:
        Current Title: {hotel.property_title}
        Location: {hotel.city_name}
        Room Type: {hotel.room_type}
        Rating: {hotel.rating}/5
        
        Rules:
        1. Keep it concise but descriptive
        2. Include the location if relevant
        3. Highlight any unique features
        4. Maintain professionalism
        5. Return only the new title, no additional text
        """
        return self.generate_text(prompt)
    
    def generate_property_description(self, property_data):
        prompt = f"""Generate an engaging hotel description:
        Hotel: {property_data['property_title']}
        Location: {property_data['city_name']}
        Room Type: {property_data['room_type']}
        Rating: {property_data['rating']}/5
        Price: ${property_data['price']} per night

        Write 2-3 paragraphs highlighting location, amenities, and value proposition.
        """
        return self.generate_text(prompt)

    def generate_property_summary(self, property_data):
        prompt = f"""Create a brief summary for this hotel:
        Name: {property_data['property_title']}
        Location: {property_data['city_name']}
        Price: ${property_data['price']}
        Rating: {property_data['rating']}/5
        Description: {property_data.get('description', 'Not available')}

        Create a concise 2-3 sentence summary highlighting key features.
        """
        return self.generate_text(prompt)

    def generate_property_review(self, property_data):
        prompt = f"""Generate a hotel review:
        Name: {property_data['property_title']}
        Location: {property_data['city_name']}
        Price: ${property_data['price']}
        Current Rating: {property_data['rating']}/5
        
        Please provide a review in exactly this format:
        RATING: [single number between 1-5]
        REVIEW: [your detailed review]
        """
        response = self.generate_text(prompt)
        if not response:
            return None, None
            
        try:
            # More robust parsing
            rating_part = response.split('REVIEW:')[0].split('RATING:')[1].strip()
            review_part = response.split('REVIEW:')[1].strip()
            
            # Convert rating to float, handling various formats
            rating = float(rating_part.split('/')[0].strip())
            
            return rating, review_part
        except (ValueError, IndexError) as e:
            print(f"Error parsing response: {str(e)}")
            # Fallback to current rating if parsing fails
            return float(property_data['rating']), response