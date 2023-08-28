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

# License

The content of this repository is freely available under the CC0 license. The original metadata used in creating this data set is not copyrightable.

The original publications referenced in this data set are copyrighted by their authors and/or publishers.

# Credits

* Original authors of the publications
* The people who originally entered metadata for the publications in DSpace (often the authors themselves)
* Tuukka Hämäläinen who curated and harmonized the metadata
* NatLibFi automated cataloguing team (Mona Lehtinen, Osma Suominen, Juho Inkinen) for overseeing the project
