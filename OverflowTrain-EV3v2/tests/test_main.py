import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 


from destination_provider import DestinationProvider
from stations import Stations
from tests.fake_train_robot import FakeTrainRobot
from train_driver import TrainDriver
from train_service import TrainService
from path_navigator import PathNavigator


provider = DestinationProvider()
stations = Stations()
train = FakeTrainRobot()
driver = TrainDriver(stations, train)
navigator = PathNavigator(stations)

service = TrainService(provider, stations, train, driver, navigator)
service.start()
