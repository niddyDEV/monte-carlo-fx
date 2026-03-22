from src.data_loader import load_fx_data, load_returns
from src.garch_model import calculate_drift_volatility, fit_garch
from src.simulator import simulate_gbm
from src.portfolio import portfolio_value, calculate_var, calculate_cvar
from src.visualizer import plot_fan_chart, plot_portfolio_distribution, plot_sample_paths

# ── Настройки ────────────────────────────────────────────────
WEIGHTS       = {"BTC/USD": 0.6, "ETH/USD": 0.4}
CAPITAL       = 10_000.0
N_SIMULATIONS = 10_000
N_DAYS        = 252

# ── 1. Данные ────────────────────────────────────────────────
print("Загрузка данных...")
df  = load_fx_data()
ret = load_returns(df)
print(f"Загружено строк: {len(df)}\n")

# ── 2. GARCH + симуляция ─────────────────────────────────────
print("Симуляция Монте-Карло...")
paths = {}
for col in df.columns:
    S0            = float(df[col].iloc[-1])
    drift, _      = calculate_drift_volatility(ret[col])
    garch_vol     = fit_garch(ret[col])
    paths[col]    = simulate_gbm(S0, drift, garch_vol, N_SIMULATIONS, N_DAYS)
    print(f"   {col}: S0=${S0:,.2f} | GARCH vol={garch_vol:.4f}")

# ── 3. Портфель ──────────────────────────────────────────────
print("\nРасчёт портфеля...")
portfolio = portfolio_value(paths, WEIGHTS, CAPITAL)
final     = portfolio[-1, :]
var       = calculate_var(final, CAPITAL)
cvar      = calculate_cvar(final, CAPITAL)

print(f"\n{'─'*40}")
print(f"  Начальный капитал : ${CAPITAL:>10,.0f}")
print(f"  Медиана через год : ${float(__import__('numpy').median(final)):>10,.0f}")
print(f"  VaR  95%          : {var*100:>9.1f}%  (${var*CAPITAL:,.0f})")
print(f"  CVaR 95%          : {cvar*100:>9.1f}%  (${cvar*CAPITAL:,.0f})")
print(f"{'─'*40}\n")

# ── 4. Визуализация ──────────────────────────────────────────
print("Сохранение графиков...")
for col in df.columns:
    S0 = float(df[col].iloc[-1])
    plot_fan_chart(paths[col], col, S0)
    plot_sample_paths(paths[col], col)

plot_portfolio_distribution(final, CAPITAL, var, cvar)
print("\n✅ Готово! Графики в папке output/")
