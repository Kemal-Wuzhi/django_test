import json
from django.db.utils import IntegrityError
from datetime import datetime

# TODO modify data insert function to implement data correlation structure.
# handle primary key and foreign key


def insert_campaign_data(file_path):
    from main.models import Campaign, CampaignLocationInfo, Category, Ticket, Unit, Website, CampaignUnitRelation
    try:
        with open(file_path, 'r') as file:
            campaigns = json.load(file)
            print("CAMPAIGNS:", campaigns)

            for c in campaigns:

                # handle datetime formate, strpt = string parse time strft = string formate time
                start_d_object = datetime.strptime(c['startDate'], '%Y/%m/%d')
                end_d_object = datetime.strptime(c['endDate'], '%Y/%m/%d')
                correct_start = start_d_object.strftime("%Y-%m-%d")
                correct_end = end_d_object.strftime("%Y-%m-%d")
                c['startDate'] = correct_start
                c['endDate'] = correct_end

                campaign = Campaign.objects.create(
                    version=c.get('version'),
                    title=c.get('title'),
                    description_html=c.get('descriptionFilterHtml'),
                    image_url=c.get('imageUrl'),
                    comment=c.get('comment'),
                    start_date=c.get('startDate'),
                    end_date=c.get('endDate'),
                    hit_rate=c.get('hitRate')
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

                # check unit type
                for unit_type in ['showUnit', 'supportUnit', 'subUnit', 'masterUnit', 'otherUnit']:
                    units = c.get(unit_type, [])
                    print('UNITS:', units)
                    if not isinstance(units, list):
                        units = [units]

                    for unit_name in units:
                        if unit_name:
                            unit, _ = Unit.objects.get_or_create(
                                unitname=unit_name,
                                defaults={'unittype': unit_type}
                            )
                            CampaignUnitRelation.objects.get_or_create(
                                campaign=campaign,
                                unit=unit,
                                defaults={'relation_type': unit_type}
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
