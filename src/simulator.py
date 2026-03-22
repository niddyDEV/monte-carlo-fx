import numpy as np
import pandas as pd

def simulate_gbm(
    S0: float,
    drift: float,
    volatility: float,
    n_simulations: int = 10_000,
    n_days: int = 252,
    seed: int = 42,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    dt = 1
    
    Z = rng.standard_normal((n_days, n_simulations))
    
    daily_returns = np.exp((drift - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * Z)
    
    price_paths = S0 * np.cumprod(daily_returns, axis=0)
    
    return price_paths

if __name__ == "__main__":
    from data_loader import load_fx_data, load_returns
    from garch_model import calculate_drift_volatility, fit_garch

    df = load_fx_data()
    ret = load_returns(df)

    for col in df.columns:
        S0 = df[col].iloc[-1]
        drift, hist_vol = calculate_drift_volatility(ret[col])
        garch_vol = fit_garch(ret[col])

        paths = simulate_gbm(S0, drift, garch_vol)

        final_prices = paths[-1, :]
        print(f"\n{col}")
        print(f"  Старт (S0):        {S0:.2f}")
        print(f"  GARCH волатильность: {garch_vol:.4f}")
        print(f"  Медиана через 252д: {np.median(final_prices):.2f}")
        print(f"  5-й перцентиль:     {np.percentile(final_prices, 5):.2f}")
        print(f"  95-й перцентиль:    {np.percentile(final_prices, 95):.2f}")