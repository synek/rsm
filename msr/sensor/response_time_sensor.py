"""Body Size Sensor

@author Rory Byrne <rory@rory.bio>
"""
import time

from aiohttp import ClientSession

from msr.model import URL, Measurement
from msr.sensor.base import Sensor
from msr.sensor.exceptions import PhenomenonFailed
from msr.util.log import Logger


class ResponseTimeSensor(Sensor, Logger):

    dimension = 'Response Time'
    unit = 'ms'

    def __init__(self, session: ClientSession = None):
        super().__init__()
        self.session = session

    async def measure(self, url: URL):
        """Perform a GET request and measure the response time"""
        try:
            print(f'Sensing {url.href}')
            tick = time.perf_counter()
            await self.session.get(url.href)
            tock = time.perf_counter()

            delta_ms = (tock - tick)*1000
            # print(f'{url.href} took {delta_ms} ms')

            return Measurement(float(delta_ms), self.dimension)
        except Exception as e:
            # @todo - expand error handling
            self.log.error(e)
            raise PhenomenonFailed()

