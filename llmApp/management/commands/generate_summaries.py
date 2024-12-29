# llmApp/management/commands/generate_summaries.py
from django.core.management.base import BaseCommand
from django.db import transaction
from llmApp.models import Hotel, PropertySummary
from llmApp.services.ollama_service import OllamaService
import time

class Command(BaseCommand):
    help = 'Generate summaries for hotels using Ollama'

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
        
        # Get hotels without summaries
        hotels = Hotel.objects.filter(summaries__isnull=True)
        total_hotels = hotels.count()
        
        self.stdout.write(f"Found {total_hotels} hotels without summaries")

        for i in range(0, total_hotels, batch_size):
            batch = hotels[i:i + batch_size]
            self.stdout.write(f"Processing batch {i//batch_size + 1}")

            for hotel in batch:
                try:
                    with transaction.atomic():
                        self.generate_hotel_summary(hotel, ollama_service)
                        time.sleep(1)  # Prevent overwhelming the API
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f"Error processing hotel {hotel.id}: {str(e)}")
                    )

    def generate_hotel_summary(self, hotel, ollama_service):
        self.stdout.write(f"Generating summary for hotel: {hotel.property_title}")
        
        property_data = {
            'property_title': hotel.property_title,
            'city_name': hotel.city_name,
            'address': hotel.address,
            'price': str(hotel.price),
            'rating': str(hotel.rating),
            'room_type': hotel.room_type,
            'description': hotel.description
        }

        summary = ollama_service.generate_property_summary(property_data)
        
        if summary:
            PropertySummary.objects.create(
                property=hotel,
                summary=summary
            )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully generated summary for: {hotel.property_title}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"Could not generate summary for: {hotel.property_title}")
            )