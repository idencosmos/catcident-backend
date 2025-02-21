# uploads/migrations/0001_initial.py
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('is_used_cached', models.BooleanField(default=False, editable=False)),
            ],
            options={
                'verbose_name': 'Media File',
                'verbose_name_plural': 'Media Files',
            },
        ),
    ]