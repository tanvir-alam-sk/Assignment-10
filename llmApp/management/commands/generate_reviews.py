# llmApp/management/commands/generate_reviews.py
from django.core.management.base import BaseCommand
from django.db import transaction
from llmApp.models import Hotel, PropertyReview
from llmApp.services.ollama_service import OllamaService
import time

class Command(BaseCommand):
    help = 'Generate reviews for hotels using Ollama'

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=2,
            help='Number of hotels to process in each batch'
        )

    def handle(self, *args, **kwargs):
        batch_size = kwargs['batch_size']
        ollama_service = OllamaService()
        
        # Get hotels without reviews
        hotels = Hotel.objects.filter(reviews__isnull=True)
        total_hotels = hotels.count()
        
        self.stdout.write(f"Found {total_hotels} hotels without reviews")

        for i in range(0, total_hotels, batch_size):
            batch = hotels[i:i + batch_size]
            self.stdout.write(f"Processing batch {i//batch_size + 1}")

            for hotel in batch:
                try:
                    with transaction.atomic():
                        self.generate_hotel_review(hotel, ollama_service)
                        time.sleep(1)  # Prevent overwhelming the API
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error processing hotel {hotel.id}: {str(e)}")
                    )

    def generate_hotel_review(self, hotel, ollama_service):
        self.stdout.write(f"Generating review for hotel: {hotel.property_title}")
        
        property_data = {
            'property_title': hotel.property_title,
            'city_name': hotel.city_name,
            'address': hotel.address,
            'price': str(hotel.price),
            'rating': str(hotel.rating),
            'room_type': hotel.room_type,
            'description': hotel.description
        }

        rating, review = ollama_service.generate_property_review(property_data)
        
        if review:
            PropertyReview.objects.create(
                property=hotel,
                rating=rating,
                review=review
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully generated review for: {hotel.property_title}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Could not generate review for: {hotel.property_title}")
            )