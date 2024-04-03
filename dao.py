import json
from django.db.utils import IntegrityError


# TODO modify data insert function to implement data correlation structure.
# handle primary key and foreign key
def insert_campaign_data(file_path):
    from main.models import Campaign, CampaignLocationInfo, Category, Ticket, Unit, Website
    try:
        with open(file_path, 'r') as file:
            campaigns = json.load(file)
            print("CAMPAIGNS:", campaigns)
            for c in campaigns:
                campaign = Campaign.objects.create(
                    version=c.get('version'),
                    title=c.get('title'),
                    description_html=c.get('description_html'),
                    image_url=c.get('image_url'),
                    comment=c.get('comment'),
                    start_date=c.get('start_date'),
                    end_date=c.get('end_date'),
                    hit_rate=c.get('hit_rate')
                )

                CampaignLocationInfo.objects.create(
                    campaign=campaign,
                    address=c.get('address'),
                    location_name=c.get('location_name'),
                    latitude=c.get('latitude'),
                    longitude=c.get('longitude')
                )

                Category.objects.create(
                    category_name=c.get('category_name')
                )

                Ticket.objects.create(
                    campaign=campaign,
                    on_sales=c.get('on_sale'),
                    discount_info=c.get('discount_info'),
                    price_description=c.get('price_description'),
                    end_time=c.get('end_time')
                )

                Unit.objects.create(
                    campaign=campaign,
                    unitname=c.get('unitname'),
                    unittype=c.get('unittype')
                )

                Website.objects.create(
                    campaign=campaign,
                    websales=c.get('websales'),
                    sourcewebpromote=c.get('sourcewebpromote'),
                    sourcewebname=c.get('sourcewebname')
                )

    except FileNotFoundError:
        print(f'The file {file_path} does not exist')
    except json.JSONDecodeError:
        print('Failed to decode the JSON file')
    except IntegrityError as e:
        print(f'Failed to insert a record due to integrity error: {e}')
    except Exception as e:
        print(f'An error occurred while processing the campaign data: {e}')
