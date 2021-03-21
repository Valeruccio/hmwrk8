import datetime


class Depot:

    def __init__(self, address, high, area):
        self.address = address
        self.max_high = high
        self.area = area


class Equipment:
    __instances = {}

    def __init__(self, model, power, paper_formats):
        self.model = model
        self.power = power
        self.paper_formats = paper_formats
        invent_code = len(Equipment.__instances) + 1
        self.__invent_code = invent_code
        Equipment.__instances[invent_code] = self

    def __str__(self):
        return f'Model: {self.model} (inv: {self.get_invent()}),' \
               f' power: {self.power}, available formats: {self.paper_formats}'

    def get_invent(self):
        return self.__invent_code

    @classmethod
    def get_by_inv(cls, inv):
        return cls.__instances[inv]


class BalanceException(Exception):

    def __init__(self, txt):
        self.txt = txt

    def __str__(self):
        return self.txt


class Balance:
    __instance = None
    __balance = {}

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, Balance):
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, depot):
        self.__depot = None
        if depot is not None:
            self.use(depot)

    def use(self, depot):
        self.__depot = depot
        if not (depot in self.__balance.keys()):
            self.__balance[depot] = []

    def income(self, equipment):
        """when the product arrives"""
        self.__balance[self.__depot].append(equipment)

    def outcome(self, equipment):
        """When writing off a product"""
        if not (equipment in self.__balance[self.__depot]):
            raise BalanceException(f'This equpment don\'t exist on this warehouse ({self.__depot.address})')
        self.__balance[self.__depot].remove(equipment)

    def exchange_to(self, depot_to, equipment):
        self.outcome(equipment)
        _depot = self.__depot
        self.use(depot_to)
        self.income(equipment)
        self.use(_depot)

    def report(self):
        return f'Report ({datetime.datetime.now()})\n' + f'\n'.join(
            f'{key.address} ({len(value)}):' + f'\n\t' + f'\n\t'.join(map(str, value))
            for key, value in self.__balance.items()
        )

    def __str__(self):
        return self.report()


class Printer(Equipment):

    def __init__(self, model, power, paper_formats, colors, velocity):
        super().__init__(model, power, paper_formats)
        self.colors = colors
        self.velocity = velocity


class Scanner(Equipment):

    def __init__(self, model, power, paper_formats, quality):
        super().__init__(model, power, paper_formats)
        self.quality = quality


class Copier(Equipment):

    def __init__(self, model, power, paper_formats, colors):
        super().__init__(model, power, paper_formats)
        self.colors = colors


p = Printer('Canon', 1200, ['A4', 'A5'], 'RGB', 20)
c = Copier('Xerox', 200, ['A4', ], 'RGB')
print(f'p invent = {p.get_invent()}')
print(f'c invent = {c.get_invent()}')
d1 = Depot('North', 6, 200)
d2 = Depot('South', 20, 2000)
b = Balance(d1)
b2 = Balance(d2)
b.income(p)
b.income(c)
print(b.report())
b.use(d1)
for _ in range(20):  # 20 одинаковых
    b.income(Printer('Canon', 1500, ['A4', 'A5'], 'RGB', 20))
print(b.report())
b.use(d2)
b.outcome(c)
print(b.report())
b.exchange_to(d1, p)
print(b)
b.use(d1)
for inv in range(1, 6):
    try:
        b.exchange_to(d2, Equipment.get_by_inv(inv))
    except BalanceException:
        print(f'{str(Equipment.get_by_inv(inv))}  None in warehouse')
print(b)
print(b is b2)