import json
import Levenshtein


class MetadataEvaluator:
    # similarity threshold to be considered "almost correct":
    ALMOST_THRESHOLD = 0.95

    def __init__(self, filename):
        self.filename = filename

    def _load_records(self):
        records = []
        with open(self.filename) as infile:
            for line in infile:
                rec = json.loads(line)
                records.append(rec)
        return records

    def evaluate_records(self, records=None):
        if records is None:
            records = self._load_records()
        results = []

        for rec in records:
            for field in rec['prediction'].keys():
                match_type, score = self._compare(rec, field)
                results.append(
                    {
                        "rowid": rec["rowid"],
                        "language": rec['ground_truth'].get("dc.language.iso"),
                        "field": field,
                        "predicted_val": rec['prediction'][field],
                        "true_val": rec['ground_truth'].get(field),
                        "match_type": match_type,
                        "score": score,
                    }
                )
        return results

    def _compare(self, rec, field):
        true_val = rec['ground_truth'].get(field)

        # special case for "authors" field which may contain multiple values
        if field == "dc.contributor.author":
            return self._compare_authors(rec)

        # field-specific adjustments to true values
        elif field == "dc.date.issued" and true_val is not None:
            true_val = true_val[:4]  # compare only the year
        elif field == "dc.identifier.isbn" and true_val:
            true_val = true_val[0]  # compare only against first (usually only) ISBN
            true_val = [true_val.replace("-", "")]  # strip dashes in ISBNs
        elif field == "dc.publisher" and true_val:
            true_val = true_val[0]  # compare only against first (usually only) publisher

        predicted_val = rec["prediction"][field]
        if field == "dc.publisher" and predicted_val is not None:
            predicted_val = predicted_val[0]  # compare only against first (usually only) publisher

        if predicted_val is None and true_val is None:
            return ("not-relevant", 1)
        elif predicted_val == true_val:
            return ("exact", 1)
        elif predicted_val is None:
            return ("not-found", 0)
        elif field == "dc.relation.eissn" and predicted_val == rec['ground_truth'].get(
            "dc.relation.pissn"
        ):
            if true_val is None:
                return (
                    "printed-issn",
                    1,
                )  # this is the only ISSN available, so counts as a success
            else:
                # Meteor chose the wrong (printed) ISSN even though an e-ISSN was available
                return (
                    "printed-issn",
                    0,
                )
        elif field == "dc.identifier.isbn" and predicted_val[0] == rec["ground_truth"].get(
            "dc.relation.isbn", [""]
        )[0].replace("-", ""):
            return ("related-isbn", 0)
        elif true_val is None:
            return ("found-nonexistent", 0)
        elif true_val in predicted_val:
            return ("superset", 1)
        elif isinstance(true_val, str) and true_val.lower() == predicted_val.lower():
            return ("case", 1)
        elif isinstance(true_val, str) and true_val.lower() in predicted_val.lower():
            return ("superset-case", 1)
        elif isinstance(true_val, str) and Levenshtein.ratio(true_val, predicted_val) >= self.ALMOST_THRESHOLD:
            return ("almost", 1)
        elif isinstance(true_val, str) and (
            Levenshtein.ratio(true_val.lower(), predicted_val.lower())
            >= self.ALMOST_THRESHOLD
        ):
            return ("almost-case", 1)
        else:
            # if meteor_key not in ('title', 'language', 'year'):
            # if meteor_key == 'issn':
            #    print(rec['id'], meteor_key, repr(true_val), repr(predicted_val))
            return ("wrong", 0)

    def _compare_authors(self, rec):
        true_authors = set(
            rec["ground_truth"].get("dc.contributor.author", []))
        predicted_authors = set(
            rec["prediction"].get("dc.contributor.author", []))

        if not true_authors and not predicted_authors:
            return ("not-relevant", 1)
        elif not true_authors:
            return ("found-nonexistent", 0)
        elif not predicted_authors:
            return ("not-found", 0)
        elif true_authors == predicted_authors:
            return ("exact", 1)
        elif true_authors.issubset(predicted_authors):
            return ("superset", 1)
        elif true_authors.issuperset(predicted_authors):
            return ("subset", 0)
        elif true_authors.intersection(predicted_authors):
            return ("overlap", 0)
        else:
            return ("wrong", 0)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    # Define command-line arguments
    parser.add_argument("filename", help="File with the records to evaluate.")
    args = parser.parse_args()

    evaluator = MetadataEvaluator(args.filename)
    output = evaluator.evaluate_records()

    print(output)
