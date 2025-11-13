
class MainLoop:
    def __init__(self, name):
        self.name = name
        self.cars = []

    def loop(self):
        for car in self.cars:
            car.updatePosition()
            car.updateDirection()

    def addCar(self, car):
        self.cars.append(car)


