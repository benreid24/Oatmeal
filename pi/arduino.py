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
    
    data, points = _parse_data(data)
    return points


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