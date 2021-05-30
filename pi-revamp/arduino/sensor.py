class Sensor:
    def __init__(self, sensor_type: str, value: float, index:int = None):
        self.sensor_type = sensor_type
        self.value = value
        if index:
            self.name = f'{sensor_type}:{index}'
            self.index = index
