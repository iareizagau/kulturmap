from datetime import datetime

from apps.culture.models import Events

from KulturMap import settings


def insert_culture(df):
    if df.empty:
        print("dataframe empty")
    else:
        dict_list = df.to_dict('records')
        new_events = []
        for event in dict_list:
            new_events.append(Events(**event))

        if new_events:
            try:
                total_ini = Events.objects.all().count()
                events_id_list = [event.id for event in new_events]
                existing_ids = Events.objects.filter(events_id__in=events_id_list).values_list('events_id', flat=True)
                conflicting_incidents = [event for event in new_events if event.events_id in existing_ids]
                non_conflicting_incidents = [event for event in new_events if event.events_id not in existing_ids]
                obj = Events.objects.bulk_create(non_conflicting_incidents, ignore_conflicts=True)
                # obj = Events.objects.bulk_create(non_conflicting_incidents)
                total_end = Events.objects.all().count()
                print(f"total ini {total_ini} end {total_end}")
                print(f"events_id_list {len(events_id_list)}")
                print(f"existing_ids {len(existing_ids)}")
                print(f"conflicting_events/non_conflicting_events {len(conflicting_incidents)}/{len(non_conflicting_incidents)}")
            except Exception as e:
                print("error", "Events.objects.bulk_create(new_events, ignore_conflicts=True)", e)
