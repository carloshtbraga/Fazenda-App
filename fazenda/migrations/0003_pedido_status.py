# Generated by Django 4.2.7 on 2023-11-24 21:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fazenda", "0002_alter_pedido_data_pedido"),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="status",
            field=models.CharField(
                choices=[("Pendente", "Pendente"), ("Concluído", "Concluído")],
                default="Pendente",
                max_length=10,
            ),
        ),
    ]