import json
from django.db import connection
from django.db.utils import IntegrityError
from datetime import datetime


def insert_campaign_data(file_path):
    from main.models import Campaign, CampaignLocationInfo, Unit, CampaignUnitRelation, Ticket, Website

    try:
        with open(file_path, 'r') as file:
            show_data = json.load(file)
        for data in show_data:
            # CAMPAIGN
            start_d_object = datetime.strptime(data['startDate'], '%Y/%m/%d')
            end_d_object = datetime.strptime(data['endDate'], '%Y/%m/%d')
            data['startDate'] = start_d_object.strftime("%Y-%m-%d")
            data['endDate'] = end_d_object.strftime("%Y-%m-%d")

            campaign, created = Campaign.objects.get_or_create(
                uid=data['UID'],
                defaults={
                    'version': data.get('version'),
                    'title': data.get('title'),
                    'description_html': data.get('descriptionFilterHtml'),
                    'image_url': data.get('imageUrl'),
                    'comment': data.get('comment'),
                    'start_date': data['startDate'],
                    'end_date': data['endDate'],
                    'hit_rate': data.get('hitRate'),
                }
            )
            # LOCATION
            location_list = set()
            for item in data['showInfo']:
                location_list.add(item['locationName'].strip())

            for location_name in location_list:
                CampaignLocationInfo.objects.get_or_create(
                    location_name=location_name
                )
            # TICKET
            ticket_set = set(item['price'] for item in data['showInfo'])
            for price in ticket_set:
                Ticket.objects.get_or_create(
                    price_description=price
                )
            # UNIT
            for unit_type in ['showUnit', 'supportUnit', 'subUnit', 'masterUnit', 'otherUnit']:
                units = data.get(unit_type, [])
                if not isinstance(units, list):
                    units = [units]
                for unit_name in units:
                    unit, _ = Unit.objects.get_or_create(
                        unitname=unit_name,
                        defaults={'unittype': unit_type}
                    )
                    CampaignUnitRelation.objects.get_or_create(
                        campaign=campaign,
                        unit=unit,
                        defaults={'relation_type': unit_type}
                    )
            # WEBSITE
            webiste_list = set()
            if data['soureWebPromote']:
                webiste_list.add(data['soureWebPromote'])
            for web_info in webiste_list:
                Website.objects.get_or_create(
                    source_web_name=data['sourceWebName'],
                    web_sales=data['webSales'],
                    source_web_promote=web_info,
                )

    except FileNotFoundError:
        print(f'The file {file_path} does not exist')
    except json.JSONDecodeError:
        print('Failed to decode the JSON file')
    except Exception as e:
        print(f'An error occurred: {str(e)}')


