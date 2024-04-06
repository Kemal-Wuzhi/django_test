# Generated by Django 4.2.11 on 2024-04-06 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='category_id',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='location_id',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='ticket_id',
        ),
        migrations.RemoveField(
            model_name='campaign',
            name='website_id',
        ),
        migrations.RemoveField(
            model_name='campaignunitrelation',
            name='campaign_id',
        ),
        migrations.RemoveField(
            model_name='campaignunitrelation',
            name='unit_id',
        ),
        migrations.AddField(
            model_name='campaign',
            name='category',
            field=models.ForeignKey(blank=True, db_column='CategoryID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.category'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='location',
            field=models.ForeignKey(blank=True, db_column='LocationID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.campaignlocationinfo'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='ticket',
            field=models.ForeignKey(blank=True, db_column='TicketID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.ticket'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='website',
            field=models.ForeignKey(blank=True, db_column='WebsiteID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.website'),
        ),
        migrations.AddField(
            model_name='campaignunitrelation',
            name='campaign',
            field=models.ForeignKey(blank=True, db_column='UID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.campaign'),
        ),
        migrations.AddField(
            model_name='campaignunitrelation',
            name='unit',
            field=models.ForeignKey(blank=True, db_column='UnitID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.unit'),
        ),
    ]