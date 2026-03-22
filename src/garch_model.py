import numpy as np
import pandas as pd
from arch import arch_model

WINDOW = 252

def calculate_drift_volatility(returns: pd.Series, window: int = WINDOW) -> tuple[float, float]:
    drift = returns.mean() - 0.5 * returns.var()
    volatility = returns.std
    return drift, volatility
    
def fit_garch(returns: pd.Series) -> float:
    scaled = returns * 100
    model = arch_model(scaled, vol="GARCH", p=1, q=1, dist="Normal", rescale=False)
    result = model.fit(disp="off")
    forecast = result.forecast(horizon=1)
    garch_var = forecast.variance.values[-1, 0]
    return np.sqrt(garch_var) / 100

if __name__ == "__main__":
    from data_loader import load_returns, load_fx_data
    df = load_fx_data()
    ret = load_returns(df)
    for col in ret.columns:
        d, v = calculate_drift_volatility(ret[col])
        g = fit_garch(ret[col])
        print(f"{col}: drift={d:.6f}, hist_vol={v:.6f}, garch_vol={g:.6f}")

    