# For campaign foreign id
locations_data = {1: '台北捷運音樂進站', 2: '國立臺灣交響樂團', 3: '陽明交大演藝廳', 4: '高雄市文化中心至善廳', 5: '嘉義市政府文化局音樂廳', 6: '國家音樂廳', 7: '臺中市屯區藝文中心演藝廳', 8: '衛武營國家藝術文化中心音樂廳', 9: '高雄市現代化綜合體育館﹝高雄巨蛋﹞', 10: '苗栗縣苗北藝文中心', 11: '高雄市政府文化局﹝高雄市文化中心﹞', 12: '金沙鎮（金門縣）', 13: '衛武營國家藝術文化中心', 14: '衛武營國家藝術文化中心戲劇院', 15: '高雄市駁二藝術特區', 16: '金門文化園區', 17: '金湖鎮（金門縣）', 18: '烈嶼鄉（金門縣）', 19: '金寧鄉（金門縣）', 20: '國立中正紀念堂管理處', 21: '國家兩廳院演奏廳', 22: '日月潭國家風景區', 23: '臺中國家歌劇院 中劇院', 24: '衛武營國家藝術文化中心表演廳', 25: '苗栗縣泰雅原住民文化產業區', 26: '國家兩廳院表演聽', 27: '台中國家歌劇院小劇場', 28: '衛武營國家藝術文化中心表演聽', 29: '誠品表演廳', 30: '苗栗縣賽夏族民俗文物館', 31: '國家兩廳院 演奏廳', 32: '大東文化藝術中心演藝廳', 33: '大園區（桃園市）', 34: '橫山書法藝術館', 35: '臺中市葫蘆墩文化中心', 36: '衛武營國家藝術文化中心 音樂廳', 37: '臺中國家歌劇院 大劇院', 38: '國家兩廳院 國家音樂廳', 39: '國立臺中教育大學', 40: '高雄市文化中心至德堂', 41: '板橋區（新北市）', 42: '苗栗市（苗栗縣）', 43: '益品美術館', 44: '信義鄉（南投縣）', 45: '雲林縣政府文化觀光處', 46: '中寮鄉（南投縣）', 47: '魚池鄉（南投縣）', 48: '埔里鎮（南投縣）', 49: '苗栗縣政府文化觀光局', 50: '西屯區（臺中市）', 51: '鹿谷鄉（南投縣）', 52: '花蓮縣文化局', 53: '霧峰林家宮保第園區', 54: '中原大學', 55: '松山文化創意園區', 56: '桃園市平鎮區婦幼活動中心',
                  57: '南崁兒童藝術村', 58: '八德區（桃園市）', 59: '蘆竹區（桃園市）', 60: '桃園市立圖書館總館', 61: '功學社音樂廳', 62: '嘉義市政府文化局', 63: '桃園展演中心', 64: '國立臺灣工藝研究發展中心（臺灣工藝文化園區）', 65: '西區（臺中市）', 66: '桃園市大園區竹圍國民小學', 67: '國家兩廳院', 68: '懷舊系列IV民歌暖壽PA', 69: '國立東華大學', 70: '南投縣埔里藝文中心', 71: '彰化縣員林演藝廳', 72: '臺中國家歌劇院小劇場', 73: '桃園北區客家會館', 74: '桃園市中壢區社福館', 75: '桃園市客家文化館', 76: '臺灣戲曲中心小表演廳3202排練廳', 77: '楊梅區（桃園市）', 78: '中壢藝術館', 79: '臺中市港區藝術中心', 80: '六龜區（高雄市）', 81: '嘉義縣表演藝術中心演藝廳', 82: '臺南市新營文化中心', 83: '臺北市中山堂', 84: '台北新兒童樂園—如果兒童劇場', 85: '台北新兒童樂園—如果兒童劇團', 86: '金城鎮（金門縣）', 87: '嘉義縣表演藝術中心', 88: '澎湖縣政府文化局', 89: '民主大道', 90: '國立臺灣交響樂團演奏廳 NTSO Concert Hall', 91: '雲林表演廳 Yunlin Performance Hall', 92: '臺中市葫蘆墩文化中心 Taichung City Huludun Cultural Center', 93: '新竹市文化局演藝廳 Hsinchu City Performance Hall', 94: '花蓮縣文化局演藝廳 Performance Hall of Hualien County', 95: '宜蘭演藝廳 Yilan Performing Arts Center', 96: '臺中國家歌劇院中劇院', 97: '臺南文化中心', 98: '臺中市大墩文化中心', 99: '南屯區（臺中市）', 100: '高雄國家體育場﹝2009世運會主場館﹞', 101: '高雄流行音樂中心', 102: '竹山鎮（南投縣）', 103: '時代的情書'}

