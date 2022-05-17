# Generated by Django 4.0.2 on 2022-05-17 13:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statementReader', '0006_realizedandunrealizedperformancesummary'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenPositions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=100)),
                ('assetClass', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=100)),
                ('quantity', models.DecimalField(decimal_places=10, max_digits=19)),
                ('mult', models.DecimalField(decimal_places=10, max_digits=19)),
                ('cost_price', models.DecimalField(decimal_places=10, max_digits=19)),
                ('cost_basis', models.DecimalField(decimal_places=10, max_digits=19)),
                ('close_price', models.DecimalField(decimal_places=10, max_digits=19)),
                ('value', models.DecimalField(decimal_places=10, max_digits=19)),
                ('unrealized_PL', models.DecimalField(decimal_places=10, max_digits=19)),
                ('code', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.AlterField(
            model_name='marktomarketperformancesummary',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='netassetvalue',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='realizedandunrealizedperformancesummary',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
