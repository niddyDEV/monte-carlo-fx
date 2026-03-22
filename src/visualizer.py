import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path 

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

def plot_fan_chart(paths: np.ndarray,asset_name: str, S0: float) -> None:
    days = np.arange(paths.shape[0])
    
    p5 = np.percentile(paths, 5, axis=1)
    p25 = np.percentile(paths, 25, axis=1)
    p50 = np.percentile(paths, 50, axis=1)
    p75 = np.percentile(paths, 75, axis=1)
    p95 = np.percentile(paths, 95, axis=1)
   
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.fill_between(days, p5,  p95, alpha=0.15, color="#1f77b4", label="5–95%")
    ax.fill_between(days, p25, p75, alpha=0.30, color="#1f77b4", label="25–75%")
    ax.plot(days, p50, color="#1f77b4", linewidth=2, label="Медиана")
    ax.axhline(S0, color="gray", linestyle="--", linewidth=1, label=f"Старт: ${S0:,.0f}")
    
    ax.set_title(f"Monte Carlo Fan Chart — {asset_name} (10 000 симуляций)", fontsize=14)
    ax.set_xlabel("Торговые дни")
    ax.set_ylabel("Цена (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend()
    ax.grid(alpha=0.3)
    
    path = OUTPUT_DIR / f"fan_{asset_name.replace('/', '_')}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Сохранён: {path}")
    
def plot_portfolio_distribution(final_values: np.ndarray, capital: float, var: float, cvar: float) -> None:
    """Гистограмма финальных стоимостей портфеля + VaR/CVaR."""
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.hist(final_values, bins=100, color="#2ca02c", alpha=0.7, edgecolor="none")

    var_line  = capital * (1 - var)
    cvar_line = capital * (1 - cvar)

    ax.axvline(var_line,  color="orange", linewidth=2, linestyle="--", label=f"VaR  95%: ${var_line:,.0f}")
    ax.axvline(cvar_line, color="red",    linewidth=2, linestyle="--", label=f"CVaR 95%: ${cvar_line:,.0f}")
    ax.axvline(capital,   color="gray",   linewidth=1, linestyle=":",  label=f"Старт: ${capital:,.0f}")

    ax.set_title("Распределение стоимости портфеля через 252 дня", fontsize=14)
    ax.set_xlabel("Стоимость портфеля (USD)")
    ax.set_ylabel("Количество сценариев")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend()
    ax.grid(alpha=0.3)

    path = OUTPUT_DIR / "portfolio_distribution.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Сохранён: {path}")
    
def plot_sample_paths(paths: np.ndarray, asset_name: str, n: int = 50) -> None:
    """N случайных траекторий для наглядности."""
    days = np.arange(paths.shape[0])
    idx  = np.random.choice(paths.shape[1], size=n, replace=False)

    fig, ax = plt.subplots(figsize=(12, 6))

    for i in idx:
        ax.plot(days, paths[:, i], alpha=0.3, linewidth=0.8, color="#ff7f0e")

    ax.plot(days, np.percentile(paths, 50, axis=1), color="black", linewidth=2, label="Медиана")
    ax.set_title(f"Примеры траекторий — {asset_name} ({n} из 10 000)", fontsize=14)
    ax.set_xlabel("Торговые дни")
    ax.set_ylabel("Цена (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    ax.legend()
    ax.grid(alpha=0.3)

    path = OUTPUT_DIR / f"paths_{asset_name.replace('/', '_')}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Сохранён: {path}")
    