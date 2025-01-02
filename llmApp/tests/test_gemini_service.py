import unittest
from unittest.mock import patch, MagicMock
from llmApp.services.gemini_service import GeminiService

class TestGeminiService(unittest.TestCase):
    def setUp(self):
        self.gemini_service = GeminiService()
        self.mock_hotel_data = {
            'property_title': 'Sunrise Beach Resort',
            'city_name': 'Miami Beach',
            'room_type': 'Ocean View Suite',
            'rating': 4.5,
            'price': 299,
            'description': 'Luxurious beachfront resort with stunning ocean views.'
        }

    @patch('llmApp.services.gemini_service.requests.post')
    def test_rewrite_property_title_success(self, mock_post):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Luxurious Ocean View Suite at Sunrise Beach Resort - Miami Beach'
                    }]
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Create a mock hotel object
        mock_hotel = MagicMock()
        mock_hotel.property_title = self.mock_hotel_data['property_title']
        mock_hotel.city_name = self.mock_hotel_data['city_name']
        mock_hotel.room_type = self.mock_hotel_data['room_type']
        mock_hotel.rating = self.mock_hotel_data['rating']

        result = self.gemini_service.rewrite_property_title(mock_hotel)
        self.assertEqual(result, 'Luxurious Ocean View Suite at Sunrise Beach Resort - Miami Beach')

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_description_success(self, mock_post):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Experience luxury at its finest in Miami Beach...'
                    }]
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.gemini_service.generate_property_description(self.mock_hotel_data)
        self.assertEqual(result, 'Experience luxury at its finest in Miami Beach...')

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_summary_success(self, mock_post):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Stunning beachfront resort in Miami Beach...'
                    }]
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.gemini_service.generate_property_summary(self.mock_hotel_data)
        self.assertEqual(result, 'Stunning beachfront resort in Miami Beach...')

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_review_success(self, mock_post):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'RATING: 4.5\nREVIEW: Excellent beachfront location...'
                    }]
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        rating, review = self.gemini_service.generate_property_review(self.mock_hotel_data)
        self.assertEqual(rating, 4.5)
        self.assertEqual(review, 'Excellent beachfront location...')

    @patch('llmApp.services.gemini_service.requests.post')
    def test_request_failure(self, mock_post):
        # Mock failed API response
        mock_post.side_effect = Exception('API Error')

        result = self.gemini_service.generate_property_description(self.mock_hotel_data)
        self.assertIsNone(result)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_invalid_response_format(self, mock_post):
        # Mock invalid API response
        mock_response = MagicMock()
        mock_response.json.return_value = {'invalid': 'response'}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = self.gemini_service.generate_property_description(self.mock_hotel_data)
        self.assertIsNone(result)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_review_invalid_format(self, mock_post):
        # Mock invalid review format response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [{
                'content': {
                    'parts': [{
                        'text': 'Invalid format response'
                    }]
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        rating, review = self.gemini_service.generate_property_review(self.mock_hotel_data)
        self.assertIsNone(rating)
        self.assertIsNone(review)

if __name__ == '__main__':
    unittest.main()