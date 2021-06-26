import pandas as pd
from itertools import permutations


########## Part A ###############


def opt_bnd(data, k, years):
    cars = ['ford', 'bmw', 'kia', 'vw', 'ferrari']
    total_cost = 0
    winning_cars = []
    for index in range(k):
        lowest_v = 1000000000000
        lowest_index_lst = []
        permut = permutations(years, 5)
        for p in permut:
            v = 0
            index_lst = []
            gotNewPern = True
            for index, car in enumerate(cars):
                data_car = data[(data.brand == car) & (data.year == p[index])]
                min_price = data_car['value'].min()
                if pd.isnull(min_price):
                    gotNewPern = False
                    break
                index_lst.append(data_car['value'].idxmin(axis=1))
                v += min_price
            if v < lowest_v and gotNewPern:
                lowest_v = v
                lowest_index_lst = index_lst

        total_cost += lowest_v
        winning_cars.extend(list(data.loc[lowest_index_lst, :]['id']))
        data.drop(lowest_index_lst, inplace=True)
        data.reset_index(inplace=True, drop=True)

    return {"cost": total_cost, "bundle": winning_cars}


def proc_vcg(data, k, years):
    cars_dict = {}
    data_copy = data.copy(deep=True)
    bundle = opt_bnd(data_copy, k, years)
    cost = bundle['cost']
    cars = bundle['bundle']
    for car in cars:
        cars_dict[car] = abs((cost - int(data.loc[data['id'] == car, 'value'])) -
                             opt_bnd(data.drop(data[data.id == car].index), k, years)['cost'])
    return cars_dict


########## Part B ###############
def extract_data(brand, year, size, data):
    sub_df = data[(data["brand"] == brand) & (data["year"] == year) & (data["engine_size"] == size)]
    return sub_df


def cumsum(l: list):
    if not l:
        return []

    sums = []
    sums.append(l[0])

    return helper(sums, l[1:])


def helper(sums: list, xs: list):
    if not xs:
        return sums

    s = sums[len(sums) - 1]
    sums.append([xs[0][0], s[1] + xs[0][1]])

    if len(xs) > 1:
        return helper(sums, xs[1:])

    return sums


class Type:
    cars_num = 0  # Number of cars you buy
    buyers_num = 0  # Number of bidders in the future auction

    def __init__(self, brand, year, size, data):
        self.data = extract_data(brand, year, size, data)

    def avg_buy(self) -> float:
        # runs a procurement vcg auction for buying cars_num cars on the given self.data.
        # returns the average price paid for a winning car.
        prices = list(self.data["value"])
        return sorted(prices)[self.cars_num]

    def cdf(self, x):
        # return F(x) for the histogram self.data
        hist = {}
        counter = 0
        for i in self.data["value"]:
            hist[i] = hist.get(i, 0) + 1
            counter = counter + 1
        data = [[k, v / counter] for k, v in hist.items()]
        data.sort(reverse=False)
        cdf = cumsum(data)
        Xvals = [str(item[0]) for item in cdf]
        if x < int(Xvals[0]):
            return 0
        if x >= int(Xvals[-1]):
            return 1
        lb, ub = self.find_prev_con(x, Xvals)
        return Fx(x, lb, ub, cdf)

    def find_prev_con(self, x, A):
        for i in range(1, len(A)):
            if int(A[i - 1]) <= x <= int(A[i]):
                return int(A[i - 1]), int(A[i])

    def os_cdf(self, r, n, x):
        # The r out of n order statistic CDF
        sum = 0
        for j in range(r, n + 1):
            FX = self.cdf(x)
            sum += (comb(n, j) * (FX ** j) * ((1 - FX) ** (n - j)))
        return sum

    def exp_rev(self):
        # returns the expected revenue in future auction for cars_num items and buyers_num buyers
        n_minus_k_statistic_num = self.buyers_num - self.cars_num
        max_price = max(list(self.data["value"]))
        tail_func = sum(
            [1 - self.os_cdf(n_minus_k_statistic_num, self.buyers_num, x) for x in range(max_price, -1, -1)])
        return self.cars_num * tail_func

    def find_median(self, lst):
        n = len(lst)
        s = sorted(lst)
        return (sum(s[n // 2 - 1:n // 2 + 1]) / 2.0, s[n // 2])[n % 2] if n else None

    def exp_rev_median(self, n):
        value_list = list(self.data["value"])
        med_price = self.find_median(value_list)
        prob = self.cdf(med_price)
        expectancy = n * (prob ** (n - 1)) * (1 - prob) * med_price + sum(
            [1 - self.os_cdf(n - 1, n, med_price) for index in range(med_price)]) + sum(
            [1 - self.os_cdf(n - 1, n, p) for p in range(med_price, max(value_list) + 1)])
        return expectancy

    ########## Part C ###############

    def reserve_price(self):
        # returns your suggestion for a reserve price based on the self_data histogram.
        return 0
