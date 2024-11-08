* Prompt metrics
  1. Create prompt in `.prompty` file in `src\evaltools\eval\evaluate_metrics\prompts`
  2. Create class in `src\evaltools\eval\evaluate_metrics\prompt_metrics.py`
    * `METRIC_NAME` must match filename

* Code metrics
  1. Create class in `src\evaltools\eval\evaluate_metrics\code_metrics.py` with desired behavior

* All metrics
  1. Import class in  `src\evaltools\eval\evaluate_metrics\__init__.py` and add to `metrics`
