class Router:
    """
    Class representing a Router
    """
    def __init__(self):
        self.paths = [
        ]

    def navigate(self, path: str):
        """ Allows to activate a controller if he is coupled with a path"""
        for p, ctrl in self.paths:
            if path == p:
                ctrl()

    def add_route(self, path, controller):
        """ Allows to add a route in self.paths"""
        self.paths.append((path, controller))


router = Router()
