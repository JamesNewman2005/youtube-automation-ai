import os

def write_script_to_file(niche: str, script: str) -> bool:
    os.makedirs('output/scripts', exist_ok=True)
    
    filename = niche
    if ' ' in filename:
        filename = filename.replace(' ', '-')
    elif '-' in filename:
        filename = filename.replace('-', '_')
    
    filepath = f'output/scripts/{filename}.txt'
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(script)
        return True
