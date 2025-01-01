import unittest
from unittest.mock import patch, MagicMock
from llmApp.services.gemini_service import GeminiService

class TestGeminiService(unittest.TestCase):

    def setUp(self):
        self.service = GeminiService()
        self.mock_hotel = MagicMock()
        self.mock_hotel.property_title = "Cozy Downtown Hotel"
        self.mock_hotel.city_name = "New York"
        self.mock_hotel.room_type = "Suite"
        self.mock_hotel.rating = 4.5
        
        self.mock_property_data = {
            "property_title": "Beachfront Villa",
            "city_name": "Miami",
            "room_type": "Villa",
            "rating": 4.8,
            "price": 350,
            "description": "A beautiful villa by the beach with stunning ocean views."
        }

    @patch('llmApp.services.gemini_service.requests.post')
    def test_rewrite_property_title(self, mock_post):
        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "Luxurious Downtown Hotel Suite in New York"}]}}
            ]
        }

        response = self.service.rewrite_property_title(self.mock_hotel)
        self.assertEqual(response, "Luxurious Downtown Hotel Suite in New York")
        self.assertTrue(mock_post.called)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_description(self, mock_post):
        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "This beachfront villa in Miami offers stunning ocean views and luxurious amenities."}]}}
            ]
        }

        response = self.service.generate_property_description(self.mock_property_data)
        self.assertIn("beachfront villa in Miami", response)
        self.assertTrue(mock_post.called)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_summary(self, mock_post):
        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "A luxurious villa in Miami priced at $350 with an excellent rating of 4.8/5."}]}}
            ]
        }

        response = self.service.generate_property_summary(self.mock_property_data)
        self.assertIn("luxurious villa in Miami", response)
        self.assertTrue(mock_post.called)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_generate_property_review(self, mock_post):
        # Mock API response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "RATING: 5\nREVIEW: Amazing property with top-notch amenities and breathtaking views."}]}}
            ]
        }

        rating, review = self.service.generate_property_review(self.mock_property_data)
        self.assertEqual(rating, 5)
        self.assertIn("Amazing property with top-notch amenities", review)
        self.assertTrue(mock_post.called)

    @patch('llmApp.services.gemini_service.requests.post')
    def test_error_handling_in_request(self, mock_post):
        # Simulate a failed request
        mock_post.side_effect = Exception("API request failed")
        
        response = self.service.rewrite_property_title(self.mock_hotel)
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()

# import unittest
# from unittest.mock import patch, MagicMock
# from llmApp.services.gemini_service import GeminiService

# class TestGeminiService(unittest.TestCase):

#     @patch('llmApp.services.gemini_service.requests.post')
#     def test_rewrite_property_title(self, mock_post):
#         # Arrange
#         mock_response = MagicMock()
#         mock_response.json.return_value = {
#             'candidates': [{
#                 'content': {
#                     'parts': [{
#                         'text': "Luxury Hotel in New York with spacious rooms and excellent amenities."
#                     }]
#                 }
#             }]
#         }
#         mock_post.return_value = mock_response
        
#         hotel = {
#             'property_title': "Luxury Hotel",
#             'city_name': "New York",
#             'room_type': "Spacious Room",
#             'rating': 4.5
#         }

#         gemini_service = GeminiService()

#         # Act
#         result = gemini_service.rewrite_property_title(hotel)

#         # Assert
#         self.assertEqual(result, "Luxury Hotel in New York with spacious rooms and excellent amenities.")
#         mock_post.assert_called_once()

#     @patch('llmApp.services.gemini_service.requests.post')
#     def test_generate_property_description(self, mock_post):
#         # Arrange
#         mock_response = MagicMock()
#         mock_response.json.return_value = {
#             'candidates': [{
#                 'content': {
#                     'parts': [{
#                         'text': "This luxurious hotel in New York offers spacious rooms with modern amenities, perfect for both business and leisure travelers."
#                     }]
#                 }
#             }]
#         }
#         mock_post.return_value = mock_response
#         property_data = {
#             'property_title': "Luxury Hotel",
#             'city_name': "New York",
#             'room_type': "Spacious Room",
#             'rating': 4.5,
#             'price': 250
#         }

#         gemini_service = GeminiService()

#         # Act
#         result = gemini_service.generate_property_description(property_data)

#         # Assert
#         self.assertEqual(result, "This luxurious hotel in New York offers spacious rooms with modern amenities, perfect for both business and leisure travelers.")
#         mock_post.assert_called_once()

#     @patch('llmApp.services.gemini_service.requests.post')
#     def test_generate_property_summary(self, mock_post):
#         # Arrange
#         mock_response = MagicMock()
#         mock_response.json.return_value = {
#             'candidates': [{
#                 'content': {
#                     'parts': [{
#                         'text': "This is a great hotel in New York with excellent service and amenities."
#                     }]
#                 }
#             }]
#         }
#         mock_post.return_value = mock_response
        
#         property_data = {
#             'property_title': "Luxury Hotel",
#             'city_name': "New York",
#             'price': 250,
#             'rating': 4.5
#         }

#         gemini_service = GeminiService()

#         # Act
#         result = gemini_service.generate_property_summary(property_data)

#         # Assert
#         self.assertEqual(result, "This is a great hotel in New York with excellent service and amenities.")
#         mock_post.assert_called_once()

#     @patch('llmApp.services.gemini_service.requests.post')
#     def test_generate_property_review(self, mock_post):
#         # Arrange
#         mock_response = MagicMock()
#         mock_response.json.return_value = {
#             'candidates': [{
#                 'content': {
#                     'parts': [{
#                         'text': "RATING: 4\nREVIEW: The hotel offers a great stay with spacious rooms, excellent service, and a central location."
#                     }]
#                 }
#             }]
#         }
#         mock_post.return_value = mock_response
        
#         property_data = {
#             'property_title': "Luxury Hotel",
#             'city_name': "New York",
#             'price': 250,
#             'rating': 4.5
#         }

#         gemini_service = GeminiService()

#         # Act
#         rating, review = gemini_service.generate_property_review(property_data)

#         # Assert
#         self.assertEqual(rating, 4.0)
#         self.assertEqual(review, "The hotel offers a great stay with spacious rooms, excellent service, and a central location.")
#         mock_post.assert_called_once()

# if __name__ == '__main__':
#     unittest.main()
