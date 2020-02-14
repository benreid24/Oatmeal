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
RECOVERY_HUMIDITY = 70
RETRY_INTERVAL = 60
humid_trys = None
last_spray_try = None

morning_mist = None
night_mist = None

heat_active = False
heat_time = None


def climate_control(high_temp, low_temp, humidity):
    global last_spray_try
    global humid_trys
    global morning_mist
    global night_mist
    now = datetime.datetime.now()

    # Day/Night Lighting
    if _is_night(now):
        _set_heat_active(False)
        _set_light_active(False)
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
        if spray:
            humid_trys += 1
            last_spray_try = now
            _mist(3)
            if humid_trys > 3:
                _error(f'Humidity is {humidity} despite {humid_trys} three second mistings')

    # Morning Spray
    if now.time().hour == NIGHT_END.hour:
        mist = True
        if not morning_mist:
            morning_mist = now()
        elif morning_mist.date().day == now.date().day:
            mist = False
        if mist:
            morning_mist = now
            _mist(3)

    # Night Spray
    if now.time().hour == NIGHT_START.hour:
        mist = True
        if not night_mist:
            night_mist = now
        if night_mist.date().day == now.date().day:
            mist = False
        if mist:
            night_mist = now
            _mist(5)


def _is_night(dt):
    return dt.time() >= NIGHT_START or dt.time() < NIGHT_END


def _set_heat_active(active):
    global heat_active
    global heat_time

    if active and not heat_active:
        heat_time = datetime.datetime.now()
    if not active:
        heat_time = None
    heat_active = active

    arduino.heat(active)


def _set_light_active(active):
    arduino.light(active)


def _mist(seconds):
    arduino.mist(int(seconds*1000))


def _error(msg):
    global last_error
    print(f'Climate control error: {msg}')

    send = True
    now = datetime.datetime.now()
    if not last_error:
        last_error = now
    elif now - last_error).total_seconds() < ERROR_TIMEOUT:
        send = False
    if send:
        web.send_email('CRITICAL: Climate Control Error', msg)
