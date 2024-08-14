import numpy as np
import pandas as pd
import requests
import math
import json
import statistics
import pprint
import scipy
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from Secrets.upstox_secrets import UPSTOX_API_KEY
from Secrets.upstox_secrets import UPSTOX_API_SECRET

access_token = "eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiJLQjQ3MTYiLCJqdGkiOiI2NmJjMjk4ZDZkOWM2MjNhZTE1MDIzMDIiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzIzNjA3NDM3LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MjM2NzI4MDB9.oMg0xKGHo3RE4awf6aLbJzdtoHruuCNFlmZtsSXaYcc"

historical_keys = {"NSE_EQ|INE002A01018":"RELIANCE",
        "NSE_EQ|INE018A01030":"LT",
        "NSE_EQ|INE040A01034":"HDFCBANK",
        "NSE_EQ|INE296A01024":"BAJFINANCE",
        "NSE_EQ|INE021A01026":"ASIANPAINT",
        "NSE_EQ|INE280A01028":"TITAN",
        "NSE_EQ|INE481G01011":"ULTRACEMCO",
        "NSE_EQ|INE397D01024":"BHARTIARTL",
        "NSE_EQ|INE318A01026":"PIDILITIND",
        "NSE_EQ|INE376G01013":"BIOCON"
        }

def portfolio_custom_date(keys, date):

        data = {'Stock':[], 'Price':[], 'month3':[], 'month3per':[], 'month6':[], 'month6per':[], 'year1':[], 'year1per':[], 'perScore':[], 'analysis':[]}

        open_in = 1
        high_in = 2
        low_in = 3
        close_in = 4

        start = date.strftime('%Y-%m-%d')
        end = (date - timedelta(days=365)).strftime('%Y-%m-%d')

        # testSt = "2017-07-02"
        # testEn = "2016-07-02"

        # print(start)
        # print(end)

        for key,value in keys.items():

            url2 = f'https://api.upstox.com/v2/historical-candle/{key}/month/{start}/{end}'
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            response2 = requests.get(url2, headers=headers).json()
            # pprint.pprint(response2)

            if (len(response2["data"]["candles"])<12):
                last = list(response2["data"]["candles"][-1])
                # print(last)
                response2["data"]["candles"].append(last * (12-len(response2["data"]["candles"])))

            size = 12

            # print(size)
            # pprint.pprint(response2)
            # print(f"Stock: {value}, Size: {size}, Response: {response2["status"]}")

            m3 = []
            m6 = []
            y1 = []

            for i in range(0, size-1, 3):
                # print(i)
                a = (response2["data"]["candles"][i][close_in] - response2["data"]["candles"][i+2][close_in])*100/(response2["data"]["candles"][i+2][close_in])
                # print(a)
                m3.append(a)
            for i in range(0, size-1, 6):
                a = (response2["data"]["candles"][i][close_in] - response2["data"]["candles"][i+5][close_in])*100/(response2["data"]["candles"][i+5][close_in])
                # print(a)
                m6.append(a)
            y1.append((response2["data"]["candles"][0][close_in] - response2["data"]["candles"][size-1][close_in])*100/(response2["data"]["candles"][size-1][close_in]))

            data['Stock'].append(value)
            data['Price'].append(response2["data"]["candles"][0][4])
            data["month3"].append(statistics.mean(m3))
            data["month6"].append(statistics.mean(m6))
            data["year1"].append(statistics.mean(y1))

        for i in range(len(data['Stock'])):
            data["month3per"].append(scipy.stats.percentileofscore(data["month3"], data["month3"][i])) #3 month percentile
            data["month6per"].append(scipy.stats.percentileofscore(data["month6"], data["month6"][i])) #6 month percentile
            data["year1per"].append(scipy.stats.percentileofscore(data["year1"], data["year1"][i])) #1 year percentile

            score = data["month3"][i]*0.5 + data["month6"][i]*0.4 + data["year1"][i]*0.1

            if score>=10:
                data["analysis"].append("buy")
            elif score<10 and score>0:
                data["analysis"].append("hold")
            else:
                data["analysis"].append("sell")

            data["perScore"].append(score)

        return data

