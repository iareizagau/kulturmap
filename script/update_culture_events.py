import requests
import pandas as pd

from apps.culture.models import Events
import apps.traffic.crud as crud

from OpenDataEuskadi import settings

events = Events.objects.all()
if False:
    print(events)
else:
    url_base = 'https://api.euskadi.eus/culture/events/v1.0/events?'
    headers = dict(accept='application/json')
    number_elements = 1000
    for page_number in range(1, 10):
        print("page_number", page_number)
        url = f'{url_base}_elements={number_elements}&_page={page_number}'
        response = requests.get(url=url, headers=headers)
        data = response.json()
        events_ = data['items']
        for event in events_:
            try:
                print("event id", event['id'])
                event['images'] = event['images'][0]['imageUrl']
            except Exception as e:
                print("error", e)
        df = pd.DataFrame.from_records(events_)
        for date_ in ['startDate', 'endDate', 'publicationDate']:
            df[date_] = pd.to_datetime(df[date_], format='mixed')
            df[date_] = df[date_].dt.tz_convert(settings.TIME_ZONE)

        crud.insert_culture(df)
