class Body:

    def __init__(self, mass, heat_capacity, temperature):
        if mass > 0 and heat_capacity > 0 and temperature >= 0:
            self.mass = mass
            self.heat_capacity = heat_capacity
            self.temperature = temperature
        else:
            print("Error: mass and heat capacity must be greater than 0, temperature must be 0 or more")

    def add_heat(self, heat):
        delta_t = heat / (self.mass * self.heat_capacity)
        self.temperature = self.temperature + delta_t
        return self.temperature


if __name__ == "__main__":
    body1 = Body(100, 0.15, 200)
    print(body1.add_heat(20))
    print(body1.add_heat(-40))