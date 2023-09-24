from typing import Optional
from dataclasses import dataclass
import pandas as pd

from waltzboard.explorer import Explorer, TrainResult
from waltzboard.generator import Generator
from waltzboard.model import WaltzboardDashboard, BaseChart, ChartTokens
from waltzboard.config import WaltzboardConfig
from waltzboard.oracle import Oracle
from waltzboard.utills import display_function
from waltzboard.model import (
    is_valid_tokens,
    get_variants_from_charts,
    get_chart_from_tokens,
    get_all_charts,
)


class Waltzboard:
    oracle: Oracle
    generator: Generator
    explorer: Explorer
    config: WaltzboardConfig
    preferences: list[str]

    def __init__(
        self, df: pd.DataFrame, config: WaltzboardConfig | None = None
    ) -> None:
        self.df = df
        if config and (df is not config.df):
            raise RuntimeError("df and config.df must be same")

        self.config = WaltzboardConfig(df)
        self.update_config()
        self.preferences = []

    def update_config(self):
        self.oracle = Oracle(self.config)
        self.generator = Generator(self.config)
        self.explorer = Explorer(self.config)

    def train_display(self, preferences: list[str]) -> None:
        self.preferences = preferences
        train_results: list[TrainResult] = []
        for epoch in range(self.config.n_epoch):
            train_result = self.explorer._train(
                self.generator, self.oracle, preferences
            )
            train_results.append(train_result)
            display_function(epoch, train_results)

    def train(self, preferences: list[str]) -> list[TrainResult]:
        self.preferences = preferences
        return self.explorer.train(self.generator, self.oracle, preferences)

    def is_valid_tokens(self, key: ChartTokens):
        return is_valid_tokens(key, self.config)

    def get_variants_from_chart(self, chart: BaseChart):
        return get_variants_from_charts(chart, self.config)

    def get_chart_from_tokens(self, key: ChartTokens):
        if not self.is_valid_tokens(key):
            raise Exception("Chart tuple is not valid")
        return get_chart_from_tokens(key, self.config)

    def get_all_charts(self):
        return get_all_charts(self.config)