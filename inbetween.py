import inspect
import json
from collections import Callable
from functools import wraps
from pydoc import locate
import time


def debug(fn):
    """
    Decorate a function for debug purposes. In this instance, I was just measuring the time.
    :param fn: the function that was decorated
    :return: a debug, after running the function
    """
    @wraps(fn)
    def decorated_func(*args, **kwargs):
        print('=====================================================')
        print('fn: {0} \nargs: {1} \nkwargs: {2}'.format(fn.__name__, args, kwargs))
        start = time.time()
        result = fn(*args, **kwargs)
        print("Execution time = {0:.5f}".format(time.time() - start))
        # pprint(result[0])
        # print(result[1])
        print('=====================================================')
        return result

    return decorated_func


@debug
def pull_data(json_input):
    """
    Dynamically import and use a method within your code
    :param json_input: the parameters comes in as a string but in JSON format
    :return: the expected function call
    """
    json_input = json.loads(json_input)

    location = json_input.get('begin').get('location')
    fn = json_input.get('begin').get('function')
    arguments = json_input.get('args')

    expected_variables, needed_function = [], getattr(locate(location), fn)

    if isinstance(needed_function, Callable):
        if arguments:
            for each in inspect.getargspec(needed_function).args:
                # the example below only works for methods but not functions
                # get_the_method.setdefault(each, fields.get(each))
                expected_variables.append(arguments.get(each))
            return needed_function(*expected_variables)
        else:
            return needed_function()


if __name__ == "__main__":
    data = '{"begin": {"location": "collectibles", "function": "defines"}, "args": {"age": "3", "name": "ChatBot"}}'
    print(pull_data(data))

    print("\n")
    data = '{"begin": {"location": "collectibles", "function": "utc"}}'
    print(pull_data(data))
