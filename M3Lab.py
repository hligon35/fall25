#Harold Ligon
#File: M3Lab.py
#Description: Defines a Vehicle superclass and an Automobile subclass. Prompts user for car details and displays the information.

class Vehicle:
    def __init__(self, vehicle_type):
        self.vehicle_type = vehicle_type


class Automobile(Vehicle):
    def __init__(self, year, make, model, doors, roof):
        super().__init__("car") 
        self.year = year
        self.make = make
        self.model = model
        self.doors = doors
        self.roof = roof

    def display_info(self):
        print("\nVehicle Information:")
        print(f"  Vehicle type: {self.vehicle_type}")
        print(f"  Year: {self.year}")
        print(f"  Make: {self.make}")
        print(f"  Model: {self.model}")
        print(f"  Number of doors: {self.doors}")
        print(f"  Type of roof: {self.roof}")


def main():
    print("Enter car details:")

    year = input("Year: ")
    make = input("Make: ")
    model = input("Model: ")

    # Verify # of doors
    while True:
        doors = input("Number of doors (2 or 4): ")
        if doors in ["2", "4"]:
            break
        print("Enter either 2 or 4.")

    # Verify roof type
    while True:
        roof = input("Roof type (solid or sun roof): ").lower()
        if roof in ["solid", "sun roof"]:
            break
        print("Enter 'solid' or 'sun roof'.")


    car = Automobile(year, make, model, doors, roof)
    car.display_info()


if __name__ == "__main__":
    main()