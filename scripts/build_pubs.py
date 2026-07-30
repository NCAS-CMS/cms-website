import os
import bibtexparser
import yaml

BIB_FILE = '_bibliography/references.bib'
OUTPUT_FILE = '_data/publications.yml'

def get_existing_titles(output_file):
    """Parses existing publication titles from the output YAML file to avoid duplicates."""
    if not os.path.exists(output_file):
        return set()

    titles = set()
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or []
            
        for year_block in data:
            if not isinstance(year_block, dict):
                continue
            for pub_type in year_block.get('publication_type', []):
                for doc in pub_type.get('docs', []):
                    if 'title' in doc:
                        clean_title = doc['title'].strip().lower()
                        titles.add(clean_title)
    except Exception as e:
        print(f"Warning: Could not parse existing {output_file} ({e}). Proceeding carefully.")
    
    return titles

def format_journal_citation(entry):
    """Formats a BibTeX entry into a standard academic journal citation string without Markdown formatting."""
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

def main():
    if not os.path.exists(BIB_FILE):
        print(f"Error: Could not find {BIB_FILE}")
        return

    # 1. Fetch existing titles to prevent duplication
    existing_titles = get_existing_titles(OUTPUT_FILE)

    # 2. Parse BibTeX
    with open(BIB_FILE, 'r', encoding='utf-8') as f:
        bib_data = bibtexparser.load(f)

    # 3. Filter out entries that already exist in publications.yml
    new_docs = []
    skipped_count = 0

    for entry in bib_data.entries:
        formatted_entry = format_journal_citation(entry)
        clean_title = formatted_entry['title'].strip().lower()

        if clean_title in existing_titles:
            skipped_count += 1
        else:
            new_docs.append(formatted_entry)
            existing_titles.add(clean_title)

    if not new_docs:
        print(f"No new entries to append. ({skipped_count} entries already exist in {OUTPUT_FILE}).")
        return

    # 4. Structure new entries under 'Work in Progress'
    new_yaml_block = [{
        'year': 'Work in Progress',
        'publication_type': [{
            'type': 'Publications',
            'docs': new_docs
        }]
    }]

    # 5. Append with a visual YAML comment marker
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write("\n# --- WORK IN PROGRESS (AUTO-GENERATED FROM BIBTEX) ---\n")
        f.write(yaml.dump(new_yaml_block, sort_keys=False, allow_unicode=True))

    print(f"Successfully appended {len(new_docs)} new citation(s) to {OUTPUT_FILE} (Skipped {skipped_count} existing).")

if __name__ == '__main__':
    main()
