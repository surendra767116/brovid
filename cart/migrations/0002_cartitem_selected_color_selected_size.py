from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="selected_color",
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="selected_size",
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddConstraint(
            model_name="cartitem",
            constraint=models.UniqueConstraint(
                fields=("cart", "product", "selected_size", "selected_color"),
                name="unique_cart_item_variant",
            ),
        ),
    ]
