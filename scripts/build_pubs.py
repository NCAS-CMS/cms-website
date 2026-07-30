import os
import re
import bibtexparser
import yaml

BIB_FILE = '_bibliography/references.bib'
OUTPUT_FILE = '_data/publications.yml'
TARGET_SECTION = 'Recent Publications'  # Target top-level section name

def clean_title(title):
    """Normalize title for strict deduplication matching."""
    if not title:
        return ""
    return re.sub(r'[\{\}\s\W]+', '', title).lower()

def extract_year(doc):
    """Extract numeric year from doc dict, location string, or title."""
    if 'year' in doc and str(doc['year']).isdigit():
        return int(doc['year'])

    # Search location and title for any 4-digit year pattern (19xx or 20xx)
    text_to_search = f"{doc.get('location', '')} {doc.get('title', '')}"
    matches = re.findall(r'(?:19|20)\d{2}', text_to_search)
    if matches:
        return int(matches[-1])  # Take the last year found
    return 0

def format_journal_citation(entry):
    """Formats a BibTeX entry into a standard academic journal citation dict."""
    title = entry.get('title', '').replace('{', '').replace('}', '').strip()

    raw_authors = entry.get('author', entry.get('authors', '')).replace('\n', ' ')
    author_list = [a.strip() for a in raw_authors.split(' and ') if a.strip()]
    if len(author_list) > 1:
        authors = ", ".join(author_list[:-1]) + ", and " + author_list[-1]
    elif author_list:
        authors = author_list[0]
    else:
        authors = ""

    journal = entry.get('journal', entry.get('booktitle', entry.get('howpublished', ''))).strip()
    volume = entry.get('volume', '').strip()
    number = entry.get('number', '').strip()
    pages = entry.get('pages', '').replace('--', '-').strip()
    year = entry.get('year', '').strip()

    location_parts = []
    if journal:
        location_parts.append(journal)
    if volume:
        location_parts.append(f"vol. {volume}")
    if number:
        location_parts.append(f"no. {number}")
    if pages:
        location_parts.append(f"pp. {pages}")
    if year:
        location_parts.append(f"({year})")

    location_str = ", ".join(location_parts)

    url = entry.get('url', entry.get('doi', '')).strip()
    if url and not url.startswith('http'):
        url = f"https://doi.org/{url}"

    return {
        'title': title,
        'authors': authors,
        'location': location_str,
        'url': url,
        'year': year
    }

def process_and_deduplicate():
    existing_data = []

    # 1. Load existing YAML file
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = yaml.safe_load(f) or []
        except Exception as e:
            print(f"Error reading {OUTPUT_FILE}: {e}")
            return

    # 2. Parse BibTeX and collect new entries FIRST (BibTeX takes priority for details)
    if not os.path.exists(BIB_FILE):
        print(f"Error: Could not find {BIB_FILE}")
        return

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_data = bibtexparser.load(f)

    seen_titles = set()
    new_docs = []
    for entry in bib_data.entries:
        formatted = format_journal_citation(entry)
        t = clean_title(formatted['title'])
        if t and t not in seen_titles:
            seen_titles.add(t)
            new_docs.append(formatted)

    cleaned_data = []

    # 3. Process existing YAML blocks safely and exclude items that are in BibTeX
    for year_block in existing_data:
        if not isinstance(year_block, dict):
            continue

        if year_block.get('year') in ['Work in Progress', TARGET_SECTION]:
            continue

        new_pub_types = []
        pub_types = year_block.get('publication_type') or []
        
        for pub_type in pub_types:
            if not isinstance(pub_type, dict):
                continue

            new_docs_in_type = []
            docs = pub_type.get('docs') or []
            for doc in docs:
                if not isinstance(doc, dict):
                    continue
                t = clean_title(doc.get('title', ''))
                if t and t not in seen_titles:
                    seen_titles.add(t)
                    new_docs_in_type.append(doc)

            if new_docs_in_type:
                pub_type['docs'] = new_docs_in_type
                new_pub_types.append(pub_type)

        if new_pub_types:
            year_block['publication_type'] = new_pub_types
            cleaned_data.append(year_block)

    # 4. Construct target block for 'Recent Publications'
    target_block = {
        'year': TARGET_SECTION,
        'publication_type': [{
            'type': 'Publications',
            'docs': new_docs
        }]
    }

    # 5. Sort papers inside 'Recent Publications' (Newest First)
    for pub_type in target_block['publication_type']:
        if 'docs' in pub_type:
            pub_type['docs'].sort(key=extract_year, reverse=True)

    # 6. Prepend 'Recent Publications' as the VERY FIRST section
    cleaned_data.insert(0, target_block)

    # 7. Write back clean YAML structure
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(cleaned_data, f, sort_keys=False, allow_unicode=True)

    print(f"Successfully cleaned, sorted, and updated {OUTPUT_FILE}!")

if __name__ == '__main__':
    process_and_deduplicate()
