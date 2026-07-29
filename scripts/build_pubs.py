import os
import bibtexparser
import yaml
from collections import defaultdict

BIB_FILE = '_bibliography/references.bib'
OUTPUT_FILE = '_data/publications.yml'

def append_raw_bib_to_publications():
    if not os.path.exists(BIB_FILE):
        print(f"Error: Could not find {BIB_FILE}")
        return

    # 1. Collect titles from existing file to avoid adding exact duplicates
    existing_titles = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as ymlfile:
            try:
                existing_data = yaml.safe_load(ymlfile) or []
                for year_block in existing_data:
                    for p_type in year_block.get('publication_type', []):
                        for doc in p_type.get('docs', []):
                            if 'title' in doc and doc['title']:
                                existing_titles.add(doc['title'].strip().lower())
            except Exception:
                pass  # If yaml parsing fails, we just won't duplicate-check

    # 2. Parse _bibliography/references.bib
    with open(BIB_FILE, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)

    years_data = defaultdict(lambda: {"Publications": [], "Presentations": []})
    added_count = 0

    for entry in bib_database.entries:
        title = entry.get('title', '').replace('{', '').replace('}', '').strip()
        
        # Skip duplicate titles
        if title.lower() in existing_titles:
            continue

        year = entry.get('year', 'Unknown').strip()
        
        # Format author list
        raw_authors = entry.get('author', '').replace('\n', ' ')
        author_list = [a.strip() for a in raw_authors.split(' and ') if a.strip()]
        if len(author_list) > 1:
            authors = ", ".join(author_list[:-1]) + ", and " + author_list[-1]
        elif author_list:
            authors = author_list[0]
        else:
            authors = ""

        # Retrieve URL or construct DOI link
        url = entry.get('url', entry.get('doi', '')).strip()
        if url and not url.startswith('http'):
            url = f"https://doi.org/{url}"

        journal = entry.get('journal', entry.get('booktitle', entry.get('howpublished', ''))).strip()

        item = {
            'title': title,
            'authors': authors,
            'location': journal,
            'url': url
        }

        # Categorize entry
        entry_type = entry.get('ENTRYTYPE', '').lower()
        if entry_type in ['article', 'inproceedings', 'book', 'techreport', 'phdthesis']:
            years_data[year]["Publications"].append(item)
        else:
            years_data[year]["Presentations"].append(item)
        
        added_count += 1

    if added_count == 0:
        print("No new entries found in BibTeX!")
        return

    # 3. Format only the NEW entries into YAML
    new_blocks = []
    sorted_years = sorted(years_data.keys(), key=lambda y: int(y) if y.isdigit() else 0, reverse=True)

    for year in sorted_years:
        pub_types = []
        if years_data[year]["Presentations"]:
            pub_types.append({'type': 'Presentations', 'docs': years_data[year]["Presentations"]})
        if years_data[year]["Publications"]:
            pub_types.append({'type': 'Publications', 'docs': years_data[year]["Publications"]})

        new_blocks.append({
            'year': int(year) if year.isdigit() else year,
            'publication_type': pub_types
        })

    # Dump ONLY the new blocks to a YAML string
    new_yaml_text = yaml.dump(new_blocks, sort_keys=False, allow_unicode=True)

    # 4. Append to the end of _data/publications.yml in append mode ('a')
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as ymlfile:
        ymlfile.write("\n" + new_yaml_text)

    print(f"Successfully appended {added_count} new entries to the bottom of {OUTPUT_FILE}!")

if __name__ == '__main__':
    append_raw_bib_to_publications()
