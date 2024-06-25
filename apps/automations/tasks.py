import logging
import requests
import sys
import pandas as pd
from datetime import datetime

import telegram.constants
from telegram import Bot

from celery import shared_task
from django.core.mail import send_mail
from apps.culture.models import Events
import apps.culture.crud as crud 

from KulturMap import settings

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



async def telegram_bot(message):
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    # await bot.sendMessage(chat_id=settings.TELEGRAM_CHAT_ID, text=message)
    # bot.send_message(text='kaixo', chat_id=settings.TELEGRAM_CHAT_ID, parse_mode=telegram.constants.ParseMode)
    # bot.send_photo()


def send_message_2_telegram(message, task):
    try:
        url = f"{settings.TELECGRAM_SEND_MESSAGE}{message}"
        response = requests.get(url)
        print("Mensaje enviado:", message)
    except Exception as e:
        print("error", f"{task}.telegram", e)


@shared_task
def telegram_bot():
    message = f"test | {datetime.now()}"
    send_message_2_telegram(message, task='telegram_bot')
    print(message)
    logger.error(f"telegram_bot: message {message}")
    logger.warning(f"telegram_bot: message {message}")


@shared_task
def ingest_culture_events():
    message = f"Descargando nuevos eventos de cultura | {datetime.now()}"
    send_message_2_telegram(message, task='ingest_culture_events')
    try:
        headers = dict(accept='application/json')
        url_base = settings.OPEN_DATA_API_CULTURE_EVENTS
        number_elements = 1000
        for page_number in range(1, 20):
            print("page_number", page_number)
            response = requests.get(url=f'{url_base}_elements={number_elements}&_page={page_number}', headers=headers)
            if response.status_code == 200:
                data = response.json()
                events_ = data['items']
                for event in events_:
                    try:
                        search_terms = ['Porrotx', 'Ipuin kontalaria', 'Clown', 'Kiki eta Koko', 'Gora bihotzak!',
                                        'Txirri, Mirri eta Txiribiton', 'Tomaxen Abenturak', 'Matraka ma non tropo',
                                        'Go!azen karaokea', 'Rock Familian']
                        if any(term in event['nameEu'] for term in search_terms):
                            event['type'] = 14
                            event['typeEs'] = 'Actividad infantil'
                            event['typeEu'] = 'Haur jarduera'
                        image_url = event['images'][0]['imageUrl'] if event['images'] else None
                        event['images'] = image_url
                        """
                        if image_url:
                            response = requests.get(url=image_url)
                            if response.status_code == 200:
                                event['images'] = image_url
                            else:
                                event['images'] = None
                        """
                    except Exception as e:
                        print("event['images'] = event['images'][0]['imageUrl']", e)
                        print("event['images']", event['images'])

                    event['nameEu'] = event['nameEu'].replace('`', '')
                    event['nameEs'] = event['nameEs'].replace('`', '')
                df = pd.DataFrame.from_records(events_)
                for date_ in ['startDate', 'endDate', 'publicationDate']:
                    try:
                        df[date_] = pd.to_datetime(df[date_], format='mixed')
                        df[date_] = df[date_].dt.tz_convert(settings.TIME_ZONE)
                    except Exception as e:
                        print("error | dates", e)
                crud.insert_culture(df)

    except Exception as e:
        print("error", e)
        logger.exception("Error occurred while sending daily message: %s", str(e))


