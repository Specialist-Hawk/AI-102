from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import requests


class Country:

    def __init__(self, name):
        self.name = name.lower().replace(" ", "")
        self.url = "https://www.worldometers.info/world-population/" + self.name + "-population/"
        self.website = requests.get(self.url)

        self.keys = ["Year", "Population", "Median", "Fertility", "Density"]
        self.indexes = [0, 1, 5, 6, 7]

        self.data = {key: [] for key in self.keys}


        self.StatusCheck()
        self.ScrapeData()

    def StatusCheck(self):
        if(self.website.status_code == 200):
            pass
        else:
            raise ValueError("Please enter a valid name, such country doesn't exist in the database.")

    def ScrapeData(self):
        soup = BeautifulSoup(self.website.content, "html.parser")
        table = soup.find_all("table", class_=["datatable", "w-full", "border", "border-zinc-200", "datatable-table"])

        population_history_table = table[0]
        population_forecast_table = table[1]

        for table_row in population_history_table.find("tbody").find_all("tr"):
            rows = table_row.find_all("td")

            for key,index in zip(self.keys, self.indexes):
                self.data[key].append(rows[index].text)




country_name = input("Enter the name of your country: ")

Country1 = Country(country_name)

# Country1.data["Density"]
# Country1.data["Fertility"]
# Country1.data["Median"]
# Country1.data["Population"]
Country1.data["Year"].reverse()


plt.plot(Country1.data["Year"], Country1.data["Population"], marker='o')
plt.title(f"{Country1.name.capitalize()}")
plt.xlabel("Year")
plt.ylabel("Population")

plt.grid()
plt.show()
