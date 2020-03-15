import datetime

import web
import arduino

ERROR_TIMEOUT = 30 * 60
last_error = None

MAX_TEMP = 83
SHUTOFF_TEMP = 81
MIN_TEMP = 66
HEAT_TEMP = 76

NIGHT_START = datetime.time(21, 0)
NIGHT_END = datetime.time(9, 0)

MIN_HUMIDITY = 50
RETRY_INTERVAL = 240
MAX_HUMID_TRIES = 3
humid_trys = None
last_spray_try = None

MORNING_MIST_LEN = 15
morning_mist = None

NIGHT_MIST_LEN = 30
night_mist = None

heat_active = False
heat_time = None

light_on = False


def climate_control(now, high_temp, low_temp, humidity):
    global last_spray_try
    global humid_trys
    global morning_mist
    global night_mist

    # Day/Night Lighting
    if _is_night(now):
        _set_light_active(False)
        if high_temp > MIN_TEMP:
            _set_heat_active(False)
    else:
        _set_light_active(True)

    # Max Temp
    if high_temp > SHUTOFF_TEMP:
        _set_heat_active(False)
    if high_temp > MAX_TEMP:
        _error(f'Temperature is above safe limit {MAX_TEMP}. Current is {high_temp}')
    
    # Min Temp
    if high_temp < HEAT_TEMP and not _is_night(now):
        _set_heat_active(True)
        if (now - heat_time).total_seconds() > 3600:
            _error(f'Suspect bulb failure. Temperature has been below {HEAT_TEMP} for 1hr despite heating')
    if high_temp < MIN_TEMP:
        _set_heat_active(True)
        _error(f'Temperature is {high_temp}, activating heat')

    # Min Humidity
    if humidity < MIN_HUMIDITY:
        spray = True
        if not humid_trys:
            humid_trys = 0
        elif (now - last_spray_try).total_seconds() < RETRY_INTERVAL:
            spray = False
        if humidy_trys >= MAX_HUMID_TRIES:
            spray = False
            _error(f'Humidity is {humidity}% and reached max spray count')
        if spray:
            humid_trys += 1
            last_spray_try = now
            _mist(3)
    else:
        last_spray_try = None
        humid_trys = None
    if humid_trys and humid_trys >= MAX_HUMID_TRIES:
        if now.day != last_spray_try.day:
            print('Resetting humidity retry on new day')
            humid_trys = None
            last_spray_try = None

    # Morning Spray
    if now.time().hour == NIGHT_END.hour:
        mist = True
        if not morning_mist:
            morning_mist = now
        elif morning_mist.date().day == now.date().day:
            mist = False
        if mist:
            morning_mist = now
            _mist(MORNING_MIST_LEN)

    # Night Spray
    if now.time().hour == NIGHT_START.hour:
        mist = True
        if not night_mist:
            night_mist = now
        elif night_mist.date().day == now.date().day:
            mist = False
        if mist:
            night_mist = now
            _mist(NIGHT_MIST_LEN)


def _is_night(dt):
    return dt.time() >= NIGHT_START or dt.time() < NIGHT_END


def _set_heat_active(active):
    global heat_active
    global heat_time

    if active and not heat_active:
        web.log_message('Turning on heat', web.INFO)
        heat_time = datetime.datetime.now()
    elif heat_active and not active:
        web.log_message('Turning off heat', web.INFO)

    if not active:
        heat_time = None
    heat_active = active

    arduino.heat(active)


def _set_light_active(active):
    global light_on
    if active and not light_on:
        web.log_message('Turning on light', web.INFO)
    elif not active and light_on:
        web.log_message('Turning off light', web.INFO)
    light_on = active
    arduino.light(active)


def _mist(seconds):
    web.log_message(f'Misting for {seconds} seconds', web.INFO)
    arduino.mist(int(seconds*1000))


def _error(msg):
    global last_error
    print(f'Climate control error: {msg}')

    send = True
    now = datetime.datetime.now()
    if not last_error:
        last_error = now
    elif (now - last_error).total_seconds() < ERROR_TIMEOUT:
        send = False
    if send:
        web.log_message(msg, web.CRITICAL)
        web.send_email('CRITICAL: Climate Control Error', msg)
