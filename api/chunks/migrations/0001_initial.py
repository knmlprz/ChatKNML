# Generated by Django 4.2.13 on 2024-06-02 10:10

from django.db import migrations, models
import django.db.models.deletion
import pgvector.django


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("documents", "0002_remove_document_embedding"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chunk",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=100)),
                ("embedding", pgvector.django.VectorField(dimensions=4096)),
                ("chunk_idx", models.IntegerField()),
                ("start_char", models.IntegerField()),
                ("end_char", models.IntegerField()),
                (
                    "document_idx",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="documents.document",
                    ),
                ),
            ],
        ),
    ]
