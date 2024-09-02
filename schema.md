# Metadata Schema

These fields are used in the metadata records. Most fields are adapted from Dublin Core, but some are custom adaptations or ad-hoc extensions.
The type column indicates whether the field is allowed to have only a single value or multiple values, or whether it's a sub-object:

- S: single-value
- M: multi-value 
- O: object

For some statistics on actual usage of these metadata fields in different types of document, see the [statistics report](statistics.md).

## General information

| Field name                | Description                                                                                                              | Example                                                                                                          | Type |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|------|
| `doctype`                   | The document type: `thes`, `docthes`, `report`, `book` or `article`.                                                   | `docthes`                                                                                                        | S |
| `subset`                    | The subset for machine learning purposes which this document belongs to, either `train` or `test`.                       | `train`                                                                                                          | S |
| `repository`                | The name of the repository from which the record was harvested.                                                         | `Theseus`                                                                                                        | S |
| `id`                        | The identifier of the document. This is a DSpace URL that will show a landing page for the document.                    | `https://www.utupub.fi/handle/10024/148744`                                                                    | S |
| `url`                       | The URL of the PDF document.                                                                                             | `https://www.utupub.fi/bitstream/handle/10024/148744/Kossila_Johannes_opinnayte.pdf`                             | S |
| `rowid`                     | The sheet ID and row number of the record in the metadata curation spreadsheet. Used for tracing changes back to the spreadsheet to make corrections. | `thes123`                                                                                                     | S |
| `ground_truth`              | The ground truth metadata about the document as a sub-object, see below.                                                 | `{ "title": "My title" }`                                                                                     | O | 

## Ground truth metadata

The ground truth metadata is given as a separate object in the field `ground_truth`. In this context, "ground truth" means that the metadata corresponds with what can be seen by a human cataloguer looking at the PDF document.

Ground truth metadata can contain the following fields:


| Field name                | Description                                                                                                              | Example                                                                                                          | Type |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|------|
| `language`           | The language of the resource expressed as a BCP47 language tag.                                                               | `fi`                                                                                                            | S |
| `title`                  | The main title of the publication.                                                                                       | `Developing a football game for Android`                                                                                 | S |
| `alt_title`                  | Alternative or parallel titles of the publication, suffixed with a BCP47 language tag.                               | `Jalkapallopelin kehittäminen Androidille {fi}`                                                                                 | S |
| `creator`     | The primary author(s) of the resource.                                                                                      | `Rajala, Hanna`                                                                                                  | M |
| `year`        | The year on which the resource was issued or made available.                                                              | `2023`                                                                                                     | S |
| `publisher`              | The entity/entities responsible for making the resource available.                                                                 | `Luonnonvarakeskus`                                                                                              | M |
| `doi`         | The Digital Object Identifier (DOI) associated with the resource.                                                          | `10.1234/abcd.56789`                                                                                            | S |
| `e-isbn`      | The International Standard Book Number (ISBN) associated with the resource.                                               | `978-0-123456-78-9`                                                                                             | M |
| `p-isbn`          | The ISBN of the printed version of this document.                                               | `978-0-987654-32-1`                                                                                             | M |
| `e-issn`         | The Electronic International Standard Serial Number (e-ISSN) of the resource.                                               | `1234-5678`                                                                                                      | S |
| `p-issn`         | The Print International Standard Serial Number (p-ISSN) of the printed version of this document.                                                   | `9876-5432`                                                                                                      | S |
| `type_coar`              | The type of the resource according to the Confederation of Open Access Repositories [Resource Types classification](https://vocabularies.coar-repositories.org/resource_types/). | `research article`                                                                                            | S |

