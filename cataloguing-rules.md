# Cataloguing rules

This document describes the cataloguing rules that are being applied for creating the ground truth metadata for FinGreyLit.

## Ground Truth principle

The **most important rule** is that FinGreyLit metadata should follow the [ground truth](https://en.wikipedia.org/wiki/Ground_truth) principle, that is, the statements in the metadata should be **grounded** in the publications themselves. This means that the metadata must only contain statements that a human cataloguer would make by looking at the document itself, without access to any external registries, institutional websites or other information sources (apart from knowing the controlled vocabularies used in the metadata such as language codes and the COAR Resource Types vocabulary). This means that if the publication mentions a piece of information such as an ISBN, ISSN, DOI or publisher, it should be stated in the metadata as well. On the contrary, if the publication is published in a journal that has an ISSN and a well-known publisher, but the ISSN and publisher are not visible in the document itself, then they shouldn't be stated in the metadata either.

## Information available as images only

In some cases information in PDFs may only appear in the form of images. For example the publisher may be indicated using a logo that has no alt text that could be extracted; or a preprint of an article may be an image format without corresponding text. As long as this information is visible and legible to a (sighted) human reader, these still count as being stated in the publication, even though the information may be more difficult to extract for a machine process.

## Embedded PDF metadata

Information such as publication date or author/creator that is only available in the embedded PDF metadata (pdfinfo) but not visible in the document itself (for example when printed on paper) does not count as being stated in the publication.

## Field-specific syntax rules

There are some syntactic rules (mainly based on ISBD) that should be applied when creating the metadata, so the information isn't always catalogued in the exact same format that was used in the publication.

### Language

The main language of the publication should be stated using a BCP47 language tag, e.g. `fi`, `sv`, `en`. (Note: this is still WIP, currently ISO-639-1 codes are still used)

### Title

The main title of the publication. If there are multiple variations of the title used in the publication, prefer the full form instead of any abbreviated forms. If the different titles are of similar length, prefer the one that is given on a [title page](https://en.wikipedia.org/wiki/Title_page) along with other metadata such as author, publication date, identifiers etc.

Parallel titles, e.g. titles in other languages than the main language of the publication, should not be included in the main title. Instead they should be described in the alternative title field (see below).

#### Capitalization

Titles should be stated in sentence case, that is, capital letters should only be used as the first letter of a title and for proper names, abbreviations etc. Titles given in Title Case and ALL CAPS should be converted to sentence case.

#### Title parts

If the title consists of several parts (separated either using different font size or other layout differences, or by delimiters such as a dash, colon or full stop) and the first part is complete and specific enough to be used as a title on its own, the parts should be separated using space-colon-space according to [ISBD](https://www.ifla.org/g/isbd-rg/isbd-editions/) style. Only the first part (title proper) should be capitalized; subsequent parts should start with a lowercase letter unless there is a specific reason for using capital letters.

Example 1: (title proper and subtitle separated using space-colon-space; subtitle starts with lowercase letter)

 * Original title: [Public service media: Exploring the influence of strong public service media on democracy](https://www.theseus.fi/bitstream/handle/10024/745029/Public_service_media_Gronvall.pdf)
 * Catalogued as: **Public service media : exploring the influence of strong public service media on democracy**

Example 2: (space-colon-space; Title Case converted to sentence case)

 * Original title: [Full-Body Interaction in a Remote Context: Adapting a Dance Piece to a Browser-Based Installation](https://taju.uniarts.fi/bitstream/handle/10024/7713/Masu_Pajala-Assefa_et_al_2022_Full-Body_Interaction_in_a_Remote_Context_Final_draft.pdf)
 * Catalogued as: **Full-body interaction in a remote context : adapting a dance piece to a browser-based installation**

Example 3: (dash is retained, because the title proper would be incomplete or misleading without it)

 * Original title: [Suomalaiset ovat kielitaitoisia – vai ovatko sittenkään?](https://www.theseus.fi/bitstream/handle/10024/503162/K%C3%A5laMattila_2021.pdf)
 * Catalogued as: **Suomalaiset ovat kielitaitoisia – vai ovatko sittenkään?**

Example 4: (colon is retained without space, because the title proper would otherwise be incomplete; drop capitalization for the subtitle)

 * Original title: [Tutkittua tietoa: Ossaamista on!](https://www.theseus.fi/bitstream/handle/10024/511633/Oamk%20Journal%2086_2021.pdf)
 * Catalogued as: **Tutkittua tietoa: ossaamista on!**

Example 5: (multiple versions - prefer the title page version; drop capitalization)
 * Title on cover page: [Viet Nam Plastics Waste Strategy](https://www.theseus.fi/bitstream/handle/10024/498683/VIET%20NAM%20PLASTICS%20STRATEGY%20final%20fix(Autosaved)%202-compressed.pdf)
 * Title on page 2 (title page): Viet Nam Plastic Waste Strategies
 * Catalogued as **Viet Nam plastic waste strategies**

### Alternative title(s)

Alternative titles are generally parallel versions of the main title in different languages.

Alternative titles should follow the same syntactic rules as the main title and also indicate the language by suffixing the title with a BCP47 language tag such as `{fi}`, `{sv}` or `{en}`.

In the case of several alternative titles, they should be listed in the order that they appear on the publication.

Example 1:
 * Original title in Swedish: [Utveckling av streaming-tjänster för sociala medier som marknadsföring och produkt](https://www.theseus.fi/bitstream/handle/10024/496477/Aberg_Jacob.pdf)
 * English title (page 4): Development of streaming services for social media as marketing and product
 * Finnish title (page 5): Suoratoistopalvelujen kehittäminen sosiaaliseen mediaan markkinointina ja tuotteena
 * Alternative titles catalogued as:
    * **Development of streaming services for social media as marketing and product {en}**
    * **Suoratoistopalvelujen kehittäminen sosiaaliseen mediaan markkinointina ja tuotteena {fi}**

### Creator(s)

Person names should be given in the style "Lastname, First Names". The most complete form of a name available in the publication should be preferred. The names should be listed in the order they appear on the publication.

Example 1: (full form available only as image)
 * Title of publication: [Siivouskemikaalien ja -menetelmien vaikutukset koulu- ja päiväkotiympäristön mikrobistoon ja sisäilman laatuun](https://www.theseus.fi/bitstream/handle/10024/276865/Siivouskemikaalien_ja_menetelmien_vaikutukset.pdf)
 * This is a self-archived version of an original article. The names are given in different forms on the cover page and in the article itself.
   * Cover page (page 1) only includes abbreviated names: "Kakko, L., Reunanen, E., Kylmäkorpi, P., Alapieti, T., Täubel, M., Mikkola, R. & Salonen, H."
   * Article itself (page 2) uses full names (e.g. Leila Kakko, Eija Reunanen), but it is an image with no text that can be easily extracted.
 * Creators catalogued as:
   * **Kakko, Leila**
   * **Reunanen, Eija**
   * **Kylmäkorpi, Paula**
   * **Alapieti, Tuomas**
   * **Täubel, Martin**
   * **Mikkola, Raimo**
   * **Salonen, Heidi**

### Editor(s)

TBD. Same syntax as creators.

### Publication year

Publication year should be indicated if and only if it is clearly visible in the publication itself and stated as a separate item, not as part of the title, abstract, DOI etc.

If more than one year is given (for example copyright year and year of printing), the latest should be chosen.

Example 1:

 * Title of publication: [Yhteiskuntavastuuraportti : Oulun ammattikorkeakoulu, lukuvuosi 2018-2019](https://www.theseus.fi/bitstream/handle/10024/475985/Oamk_Yhteiskuntavastuuraportti_2018-2019.pdf)
 * Embedded PDF metadata:
   * Created: Tue 01 Oct 2019 11:12:56 +03:00
   * Modified: Mon 14 Oct 2019 14:07:41 +03:00
 * The likely publication year 2019 can be deduced from the title and the embedded PDF metadata, but it's not clearly stated in the publication, so it **will be left blank**.

### Publisher(s)

The names of the publishers should be given in the same form as was used on the publication. If the name of the publisher is given in multiple languages, the name in the main language of the publication should be preferred.

If there are several publishers that are clearly separate entities, they should all be listed in the order they appear in the publication.

For theses, the publisher is generally the educational institution where the thesis was completed.

If the publisher name consist of several parts, they should be separated using commas.

Capitalization should follow the original publication. If there are multiple capitalization variants, sentence case should be preferred (no unnecessary capital letters).

Example 1: (multiple parts)
 * Title of publication: [Music Competitions within the Internationalization of an Arts University - Case Study of International Maj Lind Piano Competition](https://taju.uniarts.fi/bitstream/handle/10024/6481/outi_niemensivu_masters_thesis.pdf)
 * Publisher given as "Sibelius Academy" followed by "University of the Arts Helsinki" on the next line
 * Publisher catalogued as **Sibelius Academy, University of the Arts Helsinki**

Example 2: (not official name form; multiple capitalization styles)
 * Title of publication: [Viet Nam Plastic Waste Strategies](https://www.theseus.fi/bitstream/handle/10024/498683/VIET%20NAM%20PLASTICS%20STRATEGY%20final%20fix(Autosaved)%202-compressed.pdf)
 * Name of the institution given as "ARCADA" on the cover page logo and "Arcada" on the title page, even though its full official name is "Arcada University of Applied Sciences" or "Yrkeshögskolan Arcada"
 * Publisher catalogued as **Arcada**

### DOI

DOI should be given in the short form, e.g. `10.1000/182`, not in URL form that includes the resolver service.

Although DOIs themselves are case-insensitive and some punctuation may not always be significant, the DOI should be catalogued with the exact same form given in the publication.

### ISBNs (printed and electronic)

ISBNs should be catalogued without any dashes.

### ISSNs (printed and electronic)

ISSNs should be catalogued using a plain hyphen as the separator, even though the publication may use another separator style.

# Type according to COAR

The publication type should be given using the English language label from the [COAR Resource Types](https://vocabularies.coar-repositories.org/resource_types/) vocabulary.

In practice, only the following types are currently in use:
 * bachelor thesis
 * blog post
 * book
 * book part
 * book review
 * conference paper
 * doctoral thesis
 * editorial
 * journal article
 * master thesis
 * newspaper article
 * report
 * research article
 * research report
 * review article
 * thesis

TBD. In practice the classification is a bit subjective and some classes are unclear and/or overlapping.
