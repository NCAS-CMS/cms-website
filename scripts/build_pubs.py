import os
import re
import yaml
import bibtexparser

def load_people(people_path):
    """Load people from YAML and extract name details."""
    if not os.path.exists(people_path):
        return []
    with open(people_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or []
    
    people = []
    for person in data:
        if isinstance(person, dict) and person.get('lastname'):
            firstname = person.get('firstname', '').strip()
            lastname = person.get('lastname', '').strip()
            fn_tokens = [t for t in firstname.split() if t]
            
            people.append({
                'firstname': firstname,
                'fn_tokens': fn_tokens,
                'lastname': lastname
            })
    return people

def normalize_single_author(author_str):
    """
    Standardizes 'LastName, FirstName Middle' to 'FirstName Middle LastName'.
    Leaves 'FirstName Middle LastName' untouched.
    """
    author_str = author_str.strip()
    if ',' in author_str:
        parts = author_str.split(',', 1)
        last_name = parts[0].strip()
        first_names = parts[1].strip()
        return f"{first_names} {last_name}".strip()
    return author_str

def underline_single_author(author_name, people_list):
    """
    Checks if an author matches a CMS team member.
    If matched, wraps ONLY their surname in <u>...</u>.
    """
    for person in people_list:
        lastname = person['lastname']
        fn_tokens = person['fn_tokens']

        if not lastname or not fn_tokens:
            continue

        surname_regex = re.compile(rf'\b{re.escape(lastname)}\b', re.IGNORECASE)
        if not surname_regex.search(author_name):
            continue

        token_patterns = []
        for t in fn_tokens:
            token_patterns.append(re.escape(t))
            token_patterns.append(f"{re.escape(t[0])}\\.?")
        
        given_pattern = f"(?:{'|'.join(token_patterns)})"

        if re.search(rf'\b{given_pattern}\b', author_name, re.IGNORECASE):
            return surname_regex.sub(lambda m: f"<u>{m.group(0)}</u>", author_name)

    return author_name

def format_authors(authors_raw, people_list):
    """Splits raw BibTeX string, normalizes name order, and underlines team surnames."""
    if not authors_raw:
        return ""

    raw_authors = [a.strip() for a in re.split(r'\s+and\s+', authors_raw, flags=re.IGNORECASE) if a.strip()]
    
    formatted_authors = []
    for author in raw_authors:
        normalized = normalize_single_author(author)
        processed = underline_single_author(normalized, people_list)
        formatted_authors.append(processed)

    return ", ".join(formatted_authors)

def build_yaml_from_bib(bib_path, output_yaml, people_path="_data/people.yml"):
    if not os.path.exists(bib_path):
        print(f"BibTeX file '{bib_path}' not found.")
        return

    people = load_people(people_path)

    with open(bib_path, 'r', encoding='utf-8') as f:
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        bib_database = bibtexparser.load(f, parser=parser)

    by_year = {}

    for entry in bib_database.entries:
        raw_authors = entry.get('authors') or entry.get('author', '')
        highlighted_authors = format_authors(raw_authors, people)
        
        year_str = str(entry.get('year', '')).strip() or 'Recent Publications'
        journal_loc = (entry.get('journal', '') or entry.get('location', '')).strip()

        # Append year in parentheses to the location string if year is present
        if journal_loc and year_str and year_str != 'Recent Publications':
            full_location = f"{journal_loc}, ({year_str})"
        elif year_str and year_str != 'Recent Publications':
            full_location = f"({year_str})"
        else:
            full_location = journal_loc

        doc_item = {
            'title': entry.get('title', '').strip('{}'),
            'authors': highlighted_authors,
            'location': full_location,
            'url': entry.get('url', '')
        }

        if year_str not in by_year:
            by_year[year_str] = []
        by_year[year_str].append(doc_item)

    structured_data = []
    sorted_years = sorted(by_year.keys(), reverse=True)

    for y in sorted_years:
        structured_data.append({
            'year': y,
            'docs': by_year[y]
        })

    os.makedirs(os.path.dirname(output_yaml), exist_ok=True)
    with open(output_yaml, 'w', encoding='utf-8') as f:
        yaml.dump(structured_data, f, allow_unicode=True, sort_keys=False)

    print(f"Successfully updated '{output_yaml}'.")

if __name__ == '__main__':
    build_yaml_from_bib("_bibliography/references.bib", "_data/publications.yml")
