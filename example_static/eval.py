import os
import json

import dotenv
import pandas as pd
from tqdm import tqdm

from evaltools import service_setup
from evaltools.eval.evaluate import process_config
from evaltools.eval.evaluate_metrics import metrics_by_name

if __name__ == "__main__":
    config_path = "./config.json"
    dotenv_path = "../.env"

    dotenv_result = dotenv.load_dotenv(dotenv_path)
    print(f"Loaded dotenv: {dotenv_result}")

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)
        process_config(config)

    qafilepath = config["testdata_path"]
    requested_metrics = config["requested_metrics"]

    folder = os.path.dirname(qafilepath)
    df = pd.read_csv(qafilepath)

    for metric in requested_metrics:
        if metric not in metrics_by_name:
            print(f"Requested metric {metric} is not available. Available metrics: {metrics_by_name.keys()}")

    requested_metrics = [
        metrics_by_name[metric_name] for metric_name in requested_metrics if metric_name in metrics_by_name
    ]

    questions_with_ratings = []
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        output = {}
        output["question"] = row["question"]
        output["truth"] = row["truth"]
        output["answer"] = row["answer"]
        output["context"] = row["context"]

        for metric in tqdm(requested_metrics, leave=False):
            result = metric.evaluator_fn(
                openai_config=service_setup.get_openai_config(),
            )(
                query=row["question"],
                response=output["answer"],
                context=output["context"],
                ground_truth=row["truth"],
            )
            output.update(result)

        questions_with_ratings.append(output)

    df_out = pd.DataFrame(questions_with_ratings)
    outpath = os.path.join(folder, "results.csv")
    print(f"Writing results to {outpath}")
    df_out.to_csv(outpath, index=False)
