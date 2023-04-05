import os
import cmd
import readline
import datetime
import shutil
import time
from pathlib import Path
import atexit
import argparse


class MS_DOS(cmd.Cmd):
    """Интерпретатор MS-DOS"""

    def __init__(self):
        super().__init__()
        self.prompt = os.getcwd() + "> "
        self.intro = "Добро пожаловать в интерпретатор MS-DOS!\nВведите 'help' для получения справки по командам."
        self.doc_header = "Список доступных команд (для получения справки по конкретной команде введите 'help <команда>'):"
        self.undoc_header = "Список недокументированных команд:"
        self.misc_header = "Разное:"
        self.ruler = "-"
        self.use_rawinput = False


    def do_dir(self, arg):
        """
        dir [-a] [-l] [-t] [-r] [<directory>]
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--all", action="store_true",
                            help="show hidden files")
        parser.add_argument("-l", "--long", action="store_true",
                            help="use a long listing format")
        parser.add_argument("-t", "--time", action="store_true",
                            help="sort by modification time")
        parser.add_argument("-r", "--reverse", action="store_true",
                            help="reverse order while sorting")
        parser.add_argument("directory", nargs="?", default=os.getcwd(),
                            help="the directory to list")
        args = parser.parse_args(arg.split())

        if not os.path.isdir(args.directory):
            print("No such directory")
            return

        files = os.listdir(args.directory)

        if not args.all:
            files = [f for f in files if not f.startswith('.')]

        if args.time:
            files.sort(key=lambda f: os.path.getmtime(os.path.join(args.directory, f)),
                       reverse=args.reverse)
        else:
            files.sort(reverse=args.reverse)

        if args.long:
            for f in files:
                path = os.path.join(args.directory, f)
                stat = os.stat(path)
                size = stat.st_size
                modified = datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                print(f"{stat.st_mode:0o}  {stat.st_nlink:2} {stat.st_uid:5} {stat.st_gid:5} {size:6} {modified} {f}")
        else:
            print("\t".join(files))

    def do_ls(self, arg):
        """
        ls [-a] [-l] [-t] [-r] [<directory>]
        """
        self.do_dir(arg)

    def do_cd(self, args):
        """Переходит в указанную директорию"""
        try:
            os.chdir(args)
        except FileNotFoundError:
            print("Указанной директории не существует")
        except PermissionError:
            print("У вас нет прав на доступ к этой директории")
        self.prompt = f'C:{os.path.abspath(".")}> '

    def do_type(self, args):
        """Выводит содержимое указанного файла"""
        try:
            with open(args, 'r') as f:
                contents = f.read()
                print(contents)
        except FileNotFoundError:
            print("Указанный файл не существует")
        except PermissionError:
            print("У вас нет прав на чтение этого файла")

    def do_mkdir(self, args):
        """Создает директорию"""
        try:
            os.mkdir(args)
        except FileExistsError:
            print("Указанная директория уже существует")
        except PermissionError:
            print("У вас нет прав на создание этой директории")

    def do_rmdir(self, args):
        """Удаляет директорию"""
        try:
            os.rmdir(args)
        except FileNotFoundError:
            print("Указанная директория не существует")
        except OSError:
            print("Невозможно удалить эту директорию")

    def do_echo(self, args):
        """Выводит текст на экран"""
        print(args)

    def do_help(self, args):
        """Выводит список доступных команд"""
        print("run - Запускает Python скрипт")
        print("dir - Выводит содержимое текущей директории")
        print("cd - Переходит в указанную директорию")
        print("type - Выводит содержимое указанного файла")
        print("mkdir - Создает директорию")
        print("rmdir - Удаляет директорию")
        print("echo - Выводит текст на экран")
        print("help - Выводит список доступных команд")
        print("cls - Очищает экран")
        print("copy - Копирует файл или директорию")
        print("date - Выводит текущую дату")
        print("del - Удаляет указанный файл")
        print("fc - Сравнивает два файла")
        print("md - Создает директорию")
        print("move - Перемещает файл или директорию")
        print("pause - Приостанавливает выполнение программы")
        print("rd - Удаляет директорию")
        print("ren - Переименовывает файл или директорию")
        print("set - Устанавливает переменную среды")
        print("sort - Сортирует содержимое файла")
        print("tree - Отображает структуру директорий")
        print("ver - Выводит версию интерпретатора")

    def do_cls(self, args):
        """Очищает экран"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def do_date(self, args):
        """Выводит текущую дату"""
        print(datetime.datetime.now().strftime("%Y-%m-%d"))

    def do_del(self, args):
        """Удаляет указанный файл"""
        try:
            os.remove(args)
        except FileNotFoundError:
            print("Указанный файл не существует")
        except PermissionError:
            print("У вас нет прав на удаление файла")

    def do_fc(self, args):
        """Сравнивает два файла и выводит различия"""
        if args:
            try:
                file1, file2 = args.split()
                if os.path.isfile(file1) and os.path.isfile(file2):
                    with open(file1, 'r') as f1, open(file2, 'r') as f2:
                        diff = list(difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2))
                        if diff:
                            for line in diff:
                                print(line, end="")
                        else:
                            print("Файлы идентичны")
                else:
                    print("Один или оба файла не существуют")
            except ValueError:
                print("Введите два файла для сравнения (например, 'fc file1.txt file2.txt')")
        else:
            print("Введите аргументы для команды fc (например, 'fc file1.txt file2.txt')")


    def do_mkdir(self, args):
        """Создает директорию"""
        if args:
            try:
                os.mkdir(args)
            except FileExistsError:
                print("Указанная директория уже существует")
            except PermissionError:
                print("У вас нет прав на создание этой директории")
        else:
            print("Введите имя директории для создания (например, 'mkdir new_directory')")

    def do_md(self, args):
        """Алиас для команды mkdir"""
        self.do_mkdir(args)

    def do_move(self, args):
        """Перемещает файл или директорию"""
        if args:
            try:
                src, dest = args.split()
                if os.path.exists(src):
                    shutil.move(src, dest)
                    print(f"'{src}' перемещено в '{dest}'")
                else:
                    print(f"Исходный файл или директория '{src}' не существует")
            except ValueError:
                print("Введите исходный и целевой пути (например, 'move src.txt dest.txt')")
        else:
            print("Введите аргументы для команды move (например, 'move src.txt dest.txt')")

    def do_pause(self, args):
        """Приостанавливает выполнение программы"""
        input("Нажмите Enter для продолжения...")

    def do_ren(self, args):
        """Переименовывает файл или директорию"""
        src, dest = args.split()
        try:
            os.rename(src, dest)
        except FileNotFoundError:
            print("Указанный файл или директория не существует")
        except PermissionError:
            print("У вас нет прав на переименование")
    def do_ver(self, args):
        """Выводит версию интерпретатора"""
        print(sys.version)
    def do_exit(self, args):
        """Выход из программы"""
        return True
    def completedefault(self, text, line, begidx, endidx):
        """Автодополнение команд и имен файлов по нажатию на Tab"""
        cmds = ['dir', 'cd', 'type', 'exit', 'mkdir', 'rmdir', 'echo', 'help', 'cls', 'copy', 'date', 'del', 'fc', 'md', 'move', 'pause', 'rd', 'ren', 'set', 'sort', 'tree', 'ver']
        files = os.listdir('.')
        return [i for i in cmds + files if i.startswith(text)]

    def do_copy(self, args):
        """Копирует файлы или директории"""
        if args:
            try:
                src, dest = args.split()
                if os.path.exists(src):
                    shutil.copy(src, dest)
                    print(f"'{src}' скопировано в '{dest}'")
                else:
                    print(f"Исходный файл или директория '{src}' не существует")
            except ValueError:
                print("Введите исходный и целевой пути (например, 'copy src.txt dest.txt')")
        else:
            print("Введите аргументы для команды copy (например, 'copy src.txt dest.txt')")


    def do_set(self, args):
        """Устанавливает или отображает переменные среды"""
        if args:
            try:
                var, value = args.split('=')
                os.environ[var] = value
            except ValueError:
                print("Ошибка: Неверный формат аргумента")
        else:
            for key, value in os.environ.items():
                print(f"{key}={value}")

    def do_sort(self, args):
        """Сортирует строки текстового файла"""
        try:
            with open(args, 'r') as file:
                content = file.readlines()
                content.sort()
                print(''.join(content))
        except FileNotFoundError:
            print("Указанный файл не существует")
        except PermissionError:
            print("У вас нет прав на чтение этого файла")
    def do_tree(self, args):
        """Отображает структуру каталогов"""
        def walk_dir(directory, level):
            for item in os.listdir(directory):
                path = os.path.join(directory, item)
                print(' ' * 4 * level + '|--', item)
                if os.path.isdir(path):
                    walk_dir(path, level + 1)

        walk_dir('.', 0)
    def do_run(self, args):
        """Запускает Python скрипт"""
        if args.endswith(".py"):
            try:
                with open(args) as file:
                    exec(file.read())
            except FileNotFoundError:
                print("Указанный файл не существует")
            except PermissionError:
                print("У вас нет прав на чтение этого файла")
        else:
            print("Укажите файл с расширением .py")

    def do_ver(self, args):
        """Выводит версию интерпретатора"""
        print("Python MS-DOS-like interpreter v1.0")
    def do_attrib(self, args):
        """Изменяет или отображает атрибуты файлов"""
        if args:
            try:
                file = args.split()[-1]
                if os.path.isfile(file):
                    import stat
                    st = os.stat(file)
                    if '+r' in args:
                        os.chmod(file, st.st_mode | stat.S_IREAD)
                        print(f"Атрибуты {file} изменены.")
                    elif '-r' in args:
                        os.chmod(file, st.st_mode & ~stat.S_IREAD)
                        print(f"Атрибуты {file} изменены.")
                    else:
                        print(f"Неподдерживаемые аргументы. Используйте '+r' или '-r'.")
                else:
                    print(f"Файл '{file}' не найден.")
            except Exception as e:
                print(f"Ошибка: {e}")
        else:
            print("Введите аргументы для команды attrib (например, '+r file.txt').")

