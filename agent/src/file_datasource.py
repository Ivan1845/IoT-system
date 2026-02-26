from csv import reader
from datetime import datetime
from domain.aggregated_data import AggregatedData
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accel_file = None
        self.gps_file = None
        self.parking_file = None
        self.accel_reader = None
        self.gps_reader = None
        self.parking_reader = None

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.accel_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.parking_file = open(self.parking_filename, 'r')
        self.accel_reader = reader(self.accel_file)
        self.gps_reader = reader(self.gps_file)
        self.parking_reader = reader(self.parking_file)

        next(self.accel_reader, None)
        next(self.gps_reader, None)
        next(self.parking_reader, None)

    def read(self):
        """Метод повертає дані отримані з датчиків"""
        try:
            accel_row = next(self.accel_reader)
            gps_row = next(self.gps_reader)
            parking_row = next(self.parking_reader)
        except StopIteration:
            self.accel_file.seek(0)
            self.gps_file.seek(0)
            self.parking_file.seek(0)
            next(self.accel_reader, None)
            next(self.gps_reader, None)
            next(self.parking_reader, None)
            accel_row = next(self.accel_reader)
            gps_row = next(self.gps_reader)
            parking_row = next(self.parking_reader)

        #Формуємо дані акселерометра та GPS
        accelerometer = Accelerometer(x=int(accel_row[0]), y=int(accel_row[1]), z=int(accel_row[2]))
        gps = Gps(longitude=float(gps_row[0]), latitude=float(gps_row[1]))

        aggregated_data = AggregatedData(
            accelerometer=accelerometer,
            gps=gps,
            timestamp=datetime.now(),
            user_id=1
        )

        #Формуємо дані паркінгу
        parking_gps = Gps(longitude=float(parking_row[1]), latitude=float(parking_row[2]))
        parking_data = Parking(empty_count=int(parking_row[0]), gps=parking_gps)

        return aggregated_data, parking_data

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        if self.accel_file: self.accel_file.close()
        if self.gps_file: self.gps_file.close()
        if self.parking_file: self.parking_file.close()