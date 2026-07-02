from pprint import pprint

from tools.ds_tools.dataset_analyzer import (
    DatasetAnalyzer
)

tool = DatasetAnalyzer()

report = tool.analyze(
    "../datasets/data_science/sample.csv"
)

pprint(report)