# tickets_data = {1: '', 2: '300', 3: '600、400、300', 4: '300/500/800/1200', 5: '1850、1550、1250、950、650', 6: '1550、1250、950、650', 7: '座位區+1680;座位區+2080;座位區+2480;座位區+2880;座位區+3280;座位區+3680;搖滾站區+1280;搖滾站區+3480', 8: '票價+400;票價+600;票價+800;票價+1000;票價+1200;票價+1500;票價+1800;票價+2200', 9: '--+600;--+900;--+1200;--+1500;--+1800;--+2000', 10: '2500、2000、1500、1000、500', 11: '/+300;/+500;/+800;/+1200', 12: '500、300、200', 13: '票價： 500 、800', 14: '2500、2000、1600、1200、900、500', 15: '1200、800、500、300', 16: '200', 17: '500、300', 18: '1200、1000、800、600', 19: '票價： 800 、1,200 、1,600 、2,000', 20: ' 票價： 800 、1,200 、1,600 、2,000', 21: '2500、2000、1500、1000', 22: '全票+30;團體票+20;優待票+10', 23: ' NT$500、800、1000 (兩廳院 Opentix) ', 24: '800、500、300', 25: '600/800/1000/1200/1500/1800元  \r\n\r\n（*另本場演出參與文化部青年席位計畫，持文化幣購買可享折扣，席位有限、售完為止）', 26: '全票+300', 27: '600', 28: '門票+100', 29: ' 600 、800 、1,000 、1,200 、1,500 、1,800', 30: '全票+200', 31: '1000、800、600、400', 32: '票價+250', 33: 'NT$500、800、1000 (兩廳院 Opentix) ', 34: '全票+3200;全票+2800;全票+2400;全票+2000;全票+1600;全票+1200', 35: '全票+250;12歲以上學生、65歲以上老人、台中市民+200;6歲以上學童票+125', 36: '票價+300', 37: '票價+200', 38: '/+500;/+800;/+1200;/+1500;/+2000;/+3000', 39: '票價：800、1000\r\n優惠折扣：4/25前購票8折、身障者5折', 40: '全票+100;全票+300', 41: '票價+100', 42: '/+400;/+700;/+1000;/+1500;/+1800;/+2400;/+3000',
#                 43: '票價：NT$500、800、1200、1500、2000、3000，購票請上TixFun購票網。', 44: '票價： NT$500、800、1200、1500、2000、3000，購票請上TixFun購票網。', 45: '票價：500', 46: '票價：500、700', 47: '票價：350、700', 48: '100', 49: '150', 50: '博幼票+450;兒童票+700;成人票、學生票+780', 51: '票價+100;票價+200', 52: '票價 |\r\n400/600/800\r\n', 53: '300、200', 54: '票價： 600 、800 、1,200', 55: '5000、3000、2000、1000、500', 56: '/+500', 57: ' 票價： 300 、500 、800 、1,000\r\n\r\n折扣方案\r\n\r\n◎身心障礙人士及陪同者1名購票5折優待，入場時應出示身心障礙手冊，陪同者與身障者需同時入場\r\n\r\n◎早鳥票：即日起至4月3日23時59分前，購買享8折優惠\r\n\r\n◎團體票：10張(含)以上8折\r\n\r\n◎兩廳院會員：9折\r\n\r\n◎敬老票：65歲以上年長者購票可享5折優惠，入場時請出示證件\r\n\r\n◎青年席位專屬優惠：提供每席票價300元之限量青年專屬席位（需搭配使用文化幣100點以上折抵）。\r\n\r\n持青年席位票券者，請憑證件（身分證或健保卡）入場」，並將驗票出示身分切換為「出示證件」', 58: '票價:150/300/500/650', 59: '--+100', 60: '全票+800', 61: '--+500;--+800;--+1200;--+1800;--+2400', 62: '--+500;--+800;--+1000;--+1200;--+1500', 63: '--+300;--+2400;--+2800;--+3200;--+3600;--+3900;--+4800', 64: '/+500;/+900;/+1200;/+2500', 65: '--+800;--+1200;--+1600;--+2000', 66: '全票+600', 67: '看台區+880;看台區+1280;看台區+1880;看台區+2280;看台區+2880;漫遊站區｜人生海海 漫遊站區+2280;對號座席｜瘋狂世界搖滾區+2880;對號座席｜瘋狂世界搖滾區+3280;對號座席｜瘋狂世界搖滾區+3880;對號座席｜瘋狂世界搖滾區+4580', 68: '--+350', 69: '--+500', 70: '--+400', 71: ' 票價：NT$500、800、1200、1500、2000、3000，購票請上TixFun購票網。', 72: '購票：NT$500、800、1200、1500、2000、3000，購票請上TixFun購票網。', 73: '/+500;/+800;/+1000;/+1200'}


def update_campaign_with_ticket_id(file_path):
    from main.models import Campaign, Ticket

    with open(file_path) as file:
        data = json.load(file)
        for d in data:
            for item in d['showInfo']:
                ticket_price = item['price']
                ticket_id = None
                try:
                    ticket = Ticket.objects.get(price_description=ticket_price)
                    ticket_id = ticket.ticket_id
                except Ticket.DoesNotExist:
                    print(f"No ticket with price {ticket_price} found.")

                if ticket_id is not None:
                    Campaign.objects.filter(
                        uid=d['UID']).update(ticket_id=ticket_id)
                    print(
                        f"Updated Campaign {d['UID']} with Ticket ID {ticket_id}")
                else:
                    print(f"No valid ticket_id found for price {ticket_price}")


def update_campaign_with_location_id(file_path):
    from main.models import Campaign

    with open(file_path) as file:
        data = json.load(file)
        for d in data:
            print(d['title'])
            for item in d['showInfo']:
                location_name = item['locationName']
                print(item['locationName'])

            location_id = None
            for id, name in locations_data.items():
                if name == location_name:
                    location_id = id

                    break

            if location_id is not None:
                print(f"找到匹配的 location: {location_name} -> ID: {location_id}")
            Campaign.objects.filter(uid=d['UID']).update(
                location=location_id)


def update_campaign_with_website_id(file_path):
    from main.models import Campaign, Website

    with open(file_path) as file:
        data = json.load(file)
        for d in data:
            website_promote_info = d['sourceWebPromote']
            website_id = None
            try:
                website = Website.objects.filter(
                    source_web_promote=website_promote_info).first()
                if website:
                    website_id = website.website_id
            except Website.DoesNotExist:
                print(
                    f"No website with promote info {website_promote_info} found.")

            if website_id is not None:
                Campaign.objects.filter(uid=d['UID']).update(
                    website_id=website_id)
                print(
                    f"Updated Campaign {d['UID']} with website ID {website_id}")
            else:
                print(
                    f"No valid website_id found for promote info {website_promote_info}")
