

from datetime import datetime
import hashlib
import shutil
import os
import re

class Tig:

    def __init__(self):
        self.file = ""
        self.file_name = ""
        self.base_dir = r"C:\Users\lucas\Desktop\Lucas\Programação\Estudo\Python\Git"

    def init(self, file):
        """
            Realilza toda a configuração inicial do versionamento, criando as pastas do arquivo, junto com o
            diretório save e os arquivos hist.txt e current.txt. Deve ser executado apenas quando uma arquivo
            não versionado começará a ser versionado.
        """
        self._configure_file(file)
        if self._already_init():
            print("The file is being versioned already!")
            return

        path_version_directory = f"{self.base_dir}\\.{self.file_name}"
        self._generate_version_directory(path_version_directory)
        self._generate_save_directory(path_version_directory)
        self._create_hist_file(path_version_directory)
        self.save(file, "Initializing versioning")

    def save(self, file, *message):
        """
            Executa um save do formato atual do arquivo. Através deste comando é realizado a cópia do arquivo
            no diretório save, assim como é inserido um novo log no arquivo hist.txt e o current.txt é
            atualizado para o hash do novo save recém realizado.
        """
        self._configure_file(file)
        message = " ".join(message)
        file_content_hash = self._file_content_hash()
        modified_file = self._file_has_changes()
        if modified_file:
            self._save_file(file_content_hash)
            self._append_hist_log(file_content_hash, message)
            self._update_current(file_content_hash)
        else:
            print(f"This state was already saved on: {file_content_hash}\n")

    def hist(self, file):
        """
            Retorna todos os saves realizado no versionamento do arquivo informado. Neste caso casa save
            é exibido em ordem de realização, e não faz distinção entre a posição atual, exibindo todas as
            versões de todas as ramificações, para frente e para trás.
        """
        self._configure_file(file)
        hist_list = reversed(self._list_all_hist())
        for hist_item in hist_list:
            if hist_item[2] == self._get_current():
                print("CURRENT")
            self._hist_message(hist_item)

    def jump(self, file, version_hash):
        """
            Permite transicionar entre diferentes versões marcadas por cada save. É indiferente quanto
            aos ramos, podendo transicionar para frente, para trás ou mesmo entre diferentes ramos.
            É importante considerar que uma alteração em um arquivo do passado irá gerar um novo ramo,
            e por enquanto não existe sistema de união de ramos.
        """
        self._configure_file(file)
        modified_file = self._file_has_changes()
        if modified_file:
            command = input("This action will result in the loss of file changes. Do you want to proceed?\n(y\\n): ")
            if command.lower() != "y":
                return

        saved_file_path = f"{self.base_dir}\\.{self.file_name}\\save\\{version_hash}.txt"
        saved_file_content = "".join(self._get_saved_content_lines(saved_file_path))
        self._replace_file_content(file, saved_file_content)
        self._update_current(self._file_content_hash())

    def prev(self, file):
        """
            Retorna todos os saves que precedem a versão atual. desta forma é possível verificar cada etapa
            trilhada para chegar até este ponto, descansiderando outras ramificações e os saves que
            possam suceder o save atual.
        """
        self._configure_file(file)
        current = self._get_current()
        hist_list = self._list_all_hist()
        prev_list = self._list_prev_saves(current, hist_list)
        for prev_item in prev_list:
            self._hist_message(prev_item)

    def diff(self, file, first_hash="", second_hash=""):
        """
            Exibe as alterações entre dois estados diferentes, indicando as linhas removidas e as linhas inseridas.
            Pode funcionar comparando o current com o estado atual do arquivo, uma save qualquer com o estado
            atual do arquivo, ou mesmo dois saves distintos. A comparação entre dois saves não considera a ordem
            cronológica, mas apenas a ordem de declaração, onde o primeiro hash será considerado a primeira versão
            e o segundo hash será considerada uma versão seguinte. Assim, é possível saber qual seria o processo de
            reversão de um arquivo para o estado anterior.
        """
        self._configure_file(file)
        first_file, second_file = self._define_diff_files(first_hash, second_hash)
        first_file_content = self._get_saved_content_lines(first_file)
        second_file_content = self._get_saved_content_lines(second_file)

        removed_lines = [(i+1, line) for i, line in enumerate(first_file_content) if line not in second_file_content]
        inserted_lines = [(i+1, line) for i, line in enumerate(second_file_content) if line not in first_file_content]

        has_removed_lines = len(removed_lines) > 0
        has_inserted_lines = len(inserted_lines) > 0
        nothing_has_changed = len(removed_lines) == 0 and len(inserted_lines) == 0
        if has_removed_lines:
            print("REMOVED LINES")
            self._print_changes(removed_lines, operator="-")
        if has_inserted_lines:
            print("INSERTED LINES")
            self._print_changes(inserted_lines, operator="+")
        if nothing_has_changed:
            print("No changes were found.\n")
        print("")

    def _define_diff_files(self, first_hash, second_hash):
        first_file = ""
        second_file = ""
        if not first_hash and not second_hash:
            first_file = f"{self.base_dir}\\.{self.file_name}\\save\\{self._get_current()}.txt"
            second_file = self.file
        elif first_hash and not second_hash:
            first_file = f"{self.base_dir}\\.{self.file_name}\\save\\{first_hash}.txt"
            second_file = self.file
        elif first_hash and second_hash:
            first_file = f"{self.base_dir}\\.{self.file_name}\\save\\{first_hash}.txt"
            second_file = f"{self.base_dir}\\.{self.file_name}\\save\\{second_hash}.txt"
        return first_file, second_file

    def _save_file(self, file_content_hash):
        final_path_file = f"{self.base_dir}\\.{self.file_name}\\save\\{file_content_hash}.txt"
        shutil.copy(self.file, final_path_file)

    def _update_current(self, file_content_hash):
        current_file = f"{self.base_dir}\\.{self.file_name}\\current.txt"
        with open(current_file, 'w') as f:
            f.write(file_content_hash)

    def _append_hist_log(self, file_content_hash, message):
        num_saves = len(self._list_all_hist())
        if num_saves == 0:
            log = f"{datetime.now()}\t{'0' * 64}\t{file_content_hash}\t{message}\n"
        else:
            log = f"{datetime.now()}\t{self._get_current()}\t{file_content_hash}\t{message}\n"
        hist_file = f"{self.base_dir}\\.{self.file_name}\\hist.txt"
        with open(hist_file, 'a') as f:
            f.write(log)

    def _file_content_hash(self):
        file_content = "".join(self._get_saved_content_lines(self.file)).encode('utf-8')
        file_content_hash = hashlib.sha256(file_content).hexdigest()
        return file_content_hash

    def _get_current(self):
        current = f"{self.base_dir}\\.{self.file_name}\\current.txt"
        with open(current, 'r') as f:
            contents = f.readlines()
        return contents[0]

    def _configure_file(self, file):
        if os.path.exists(file):
            self.file = file
            self.file_name = file.split(".")[0]

    def _already_init(self):
        path = f"{self.base_dir}\\.{self.file_name}"
        if os.path.exists(path):
            return True
        return False

    def _file_has_changes(self):
        hash_hist = [version_hash for _, _, version_hash, _ in self._list_all_hist()]
        if self._file_content_hash() in hash_hist:
            return False
        return True

    def _list_all_hist(self):
        lines = []
        hist_file = f"{self.base_dir}\\.{self.file_name}\\hist.txt"
        with open(hist_file, 'r') as f:
            content = f.readlines()
            for line in content:
                lines.append(re.split(r"\t", line))
        return lines

    @staticmethod
    def _print_changes(lines, operator):
        for line in lines:
            spaces = ' ' * (5 - (len(str(line[0]))))
            print(f"{operator} {line[0]}{spaces}| {line[1].strip()}")

    @staticmethod
    def _list_prev_saves(current, hist_list):
        tree_save_hist = []
        while current != "0" * 64:
            current_save = list(filter(lambda save: save[2] == current, hist_list))[0]
            tree_save_hist.append(current_save)
            current = current_save[1]
        return tree_save_hist

    @staticmethod
    def _replace_file_content(file, content):
        with open(file, 'w') as f:
            f.write(content)

    @staticmethod
    def _get_saved_content_lines(path):
        with open(path, 'r') as f:
            contents = f.readlines()
        return contents

    @staticmethod
    def _hist_message(line):
        print(f"Data: {line[0]}\n"
              f"Hash: {line[2]}\n"
              f"Anterior: {line[1]}\n"
              f"Mensagem: {line[3]}")

    @staticmethod
    def _generate_version_directory(path):
        os.mkdir(path)

    @staticmethod
    def _generate_save_directory(path):
        path_save = f"{path}\\save"
        os.mkdir(path_save)

    @staticmethod
    def _create_hist_file(path):
        hist_file = f"{path}\\hist.txt"
        with open(hist_file, 'w') as f:
            f.write("")
