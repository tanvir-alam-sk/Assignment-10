# llmApp/services/ollama_service.py
import requests
import json
import time
import re

class OllamaService:
    def __init__(self, model_name="phi"):
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

        Format your response EXACTLY like this:
        RATING: [single number 1-5]
        REVIEW: [detailed review text]

        Note: The rating should be just a single number between 1 and 5."""
        
        response = self.generate_text(prompt)
        if not response:
            return None, None

        try:
            # First try to extract rating using the expected format
            rating_match = re.search(r'RATING:\s*(\d+(?:\.\d+)?)', response)
            if rating_match:
                rating = float(rating_match.group(1))
            else:
                # Fallback: try to find any number between 1-5 at the start of the response
                rating_match = re.search(r'^[^\d]*(\d+(?:\.\d+)?)', response)
                if rating_match:
                    rating = float(rating_match.group(1))
                else:
                    # If no rating found, use the hotel's current rating
                    rating = float(property_data['rating'])

            # Extract review text
            review_match = re.search(r'REVIEW:\s*(.+)', response, re.DOTALL)
            if review_match:
                review = review_match.group(1).strip()
            else:
                # If no "REVIEW:" marker found, use everything after the rating
                review = re.sub(r'^[^\d]*\d+(?:\.\d+)?[^\w]*', '', response, 1).strip()
                review = re.sub(r'[#*]+', '', review).strip()  # Remove markdown markers

            # Validate rating is within bounds
            rating = min(max(rating, 1), 5)  # Ensure rating is between 1 and 5
            
            return rating, review

        except Exception as e:
            print(f"Error parsing response: {str(e)}\nRaw response: {response}")
            # Fallback to current rating if parsing fails
            default_rating = float(property_data['rating'])
            cleaned_review = re.sub(r'[#*]+', '', response).strip()  # Remove markdown markers
            return default_rating, cleaned_review
