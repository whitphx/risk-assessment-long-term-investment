import argparse
import logging
from typing import Optional

from matplotlib import pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


def calc_long_term_investment_statistics(
    yearly_average: float,
    yearly_stddev: float,
    years: int,
    n_samples: int,
    out_filepath: Optional[str],
):
    logger.info("Yearly average: %f", yearly_average)
    logger.info("Yearly standard deviation: %f", yearly_stddev)
    logger.info("Investment for %d years", years)
    logger.info("# of samples: %d", n_samples)

    realized_yearly_returns = np.random.normal(
        loc=yearly_average,
        scale=yearly_stddev,
        size=(n_samples, years),
    )

    realized_total_returns = 1 + realized_yearly_returns
    for shift in range(1, years):
        realized_total_returns *= (
            1
            + np.pad(realized_yearly_returns, ((0, 0), (shift, 0)), constant_values=0)[
                :, :-shift
            ]
        )
    realized_total_returns -= 1

    mean = np.mean(realized_total_returns, axis=0)
    std = np.std(realized_total_returns, axis=0)
    sharpe_ratio = mean / std
    p_loss_of_principal = np.mean(realized_total_returns < 0, axis=0)

    return mean, std, sharpe_ratio, p_loss_of_principal


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--yearly-average", "-m", type=float, default=0.04)
    parser.add_argument("--yearly-stddev", "-v", type=float, default=0.15)
    parser.add_argument("--years", "-y", type=int, default=20)
    parser.add_argument("--n_samples", "-n", type=int, default=100000)
    parser.add_argument("--save-fig", "-f", type=str)

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    mean, std, sharpe_ratio, p_loss_of_principal = calc_long_term_investment_statistics(
        yearly_average=args.yearly_average,
        yearly_stddev=args.yearly_stddev,
        years=args.years,
        n_samples=args.n_samples,
        out_filepath=args.save_fig,
    )

    print("Mean")
    print(mean)
    print("Standard deviation")
    print(std)
    print("Sharpe ratio")
    print(sharpe_ratio)
    print("P(loss of principal)")
    print(p_loss_of_principal)

    if args.save_fig:
        fig, axs = plt.subplots(3, 1)
        year_vals = np.arange(1, args.years + 1)

        axs[0].xaxis.set_ticks(year_vals)
        axs[0].plot(year_vals, mean, label="Mean")
        axs[0].plot(year_vals, std, label="Standard deviation")
        axs[0].legend()

        axs[1].xaxis.set_ticks(year_vals)
        axs[1].plot(year_vals, sharpe_ratio, label="Mean/Standard deviation")
        axs[1].legend()

        axs[2].xaxis.set_ticks(year_vals)
        axs[2].plot(year_vals, p_loss_of_principal, label="P(loss of principal)")
        axs[2].legend()

        plt.savefig(args.save_fig)
