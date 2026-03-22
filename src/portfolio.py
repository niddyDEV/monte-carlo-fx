import numpy as np
import pandas as pd


def portfolio_value(
    paths: dict[str, np.ndarray],
    weights: dict[str, float],
    initial_capital: float = 10_000.0,
) -> np.ndarray:
    """
    paths: {"BTC/USD": array(252, 10000), "ETH/USD": array(252, 10000)}
    weights: {"BTC/USD": 0.6, "ETH/USD": 0.4}
    Возвращает массив (252, 10000) — стоимость портфеля по дням.
    """
    assert abs(sum(weights.values()) - 1.0) < 1e-6, "Веса должны суммироваться в 1"

    first = next(iter(paths.values()))
    n_days, n_sim = first.shape
    portfolio = np.zeros((n_days, n_sim))

    for asset, path in paths.items():
        S0 = path[0, :].mean() / (1 + 0)  # приближение S0 из первого дня
        alloc = initial_capital * weights[asset]
        portfolio += alloc * (path / path[0, :])  # нормируем к стартовой цене

    return portfolio


def calculate_var(final_values: np.ndarray, initial_capital: float, confidence: float = 0.95) -> float:
    """Value at Risk — максимальный убыток с вероятностью confidence."""
    returns = (final_values - initial_capital) / initial_capital
    return float(-np.percentile(returns, (1 - confidence) * 100))


def calculate_cvar(final_values: np.ndarray, initial_capital: float, confidence: float = 0.95) -> float:
    """Conditional VaR (Expected Shortfall) — средний убыток за порогом VaR."""
    returns = (final_values - initial_capital) / initial_capital
    var_threshold = np.percentile(returns, (1 - confidence) * 100)
    tail = returns[returns <= var_threshold]
    return float(-tail.mean())


if __name__ == "__main__":
    from data_loader import load_fx_data, load_returns
    from garch_model import calculate_drift_volatility, fit_garch
    from simulator import simulate_gbm

    df = load_fx_data()
    ret = load_returns(df)

    paths = {}
    for col in df.columns:
        S0 = df[col].iloc[-1]
        drift, _ = calculate_drift_volatility(ret[col])
        garch_vol = fit_garch(ret[col])
        paths[col] = simulate_gbm(S0, drift, garch_vol)

    weights = {"BTC/USD": 0.6, "ETH/USD": 0.4}
    capital = 10_000.0

    portfolio = portfolio_value(paths, weights, capital)
    final = portfolio[-1, :]

    var = calculate_var(final, capital)
    cvar = calculate_cvar(final, capital)

    print(f"Начальный капитал:  ${capital:,.0f}")
    print(f"Медиана через год:  ${np.median(final):,.0f}")
    print(f"VaR  95%:           {var*100:.1f}% (${var*capital:,.0f})")
    print(f"CVaR 95%:           {cvar*100:.1f}% (${cvar*capital:,.0f})")
