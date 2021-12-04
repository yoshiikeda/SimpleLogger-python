class DomainError(Exception):
    pass


class Singleton(type):
    _instances = {}

    def __call__(class_, *args_, **kargs_):
        result = None

        if class_ in class_._instances:
            # Empty
            pass

        else:
            class_._instances[class_] = super(Singleton, class_).__call__(*args_, **kargs_)

        result = class_._instances[class_]

        return result