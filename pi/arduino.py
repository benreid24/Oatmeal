import serial

serialport = None
data = ''


def init():
    global serialport
    serialport = serial.Serial('/dev/ttyAMA0', 115200, timeout=0.1)


def get_readings():
    global data
    if not serialport:
        print('Reading serial port before initialization')
        return []

    char = serialport.read(1)
    while char:
        data = data + char.decode('utf-8')
        char = serialport.read(1)
    
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


def _write(data):
    serialport.write(f'{data}\n'.encode('ascii'))


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
        is_float = items[0] == 'f'
        has_num = items[1] == 'i'
        point = {
            'name': items[2]
        }
        i = 3
        if has_num:
            point['num'] = int(items[3])
            i = 4
        if is_float:
            point['value'] = float(items[i])
        else:
            point['value'] = ' '.join(items[i:])
        points.append(point)
    
    return residual, points