import json
import os

class EventFileManager:
    FILE_PATH = r"/Users/alex.abm/Desktop/ELTE/python/assigment1/assignment1/event.json"

    @staticmethod
    def read_events_from_file():
        try:
            with open(EventFileManager.FILE_PATH, 'r') as file:
                events = json.load(file)
        except FileNotFoundError:
            events = []
        return events

    @staticmethod
    def write_events_to_file(events):
        with open(EventFileManager.FILE_PATH, 'w') as file:
            json.dump(events, file)