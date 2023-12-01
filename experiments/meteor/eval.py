"""
Description.  # TODO
"""

import json
import Levenshtein


ALMOST_THRESHOLD = 0.95  # similarity threshold to be considered "almost correct"

LANGMAP = {"fin": "fi", "swe": "sv", "eng": "en"}

FIELDS = {
    "year": "dc.date.issued",
    "language": "dc.language.iso",
    "title": "dc.title",
    "publisher": "dc.publisher",
    "authors": "dc.contributor.author",
    "isbn": "dc.identifier.isbn",
    "issn": "dc.relation.eissn",
}


def evaluate_records(records, prediction_output_key):
    results = []

    for rec in records:
        for field, dc_field in FIELDS.items():
            match_type, score = compare(rec, prediction_output_key, dc_field, field)
            results.append(
                {
                    "rowid": rec["rowid"],  # TODO Should this be optional?
                    "language": rec["dc.language.iso"],
                    "field": field,
                    "predicted_val": get_prediction(rec, prediction_output_key, field),
                    "true_val": rec.get(dc_field),
                    "match_type": match_type,
                    "score": score,
                }
            )
    return results


def compare(rec, prediction_output_key, dc_key, field_key):
    true_val = rec.get(dc_key)

    # special case for "authors" field which may contain multiple values
    if dc_key == "dc.contributor.author":
        return compare_authors(rec, prediction_output_key)

    # field-specific adjustments
    if dc_key == "dc.language.iso":
        true_val = LANGMAP[true_val]  # convert to ISO 639-1 2-letter language code
    elif dc_key == "dc.date.issued" and true_val is not None:
        true_val = true_val[:4]  # compare only the year
    elif dc_key == "dc.identifier.isbn" and true_val:
        true_val = true_val[0]  # compare only against first (usually only) ISBN
        true_val = true_val.replace("-", "")  # strip dashes in ISBNs
    elif dc_key == "dc.publisher" and true_val:
        true_val = true_val[0]  # compare only against first (usually only) publisher

    predicted_val = get_prediction(rec, prediction_output_key, field_key)

    if predicted_val is None and true_val is None:
        return ("not-relevant", 1)
    elif predicted_val == true_val:
        return ("exact", 1)
    elif predicted_val is None:
        return ("not-found", 0)
    elif dc_key == "dc.relation.eissn" and predicted_val == rec.get(
        "dc.relation.pissn"
    ):
        if true_val is None:
            return (
                "printed-issn",
                1,
            )  # this is the only ISSN available, so counts as a success
        else:
            return (
                "printed-issn",
                0,
            )  # Meteor chose the wrong (printed) ISSN even though an e-ISSN was available
    elif dc_key == "dc.identifier.isbn" and predicted_val == rec.get(
        "dc.relation.isbn", [""]
    )[0].replace("-", ""):
        return ("related-isbn", 0)
    elif true_val is None:
        return ("found-nonexistent", 0)
    elif true_val in predicted_val:
        return ("superset", 1)
    elif true_val.lower() == predicted_val.lower():
        return ("case", 1)
    elif true_val.lower() in predicted_val.lower():
        return ("superset-case", 1)
    elif Levenshtein.ratio(true_val, predicted_val) >= ALMOST_THRESHOLD:
        return ("almost", 1)
    elif Levenshtein.ratio(true_val.lower(), predicted_val.lower()) >= ALMOST_THRESHOLD:
        return ("almost-case", 1)
    else:
        # if meteor_key not in ('title', 'language', 'year'):
        # if meteor_key == 'issn':
        #    print(rec['id'], meteor_key, repr(true_val), repr(predicted_val))
        return ("wrong", 0)


def compare_authors(rec, prediction_output_key):
    true_authors = set(rec.get("dc.contributor.author", []))
    try:
        predicted_authors = set(
            [
                f"{author['lastname']}, {author['firstname']}"
                for author in rec[prediction_output_key]["authors"]
            ]
        )
    except (KeyError, TypeError):
        predicted_authors = set()

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


def get_prediction(rec, prediction_output_key, prediction_field_key):
    try:
        return str(rec[prediction_output_key][prediction_field_key]["value"])
    except (KeyError, TypeError):
        return None


if __name__ == "__main__":
    import argparse

    # TODO ADD description="A script for evaluating extracted metadata records."
    parser = argparse.ArgumentParser()

    # Define command-line arguments
    parser.add_argument("filename", help="Description of the filename")
    parser.add_argument("--fields", type=str)
    args = parser.parse_args()

    prediction_output_key = "meteor_output"

    records = []
    with open(args.filename) as infile:
        for line in infile:
            rec = json.loads(line)
            records.append(rec)

    output = evaluate_records(records, prediction_output_key)  # args.fields)

    print(output)