@shared_task
def ingest_culture_events_upcoming():
    message = f"Descargando nuevos eventos de cultura | {datetime.now()}"
    send_message_2_telegram(message, task='ingest_culture_events')
    try:
        headers = dict(accept='application/json')
        url_base = settings.OPEN_DATA_API_CULTURE_EVENTS
        number_elements = 1000
        for page_number in range(1, 20):
            print("page_number", page_number)
            response = requests.get(url=f'{url_base}_elements={number_elements}&_page={page_number}', headers=headers)
            if response.status_code == 200:
                data = response.json()
                events_ = data['items']
                for event in events_:
                    try:
                        search_terms = ['Porrotx', 'Ipuin kontalaria', 'Clown', 'Kiki eta Koko', 'Gora bihotzak!',
                                        'Txirri, Mirri eta Txiribiton', 'Tomaxen Abenturak', 'Matraka ma non tropo',
                                        'Go!azen karaokea', 'Rock Familian']
                        if any(term in event['nameEu'] for term in search_terms):
                            event['type'] = 14
                            event['typeEs'] = 'Actividad infantil'
                            event['typeEu'] = 'Haur jarduera'
                        image_url = event['images'][0]['imageUrl'] if event['images'] else None
                        event['images'] = image_url
                        """
                        if image_url:
                            response = requests.get(url=image_url)
                            if response.status_code == 200:
                                event['images'] = image_url
                            else:
                                event['images'] = None
                        """
                    except Exception as e:
                        print("event['images'] = event['images'][0]['imageUrl']", e)
                        print("event['images']", event['images'])

                    event['nameEu'] = event['nameEu'].replace('`', '')
                    event['nameEs'] = event['nameEs'].replace('`', '')
                df = pd.DataFrame.from_records(events_)
                for date_ in ['startDate', 'endDate', 'publicationDate']:
                    try:
                        df[date_] = pd.to_datetime(df[date_], format='mixed')
                        df[date_] = df[date_].dt.tz_convert(settings.TIME_ZONE)
                    except Exception as e:
                        print("error | dates", e)
                crud.insert_culture(df)

    except Exception as e:
        print("error", e)
        logger.exception("Error occurred while sending daily message: %s", str(e))



@shared_task
def ingest_culture_events_kids():
    message = f"Descargando nuevos eventos de cultura | KIDS | {datetime.now()}"
    send_message_2_telegram(message, task='ingest_culture_events')
    try:
        headers = dict(accept='application/json')
        url_base = settings.OPEN_DATA_API_CULTURE_EVENTS
        number_elements = 20
        for page_number in range(1, 2):
            url = f'{url_base}_elements={number_elements}&_page={page_number}&type={14}'
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                events_ = data['items']
                for event in events_:
                    print(f"KIDS | page_number {page_number} | id: {event['id']} type: {event['type']}")
                    try:
                        search_terms = ['Porrotx', 'Ipuin kontalaria', 'Clown', 'Kiki eta Koko', 'Gora bihotzak!',
                                        'Txirri, Mirri eta Txiribiton', 'Tomaxen Abenturak', 'Matraka ma non tropo',
                                        'Go!azen karaokea', 'Rock Familian']
                        if any(term in event['nameEu'] for term in search_terms):
                            event['type'] = 14
                            event['typeEs'] = 'Actividad infantil'
                            event['typeEu'] = 'Haur jarduera'

                        image_url = event['images'][0]['imageUrl'] if event['images'] else None
                        event['images'] = image_url
                        print("event['images']", event['images'])
                        print('image_url', image_url)
                        """
                        if image_url:
                            response = requests.get(url=image_url)
                            if response.status_code == 200:
                                event['images'] = image_url
                            else:
                                event['images'] = None
                        """
                    except Exception as e:
                        print("KIDS | event['images'] = event['images'][0]['imageUrl']", e)
                        print("KIDS | event['images']", event['images'])

                    event['nameEu'] = event['nameEu'].replace('`', '')
                    event['nameEs'] = event['nameEs'].replace('`', '')
                df = pd.DataFrame.from_records(events_)
                print(df.head(1))
                for date_ in ['startDate', 'endDate', 'publicationDate']:
                    try:
                        df[date_] = pd.to_datetime(df[date_], format='mixed')
                        df[date_] = df[date_].dt.tz_convert(settings.TIME_ZONE)
                    except Exception as e:
                        print("KIDS | ", e)
                        print(df.head(1))
                crud.insert_culture(df)

    except Exception as e:
        print("KIDS | error", e)
        logger.exception("KIDS | Error occurred while sending daily message: %s", str(e))
