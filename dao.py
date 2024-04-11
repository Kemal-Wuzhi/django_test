import json
from django.db import connection
from django.db.utils import IntegrityError
from datetime import datetime

# locations_record = {}


def insert_website_directly(websales, sourcewebpromote, sourcewebname):
    with connection.cursor() as cursor:
        sql = "INSERT INTO Website (WebSales, SourceWebPromote, SourceWebName) VALUES (%s, %s, %s)"
        cursor.execute(sql, [websales, sourcewebpromote, sourcewebname])


# def insert_ticket_directly(on_sales, discount_info, price):
#     with connection.cursor() as cursor:
#         sql = "INSERT INTO Ticket(OnSales, DiscountInfo, Price, EndTime) VALUES (%s, %s, %s, %s)"
#         cursor.execute(sql, [on_sales, discount_info, price])


def insert_campaign_data(file_path):
    from main.models import Campaign, CampaignLocationInfo, Unit, CampaignUnitRelation

    try:
        with open(file_path, 'r') as file:
            show_data = json.load(file)
        # for location info
        location_list = []
        for data in show_data:

            start_d_object = datetime.strptime(data['startDate'], '%Y/%m/%d')
            end_d_object = datetime.strptime(data['endDate'], '%Y/%m/%d')
            correct_start = start_d_object.strftime("%Y-%m-%d")
            correct_end = end_d_object.strftime("%Y-%m-%d")
            data['startDate'] = correct_start
            data['endDate'] = correct_end

            campaign, created = Campaign.objects.get_or_create(
                uid=data['UID'],
                defaults={
                    'version': data.get('version'),
                    'title': data.get('title'),
                    'description_html': data.get('descriptionFilterHtml'),
                    'image_url': data.get('imageUrl'),
                    'comment': data.get('comment'),
                    'start_date': data.get('startDate'),
                    'end_date': data.get('endDate'),
                    'hit_rate': data.get('hitRate'),
                }
            )
            # handle raw location info
            for item in data['showInfo']:
                if item['locationName'] in location_list:
                    pass
                else:
                    location_list.append(item['locationName'])

            # TODO:handle location insert
            new_location_list = [location.replace(
                "=", " ").strip() for location in location_list]
            locations = {index + 1: location for index,
                         location in enumerate(new_location_list)}
            for location_id, location_name in locations.items():
                CampaignLocationInfo.objects.get_or_create(
                    location_id=location_id, defaults={'location_name': location_name})
            print("地點名稱：", locations)
            # # TODO:handle ticket insert, need data formation!
            # # Ticket.objects.create(
            # #     campaign=campaign,
            # #     on_sales=data.get('on_sale'),
            # #     discount_info=data.get('discount_info'),
            # #     price_description=data.get('price_description'),
            # #     end_time=data.get('end_time')
            # # )

            # on_sales = data.get('onSale')
            # discount_info = data.get('discountInfo')
            # price = data.get('price')
            # print("PRICE:", price)
            # insert_ticket_directly(
            #     on_sales, discount_info, price)

            # # except Exception as e:
            # #     print(f'An error occurred while processing Ticket data: {e}')

            for unit_type in ['showUnit', 'supportUnit', 'subUnit', 'masterUnit', 'otherUnit']:
                units = data.get(unit_type, [])
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
            # TODO: reassign ID nums to Website table
            try:
                websales = data.get('webSales')
                sourcewebpromote = data.get('sourceWebPromote', '')
                sourcewebname = data.get('sourceWebName', '')
                if websales:
                    insert_website_directly(
                        websales, sourcewebpromote, sourcewebname)
            except Exception as e:
                print(f'An error occurred while processing Website data: {e}')
        # 把Campaign的資料抓出來然後幫每個locationname加上對應的 LocationID
        print("CAMMM:", campaign)
        for index, cam in campaign.items():
            print("CAAA:", dir(cam))

    except FileNotFoundError:
        print(f'The file {file_path} does not exist')
    except json.JSONDecodeError:
        print('Failed to decode the JSON file')
    except Exception as e:
        print(f'An error occurred while processing the campaign data: {e}')


