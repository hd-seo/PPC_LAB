from pybtex.database import parse_file

def format_person(person):
    return f"{person.last_names[0]}, {person.first_names[0]}"

def generate_md():
    bib_data = parse_file('references.bib')
    
    # Sort by year descending
    entries = sorted(bib_data.entries.items(), key=lambda x: x[1].fields.get('year', '0000'), reverse=True)
    
    md_content = "# Publications\n\n"
    
    current_year = None
    
    for key, entry in entries:
        year = entry.fields.get('year', 'Unknown')
        if year != current_year:
            md_content += f"## {year}\n\n"
            current_year = year
            
        authors = entry.persons.get('author', [])
        author_str = ", ".join([f"{p.last_names[0]} {p.first_names[0]}" for p in authors])
        
        title = entry.fields.get('title', 'No Title').replace('{', '').replace('}', '')
        journal = entry.fields.get('journal', '')
        volume = entry.fields.get('volume', '')
        number = entry.fields.get('number', '')
        pages = entry.fields.get('pages', '')
        
        citation = f"**{title}**<br>"
        citation += f"*{author_str}*<br>"
        citation += f"{journal}. {year}"
        if volume:
            citation += f";{volume}"
        if number:
            citation += f"({number})"
        if pages:
            citation += f":{pages}"
        citation += "."
        
        md_content += f"- {citation}\n\n"
        
    with open('docs/publications.md', 'w') as f:
        f.write(md_content)
        
if __name__ == "__main__":
    generate_md()
