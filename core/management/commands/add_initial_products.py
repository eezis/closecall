from django.core.management.base import BaseCommand
from core.models import Product


class Command(BaseCommand):
    help = 'Add initial products to the database'

    def handle(self, *args, **kwargs):
        products = [
            {
                'name': 'Continental Grand Prix 5000',
                'description': 'High-performance road bike tire featuring BlackChili compound for exceptional grip and low rolling resistance. Perfect for training and racing.',
                'amazon_asin': 'B088NN1S36',
                'amazon_url': 'https://www.amazon.com/Continental-Grand-Prix-5000-Black-BW/dp/B088NN1S36/',
                'category': 'tires',
                'is_featured': True,
                'order': 1,
            },
            {
                'name': 'Continental GatorSkin DuraSkin',
                'description': 'Durable puncture-resistant tire ideal for commuting and training. Features DuraSkin sidewall protection for long-lasting performance.',
                'amazon_asin': 'B01JN4YEDW',
                'amazon_url': 'https://www.amazon.com/Continental-GatorSkin-DuraSkin-2-Count-Folding/dp/B01JN4YEDW/',
                'category': 'tires',
                'order': 2,
            },
            {
                'name': 'Garmin Varia Radar with Camera',
                'description': 'Rearview radar with built-in camera that detects vehicles up to 140 meters away and continuously records your ride. Essential safety device for cyclists.',
                'amazon_asin': 'B09T5VBDPC',
                'amazon_url': 'https://www.amazon.com/Garmin-VariaTM-Continuous-Recording-Detection/dp/B09T5VBDPC/',
                'category': 'cameras',
                'is_featured': True,
                'order': 3,
            },
            {
                'name': 'Giro Isode MIPS Helmet',
                'description': 'Affordable MIPS-equipped helmet offering excellent protection with integrated Multi-Directional Impact Protection System.',
                'amazon_asin': 'B0CRVR6Z1V',
                'amazon_url': 'https://www.amazon.com/Giro-Isode-Recreational-Cycling-Helmet/dp/B0CRVR6Z1V/',
                'category': 'helmets',
                'order': 4,
            },
            {
                'name': 'Schwinn Thrasher Lightweight Helmet',
                'description': 'Budget-friendly helmet with dial-fit adjustment system and built-in ventilation for comfort during rides.',
                'amazon_asin': 'B00012M5MS',
                'amazon_url': 'https://www.amazon.com/Schwinn-Lightweight-Microshell-Featuring-Adjustment/dp/B00012M5MS/',
                'category': 'helmets',
                'order': 5,
            },
        ]

        for product_data in products:
            product, created = Product.objects.update_or_create(
                amazon_asin=product_data['amazon_asin'],
                defaults=product_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully added all initial products'))