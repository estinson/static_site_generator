import os
import shutil
from markdown_to_html import markdown_to_html

def main() -> None:
    if (initialize_public_assets()):
        for file in list_files_recursive('content'):
            if file[-3:] == ".md":
                print(f'Generating html file {generate_html_file(
                    file,
                    'template.html',
                    file[:-3].replace('content', 'public') + '.html'
                )}')
    else:
        print('Public asset creation failed, closing')

def generate_html_file(md_path:str, template_path:str, dest_path:str) -> str:
    if(open(md_path).read(2) == '# '):
        md_parsed = markdown_to_html(open(md_path).read())
        title = md_parsed.children[0].children[0].value

        html_parsed = ''
        try:
            with open(template_path, 'r') as template:
                html_parsed = template.read()
        except Exception as e:
            return f'ERROR: Template reading failed -> {e}'

        html_parsed = html_parsed.replace('{{ Title }}', title)
        html_parsed = html_parsed.replace('{{ Content }}', md_parsed.to_html())

        try:
            public_file = md_path.replace('static', 'public')
            dir_path = os.path.dirname(dest_path)
            os.makedirs(dir_path, exist_ok=True)

            with open(dest_path, 'w') as dest:
                dest.write(html_parsed)
        except Exception as e:
            return f'ERROR: Writing to destination failed -> {e}'

        return f'SUCCESS: {title} created at {dest_path}'
    else:
        return f'ERROR: {file_path} does not have a heading as the first line'

def initialize_public_assets() -> bool:
    rv = False
    shutil.rmtree('public')
    os.mkdir('public')
    static_files = list_files_recursive('static')
    for static_file in static_files:
        try:
            public_file = static_file.replace('static', 'public')
            if(os.path.exists(public_file)): print(f'{public_file} path not found'); continue
            dir_path = os.path.dirname(public_file)
            os.makedirs(dir_path, exist_ok=True)
            shutil.copy(static_file, public_file)

            print(f'Copied asset {static_file} -> {public_file}')
        except Exception as e:
            print(e)
            return rv
    return True

def list_files_recursive(path='.', ) -> list[str]:
    rv:list[str] = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if entry[0] == '.': continue
        if os.path.isdir(full_path):
            rv += list_files_recursive(full_path)
        else:
            rv.append(full_path)
    return rv

if __name__ == "__main__":
    main()
