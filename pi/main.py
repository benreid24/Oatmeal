import datetime
import statistics
import time

import arduino
import controller
import util
import web

ERROR_TIMEOUT = 30 * 60
IP_FETCH_PERIOD = 60 * 60

NAME_MAP = {
    'humid0': 'Hot Zone Humidity',
    'humid1': 'Cold Zone Humidity',
    'temp0': 'Hot Zone Temp',
    'temp1': 'Cold Zone Temp',
    'motion': 'Motion Tracker'
}


def main():
    stream = util.start_stream()
    arduino.init()

    ip = util.get_ip()
    web.set_video(f'{ip}:42069')

    last_error = None
    last_ipfetch = datetime.datetime.now()

    while True:
        now = datetime.datetime.now()

        # Check Video
        if stream.poll() is not None:
            stream = util.start_stream()

        high_temp = None
        low_temp = None
        humidity = []

        # Read Sensors
        try:
            data = arduino.get_readings()
            sensors = {}
            messages = []
            for reading in data:
                name = reading['name'] if 'num' not in reading.keys() \
                                    else reading['name'] + str(reading['num'])
                stype = reading['name']
                if isinstance(data['value'], float):
                    sensors[name] = {
                        'value': reading['value'],
                        'type:': stype
                    }
                    if stype == 'temp':
                        if not high_temp:
                            high_temp = reading['value']
                            low_temp = reading['value']
                        if reading['value'] > high_temp:
                            high_temp = reading['value']
                        if reading['value'] < low_temp:
                            low_temp = reading['value']
                    elif stype == 'humid':
                        humidity.append(reading['value'])
                else:
                    msg = f'Arduino message: {reading.value}'
                    messages.append(msg)

            for name, sensor in sensors.items():
                if name in NAME_MAP.keys():
                    name = NAME_MAP[name]
                print(f'Updating sensor {name} {sensor}')
                web.set_sensor(name, sensor['value'], sensor['type'])
            for msg in messages:
                print(f'Sending message "{msg}"')
                web.log_message(msg, web.INFO)
        except Exception as err:
            web.log_message(f'Failed to decode arduino data: {err}', web.WARNING)

        # Sensor read error
        if not high_temp or not low_temp:
            print('Failed to read temperature')
            send = True
            if not last_error:
                last_error = now
            elif (now - last_error).total_seconds() < ERROR_TIMEOUT:
                send = False
            if send:
                web.log_message('Failed to read temperature', web.CRITICAL)
                web.send_email(
                    'CRITICAL: Temperature read failure',
                    'Failed to read tank temperature. Check on Oatmeal ASAP'
                )
                last_error = now

        # Climate Control
        humidity = statistics.mean(humidity)
        controller.climate_control(high_temp, low_temp, humidity)

        # Video Feed Update
        if (now - last_ipfetch).total_seconds() >= IP_FETCH_PERIOD:
            last_ipfetch = now
            ip = util.get_ip()
            web.set_video(f'{ip}:42069')

        time.sleep(10)


if __name__ == '__main__':
    main()
