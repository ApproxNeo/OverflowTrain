from dotenv import load_dotenv
import threading
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 


from virtual.api.display import Display
from virtual.map_screen import MapScreen

from destination_provider import DestinationProvider
from stations import Stations
from virtual.virtual_train_robot import VirtualTrainRobot
from train_driver import TrainDriver
from train_service import TrainService
from path_navigator import PathNavigator


load_dotenv()


display = Display((1000, 1000))
map_screen = display.add_screen(MapScreen('train-map'))

provider = DestinationProvider()
stations = Stations()
train = VirtualTrainRobot(map_screen.get_train_element())
driver = TrainDriver(stations, train)
navigator = PathNavigator(stations)

service = TrainService(provider, stations, train, driver, navigator)

train_service_thread = threading.Thread(target=service.start, daemon=True)
train_service_thread.start()
display.start('train-map')
