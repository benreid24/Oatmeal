import sys
import datetime
import statistics
import time

import arduino
import controller
import util
import web

ERROR_TIMEOUT = 30 * 60

NAME_MAP = {
    'humid0': 'Hot Zone',
    'humid1': 'Cold Zone',
    'temp0': 'Hot Zone',
    'temp1': 'Cold Zone',
    'motion': 'Motion Tracker'
}


def main():
    stream = util.start_stream()
    arduino.init()

    last_error = None
    last_ipfetch = datetime.datetime.now()

    last_reading = datetime.datetime.now()
    humidity_avg = 75

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
                if isinstance(reading['value'], float):
                    sensors[name] = {
                        'value': reading['value'],
                        'type': stype
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
                web.log_message(msg, web.WARNING)
        except Exception as err:
            print(f'Error decoding data: {err}')
            web.log_message(f'Failed to decode arduino data: {err}', web.WARNING)

        try:

            # Sensor read error
            if not high_temp or not low_temp:
                if (now - last_reading).total_seconds() >= 60:
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
            else:
                last_reading = now

            # Climate Control
            if humidity:
                humidity_avg = statistics.mean(humidity)
            print(f'High temp: {high_temp}. Low temp: {low_temp}. Humidity: {humidity_avg}')
            if high_temp and low_temp and humidity_avg:
                controller.climate_control(now, high_temp, low_temp, humidity_avg)
        
        except Exception as err:
            print(f'Error: {err}')
            try:
                web.log_message(f'Runtime error: {err}', web.CRITICAL)
                web.send_email(
                    'CRITICAL: Pi Encountered an Error',
                    f'Recovered from runtime error: {err}'
                )
            except Exception as err:
                print(f'CRITICAL: Exception while reporting on exception: {err}')

        time.sleep(10)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        t = int(sys.argv[1])
        print(f'Delaying start for {t} seconds')
        time.sleep(t)
    print('Starting')
    main()
