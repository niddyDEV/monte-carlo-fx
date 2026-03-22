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
<img width="1567" height="820" alt="fan_BTC_USD" src="https://github.com/user-attachments/assets/3c1949f9-033a-4098-8aef-f6ade3810eb6" />


### Fan Chart — ETH/USD
<img width="1540" height="820" alt="fan_ETH_USD" src="https://github.com/user-attachments/assets/e687a0a0-c009-42ee-aa1a-a44b9f2867ae" />

### Распределение портфеля
<img width="1507" height="820" alt="portfolio_distribution" src="https://github.com/user-attachments/assets/277eb6ec-0e3f-40a4-bbcf-8a06a9a15001" />


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
