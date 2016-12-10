"""Hard code the list of Car and Driver's makes.  Use to build start_urls"""


ALL_MAKES = [('acura', 25), ('alfa-romeo', 52), ('audi', 27), ('bentley', 28),
             ('aston-martin', 26), ('bmw', 29), ('bugatti', 51), ('buick', 30), ('cadillac', 31),
             ('chevrolet', 2), ('chrysler', 32), ('dodge', 33), ('ferrari', 34), ('fiat', 64),
             ('ford', 35), ('genesis', 208), ('gmc', 36), ('honda', 37), ('hyundai', 39),
             ('infiniti', 40), ('jaguar', 42), ('jeep', 43), ('kia', 44), ('koenigsegg', 97),
             ('lamborghini', 45), ('land-rover', 46), ('lexus', 47), ('lincoln', 48),
             ('lotus', 49), ('maserati', 50), ('mazda', 3), ('mclaren', 150), ('mercedes-amg', 170),
             ('mercedes-benz', 4), ('mercedes-maybach', 185), ('mini', 6), ('mitsubishi', 7),
             ('nissan', 8), ('pagani', 98), ('porsche', 11), ('ram', 162), ('rolls-royce', 12),
             ('scion', 24), ('smart', 53), ('spyker', 59), ('subaru', 15), ('tesla', 54),
             ('toyota', 17), ('volkswagen', 18), ('volvo', 19)]


ALL_MAKES_URLS = []

for make in ALL_MAKES:
    http_format = 'http://www.caranddriver.com/api/vehicles/models-by-make/{}/json?ddIgnore=1'
    ALL_MAKES_URLS.append(http_format.format(make[-1]))
