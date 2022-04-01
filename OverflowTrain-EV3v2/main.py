#!/usr/bin/env python3
from dotenv import load_dotenv
from destination_provider import DestinationProvider
from stations import Stations
from train_robot import TrainRobot
from train_driver import TrainDriver
from train_service import TrainService
from path_navigator import PathNavigator


load_dotenv()


provider = DestinationProvider()
stations = Stations()
train = TrainRobot()
driver = TrainDriver(stations, train)
navigator = PathNavigator(stations)

service = TrainService(provider, stations, train, driver, navigator)
service.start()
