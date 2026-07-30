import os
import bibtexparser
import yaml

BIB_FILE = '_bibliography/references.bib'
OUTPUT_FILE = '_data/publications.yml'

def clean_title(title):
    """Normalize title for strict deduplication matching."""
    return title.replace('{', '').replace('}', '').strip().lower()

def format_journal_citation(entry):
    """Formats a BibTeX entry into a standard academic journal citation dict."""
    title = entry.get('title', '').replace('{', '').replace('}', '').strip()

    raw_authors = entry.get('author', '').replace('\n', ' ')
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
        'url': url
    }

def process_and_deduplicate():
    existing_data = []
    seen_titles = set()

    # 1. Load and deduplicate existing YAML file
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = yaml.safe_load(f) or []
        except Exception as e:
            print(f"Error reading {OUTPUT_FILE}: {e}")
            return

    cleaned_data = []

    for year_block in existing_data:
        if not isinstance(year_block, dict):
            continue

        new_pub_types = []
        for pub_type in year_block.get('publication_type', []):
            new_docs = []
            for doc in pub_type.get('docs', []):
                t = clean_title(doc.get('title', ''))
                if t and t not in seen_titles:
                    seen_titles.add(t)
                    new_docs.append(doc)

            if new_docs:
                pub_type['docs'] = new_docs
                new_pub_types.append(pub_type)

        if new_pub_types:
            year_block['publication_type'] = new_pub_types
            cleaned_data.append(year_block)

    # 2. Parse BibTeX and collect new entries
    if not os.path.exists(BIB_FILE):
        print(f"Error: Could not find {BIB_FILE}")
        return

    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_data = bibtexparser.load(f)

    new_wip_docs = []
    for entry in bib_data.entries:
        formatted = format_journal_citation(entry)
        t = clean_title(formatted['title'])
        if t and t not in seen_titles:
            seen_titles.add(t)
            new_wip_docs.append(formatted)

    # 3. Append new WIP entries if present
    if new_wip_docs:
        # Check if 'Work in Progress' block already exists
        wip_block = None
        for block in cleaned_data:
            if block.get('year') == 'Work in Progress':
                wip_block = block
                break

        if wip_block:
            # Append docs to existing Work in Progress block
            for pub_type in wip_block.get('publication_type', []):
                if pub_type.get('type') == 'Publications':
                    pub_type['docs'].extend(new_wip_docs)
                    break
        else:
            # Create a new Work in Progress block
            cleaned_data.append({
                'year': 'Work in Progress',
                'publication_type': [{
                    'type': 'Publications',
                    'docs': new_wip_docs
                }]
            })
        print(f"Added {len(new_wip_docs)} new citation(s) under 'Work in Progress'.")
    else:
        print("No new BibTeX citations to add.")

    # 4. Save clean structure back to YAML
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(cleaned_data, f, sort_keys=False, allow_unicode=True)

    print(f"Successfully cleaned and updated {OUTPUT_FILE}!")

if __name__ == '__main__':
    process_and_deduplicate()
