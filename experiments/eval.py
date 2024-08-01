import json
import Levenshtein
import pandas as pd


class MetadataEvaluator:
    # similarity threshold to be considered "almost correct":
    ALMOST_THRESHOLD = 0.95
    ALL_FIELDS = (
        "language",
        "title",
        "creator",
        "year",
        "publisher",
        "doi",
        "e-isbn",
        "p-isbn",
        "e-issn",
        "p-issn",
        "type_coar"
    )

    def __init__(self, filename=None):
        self.filename = filename

    def _load_records(self):
        records = []
        with open(self.filename) as infile:
            for line in infile:
                rec = json.loads(line)
                # robustness: only accept dict values for prediction
                if not isinstance(rec["prediction"], dict):
                    rec["prediction"] = {}
                records.append(rec)
        return records

    def evaluate_records(self, records=None):
        if records is None:
            records = self._load_records()
        results = []

        for rec in records:
            for field in self.ALL_FIELDS:
                match_type, score = self._compare(rec, field)
                results.append(
                    {
                        "rowid": rec["rowid"],
                        "language": rec["ground_truth"].get("language"),
                        "field": field,
                        "predicted_val": rec["prediction"].get(field),
                        "true_val": rec["ground_truth"].get(field),
                        "match_type": match_type,
                        "score": score,
                    }
                )
        return results

    def _compare(self, rec, field):
        true_val = rec["ground_truth"].get(field)
        pred_val = rec["prediction"].get(field)

        # language
        if field == 'language':
            return self._compare_simple_string(true_val, pred_val)

        # title
        if field == 'title':
            return self._compare_fuzzy_string(true_val, pred_val)

        # creator (multiple values)
        if field == 'creator':
            return self._compare_set(true_val, pred_val)

        # year
        if field == 'year':
            return self._compare_simple_string(true_val, pred_val)

        # publisher (multiple values)
        if field == 'publisher':
            return self._compare_set(true_val, pred_val)

        # DOI
        if field == 'doi':
            return self._compare_simple_string(true_val, pred_val)

        # e-isbn or p-isbn (multiple values)
        if field in ('e-isbn', 'p-isbn'):
            return self._compare_set(true_val, pred_val)

        # e-issn
        if field == 'e_issn':
            return self._compare_e_issn(true_val, pred_val, rec["ground_truth"].get("p-issn"))

        # p-issn
        if field == 'p_issn':
            return self._compare_simple_string(true_val, pred_val)

        # type_coar
        if field == 'type_coar':
            return self._compare_simple_string(true_val, pred_val)

        # other/unknown, use simple string comparison
        return self._compare_simple_string(true_val, pred_val)

    def _compare_simple_string(self, true_val, pred_val):
        if pred_val is None and true_val is None:
            return ("not-relevant", 1)
        elif true_val is None:
            return ("found-nonexistent", 0)
        elif pred_val is None:
            return ("not-found", 0)
        elif true_val == pred_val:
            return ("exact", 1)
        else:
            return ("wrong", 0)

    def _compare_e_issn(self, true_val, pred_val, p_issn_val):
        base_result = self._compare_simple_string(true_val, pred_val)

        if base_result[0] != 'wrong':
            return base_result

        # check whether the predicted ISSN is a printed ISSN
        if p_issn_val and pred_val == p_issn_val:
            if true_val:
                return ("printed-issn", 0)
            else:
                return ("printed-issn", 1)

        return ("wrong", 0)

    def _compare_fuzzy_string(self, true_val, pred_val):
        base_result = self._compare_simple_string(true_val, pred_val)

        if base_result[0] != 'wrong':
            return base_result

        # check for fuzzy matches
        if true_val.lower() == pred_val.lower():
            return ('case', 1)
        elif Levenshtein.ratio(true_val, pred_val) >= self.ALMOST_THRESHOLD:
            return ('almost', 1)
        elif Levenshtein.ratio(true_val.lower(), pred_val.lower()) >= self.ALMOST_THRESHOLD:
            return ('almost-case', 1)
        else:
            return ('wrong', 0)

    def _compare_set(self, true_val, pred_val):
        true_set = set(true_val) if true_val else set()
        pred_set = set(pred_val) if pred_val else set()
        if not true_set and not pred_set:
            return ("not-relevant", 1)
        elif not true_set:
            return ("found-nonexistent", 0)
        elif not pred_set:
            return ("not-found", 0)
        elif true_set == pred_set:
            return ("exact", 1)
        elif true_set.issubset(pred_set):
            return ("superset", 1)
        elif true_set.issuperset(pred_set):
            return ("subset", 0)
        elif true_set.intersection(pred_set):
            return ("overlap", 0)
        else:
            return ("wrong", 0)

    def save_md(self, results, filename, fields=None):
        """Save results statistics in a md file"""

        df = pd.DataFrame(results)
        if fields is not None:  # Use only given fields
            df = df[df["field"].isin(fields)]

        with open(filename, "wt") as ofile:
            print(
                df.groupby(["language", "field"])["score"]
                .agg(["mean", "size"])
                .reset_index()
                .rename(columns={"idx1": "", "idx2": ""})
                .to_markdown(tablefmt="github", floatfmt=".4f", index=False),
                file=ofile,
            )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    # Define command-line arguments
    parser.add_argument("filename", help="File with the records to evaluate.")
    parser.add_argument(
        "statistics_filename", help="File where to write evaluation statistics."
    )
    args = parser.parse_args()

    evaluator = MetadataEvaluator(args.filename)
    results = evaluator.evaluate_records()

    evaluator.save_md(results, args.statistics_filename, evaluator.ALL_FIELDS)