def do_find(self, args):
    """Ищет указанный текст в файле или файлах"""
    args = args.split()
    if len(args) >= 2:
        search_text = args[0]
        files = args[1:]

        for file in files:
            try:
                with open(file, 'r') as f:
                    content = f.readlines()
                    found = False
                    for index, line in enumerate(content):
                        if search_text in line:
                            print(f"{file} (строка {index + 1}): {line.strip()}")
                            found = True
                    if not found:
                        print(f"{file}: текст '{search_text}' не найден")
            except FileNotFoundError:
                print(f"Файл '{file}' не найден")
            except PermissionError:
                print(f"У вас нет прав на чтение файла '{file}'")
    else:
        print("Введите аргументы для команды find (например, 'текст file.txt').")
    do_clear = do_cls
    do_cp = do_copy
    do_rm = do_del
    do_mkdir = do_md
    do_mv = do_move
    do_rmdir = do_rd
    do_rename = do_ren
    do_export = do_set
    do_version = do_ver
    do_ls = do_dir
    def cmdloop(self, intro=None):
        self.preloop()
        if intro is not None:
            self.intro = intro
        if self.intro:
            self.stdout.write(str(self.intro) + "\n")
        stop = None
        while not stop:
            if self.cmdqueue:
                line = self.cmdqueue.pop(0)
            else:
                try:
                    line = input(self.prompt)
                except EOFError:
                    # Здесь обрабатываем Ctrl+D
                    self.stdout.write('\n')  # Выводим перевод строки
                    line = "exit"  # Устанавливаем команду "exit"
                except KeyboardInterrupt:
                    self.stdout.write("\nKeyboardInterrupt\n")
                    self.showtraceback()
                    continue
            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
        self.postloop()
   def do_find(self, args):
        """Ищет файлы и папки, содержащие указанную строку в имени"""
        if not args:
            print("Укажите строку для поиска")
            return
        for root, dirs, files in os.walk('.'):
            for name in dirs + files:
                if args in name:
                    print(os.path.join(root, name))

    def do_touch(self, args):
        """Создает пустой файл или изменяет время последнего изменения существующего файла"""
        if not args:
            print("Укажите имя файла")
            return
        if os.path.exists(args):
            os.utime(args, None)
        else:
            with open(args, 'w') as f:
                pass

    def do_more(self, args):
        """Выводит содержимое файла постранично"""
        if not args:
            print("Укажите имя файла")
            return
        try:
            with open(args, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if i % 20 == 0 and i != 0:
                        input("Press Enter to continue...")
                    print(line, end='')
        except FileNotFoundError:
            print("Указанный файл не существует")

    def do_grep(self, args):
        """Ищет указанную строку в содержимом файла"""
        if not args:
            print("Укажите строку и имя файла")
            return
        try:
            search_string, filename = args.split()
            with open(filename, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if search_string in line:
                        print(f"{i + 1}: {line.strip()}")
        except FileNotFoundError:
            print("Указанный файл не существует")
        except ValueError:
            print("Укажите строку и имя файла")

if __name__ == '__main__':
    ms_dos = MS_DOS()
    while True:
        try:
            ms_dos.cmdloop()
            break
        except KeyboardInterrupt:
            print("\nДля выхода из программы используйте команду 'exit'")
