import serial

serialport = None
data = ''


def init():
    global serialport
    if serialport:
        if serialport.is_open:
            serialport.close()
    serialport = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)


def get_readings():
    global data
    if not serialport:
        print('Reading serial port before initialization')
        return []

    retries = 0
    while not _read():
        retries += 1
        init()
        if retries >= 3:
            print(f'Failed to read serial data after {retries} retries')
            break
    
    data, points = _parse_data(data)
    return points


def heat(on):
    if on:
        _write('heaton')
    else:
        _write('heatoff')


def light(on):
    if on:
        _write('lighton')
    else:
        _write('lightoff')


def mist(ms):
    _write(f'mist {ms}')


def _read():
    global data
    global serialport
    try:
        char = serialport.read(1)
        while char:
            data = data + char.decode('utf-8')
            char = serialport.read(1)
    except Exception as err:
        print(f'Error reading Arduino: {err}')
        data = ''
        return False
    return True


def _write(data):
    print(f'Serial command: {data}')

    retries = 1
    while retries < 4:
        init()
        if _try_write(data):
            return
        retries += 1
    err = f'Failed to write {data} after {retries} retries'
    print(err)
    raise Exception(err)


def _try_write(data):
    global serialport
    try:
        serialport.write(f'{data}\n'.encode('ascii'))
        serialport.flush()
        return True
    except Exception as err:
        print(f'Error writing serial: {err}')
        return False


def _parse_data(data):
    lines = data.split('\n')
    residual = lines[-1]

    points = []
    for line in lines:
        if residual and line == lines[-1]:
            break
        if not line:
            continue

        items = line.split()
        if not items:
            print('Failed to split serial line')
            continue
        if items[0] != 'f' and lines[0] != 's':
            print(f'Invalid serial line: {line}')
            continue
        if len(items) < 4:
            print(f'Serial line too short: {line}')
            continue
        is_float = items[0] == 'f'
        has_num = items[1] == 'i'
        point = {
            'name': items[2]
        }
        i = 3
        if has_num:
            point['num'] = int(items[3])
            i = 4
            if len(items) < 5:
                print(f'Serial line too short: {line}')
                continue
        if is_float:
            point['value'] = float(items[i])
        else:
            point['value'] = ' '.join(items[i:])
        points.append(point)
    
    return residual, points
