from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="color_label",
            field=models.CharField(blank=True, max_length=60),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="size_label",
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
