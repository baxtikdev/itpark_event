# Generated by Django 4.0.9 on 2023-02-08 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DevicesService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('theme', models.CharField(max_length=256)),
                ('file', models.FileField(blank=True, null=True, upload_to='order_files')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('finish_time', models.TimeField()),
                ('people_number', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('devices', models.ManyToManyField(blank=True, to='orders.devicesservice')),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SnacksService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_snack_quantity', to='orders.order')),
                ('snack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.snacksservice')),
            ],
            options={
                'verbose_name': 'Snack',
                'verbose_name_plural': 'Number of Snacks',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.place'),
        ),
    ]
