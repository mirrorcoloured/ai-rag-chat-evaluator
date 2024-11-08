import logging
import re

from .base_metric import BaseMetric

logger = logging.getLogger("evaltools")


class AnswerLengthMetric(BaseMetric):
    METRIC_NAME = "answer_length"

    @classmethod
    def evaluator_fn(cls, **kwargs):
        def answer_length(*, response, **kwargs):
            if response is None:
                logger.warning("Received response of None, can't compute answer_length metric. Setting to -1.")
                return {cls.METRIC_NAME: -1}
            return {cls.METRIC_NAME: len(response)}

        return answer_length

    @classmethod
    def get_aggregate_stats(cls, df):
        # remove -1 values from the mean calculation
        df = df[df[cls.METRIC_NAME] != -1]
        return {
            "mean": round(df[cls.METRIC_NAME].mean(), 2),
            "max": int(df[cls.METRIC_NAME].max()),
            "min": int(df[cls.METRIC_NAME].min()),
        }


class HasCitationMetric(BaseMetric):
    METRIC_NAME = "has_citation"

    @classmethod
    def evaluator_fn(cls, **kwargs):
        def has_citation(*, response, **kwargs):
            if response is None:
                logger.warning("Received response of None, can't compute has_citation metric. Setting to -1.")
                return {cls.METRIC_NAME: -1}
            return {cls.METRIC_NAME: bool(re.search(r"\[[^\]]+\]", response))}

        return has_citation

    @classmethod
    def get_aggregate_stats(cls, df):
        df = df[df[cls.METRIC_NAME] != -1]
        return {
            "total": int(df[cls.METRIC_NAME].sum()),
            "rate": round(df[cls.METRIC_NAME].mean(), 2),
        }


class CitationMatchMetric(BaseMetric):
    METRIC_NAME = "citation_match"

    @classmethod
    def evaluator_fn(cls, **kwargs):
        def citation_match(*, response, ground_truth, **kwargs):
            if response is None:
                logger.warning("Received response of None, can't compute citation_match metric. Setting to -1.")
                return {cls.METRIC_NAME: -1}
            # Return true if all citations in the truth are present in the response
            truth_citations = set(re.findall(r"\[([^\]]+)\.\w{3,4}(#page=\d+)*\]", ground_truth))
            response_citations = set(re.findall(r"\[([^\]]+)\.\w{3,4}(#page=\d+)*\]", response))
            citation_match = truth_citations.issubset(response_citations)
            return {cls.METRIC_NAME: citation_match}

        return citation_match

    @classmethod
    def get_aggregate_stats(cls, df):
        df = df[df[cls.METRIC_NAME] != -1]
        return {
            "total": int(df[cls.METRIC_NAME].sum()),
            "rate": round(df[cls.METRIC_NAME].mean(), 2),
        }


class LatencyMetric(BaseMetric):
    METRIC_NAME = "latency"

    @classmethod
    def evaluator_fn(cls, **kwargs):
        def latency(**kwargs):
            # Return no additional data, since latency is already stored in the target response
            return {}

        return latency

    @classmethod
    def get_aggregate_stats(cls, df):
        return {
            "mean": round(df[cls.METRIC_NAME].mean(), 2),
            "max": df[cls.METRIC_NAME].max(),
            "min": df[cls.METRIC_NAME].min(),
        }



class NumberOfEsMetric(BaseMetric):
    METRIC_NAME = "number_of_es"

    @classmethod
    def evaluator_fn(cls, **kwargs):
        def number_of_es(*, response, **kwargs):
            if response is None:
                logger.warning(f"Received response of None, can't compute {cls.METRIC_NAME} metric. Setting to -1.")
                return {cls.METRIC_NAME: -1}
            return {cls.METRIC_NAME: sum([1 for char in response if char == "e"])}

        return number_of_es

    @classmethod
    def get_aggregate_stats(cls, df):
        # remove -1 values from the mean calculation
        df = df[df[cls.METRIC_NAME] != -1]
        return {
            "mean": round(df[cls.METRIC_NAME].mean(), 2),
            "max": int(df[cls.METRIC_NAME].max()),
            "min": int(df[cls.METRIC_NAME].min()),
        }
