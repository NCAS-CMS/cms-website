import os
import bibtexparser
import yaml
from collections import defaultdict

BIB_FILE = '_bibliography/references.bib'
OUTPUT_FILE = '_data/publications_2026.yml'

def generate_new_publications_file():
    if not os.path.exists(BIB_FILE):
        print(f"Error: Could not find {BIB_FILE}")
        return

    # 1. Parse _bibliography/references.bib
    with open(BIB_FILE, 'r', encoding='utf-8') as bibfile:
        bib_database = bibtexparser.load(bibfile)

    years_data = defaultdict(lambda: {"Publications": [], "Presentations": []})

    for entry in bib_database.entries:
        title = entry.get('title', '').replace('{', '').replace('}', '').strip()
        year = entry.get('year', 'Unknown').strip()
        
        # Format author list: "Author A and Author B" -> "Author A, and Author B"
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

    # 2. Format into Jekyll structure
    output = []
    sorted_years = sorted(years_data.keys(), key=lambda y: int(y) if y.isdigit() else 0, reverse=True)

    for year in sorted_years:
        pub_types = []
        if years_data[year]["Presentations"]:
            pub_types.append({'type': 'Presentations', 'docs': years_data[year]["Presentations"]})
        if years_data[year]["Publications"]:
            pub_types.append({'type': 'Publications', 'docs': years_data[year]["Publications"]})

        output.append({
            'year': int(year) if year.isdigit() else year,
            'publication_type': pub_types
        })

    # 3. Write directly to a brand new _data/publications_2026.yml
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as ymlfile:
        yaml.dump(output, ymlfile, sort_keys=False, allow_unicode=True)

    print(f"Successfully created brand new file: {OUTPUT_FILE} from {BIB_FILE}!")

if __name__ == '__main__':
    generate_new_publications_file()
