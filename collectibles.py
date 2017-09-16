import time
from datetime import datetime


def defines(name, age):
    """
    A simple function that returns a tuple of the inputs supplied to it
    :param name: a string variable
    :param age: another variable
    :return: tuple
    """
    return name, age


def utc():
    """
    Gets the utc time
    :return: times in seconds
    """
    now = datetime.utcnow()
    return int(time.mktime(now.timetuple()) * 1000) + now.microsecond