class backtest:
    init_portfolio = None
    init_investment = None
    total_value = 0
    old_value = 0
    new_value = 0
    s_date = None
    portfolio_size = 0
    balance = 0
    equal_value = None
    old_portfolio = None
    backtest_time = None
    keys = historical_keys
    portfolio_values = []
    total_evaluation = []


    def __init__(self, backtest_time) -> None:   
        self.portfolio_size = float(input("Enter the size of your portfolio: "))
        self.balance = self.portfolio_size
        
        self.s_date = (datetime.now() - timedelta(days = backtest_time*365))
        self.backtest_time = backtest_time*365
        
        self.init_portfolio = self.init_build()
        self.old_portfolio = self.init_portfolio.copy()

    def init_build(self):
        current_stats = portfolio_custom_date(historical_keys, self.s_date)
        position_size = self.portfolio_size/len(current_stats['Stock'])
        self.equal_value = position_size
        
        portfolio = {'Stock': [], 'Holdings': [], 'atPrice': [], 'curPrice':[]}

        for i in range(len(current_stats['Stock'])):
            portfolio['Stock'].append(current_stats['Stock'][i])
            portfolio['atPrice'].append(current_stats['Price'][i])
            portfolio['curPrice'].append(0)

            value = math.floor(position_size/current_stats['Price'][i])

            portfolio['Holdings'].append(value)

            self.total_value += value*current_stats['Price'][i]
            self.balance -= value*current_stats['Price'][i]
        
        # print(portfolio)
        
        return portfolio
    
    def update_port(self):
        self.old_value = self.total_value
        delta = 30
        # inter = 0
        iterations = int(self.backtest_time/delta)

        file_time = datetime.now().strftime("%Y_%m_%d_%H_%M")

        filename = f"BacktestLogs/backtest_log_{file_time}.txt"

        with open(filename, "a") as file:
                file.write(f"Backtesting Log {self.s_date.strftime('%Y-%m-%d')} to {(self.s_date + timedelta(days=self.backtest_time)).strftime('%Y-%m-%d')} \n\n")

        for _ in tqdm(range(iterations), desc="Backtesting Progress"):
            interim_value = 0

            with open(filename, "a") as file:
                file.write(f"\nDate: {(self.s_date + timedelta(days=delta)).strftime('%Y-%m-%d')} ---------- \n")

            time.sleep(30)
            interim = portfolio_custom_date(self.keys, self.s_date + timedelta(days=delta))
            # inter += 1
            # print(inter)
            for i in range(len(interim['Stock'])):
                equal_size_balance = self.balance/len(interim['Stock'])

                if (interim['analysis'][i]=='buy' and self.init_portfolio['Holdings'][i]==0 and self.balance>0):
                    self.balance -= self.init_portfolio['Holdings'][i]*interim['Price'][i]
                    self.init_portfolio['Holdings'][i] += math.floor(self.equal_value/interim['Price'][i])

                    with open(filename, "a") as file:
                        file.write(f"Bought {math.floor(self.equal_value/interim['Price'][i])} shares of {interim['Stock'][i]}\n")

                elif (interim['analysis'][i]=='sell' and self.init_portfolio['Holdings'][i]!=0):
                    self.balance += self.init_portfolio['Holdings'][i]*interim['Price'][i]

                    with open(filename, "a") as file:
                        file.write(f"Sold {self.init_portfolio['Holdings'][i]} shares of {interim['Stock'][i]}\n")

                    self.init_portfolio['Holdings'][i] = 0

                elif (interim['analysis'][i]=='buy' and self.init_portfolio['Holdings'][i]!=0 and self.balance>0):
                    if (equal_size_balance>interim['Price'][i]):
                        self.init_portfolio['Holdings'][i] += math.floor(equal_size_balance/interim['Price'][i])
                        self.balance -= math.floor(equal_size_balance/interim['Price'][i])*interim['Price'][i]

                        with open(filename, "a") as file:
                            file.write(f"Bought {math.floor(equal_size_balance/interim['Price'][i])} shares of {interim['Stock'][i]}\n")

                self.init_portfolio['curPrice'][i] = interim['Price'][i]
            
            for i in range(len(interim['Stock'])):
                interim_value += self.init_portfolio['Holdings'][i]*self.init_portfolio['curPrice'][i]
            
            self.portfolio_values.append(interim_value)
            self.total_evaluation.append(interim_value + self.balance)

            delta += 30

        for i in range(len(self.init_portfolio['Stock'])):
            self.new_value += self.init_portfolio['Holdings'][i]*self.init_portfolio['curPrice'][i]
    
    def old_graph(self):
        portfolio = self.old_portfolio
        initial_value = 0

        for i in range(len(portfolio['Stock'])):
            initial_value += portfolio['Holdings'][i]*portfolio['atPrice'][i]

        cmap = plt.get_cmap('viridis')  # Example colormap

        # Create pie chart
        fig, ax = plt.subplots()

        # Pie chart segments
        wedges, texts = ax.pie(portfolio['Holdings'], autopct=None, startangle=140, colors=cmap(np.linspace(0, 1, len(portfolio['Stock']))))

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        legend_labels = [f'{label}: {size}' for label, size in zip(portfolio['Stock'], portfolio['Holdings'])]

        ax.legend(wedges, legend_labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        # Title
        plt.title(f'Portfolio Details, Initial Investment: {initial_value:.2f}')

        plt.show()

    def new_graph(self):
        portfolio = self.init_portfolio
        initial_value = 0

        for i in range(len(portfolio['Stock'])):
            initial_value += portfolio['Holdings'][i]*portfolio['curPrice'][i]

        cmap = plt.get_cmap('viridis')  # Example colormap

        # Create pie chart
        fig, ax = plt.subplots()

        # Pie chart segments
        wedges, texts = ax.pie(portfolio['Holdings'], autopct=None, startangle=140, colors=cmap(np.linspace(0, 1, len(portfolio['Stock']))))

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        legend_labels = [f'{label}: {size}' for label, size in zip(portfolio['Stock'], portfolio['Holdings'])]

        ax.legend(wedges, legend_labels, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        # Title
        plt.title(f'Portfolio Details, Current Valuation: {initial_value:.2f}')

        plt.show()

    def portfolio_growth(self):
        y_values = self.portfolio_values
        x_values = np.arange(0, len(self.portfolio_values))

        plt.figure(figsize=(12, 8))  # Width=12 inches, Height=8 inches

        # Create the plot
        plt.plot(x_values, y_values, label='Portfolio Growth Chart', color='red')

        # Add labels and title
        plt.xlabel('Time Frame (months from the start)')
        plt.ylabel('Portfolio Value (Rs)')
        plt.title('Portfolio Growth Chart')
        plt.legend()

        # Display the plot
        plt.show()

    def evaluation(self):
        y_values = self.total_evaluation
        x_values = np.arange(0, len(self.total_evaluation))

        plt.figure(figsize=(12, 8))  # Width=12 inches, Height=8 inches

        # Create the plot
        plt.plot(x_values, y_values, label='Total Evaluation Growth', color='green')

        # Add labels and title
        plt.xlabel('Time Frame (months from the start)')
        plt.ylabel('Evaluation (Rs)')
        plt.title('Evaluation Growth Chart')
        plt.legend()

        # Display the plot
        plt.show()

    def calculate_CAGR(self):
        
        Vf = self.new_value
        Vi = self.old_value
        n = math.ceil(self.backtest_time/365)

        print(f"Final Value: {Vf:.2f}")
        print(f"Initial Value: {Vi:.2f}")
        print("Time (years): ", n)

        cagr = (((Vf/Vi)**(1/n)) - 1)*100

        print(f"CAGR: {cagr:.2f}")
    

backtest_time = int(input("Enter backtest duration (Years, maximum 10): "))

test = backtest(backtest_time)

test.old_graph()

test.update_port()

test.new_graph()

test.calculate_CAGR()

test.evaluation()