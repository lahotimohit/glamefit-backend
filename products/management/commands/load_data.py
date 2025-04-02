import pandas as pd
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Load product data from Excel"

    def handle(self, *args, **kwargs):
        file_path = "./styles.csv"
        df = pd.read_csv(file_path)

        products = [
            Product(
                gender=row["gender"],
                master_category=row["masterCategory"],
                sub_category=row["subCategory"],
                article_type=row["articleType"],
                base_colour=row["baseColour"],
                product_display_name=row["productDisplayName"],
                imageURL=row["imageURL"],
            )
            for _, row in df.iterrows()
        ]

        Product.objects.bulk_create(products)
        self.stdout.write(self.style.SUCCESS("Data loaded successfully!"))
