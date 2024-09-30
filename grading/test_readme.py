import re
from grading import KEY

def get_h2_sections(readme_content): 
    h2_sections = re.findall(r'(## .+)\n([^#]*)', readme_content)
    return [(heading.strip(), content.strip()) for heading, content in h2_sections]

def test_readme_h2_content():  
    with open('README.md', 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    h2_sections = get_h2_sections(readme_content)
    
    for heading, content in h2_sections:
        assert content != "...", f'The section "{heading}" contains only "..."'

        