# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavi` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Campaign(models.Model):
    uid = models.AutoField(db_column='UID', primary_key=True) 
    version = models.CharField(db_column='Version', max_length=255, blank=True, null=True)  
    title = models.CharField(db_column='Title', max_length=255, blank=True, null=True)  
    description_html = models.TextField(db_column='DescriptionHtml', blank=True, null=True)  
    image_url = models.CharField(db_column='ImageURL', max_length=255, blank=True, null=True)  
    comment = models.TextField(db_column='Comment', blank=True, null=True)  
    edit_modify_date = models.DateTimeField(db_column='EditModifyDate', blank=True, null=True)  
    start_date = models.DateField(db_column='StartDate', blank=True, null=True)  
    end_date = models.DateField(db_column='EndDate', blank=True, null=True)  
    hit_rate = models.IntegerField(db_column='HitRate', blank=True, null=True)  
    category_id = models.IntegerField(db_column='CategoryID', blank=True, null=True)  
    website_id = models.IntegerField(db_column='WebsiteID', blank=True, null=True)  
    location_id = models.IntegerField(db_column='LocationID', blank=True, null=True)  
    ticket_id = models.IntegerField(db_column='TicketID', blank=True, null=True)  

    class Meta:
        db_table = 'Campaign'

class CampaignUnitRelation(models.Model):
    relation_id = models.AutoField(db_column='RelationID', primary_key=True)  
    campaign_id = models.IntegerField(db_column='CampaignID', blank=True, null=True)  
    unit_id = models.IntegerField(db_column='UnitID', blank=True, null=True)  
    relation_type = models.CharField(db_column='RelationType', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'CampaignUnitRelation'

class CampaignLocationInfo(models.Model):
    location_id = models.AutoField(db_column='LocationID', primary_key=True)  
    address = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  
    location_name = models.CharField(db_column='LocationName', max_length=255, blank=True, null=True)  
    latitude = models.DecimalField(db_column='Latitude', max_digits=10, decimal_places=5, blank=True, null=True)  
    longitude = models.DecimalField(db_column='Longitude', max_digits=10, decimal_places=5, blank=True, null=True)  

    class Meta:
        db_table = 'Campaign_Location_Info'

class Category(models.Model):
    category_id = models.AutoField(db_column='CategoryID', primary_key=True)  
    category_name = models.CharField(db_column='CategoryName', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'Category'

class Ticket(models.Model):
    ticket_id = models.AutoField(db_column='TicketID', primary_key=True)  
    on_sales = models.BooleanField(db_column='OnSales', blank=True, null=True)  
    discount_info = models.CharField(db_column='DiscountInfo', max_length=255, blank=True, null=True)  
    price_description = models.CharField(db_column='Price', max_length=255, blank=True, null=True)  
    end_time = models.DateTimeField(db_column='EndTime', blank=True, null=True)  

    class Meta:
        db_table = 'Ticket'

class Unit(models.Model):
    unitid = models.AutoField(db_column='UnitID', primary_key=True)  
    unitname = models.CharField(db_column='UnitName', max_length=255, blank=True, null=True)  
    unittype = models.CharField(db_column='UnitType', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'Unit'

class Website(models.Model):
    websiteid = models.AutoField(db_column='WebsiteID', primary_key=True)  
    websales = models.CharField(db_column='WebSales', max_length=255, blank=True, null=True)  
    sourcewebpromote = models.CharField(db_column='SourceWebPromote', max_length=255, blank=True, null=True)  
    sourcewebname = models.CharField(db_column='SourceWebName', max_length=255, blank=True, null=True)  

    class Meta:
        db_table = 'Website'


