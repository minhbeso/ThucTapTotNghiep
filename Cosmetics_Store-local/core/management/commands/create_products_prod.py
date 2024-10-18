from django.core.management.base import BaseCommand
from core.models import Product, Category, Brand
import cloudinary.uploader


class Command(BaseCommand):
    help = "Create initial products, categories, and brands"

    def handle(self, *args, **kwargs):
        # Create products
        folder = "media/images/products/"
        products = [
            {
                
                "name": "Son môi Yves Saint Laurent",
                "description": "Son Yves Saint Laurent",
                "price": 729000.0,
                "old_price": 0.0,
                "quantity": 0,
                "image": "media/images/products/product_28.jpg",
                "category": "Son môi",
                "brand": "Yves Saint Laurent",
            },
            {
                
                "name": "Nước hoa Yves Saint Laurent Black",
                "description": "Nước hoa Yves Saint Laurent",
                "price": 1350000.0,
                "old_price": 0.0,
                "quantity": 35,
                "image": "media/images/products/product_27.jpg",
                "category": "Nước hoa",
                "brand": "Yves Saint Laurent",
            },
            {
                
                "name": "Nước hoa Chloé Eau de Parfum",
                "description": "Nước hoa Chloé",
                "price": 1450000.0,
                "old_price": 1600000.0,
                "quantity": 24,
                "image": "media/images/products/product_26.jpg",
                "category": "Nước hoa",
                "brand": "Chloé",
            },
            {
                
                "name": "Phấn nền bare Minerals Original",
                "description": "Trang điểm Minerals",
                "price": 560000.0,
                "old_price": 0.0,
                "quantity": 66,
                "image": "media/images/products/product_25.jpg",
                "category": "Trang điểm",
                "brand": "Minerals",
            },
            {
                
                "name": "Sữa tắm dạng kem Victoria's Secret",
                "description": "Sữa tắm Victoria's Secret",
                "price": 860000.0,
                "old_price": 980000.0,
                "quantity": 16,
                "image": "media/images/products/product_29.jpg",
                "category": "Sữa tắm",
                "brand": "Victoria",
            },
            {
                
                "name": "Sữa tắm Sparkling Citrus làm mượt da",
                "description": "Sữa tắm Sparkling Citrus",
                "price": 1200000.0,
                "old_price": 1300000.0,
                "quantity": 0,
                "image": "media/images/products/product_24.jpg",
                "category": "Sữa tắm",
                "brand": "Sparkling Citrus",
            },
            {
                
                "name": "Nước hoa Versace Bright Crystal",
                "description": "Nước hoa Versace",
                "price": 1800000.0,
                "old_price": 0.0,
                "quantity": 24,
                "image": "media/images/products/product_23.jpg",
                "category": "Nước hoa",
                "brand": "Versace",
            },
            {
                
                "name": "Mascara Benefit They're Real",
                "description": "Trang điểm Benefit",
                "price": 480000.0,
                "old_price": 0.0,
                "quantity": 11,
                "image": "media/images/products/product_22.jpg",
                "category": "Trang điểm",
                "brand": "Benefit",
            },
            {
                
                "name": "Son môi Christian Louboutin Silky",
                "description": "Son môi Christian Louboutin",
                "price": 1800000.0,
                "old_price": 0.0,
                "quantity": 45,
                "image": "media/images/products/product_21.jpg",
                "category": "Son môi",
                "brand": "Christian Louboutin",
            },
            {
                
                "name": "Kem lót Burberry Fresh Glow",
                "description": "Kem dưỡng da Burberry",
                "price": 960000.0,
                "old_price": 0.0,
                "quantity": 22,
                "image": "media/images/products/product_20.jpg",
                "category": "Kem dưỡng da",
                "brand": "Burberry",
            },
            {
                
                "name": "Sữa tắm Sparkling Citrus Luscious Crush",
                "description": "Sữa tắm Sparkling Citrus",
                "price": 1040000.0,
                "old_price": 0.0,
                "quantity": 44,
                "image": "media/images/products/product_9.jpg",
                "category": "Sữa tắm",
                "brand": "Sparkling Citrus",
            },
            {
                
                "name": "Sữa tắm dưỡng ẩm cho da",
                "description": "Sữa tắm AHA",
                "price": 600000.0,
                "old_price": 0.0,
                "quantity": 12,
                "image": "media/images/products/product_10.jpg",
                "category": "Sữa tắm",
                "brand": "AHA",
            },
            {
                
                "name": "Sữa tắm hương dâu dịu mát",
                "description": "Sữa tắm AHA",
                "price": 1400000.0,
                "old_price": 1500000.0,
                "quantity": 2,
                "image": "media/images/products/product_8.jpg",
                "category": "Sữa tắm",
                "brand": "AHA",
            },
            {
                
                "name": "Sữa tắm làm sáng da Victoria's Secret",
                "description": "Sữa tắm Victoria's Secret",
                "price": 1400000.0,
                "old_price": 0.0,
                "quantity": 53,
                "image": "media/images/products/product_7.jpg",
                "category": "Sữa tắm",
                "brand": "Victoria",
            },
            {
                
                "name": "Nước hoa Lancôme La Vie Est",
                "description": "Nước hoa Lancôme",
                "price": 1240000.0,
                "old_price": 0.0,
                "quantity": 34,
                "image": "media/images/products/product_6.jpg",
                "category": "Nước hoa",
                "brand": "Lancôme",
            },
            {
                
                "name": "Son dưỡng Tonymoly Mini Cherry",
                "description": "Son môi Tonymoly",
                "price": 200000.0,
                "old_price": 220000.0,
                "quantity": 98,
                "image": "media/images/products/product_5.jpg",
                "category": "Son môi",
                "brand": "Tonymoly",
            },
            {
                
                "name": "Tinh chất dưỡng da SK-II Facial",
                "description": "Kem dưỡng da SK-II",
                "price": 4000000.0,
                "old_price": 4100000.0,
                "quantity": 20,
                "image": "media/images/products/product_4.jpg",
                "category": "Kem dưỡng da",
                "brand": "SK-II",
            },
            {
                
                "name": "Nước làm sạch mặt Ibuki Softening",
                "description": "Kem dưỡng da Benefit",
                "price": 700000.0,
                "old_price": 0.0,
                "quantity": 200,
                "image": "media/images/products/product_3.jpg",
                "category": "Kem dưỡng da",
                "brand": "Benefit",
            },
            {
                
                "name": "Kem dưỡng ẩm L'Occitane Pivoine",
                "description": "Kem dưỡng da L'Occitane",
                "price": 840000.0,
                "old_price": 0.0,
                "quantity": 100,
                "image": "media/images/products/product_2.jpg",
                "category": "Kem dưỡng da",
                "brand": "L'Occitane",
            },
            {
                
                "name": "Sữa tắm Victoria's Secret quyến rũ",
                "description": "Sữa tắm Victoria's Secret",
                "price": 560000.0,
                "old_price": 0.0,
                "quantity": 10,
                "image": "media/images/products/product_1.jpg",
                "category": "Sữa tắm",
                "brand": "Victoria",
            },
        ]

        for product_data in products:
            brand, _ = Brand.objects.get_or_create(name=product_data["brand"])
            category, _ = Category.objects.get_or_create(name=product_data["category"])

            upload_result = cloudinary.uploader.upload(
                product_data["image"],
                folder="media/images/products/",
            )
            image_url = f'{folder}{upload_result['display_name']}.{upload_result['format']}'

            product = Product.objects.create(
                brand=brand,
                category=category,
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                old_price=product_data.get("old_price", None),
                quantity=product_data["quantity"],
                image=image_url,
            )
            self.stdout.write(self.style.SUCCESS(f"Created product {product.name}"))
