import argparse
import os
import re
import sys
import yaml
import requests
import bibtexparser

ORCID_BASE_URL = "https://pub.orcid.org/v3.0"

def clean_title(title):
    """Normalize title string for robust matching."""
    return re.sub(r'[\{\}\s\W]+', '', title).lower()

def get_orcid_work_groups(orcid_id):
    """Fetch all work groups from ORCID."""
    url = f"{ORCID_BASE_URL}/{orcid_id}/works"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"   [!] Error fetching works for ORCID {orcid_id} (Status: {response.status_code})")
        return []

    data = response.json()
    return data.get("group", [])

def extract_year(work_summary):
    """Extract numeric publication year from ORCID work summary."""
    pub_date = work_summary.get("publication-date")
    if pub_date and pub_date.get("year"):
        try:
            return int(pub_date["year"]["value"])
        except (ValueError, TypeError):
            pass
    return None

def extract_authors(detail):
    """Extract and format contributor names into a BibTeX author string."""
    if not isinstance(detail, dict):
        return ""

    contrib_container = detail.get("contributors") or {}
    contributors = contrib_container.get("contributor") or []

    author_names = []
    for c in contributors:
        if not isinstance(c, dict):
            continue

        credit_name_obj = c.get("credit-name") or {}
        name = credit_name_obj.get("value", "").strip()

        if not name:
            given = (c.get("given-names") or {}).get("value", "").strip() if isinstance(c.get("given-names"), dict) else ""
            family = (c.get("family-name") or {}).get("value", "").strip() if isinstance(c.get("family-name"), dict) else ""
            name = f"{given} {family}".strip()

        if name:
            author_names.append(name)

    return " and ".join(author_names)

