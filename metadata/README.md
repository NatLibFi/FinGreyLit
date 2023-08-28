# Metadata records

The metadata records representing individual documents are split into files that have been divided along three dimensions: document type, language and train/test subset.

## Data format

The metadata is represented as JSON records in [JSON Lines](https://jsonlines.org/) format. That is, each line in a file is a JSON object representing a single document. The files can be easily analyzed using tools like `grep` and `jq`. They can also be parsed in e.g. Python by iterating over the lines of a file and parsing each line as JSON, like this:

```python
import json

JSONL_FILE = "docthes-eng-test.jsonl"
with open(JSONL_FILE) as jsonl_file:
    for line in jsonl_file:
        record = json.loads(line)
        # record is now a dictionary with keys such as `url` and `dc.title`:
        print(f"PDF file at {record['url']} has title {record['dc.title']}")
```

## File naming

The files in the data set have been named using the following pattern:

    <doctype>-<language>-<subset>.jsonl

Where `<doctype>` represents the document type, `<language>` the document language and `<subset>` the train/test subset. For details on these divisions, see below.

## Document types

The records representing individual documents have been divided into four distinct categories based on the nature of the documents. This categorization has been done with the aim of grouping similar types of documents together, each sharing common metadata fields. The following document categories have been established:

### Thesis Documents (`thes`)
Thesis documents serve as supporting material for academic degrees, typically at the bachelor's or master's level. The metadata associated with these documents usually encompasses details about the academic institution, faculty or relevant organizational units, the specific degree program, and the subject of study. It's important to note that this category excludes doctoral degrees.

### Doctoral Theses (`docthes`)

Doctoral theses, commonly known as dissertations, form a distinct category. Their metadata structure closely resembles that of bachelor's and master's theses, encompassing information about the educational institution and the subject matter. Additionally, this category's metadata often provides details about the supervising professor, reviewers, and opponent(s). Doctoral theses are typically published with ISBNs, often as part of a university-managed publication series. Therefore, the metadata here includes pertinent series information such as name, ISSNs, and numbering.

### Serial Publications (`serial`)

Serial publications, including journals, book series, and institutional blogs, are grouped under this category. The metadata for these publications is designed to identify the corresponding publication series. This entails furnishing information such as the series name, ISSNs, and any relevant numbering conventions.

### Monograph Publications (`mono`)

The monograph publications category encompasses a diverse range of works. It covers all publications that don't fall under the thesis umbrella and aren't part of a series. It's worth noting that the term "monograph" might be somewhat misleading, as this category includes various works like book chapters and articles, in addition to standalone publications.

## Languages

The records are divided into Finnish (`fin`), Swedish (`swe`) or English (`eng`) according to the main language of the document.

## Train/test split

Each records has been semi-randomly assigned into either the `train` or `test` subset, with approximately 75% of records in the train set and 25% in the test set. The intent is that for machine learning approaches, the train subset will be used for training models and the test set for evaluating the models.
