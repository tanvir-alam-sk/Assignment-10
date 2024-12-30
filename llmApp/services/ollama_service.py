# llmApp/services/ollama_service.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import time
import re
import os
from typing import Optional, Tuple

class OllamaService:
    def __init__(self, model_name="llama3.2:1b", max_retries=3, timeout=60):
        self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://ollama:11434/api/generate')
        self.model_name = model_name
        self.timeout = timeout
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[408, 429, 500, 502, 503, 504],
        )
        
        # Create session with retry strategy
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def generate_text(self, prompt: str) -> Optional[str]:
        """
        Generate text using Ollama with retry logic and better error handling.
        """
        try:
            print(f"Generating text for model {self.model_name}...")
            
            response = self.session.post(
                self.base_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=self.timeout
            )
            
            if response.status_code == 404:
                print(f"Model {self.model_name} not found. Attempting to pull...")
                self._pull_model()
                return self.generate_text(prompt)  # Retry after pulling
                
            response.raise_for_status()
            
            # Add delay to prevent rate limiting
            time.sleep(2)
            
            result = response.json().get('response', '').strip()
            if not result:
                print("Warning: Empty response received")
                return None
                
            return result
            
        except requests.exceptions.Timeout:
            print(f"Timeout error after {self.timeout} seconds. Consider increasing timeout value.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error generating text: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def _pull_model(self) -> bool:
        """
        Pull the specified model if it's not already available.
        """
        try:
            pull_url = f"http://ollama:11434/api/pull"
            response = self.session.post(
                pull_url,
                json={"name": self.model_name},
                timeout=300  # Longer timeout for model pulling
            )
            response.raise_for_status()
            print(f"Successfully pulled model {self.model_name}")
            return True
        except Exception as e:
            print(f"Error pulling model: {str(e)}")
            return False

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


    def generate_property_review(self, property_data: dict) -> Tuple[Optional[float], Optional[str]]:
        """
        Generate a review with better error handling and validation.
        """
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
                # Fallback: try to find any number between 1-5 at the start
                rating_match = re.search(r'^[^\d]*(\d+(?:\.\d+)?)', response)
                if rating_match:
                    rating = float(rating_match.group(1))
                else:
                    rating = float(property_data['rating'])

            # Extract review text
            review_match = re.search(r'REVIEW:\s*(.+)', response, re.DOTALL)
            if review_match:
                review = review_match.group(1).strip()
            else:
                review = re.sub(r'^[^\d]*\d+(?:\.\d+)?[^\w]*', '', response, 1).strip()
                review = re.sub(r'[#*]+', '', review).strip()

            # Validate rating is within bounds
            rating = min(max(rating, 1), 5)
            
            return rating, review

        except Exception as e:
            print(f"Error parsing response: {str(e)}\nRaw response: {response}")
            return float(property_data['rating']), None