locations_data = {1: '台北捷運音樂進站', 2: '國立臺灣交響樂團', 3: '陽明交大演藝廳', 4: '高雄市文化中心至善廳', 5: '嘉義市政府文化局音樂廳', 6: '國家音樂廳', 7: '臺中市屯區藝文中心演藝廳', 8: '衛武營國家藝術文化中心音樂廳', 9: '高雄市現代化綜合體育館﹝高雄巨蛋﹞', 10: '苗栗縣苗北藝文中心', 11: '高雄市政府文化局﹝高雄市文化中心﹞', 12: '金沙鎮（金門縣）', 13: '衛武營國家藝術文化中心', 14: '衛武營國家藝術文化中心戲劇院', 15: '高雄市駁二藝術特區', 16: '金門文化園區', 17: '金湖鎮（金門縣）', 18: '烈嶼鄉（金門縣）', 19: '金寧鄉（金門縣）', 20: '國立中正紀念堂管理處', 21: '國家兩廳院演奏廳', 22: '日月潭國家風景區', 23: '臺中國家歌劇院 中劇院', 24: '衛武營國家藝術文化中心表演廳', 25: '苗栗縣泰雅原住民文化產業區', 26: '國家兩廳院表演聽', 27: '台中國家歌劇院小劇場', 28: '衛武營國家藝術文化中心表演聽', 29: '誠品表演廳', 30: '苗栗縣賽夏族民俗文物館', 31: '國家兩廳院 演奏廳', 32: '大東文化藝術中心演藝廳', 33: '大園區（桃園市）', 34: '橫山書法藝術館', 35: '臺中市葫蘆墩文化中心', 36: '衛武營國家藝術文化中心 音樂廳', 37: '臺中國家歌劇院 大劇院', 38: '國家兩廳院 國家音樂廳', 39: '國立臺中教育大學', 40: '高雄市文化中心至德堂', 41: '板橋區（新北市）', 42: '苗栗市（苗栗縣）', 43: '益品美術館', 44: '信義鄉（南投縣）', 45: '雲林縣政府文化觀光處', 46: '中寮鄉（南投縣）', 47: '魚池鄉（南投縣）', 48: '埔里鎮（南投縣）', 49: '苗栗縣政府文化觀光局', 50: '西屯區（臺中市）', 51: '鹿谷鄉（南投縣）', 52: '花蓮縣文化局', 53: '霧峰林家宮保第園區', 54: '中原大學', 55: '松山文化創意園區', 56: '桃園市平鎮區婦幼活動中心',
                  57: '南崁兒童藝術村', 58: '八德區（桃園市）', 59: '蘆竹區（桃園市）', 60: '桃園市立圖書館總館', 61: '功學社音樂廳', 62: '嘉義市政府文化局', 63: '桃園展演中心', 64: '國立臺灣工藝研究發展中心（臺灣工藝文化園區）', 65: '西區（臺中市）', 66: '桃園市大園區竹圍國民小學', 67: '國家兩廳院', 68: '懷舊系列IV民歌暖壽PA', 69: '國立東華大學', 70: '南投縣埔里藝文中心', 71: '彰化縣員林演藝廳', 72: '臺中國家歌劇院小劇場', 73: '桃園北區客家會館', 74: '桃園市中壢區社福館', 75: '桃園市客家文化館', 76: '臺灣戲曲中心小表演廳3202排練廳', 77: '楊梅區（桃園市）', 78: '中壢藝術館', 79: '臺中市港區藝術中心', 80: '六龜區（高雄市）', 81: '嘉義縣表演藝術中心演藝廳', 82: '臺南市新營文化中心', 83: '臺北市中山堂', 84: '台北新兒童樂園—如果兒童劇場', 85: '台北新兒童樂園—如果兒童劇團', 86: '金城鎮（金門縣）', 87: '嘉義縣表演藝術中心', 88: '澎湖縣政府文化局', 89: '民主大道', 90: '國立臺灣交響樂團演奏廳 NTSO Concert Hall', 91: '雲林表演廳 Yunlin Performance Hall', 92: '臺中市葫蘆墩文化中心 Taichung City Huludun Cultural Center', 93: '新竹市文化局演藝廳 Hsinchu City Performance Hall', 94: '花蓮縣文化局演藝廳 Performance Hall of Hualien County', 95: '宜蘭演藝廳 Yilan Performing Arts Center', 96: '臺中國家歌劇院中劇院', 97: '臺南文化中心', 98: '臺中市大墩文化中心', 99: '南屯區（臺中市）', 100: '高雄國家體育場﹝2009世運會主場館﹞', 101: '高雄流行音樂中心', 102: '竹山鎮（南投縣）', 103: '時代的情書'}


# def update_campaign_with_location_id(file_path):
#     from main.models import Campaign
#     print("LLL:", locations_record)
#     # 處理 json
#     with open(file_path) as file:
#         data = json.load(file)
#         for d in data:
#             print(d['title'])
#             for item in d['showInfo']:
#                 location_name = item['locationName']
#                 print(item['locationName'])

#             # 在 locations_data 中查找 location_name
#             location_id = None
#             for id, name in locations_data.items():
#                 if name == location_name:
#                     location_id = id

#                     break

#             if location_id is not None:
#                 print(f"找到匹配的 location: {location_name} -> ID: {location_id}")
#             Campaign.objects.filter(uid=d['UID']).update(
#                 location=location_id)

#