def fetch_bulk_work_details(orcid_id, put_codes):
    """Fetch full details for multiple put_codes in a single HTTP request."""
    if not put_codes:
        return {}

    # ORCID bulk API accepts comma-separated put-codes (up to 100)
    codes_str = ",".join(str(code) for code in put_codes[:100])
    url = f"{ORCID_BASE_URL}/{orcid_id}/works/{codes_str}"
    headers = {"Accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {}

    data = response.json()
    details_map = {}
    
    # Process bulk response list
    bulk_list = data.get("bulk", [])
    for item in bulk_list:
        work = item.get("work")
        if work and "put-code" in work:
            details_map[work["put-code"]] = work

    return details_map

def extract_doi_from_detail(detail):
    """Extract DOI from full work detail, checking external-ids and citation text."""
    if not isinstance(detail, dict):
        return ""

    # 1. Inspect external-ids array
    ext_ids_obj = detail.get("external-ids") or {}
    external_ids = ext_ids_obj.get("external-id") or []
    for ext_id in external_ids:
        if isinstance(ext_id, dict):
            ext_type = str(ext_id.get("external-id-type", "")).lower().strip()
            ext_val = str(ext_id.get("external-id-value", "")).strip()
            ext_url = str(ext_id.get("external-id-url", {}).get("value", "") if isinstance(ext_id.get("external-id-url"), dict) else "").strip()
            
            if ext_type in ("doi", "doi-resolver") or ext_val.startswith("10."):
                clean_doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', ext_val, flags=re.IGNORECASE)
                return f"https://doi.org/{clean_doi}"
            elif "doi.org/10." in ext_url.lower():
                clean_doi = re.search(r'10\.\d{4,9}/[-._;()/:A-Za-z0-9]+', ext_url)
                if clean_doi:
                    return f"https://doi.org/{clean_doi.group(0)}"

    # 2. Inspect raw BibTeX if present
    citation = detail.get("citation") or {}
    citation_val = citation.get("citation-value", "")
    if citation_val:
        doi_match = re.search(r'doi\s*=\s*[\{"]?(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)[\}"]?', citation_val, re.IGNORECASE)
        if doi_match:
            return f"https://doi.org/{doi_match.group(1)}"

    return ""

def extract_orcid_url(detail):
    """Extract URL fallback if no DOI is present."""
    if not isinstance(detail, dict):
        return ""

    doi = extract_doi_from_detail(detail)
    if doi:
        return doi

    # Check direct URL field
    url_obj = detail.get("url") or {}
    url_val = url_obj.get("value", "").strip() if isinstance(url_obj, dict) else ""
    if url_val:
        return url_val

    # Check external IDs
    ext_ids_obj = detail.get("external-ids") or {}
    external_ids = ext_ids_obj.get("external-id") or []
    for ext_id in external_ids:
        if isinstance(ext_id, dict):
            ext_val = str(ext_id.get("external-id-value", "")).strip()
            if ext_val.startswith("http://") or ext_val.startswith("https://"):
                return ext_val

    return ""

def generate_fallback_bibtex(detail, put_code, year, forced_doi=None):
    """Generate BibTeX entry if raw BibTeX text is missing."""
    if not isinstance(detail, dict):
        detail = {}

    title_obj = (detail.get("title") or {}).get("title") or {}
    title = title_obj.get("value", "Untitled")

    authors = extract_authors(detail)
    url = forced_doi if forced_doi else extract_orcid_url(detail)

    journal_obj = detail.get("journal-title") or {}
    journal = journal_obj.get("value", "")

    if not journal:
        pub_obj = detail.get("publisher") or {}
        publisher_val = pub_obj.get("value", "") if isinstance(pub_obj, dict) else ""
        work_type = str(detail.get("type", "")).upper()

        if "EGUSPHERE" in url.upper() or "EGUSPHERE" in publisher_val.upper():
            journal = "EGUsphere (Preprint)"
        elif "ARXIV" in url.upper() or "ARXIV" in publisher_val.upper():
            journal = "arXiv (Preprint)"
        elif "BIORXIV" in url.upper() or "BIORXIV" in publisher_val.upper():
            journal = "bioRxiv (Preprint)"
        elif publisher_val:
            journal = publisher_val
        elif work_type == "PREPRINT":
            journal = "Preprint"

    clean_key_title = re.sub(r'\W+', '', title)[:15]
    cite_key = f"orcid_{year or '0000'}_{clean_key_title}_{put_code}"

    entry = {
        'ENTRYTYPE': 'article',
        'ID': cite_key,
        'title': title,
        'author': authors,
        'authors': authors,
        'year': str(year) if year else '',
        'journal': journal,
        'location': journal,
        'url': url
    }
    return entry

def process_orcid_group(orcid_id, group):
    """
    Fetch all items in a group via Bulk API, locate DOIs, and return best item.
    """
    summaries = group.get("work-summary", [])
    if not summaries:
        return None, None, None, None

    year = extract_year(summaries[0])
    put_codes = [s.get("put-code") for s in summaries if s.get("put-code")]

    # Bulk fetch full details for all put_codes in 1 API call
    details_map = fetch_bulk_work_details(orcid_id, put_codes)

    group_doi = None
    best_detail = None
    best_put_code = None

    # 1. Scan all details for any DOI
    for put_code, detail in details_map.items():
        doi = extract_doi_from_detail(detail)
        if doi:
            group_doi = doi
            if not best_detail:
                best_detail = detail
                best_put_code = put_code

    # 2. If no DOI was found, select primary or first available record
    if not best_detail:
        for summary in summaries:
            p_code = summary.get("put-code")
            if p_code in details_map:
                best_detail = details_map[p_code]
                best_put_code = p_code
                if str(summary.get("display-index")) == "0":
                    break

    return best_detail, best_put_code, year, group_doi

def process_orcid(orcid_id, existing_db, title_to_index, start_year, end_year):
    """Fetch and merge publications for a single ORCID ID into existing_db."""
    groups = get_orcid_work_groups(orcid_id)
    print(f"   Found {len(groups)} unique work groups in profile.")

    added_count = 0

    for group in groups:
        detail, put_code, year, group_doi = process_orcid_group(orcid_id, group)
        if not detail:
            continue

        if start_year and (year is None or year < start_year):
            continue
        if end_year and (year is None or year > end_year):
            continue

        title_raw = (detail.get("title") or {}).get("title", {}).get("value", "Untitled")
        title_norm = clean_title(title_raw)

        if title_norm in title_to_index:
            continue

        print(f"   + Fetching ({year or 'N/A'}): {title_raw[:50]}...")

        citation = detail.get("citation")
        parsed_entry = None

        if citation and citation.get("citation-type") == "BIBTEX":
            bib_str = citation.get("citation-value")
            try:
                parsed = bibtexparser.loads(bib_str)
                if parsed.entries:
                    parsed_entry = parsed.entries[0]
            except Exception:
                pass

        if not parsed_entry:
            parsed_entry = generate_fallback_bibtex(detail, put_code, year, forced_doi=group_doi)
        else:
            # Overwrite URL field with DOI if a DOI was found anywhere in the group
            if group_doi:
                parsed_entry["url"] = group_doi
            elif not parsed_entry.get("url"):
                parsed_entry["url"] = extract_orcid_url(detail)

        if 'authors' not in parsed_entry and 'author' in parsed_entry:
            parsed_entry['authors'] = parsed_entry['author']

        existing_db.entries.append(parsed_entry)
        title_to_index[title_norm] = len(existing_db.entries) - 1
        added_count += 1

    return added_count

def load_orcids_from_people_file(filepath):
    """Extract list of dicts with name & orcid from people.yml."""
    if not os.path.exists(filepath):
        print(f"Error: People file '{filepath}' not found.")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        people = yaml.safe_load(f) or []

    records = []
    for person in people:
        if isinstance(person, dict) and person.get('orcid'):
            name = f"{person.get('firstname', '')} {person.get('lastname', '')}".strip()
            orcid_str = str(person['orcid']).strip()
            records.append({'name': name, 'orcid': orcid_str})
    return records

def update_bibtex_file(orcid_list, start_year, end_year, output_path, clean_file=False):
    if clean_file and os.path.exists(output_path):
        os.remove(output_path)
        print(f"Cleaned existing output file '{output_path}'.")

    existing_db = bibtexparser.bibdatabase.BibDatabase()

    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            parser = bibtexparser.bparser.BibTexParser(common_strings=True)
            existing_db = bibtexparser.load(f, parser=parser)

    title_to_index = {clean_title(e.get('title', '')): i for i, e in enumerate(existing_db.entries)}

    total_added = 0
    for idx, item in enumerate(orcid_list, 1):
        name = item.get('name', 'Unknown')
        orcid_id = item['orcid']
        print(f"\n[{idx}/{len(orcid_list)}] Processing {name} ({orcid_id})...")
        added = process_orcid(orcid_id, existing_db, title_to_index, start_year, end_year)
        total_added += added

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        bibtexparser.dump(existing_db, f)

    print(f"\nFinished! Added {total_added} total new entries to '{output_path}'. Total database count: {len(existing_db.entries)}")

def main():
    parser = argparse.ArgumentParser(description="Fetch citations from ORCID profiles and build/update a .bib file.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("orcid", nargs="?", help="Single ORCID iD (e.g. 0000-0002-1825-0097)")
    group.add_argument("--people-file", help="Path to YAML people file (e.g. _data/people.yml)")

    parser.add_argument("--start-year", type=int, help="Start year (inclusive)")
    parser.add_argument("--end-year", type=int, help="End year (inclusive)")
    parser.add_argument("--clean", action="store_true", help="Delete output .bib file first and start fresh")
    parser.add_argument("--output", "-o", default="_bibliography/references.bib", help="Path to output .bib file")

    args = parser.parse_args()

    if args.people_file:
        orcid_list = load_orcids_from_people_file(args.people_file)
        print(f"Loaded {len(orcid_list)} ORCID profiles from '{args.people_file}'.")
    else:
        orcid_list = [{'name': 'Single Target', 'orcid': args.orcid}]

    update_bibtex_file(
        orcid_list,
        args.start_year,
        args.end_year,
        args.output,
        clean_file=args.clean
    )

if __name__ == '__main__':
    main()
