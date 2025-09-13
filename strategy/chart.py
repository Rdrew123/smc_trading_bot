import matplotlib.pyplot as plt
import os

def generate_chart(pair, df):
    plt.figure(figsize=(10,5))
    plt.plot(df['close'], label=f'{pair} Close', color='blue')
    plt.fill_between(range(len(df['close'])), df['low'], df['high'], color='lightgray', alpha=0.3)
    plt.title(f'{pair} Price Chart')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    
    folder = "charts"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{pair}.png")
    plt.savefig(path)
    plt.close()
    return path
