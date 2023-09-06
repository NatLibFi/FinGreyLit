# FinGreyLit

This repository contains a data set of curated Dublin Core style metadata from a selection of Finnish "grey literature" publications, along with links to the PDF publications. The dataset is mainly intended to enable and facilitate the development of automated methods for metadata extraction from PDF files, including but not limited to the use of large language models (LLMs).

The publications have been sampled from various DSpace based open repository systems administered by the National Library of Finland. The dataset is trilingual, containing publications in Finnish, Swedish and English language.

All the publication PDF files are openly accessible from the original DSpace systems. Due to copyright concerns, this repository contains only the curated metadata and links to the original PDF files. The repository contains scripts for downloading the PDF publications from the original repositories and extracting the full text.

# Metadata format and schema

The metadata is represented as JSONL files. See [metadata/README.md](metadata/README.md) for details about the file format and [schema.md](schema.md) for information about the metadata schema.

For some statistics about the included documents and their metadata, see the automatically generated [statistics report](statistics.md).

# Contents

* [metadata/](metadata/) contains the metadata records as JSONL files
* [conversion/](conversion/) contains Jupyter notebooks for processing the metadata
* [experiments/](experiments/) contains experiments (in the form of Jupyter notebooks) for metadata extraction

# Collection and curation process

## Initial harvesting

The documents were originally harvested from nine different DSpace repositories (Doria, Julkari, Kaisu, LutPub, Osuva, Taju, Theseus, Trepo, UtuPub) that are used for public archiving documents from different Finnish academic and public sector organisations. The criteria for inclusion of individual documents include:

* published in a collection which has a significant number of documents is growing every year
* PDF format
* freely accessible on the web
* born digital (not digitized older documents)
* published in DSpace in 2020-2023, with the original publication date between 2012-2023
* at most 200 documents from the same collection (though in practice much less)

The harvesting resulted in approximately 7000 documents.

## Selection and curation

The harvested document metadata was placed in a Google Sheets document on four tabs, separated by document type. We curated the metadata, checking each document and harmonized the metadata fields so that similar documents from different repositories were represented in the same way despite many differences in the original metadata practices. We selected approximately 200 documents of each type, aiming for good representation in terms of document types and genres, languages and sources. We have had to exclude some documents due to various problems in the selection and curation process, so currently there are around 700 documents.

## Conversion to structured metadata

While the Sheets document is still used for curation and adjustments, we have since converted the metadata into files in an easily machine-processable, structured JSONL format, which can be found under the [metadata](metadata) directory. The conversion is handled by the Jupyter Notebook (with Python code) that can be found under the [conversion](conversion) directory.

# License

The content of this repository is freely available under the CC0 license. The original metadata used in creating this data set is not copyrightable.

The original publications referenced in this data set are copyrighted by their authors and/or publishers.

# Credits

* Original authors of the publications
* The people who originally entered metadata for the publications in DSpace (often the authors themselves)
* Tuukka Hämäläinen who curated and harmonized the metadata
* NatLibFi automated cataloguing team (Mona Lehtinen, Osma Suominen, Juho Inkinen) for overseeing the project
