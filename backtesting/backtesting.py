import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf

# 下載台灣加權指數、波若威、廣達和鴻海數據
twii = yf.download('^TWII', start='2024-06-17', end='2024-07-20')
browave = yf.download('3163.TWO', start='2024-06-17', end='2024-07-20')
quanta = yf.download('2382.TW', start='2024-06-17', end='2024-07-20')
foxconn = yf.download('2317.TW', start='2024-06-17', end='2024-07-20')

# 移除沒有開市的日期
twii = twii[twii['Volume'] > 0]
browave = browave[browave['Volume'] > 0]
quanta = quanta[quanta['Volume'] > 0]
foxconn = foxconn[foxconn['Volume'] > 0]

# 確保數據格式正確
twii.index.name = 'Date'
browave.index.name = 'Date'
quanta.index.name = 'Date'
foxconn.index.name = 'Date'

# 繪製成交量和K棒圖
def plot_volume_and_candlestick(data, title):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # 繪製成交量
    ax1.bar(data.index, data['Volume'], label='Volume', color='blue', alpha=0.6)
    ax1.set_ylabel('Volume', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.legend(loc='upper left')
    ax1.grid(True)

    # 繪製K棒圖
    mpf.plot(data, type='candle', ax=ax2, volume=False, show_nontrading=False)
    ax2.set_ylabel('Price')
    ax2.legend(['Price'], loc='upper left')
    ax2.grid(True)

    plt.suptitle(f'Volume and Price for {title}')
    plt.show()

# 繪製台灣加權指數、波若威、廣達和鴻海的成交量和K棒圖
plot_volume_and_candlestick(twii, 'TWII')
plot_volume_and_candlestick(browave, 'Browave')
plot_volume_and_candlestick(quanta, 'Quanta')
plot_volume_and_candlestick(foxconn, 'Foxconn')