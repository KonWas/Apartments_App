class Apartment:
    def __init__(self, id, location, price, area, rooms, floor, total_floors, year, parking, state, furnished, market):
        self.id = int(id)
        self.location = location
        self.price = float(price)
        self.area = float(area)
        self.rooms = int(rooms)
        self.floor = int(floor)
        self.total_floors = int(total_floors)
        self.year = int(year)
        self.parking = parking
        self.state = state
        self.furnished = furnished
        self.market = market

    def __str__(self):
        return f"{self.id}, {self.location}, {self.price}zł, {self.area}m2, r{self.rooms}, f{self.floor}, tf{self.total_floors}, y{self.year}, {self.parking}, {self.state}, {self.furnished}, {self.market}"
    

class ApartmentsList:
    def __init__(self):
        self.apartments = []

    def __len__(self):
        return len(self.apartments)

    def __iter__(self):
        return iter(self.apartments)

    def __contains__(self, apartment):
        return apartment in self.apartments

    def append(self, apartment):
        self.apartments.append(apartment)

    def get_apartments_by_criteria(self, **kwargs):
        filtered_apartments = self.apartments
        if 'price_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.price >= kwargs['price_min']]
        if 'price_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.price <= kwargs['price_max']]
        if 'area_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.area >= kwargs['area_min']]
        if 'area_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.area <= kwargs['area_max']]
        if 'rooms_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.rooms >= kwargs['rooms_min']]
        if 'rooms_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.rooms <= kwargs['rooms_max']]
        if 'floor_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.floor >= kwargs['floor_min']]
        if 'floor_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.floor <= kwargs['floor_max']]
        if 'total_floors_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.total_floors >= kwargs['total_floors_min']]
        if 'total_floors_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.total_floors <= kwargs['total_floors_max']]
        if 'year_min' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.year >= kwargs['year_min']]
        if 'year_max' in kwargs:
            filtered_apartments = [apartment for apartment in filtered_apartments if apartment.year <= kwargs['year_max']]
        return filtered_apartments