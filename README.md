# monte-carlo-fx
Monte-Carlo simulation on currency pair

# Monte Carlo FX Simulator

Симулятор стоимости криптовалютного портфеля методом **Монте-Карло** с оценкой волатильности через **GARCH(1,1)** и расчётом риск-метрик **VaR / CVaR**.

---

## Реализовано:  

- Загрузка исторических данных через `yfinance` (BTC/USD, ETH/USD)
- Оценка волатильности через GARCH(1,1) модель
- 10 000 симуляций методом Геометрического броуновского движения (GBM)
- Расчёт VaR и CVaR на уровне доверия 95%
- Визуализация: fan chart, гистограмма распределения, примеры траекторий

---

## Результаты симуляции

| Актив | Старт (S0) | Медиана (252д) | VaR 95% | CVaR 95% |
|---|---|---|---|---|
| BTC/USD | $87,509 | $96,757 | 45.0% | 53.0% |
| ETH/USD | $2,967 | $2,984 | ~55% | ~63% |

> Портфель: 60% BTC / 40% ETH  
> Начальный капитал: $10,000

---

## Визуализация

### Fan Chart — BTC/USD
![BTC Fan Chart](assets/fan_BTC_USD.png)

### Fan Chart — ETH/USD
![ETH Fan Chart](assets/fan_ETH_USD.png)

### Распределение портфеля
![Portfolio Distribution](assets/portfolio_distribution.png)

---

## Структура проекта  

monte-carlo-fx/
├── src/
│ ├── data_loader.py # Загрузка данных yfinance
│ ├── garch_model.py # GARCH(1,1) оценка волатильности
│ ├── simulator.py # GBM симуляция (Monte Carlo)
│ ├── portfolio.py # Стоимость портфеля, VaR, CVaR
│ └── visualizer.py # Графики и визуализация
├── assets/ # Скриншоты для README
├── main.py # Точка входа
├── requirements.txt
└── README.md


---

## Установка и запуск

```bash
git clone https://github.com/niddyDEV/monte-carlo-fx.git
cd monte-carlo-fx
pip install -r requirements.txt
python main.py
