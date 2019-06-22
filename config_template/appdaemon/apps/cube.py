import appdaemon.plugins.hass.hassapi as hass
from enum import Enum


DECONZ_IDS = ('switch_7', 'switch_8')
SENSOR_ID = 'sensor.aqara_cube'
EVENT_ID = 'xiaomi_aqara.cube_action'


class Action(str, Enum):
    FLIP90 = 'flip90'
    FLIP180 = 'flip180'
    MOVE = 'move'  # = slide
    TAP_TWICE = 'tap_twice'
    SHAKE_AIR = 'shake_air'
    # SWING = 'swing'  ??
    ALERT = 'alert'  # = wake?
    FREE_FALL = 'free_fall'
    ROTATE = 'rotate'


class CubeControl(hass.Hass):
    """
    Recreating xiaomi aqara binary sensor platform for cube
    https://www.home-assistant.io/components/binary_sensor.xiaomi_aqara/
    """
    def initialize(self):
        self.listen_event(self.handle_event, "deconz_event")

    def handle_event(self, event_name, data, kwargs):
        if data['id'] in DECONZ_IDS:
            if data['event'] in [1000, 2000, 3000, 4000, 5000, 6000]:
                to_side = data['event'] // 1000
                self.set_state(SENSOR_ID, state=to_side)
                self.fire_event(EVENT_ID, entity_id=SENSOR_ID, action_type=Action.MOVE)
            elif data['event'] in [1001, 2002, 3003, 4004, 5005, 6006]:
                to_side = data['event'] % 1000
                self.set_state(SENSOR_ID, state=to_side)
                self.fire_event(EVENT_ID, entity_id=SENSOR_ID, action_type=Action.TAP_TWICE)
            elif data['event'] in [1006, 2005, 3004, 4003, 5002, 6001]:
                from_side = data['event'] % 1000
                to_side = data['event'] // 1000
                self.set_state(SENSOR_ID, state=to_side, attributes={'from_side': from_side})
                self.fire_event(EVENT_ID, entity_id=SENSOR_ID, action_type=Action.FLIP180)
            elif data['event'] in [1002, 1003, 1004, 1005, 2001, 2003, 2004, 2006, 3001, 3002, 3005, 3006, 4001, 4002, 4005, 4006, 5001, 5003, 5004, 5006, 6002, 6003, 6004, 6005]:
                from_side = data['event'] % 1000
                to_side = data['event'] // 1000
                self.set_state(SENSOR_ID, state=to_side, attributes={'from_side': from_side})
                self.fire_event(EVENT_ID, entity_id=SENSOR_ID, action_type=Action.FLIP90)
            elif data['event'] == 7007:
                self.fire_event(EVENT_ID, entity_id=SENSOR_ID, action_type=Action.SHAKE_AIR)
            elif data['event'] == 7008:
                self.fire_event(EVENT_ID, entity_id=SENSOR_ID, action_type=Action.FREE_FALL)
            elif data['event'] == 7000:
                self.fire_event(EVENT_ID, entity_id=SENSOR_ID, action_type=Action.ALERT)
            else:
                degrees = data['event'] / 100
                self.fire_event(EVENT_ID, entity_id=SENSOR_ID, action_type=Action.ROTATE, action_value=degrees)

