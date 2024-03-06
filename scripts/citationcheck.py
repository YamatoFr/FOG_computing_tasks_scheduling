import re

BIB = 'report/biblio.bib'

# Read the content of the files in the report folder

tex_file = 'report/' + str(input('Enter the name of the .tex file: ')) + '.tex'

with open(tex_file, 'r') as file:
    file_content = file.read()
with open(BIB, 'r') as file:
    biblio = file.read()

def checker(file_content, biblio):
    """
    This function checks the citations in the .bib file was cited in the .tex file and if the citation was checked
    back in the .bib file.
    Checked files have a '% X' at the end of the entry
    
    Args:
        file_content (_type_): content of the .tex file
        biblio (_type_): content of the .bib file
    """

    match_table = {}

    # Extract all keys from biblio.bib
    bib_keys = re.findall(r'@[^{]+\{([^,]+),', biblio)
    
    citation_keys = re.findall(r'\\cite(?:p)?\{([^}]+)\}', file_content)
    
    # For each bib key, check if it was cited in etatdelart.tex
    for key in bib_keys:
        match_table[key] = [key in citation_keys, False]
            
    # for each citation key, check if it was checked in biblio.bib
    for key in citation_keys:
        match_table[key][1] = key in bib_keys
        
    return match_table

def print_table(table):
    """
    Print the table in a formatted way:
    | Citation key | Cited | Checked |
    |--------------|-------|---------|
    |     key1     |  Y/N  |   Y/N   |
    |     key2     |  Y/N  |   Y/N   |
    |--------------|-------|---------|
    
    All columns are aligned to the center and have the same width, based on the longest string in the key column.

    Args:
        table (_type_): dictionary with the citation keys as keys and a list with two booleans as values
    """
    
    # Find the kay with the longest length
    max_key_length = max([len(key) for key in table.keys()])
    
    # Print the table
    print(f"| {'Citation key':^{max_key_length}} | {'Cited':^5} | {'Checked':^7} |")
    print(f"|{'-' * (max_key_length + 2)}|{'-' * 7}|{'-' * 9}|")
    for key, value in table.items():
        print(f"| {key:^{max_key_length}} | {'Y' if value[0] else 'N':^5} | {'Y' if value[1] else 'N':^7} |")
    print(f"|{'-' * (max_key_length + 2)}|{'-' * 7}|{'-' * 9}|")
    
print_table(checker(file_content, biblio))