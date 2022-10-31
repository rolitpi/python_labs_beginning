from typing import Any

import pandas as pd

import matplotlib.pyplot as plt

from pandas import DataFrame
from texttable import Texttable

from TaskInput import TaskInput
from TempComparingUnit import TempComparingUnit


class Processor:
    __DEFAULT_DF_INDEX_NAME = 'date'
    __BEFORE_NOON_HOURS = [f'{i:>02}' for i in range(0, 13)]
    __AFTER_NOON_HOURS = [f'{i:>02}' for i in range(13, 24)]

    __loaded_df: DataFrame
    __max_temps: TempComparingUnit
    __min_temps: TempComparingUnit
    __mean_temps: TempComparingUnit

    def load_df(self, file_name: str) -> None:
        excel_file = pd.ExcelFile(file_name)
        df = excel_file.parse(0)

        def_col_names = [self.__DEFAULT_DF_INDEX_NAME] + self.__BEFORE_NOON_HOURS + self.__AFTER_NOON_HOURS
        df = df.set_axis(def_col_names, axis=1, copy=False)

        df = df.groupby(pd.Grouper(key=self.__DEFAULT_DF_INDEX_NAME, freq='M'))

        df.plot(legend=True)
        plt.show()

        self.__loaded_df = df

    def calculate(self) -> None:
        self.__max_temps = self.__get_max_temps()
        self.__min_temps = self.__get_min_temps()
        self.__mean_temps = self.__get_mean_temps()

    def print(self, input_tasks: [TaskInput]) -> None:
        table = Texttable()
        cols = ["Месяц",
                "MAX - AVG", "MAX - MIN", "AVG - MIN",
                "MAX - AVG (<=12:00)", "MAX - MIN (<=12:00)", "AVG - MIN (<=12:00)",
                "MAX - AVG (>12:00)", "MAX - MIN (>12:00)", "AVG - MIN (>12:00)"]
        table.header(cols)
        for task in input_tasks:
            table.add_row(self.__prepare_single_task(task))
        table.set_cols_width([15 for _ in range(0, len(cols))])
        print(table.draw())

    def __prepare_single_task(self, task: TaskInput) -> [Any]:
        order = task.month_order

        max_before = self.__max_temps.before[order].max()
        max_after = self.__max_temps.after[order].max()
        max_all = self.__max_temps.all[order].max()

        min_before = self.__min_temps.before[order].min()
        min_after = self.__min_temps.after[order].min()
        min_all = self.__min_temps.all[order].min()

        mean_all = self.__mean_temps.all[order].mean()
        mean_before = self.__mean_temps.before[order].mean()
        mean_after = self.__mean_temps.after[order].mean()

        return [task.name,
                max_all - mean_all, max_all - min_all, mean_all - min_all,
                max_before - mean_before, max_before - min_before, mean_before - min_before,
                max_after - mean_after, max_after - min_after, mean_after - min_after]

    def __get_max_temps(self) -> TempComparingUnit:
        max_temp_by_hours = self.__loaded_df.max()

        return TempComparingUnit(max_temp_by_hours[self.__BEFORE_NOON_HOURS].transpose().max(),
                                 max_temp_by_hours[self.__AFTER_NOON_HOURS].transpose().max(),
                                 max_temp_by_hours.transpose().max())

    def __get_min_temps(self) -> TempComparingUnit:
        min_temp_by_hours = self.__loaded_df.min()

        return TempComparingUnit(min_temp_by_hours[self.__BEFORE_NOON_HOURS].transpose().min(),
                                 min_temp_by_hours[self.__AFTER_NOON_HOURS].transpose().min(),
                                 min_temp_by_hours.transpose().min())

    def __get_mean_temps(self) -> TempComparingUnit:
        mean_temp_by_hours = self.__loaded_df.mean()

        return TempComparingUnit(mean_temp_by_hours[self.__BEFORE_NOON_HOURS].transpose().mean(),
                                 mean_temp_by_hours[self.__AFTER_NOON_HOURS].transpose().mean(),
                                 mean_temp_by_hours.transpose().mean())
