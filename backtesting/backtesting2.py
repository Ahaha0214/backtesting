import backtrader as bt
import yfinance as yf
import matplotlib.pyplot as plt

class DollarCostAveragingStrategy(bt.Strategy): #括弧內語法可讓這個class擁有bt.Strategy的類別及方法 (繼承)
    params = (
        ('investment_amount', 4166666),  # 每月的固定投資金額
        ('stop_loss_pct', 0.2),  # 停損點
    )

    def __init__(self): #class就像一個班級,可以初始化init(定義自己的學生) 隨時訪問和修改這個self.某位學生變量
        self.order = None
        self.buy_price = {}
        self.stop_loss = {}
        self.first_day_of_month = True  # 判斷是否每月的第一天
        self.portfolio_value = []

        self.investment_ratios = {
            'financial': {'6026.TWO': 0.4, '5878.TWO': 0.3, '6023.TWO': 0.3},
            'tech': {'3680.TWO': 0.25, '3529.TWO': 0.25, '3131.TWO': 0.2, '5274.TWO': 0.1, '3163.TWO': 0.2},
            'satellite': {'3491.TWO': 0.6, '3178.TWO': 0.15, '6514.TWO': 0.25},
            'etf': {'00888.TWO': 0.5, '00858.TWO': 0.5},
            'bond_etf': {'00724B.TWO': 1}
        }
        
        self.asset_classes = {
            'financial': 0.12,
            'tech': 0.30,
            'satellite': 0.18,
            'etf': 0.20,
            'bond_etf': 0.20
        }

    def next(self):
        if self.data.datetime.date(0).day == 1 and self.first_day_of_month:  # 每月的第一天且設置為第一天
            for asset_class, ratios in self.asset_classes.items():
                for ticker, proportion in self.investment_ratios[asset_class].items():
                    data = self.getdatabyname(ticker)
                    investment_amount = self.params.investment_amount
                    self.buy_price[data] = data.close[0]
                    self.stop_loss[data] = data.close[0] * (1 - self.params.stop_loss_pct)
                    self.order = self.buy(data=data, size=investment_amount // data.close[0])

            self.first_day_of_month = False  # 設置為非第一天，避免重複投資

        for data in self.datas:
            if self.getposition(data).size and data.close[0] < self.stop_loss[data]:
                self.order = self.sell(data=data)

        self.portfolio_value.append((self.data.datetime.datetime(), self.broker.getvalue()))

# 設置回測參數
tickers = {
    'financial': ['6026.TWO', '5878.TWO', '6023.TWO'],
    'tech': ['3680.TWO', '3529.TWO', '3131.TWO', '5274.TWO', '3163.TWO'],
    'satellite': ['3491.TWO', '3178.TWO', '6514.TWO'],
    'etf': ['00888.TWO', '00858.TWO'],
    'bond_etf': ['00724B.TWO']
}
data_list = []
start = '2021-05-16'
end = '2024-07-16'

for category in tickers.values():
    for ticker in category:
        data = yf.download(ticker, start=start, end=end)
        data.to_csv(f'{ticker}.csv')
        data_feed = bt.feeds.YahooFinanceData(dataname=f'{ticker}.csv')
        data_list.append(data_feed)

# 創建回測引擎
cerebro = bt.Cerebro()
cerebro.addstrategy(DollarCostAveragingStrategy)

# 添加數據到回測引擎
for data_feed in data_list:
    cerebro.adddata(data_feed)

# 設置初始資金和手續費
cerebro.broker.setcash(50000000)  # 初始資金設置為5000萬台幣
cerebro.broker.setcommission(commission=0.001)

# 運行回測
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
results = cerebro.run()
print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

# 獲取策略並繪製總資產走勢圖
strategy = results[0]
dates, values = zip(*strategy.portfolio_value)
plt.figure(figsize=(10, 6))
plt.plot(dates, values)
plt.title('Portfolio Value Over Time')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.grid()
plt.show()
