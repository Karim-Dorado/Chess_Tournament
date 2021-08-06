class Router:

    def __init__(self):
        self.paths = [
        ]

    def navigate(self, path: str):
        for p, ctrl in self.paths:
            if path == p:
                ctrl()

    def add_route(self, path, controller):
        self.paths.append((path, controller))




router = Router()

if __name__ == '__main__':
    router.navigate('/')
