# Generated by Django 4.2 on 2023-08-27 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_product_stripe_product_price_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="images",
            options={"verbose_name": "фотография", "verbose_name_plural": "фотографии"},
        ),
        migrations.AddField(
            model_name="product",
            name="gb",
            field=models.IntegerField(default=128),
        ),
    ]
