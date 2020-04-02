from itertools import chain

import hassapi as hass
from enum import Enum


CUBE_DECONZ_ID = 'lumi_sensor_cube'
CUBE_EVENT_TYPE = 'xiaomi_aqara.cube_action'
CUBE_ENTITY_ID = 'sensor.aqara_cube'

BUTTON_DECONZ_ID = 'switch'
BUTTON_EVENT_TYPE = 'xiaomi_aqara.click'
BUTTON_ENTITY_ID = 'binary_sensor.xiaomi_button'


class CubeAction(str, Enum):
    """
    Model no. MFKZQ01LM
    """
    FLIP90 = 'flip90'
    FLIP180 = 'flip180'
    MOVE = 'move'  # = slide
    TAP_TWICE = 'tap_twice'
    SHAKE_AIR = 'shake_air'
    # SWING = 'swing'  ??
    ALERT = 'alert'  # = wake?
    FREE_FALL = 'free_fall'
    ROTATE = 'rotate'


class ClickAction(str, Enum):
    """
    Model no. WXKG11LM
    """
    SINGLE = 'single'
    DOUBLE = 'double'
    LONG_CLICK_PRESS = 'long_click_press'
    LONG_CLICK_RELEASE = 'long_click_release'


class Main(hass.Hass):
    """
    Recreating xiaomi aqara binary sensor platform for cube
    https://www.home-assistant.io/components/binary_sensor.xiaomi_aqara/
    """
    device_mapping = {}

    def initialize(self):
        self.listen_event(self.handle_event, "deconz_event")

    def handle_event(self, event_name, data, kwargs):
        if CUBE_DECONZ_ID in data['id']:
            entity_id = self._get_entity_id(entity_type=CUBE_ENTITY_ID, unique_id=data['unique_id'])
            if data['event'] in [1000, 2000, 3000, 4000, 5000, 6000]:
                to_side = data['event'] // 1000
                self.set_state(entity_id, state=to_side)
                self.fire_event(CUBE_EVENT_TYPE, entity_id=entity_id, action_type=CubeAction.MOVE)
            elif data['event'] in [1001, 2002, 3003, 4004, 5005, 6006]:
                to_side = data['event'] % 1000
                self.set_state(entity_id, state=to_side)
                self.fire_event(CUBE_EVENT_TYPE, entity_id=entity_id, action_type=CubeAction.TAP_TWICE)
            elif data['event'] in [1006, 2005, 3004, 4003, 5002, 6001]:
                from_side = data['event'] % 1000
                to_side = data['event'] // 1000
                self.set_state(entity_id, state=to_side, attributes={'from_side': from_side})
                self.fire_event(CUBE_EVENT_TYPE, entity_id=entity_id, action_type=CubeAction.FLIP180)
            elif data['event'] in [1002, 1003, 1004, 1005, 2001, 2003, 2004, 2006, 3001, 3002, 3005, 3006, 4001, 4002, 4005, 4006, 5001, 5003, 5004, 5006, 6002, 6003, 6004, 6005]:
                from_side = data['event'] % 1000
                to_side = data['event'] // 1000
                self.set_state(entity_id, state=to_side, attributes={'from_side': from_side})
                self.fire_event(CUBE_EVENT_TYPE, entity_id=entity_id, action_type=CubeAction.FLIP90)
            elif data['event'] == 7007:
                self.fire_event(CUBE_EVENT_TYPE, entity_id=entity_id, action_type=CubeAction.SHAKE_AIR)
            elif data['event'] == 7008:
                self.fire_event(CUBE_EVENT_TYPE, entity_id=entity_id, action_type=CubeAction.FREE_FALL)
            elif data['event'] == 7000:
                self.fire_event(CUBE_EVENT_TYPE, entity_id=entity_id, action_type=CubeAction.ALERT)
            else:
                degrees = data['event'] / 100
                self.fire_event(CUBE_EVENT_TYPE, entity_id=entity_id, action_type=CubeAction.ROTATE, action_value=degrees)
        elif BUTTON_DECONZ_ID in data['id']:
            entity_id = self._get_entity_id(entity_type=BUTTON_ENTITY_ID, unique_id=data['unique_id'])
            if data['event'] == 1002:
                self.set_state(entity_id, state='on')
                self.fire_event(BUTTON_EVENT_TYPE, entity_id=entity_id, action_type=ClickAction.SINGLE)
                self.set_state(entity_id, state='off')
            elif data['event'] == 1004:
                self.fire_event(BUTTON_EVENT_TYPE, entity_id=entity_id, action_type=ClickAction.DOUBLE)
                self.set_state(entity_id, state='off')
            elif data['event'] == 1001:
                self.set_state(entity_id, state='on')
                self.fire_event(BUTTON_EVENT_TYPE, entity_id=entity_id, action_type=ClickAction.LONG_CLICK_PRESS)
            elif data['event'] == 1003:
                self.set_state(entity_id, state='off')
                self.fire_event(BUTTON_EVENT_TYPE, entity_id=entity_id, action_type=ClickAction.LONG_CLICK_RELEASE)

    def _get_entity_id(self, entity_type, unique_id):
        """
        Attempt to generate same entity_id when there is more than one device of the same type
        """
        try:
            index = self.device_mapping.setdefault(entity_type, []).index(unique_id)
        except ValueError:
            self.device_mapping[entity_type] = list(sorted(chain(self.device_mapping[entity_type], [unique_id])))
            index = self.device_mapping[entity_type].index(unique_id)
        if index > 0:
            return f'{entity_type}_{index}'
        return entity_type
