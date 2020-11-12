from datetime import datetime

import pandas as pd
from nameko.events import event_handler

from classification.detect_class import Detect_class
from classification.detect_types import Detect_type
from classification.normalize import Normalize
from consts import class_mappings, type_mappings

class EventAnalyzer:
    name = 'event_analyzer'

    @event_handler('timepad_crawler', 'event')
    def add_event(self, payload):
        events_df = pd.DataFrame(payload)

        events_df = Normalize(events_df)
        if events_df.empty:
            result = payload
            result['class'] = 'other'
            result['event_type'] = 'others'
        else:
            events_df = Detect_type(events_df)
            events_df = Detect_class(events_df)
            result = events_df.to_dict(orient='records')[0]

        result['event_time'] = datetime.strptime(result['event_time'],
                                                 '%Y-%m-%dT%H:%M:%S')
        result['class'] = class_mappings[result['class']]
        result['event_type'] = type_mappings[result['event_type']]

        result = {
            'name': result['name'],
            'event_type': result['event_type'],
            'event_time': result['event_time'],
            'city': result['city'],
            'place': result['place'],
            'source_url': result['source_url'],
            'description': result['description'],
            'categories': [result['class']],
            'logo_path': result['logo_path']
        }

        print(result)
