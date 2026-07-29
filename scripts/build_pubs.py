import os
import bibtexparser
import yaml

BIB_FILE = '_bibliography/references.bib'
OUTPUT_FILE = '_data/publications.yml'

def format_journal_citation(entry):
    """Formats a BibTeX entry into a standard academic journal citation string without Markdown formatting."""
    # 1. Title
    title = entry.get('title', '').replace('{', '').replace('}', '').strip()
    
    # 2. Authors (Clean up whitespace and newlines)
    raw_authors = entry.get('author', '').replace('\n', ' ')
    author_list = [a.strip() for a in raw_authors.split(' and ') if a.strip()]
    if len(author_list) > 1:
        authors = ", ".join(author_list[:-1]) + ", and " + author_list[-1]
    elif author_list:
        authors = author_list[0]
    else:
        authors = ""

    # 3. Journal details (Journal Name, Vol, No, Pages, Year)
    journal = entry.get('journal', entry.get('booktitle', entry.get('howpublished', ''))).strip()
    volume = entry.get('volume', '').strip()
    number = entry.get('number', '').strip()
    pages = entry.get('pages', '').replace('--', '-').strip()
    year = entry.get('year', '').strip()

    # Build the location string without asterisks
    # Format: Journal Name, vol. X, no. Y, pp. Z, (Year)
    location_parts = []
    if journal:
        location_parts.append(journal)  # Clean text with no asterisks
    if volume:
        location_parts.append(f"vol. {volume}")
    if number:
        location_parts.append(f"no. {number}")
    if pages:
        location_parts.append(f"pp. {pages}")
    if year:
        location_parts.append(f"({year})")

    location_str = ", ".join(location_parts)

    # 4. URL / DOI
    url = entry.get('url', entry.get('doi', '')).strip()
    if url and not url.startswith('http'):
        url = f"https://doi.org/{url}"

    return {
        'title': title,
        'authors': authors,
        'location': location_str,
        'url': url
    }

def main():
    if not os.path.exists(BIB_FILE):
        print(f"Error: Could not find {BIB_FILE}")
        return

    # Parse BibTeX
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_data = bibtexparser.load(f)

    # Convert entries
    formatted_docs = []
    for entry in bib_data.entries:
        formatted_docs.append(format_journal_citation(entry))

    if not formatted_docs:
        print("No entries found in BibTeX file.")
        return

# Append flat list of docs directly
    new_yaml_block = formatted_docs

    # Append directly to the bottom of _data/publications.yml
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write("\n" + yaml.dump(new_yaml_block, sort_keys=False, allow_unicode=True))
    # Append directly to the bottom of _data/publications.yml
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write("\n" + yaml.dump(new_yaml_block, sort_keys=False, allow_unicode=True))

    print(f"Successfully appended {len(formatted_docs)} clean journal citations to {OUTPUT_FILE}!")

if __name__ == '__main__':
    main()
