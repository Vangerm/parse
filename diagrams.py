import json
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def main():
    with open("cities_price_iphone13.json") as file:
        cities_prices = json.load(file)

    xlabel = []
    ylabel = []

    for city, price in cities_prices.items():
        if price == None:
            continue
        xlabel.append(city)
        ylabel.append(price)

    ylabel.sort()
    plt.plot(xlabel, ylabel)
    plt.show()


main()
