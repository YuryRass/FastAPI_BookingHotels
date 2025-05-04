import os
from pathlib import Path

import pandas as pd


def converter_json_to_csv(json_file: Path, csv_file: Path):
    with open(json_file, encoding="utf-8") as inputfile:
        df = pd.read_json(inputfile)
    df.to_csv(csv_file, encoding="utf-8", index=False)


if __name__ == "__main__":
    json_dir: Path = Path.cwd().joinpath("app").joinpath("tests")
    csv_dir: Path = Path.cwd().joinpath("csv_data")

    for fname in os.listdir(json_dir):
        if fname.endswith(".json") and "users" not in fname:
            csv_file = fname.replace("mock", "data").replace(".json", ".csv")
            converter_json_to_csv(
                json_dir.joinpath(fname),
                csv_dir.joinpath(csv_file),
            )
