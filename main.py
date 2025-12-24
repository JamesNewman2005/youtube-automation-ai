import os
from src.generator import Script_Generator
from src.niche_discovery import Niche_Discovery
from helpers.write_to_file import write_script_to_file

def main():
    print(f'----- Youtube Automation AI -----')
    print('[1] - Start')
    print('[2] - Exit')
    selection = input('Selection > ')

    if selection == '1':
        niche_discovery = Niche_Discovery('')
        print('')
        print('- Finding trending niches...')
        niches = niche_discovery.get_niches()
        print('')

        if len(niches) != 0:
            print('- Generating script(s)')
            
            for niche in niches:
                script_generator = Script_Generator('', niche)
                script = script_generator.generate_script()

                if write_script_to_file(niche, script):
                   print(f'- ✅ Successfuly generated script for - {niche}') 
                
    elif selection == '2':
        exit(0)

if __name__ == "__main__":
    main()