import os
import shutil

def main() -> None:
    shutil.rmtree('public')
    os.mkdir('public')
    static_files = list_files_recursive('static')
    for static_file in static_files:
        public_file = static_file.replace('static', 'public')
        if(os.path.exists(public_file)): continue
        dir_path = os.path.dirname(public_file)
        os.makedirs(dir_path, exist_ok=True)

        with open(public_file, mode='w') as file:
            file.write(static_file)
        print(f'Copied {static_file} -> {public_file}')

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
