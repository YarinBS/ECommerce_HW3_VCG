import pandas as pd
import math
from itertools import permutations


########## Part A ###############


def opt_bnd(data, k, years):
    # returns the optimal bundle of cars for that k and list of years and their total cost.
    return {"cost": 0, "bundle": []}


def proc_vcg(data, k, years):
    # runs the VCG procurement auction
    return {'id': 0}


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
    sums.append(s + xs[0])

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

        auction_results = proc_vcg(self.data, self.cars_num, self.data[['year']])
        price = 0
        for value in auction_results.values():
            price += value
        return price / len(auction_results)

    def cdf(self, x):
        # return F(x) for the histogram self.data
        hist = {}
        for i in self.data["value"]:
            hist[i] = hist.get(i, 0) + 1
        if hist.get(x) is None:
            return 0
        # using numpy np.cumsum to calculate the CDF
        # We can also find using the PDF values by looping and adding
        data = [[k, v] for k, v in hist.items()]  # use dic.items() for python3
        data.sort(reverse=False)
        cdf = cumsum([1,2,3])
        print(cdf)

        return hist[x]

    def os_cdf(self, r, n, x):
        # The r out of n order statistic CDF
        return 1

    def exp_rev(self):
        # returns the expected revenue in future auction for cars_num items and buyers_num buyers

        return 0

    def exp_rev_median(self, n):
        return 0

    ########## Part C ###############

    def reserve_price(self):
        # returns your suggestion for a reserve price based on the self_data histogram.
        return 0
