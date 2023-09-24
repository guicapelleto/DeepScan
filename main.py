#coding: utf-8
import os
import threading
import time
import grex
from functools import partial
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.button import Button
from plyer import filechooser
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

Builder.load_file('screen.kv')
Window.size = 1000, 800
Window.minimum_width, Window.minimum_height = 800, 600


class ButtonList(Button):

    content = None

    def __init__(self, **kwargs):
        super(ButtonList, self).__init__(**kwargs)
        self.size_hint = 1, None
        self.height = dp(50)
        self.background_color = 0, 0, 1, 0.4

    def on_press(self):
        if self.content == 'folder':
            sm.current_screen.ids.folder_txt.text = self.text
        if self.content == 'word':
            sm.current_screen.ids.word_txt.text = self.text


class BoxRolagem(BoxLayout):

    def __init__(self, **kwargs):
        super(BoxRolagem, self).__init__(**kwargs)


class TelaOperacao(Screen):

    folder_exp = False
    word_exp = False
    sensitive = False
    folders = []
    excluded_folders = []
    words = []
    total_files = 0
    master_report = {}
    keep_alive = True
    lock_window = False

    def __init__(self, **kwargs):
        super(TelaOperacao, self).__init__(**kwargs)

    def create_simple_notify(self, text, x = 0):
        notify = Notification()
        notify.duration = 1.5
        notify.ids.alert.text = text
        notify.open()

    def block_content(self):
        rolagem = sm.current_screen.ids.rolagem_principal
        if self.folder_exp == False and self.word_exp == False:
            rolagem.do_scroll = False
        else:
            rolagem.do_scroll = True

    def reload_words(self):
        word_list_box = sm.current_screen.ids.word_box
        self.words = list(set(word.lower() for word in self.words))
        word_list_box.clear_widgets()
        def create_word_in_list(word):
            cbtn = ButtonList()
            cbtn.text = word
            cbtn.content = 'word'
            word_list_box.add_widget(cbtn)
        for word in self.words: create_word_in_list(word)

    def turn_sensitive(self):
        if self.sensitive:
            self.sensitive = False
            sm.current_screen.ids.btn_sensitive.text = 'Sensitive OFF'
            self.reload_words()
            return
        if self.sensitive == False:
            self.sensitive = True
            sm.current_screen.ids.btn_sensitive.text = 'Sensitive ON'
            return

    def exp_f(self,signal):
        folder_list = sm.current_screen.ids.folders
        btn_exp = sm.current_screen.ids.btn_exp_folder
        if signal:
            folder_list.height = dp(0)
            folder_list.opacity = 0.2
            self.folder_exp = False
            btn_exp.text = 'V'
        else:
            folder_list.height = dp(150)
            folder_list.opacity = 1
            self.folder_exp = True
            btn_exp.text = '^'

    def expand_folder_list(self):
        if self.folder_exp: self.exp_f(True)
        else: self.exp_f(False)

    def exp_w(self,signal):
        word_list = sm.current_screen.ids.words
        btn_exp = sm.current_screen.ids.btn_exp_word
        if signal:
            word_list.height = dp(0)
            word_list.opacity = 0.2
            self.word_exp = False
            btn_exp.text = 'V'
        else:
            word_list.height = dp(150)
            word_list.opacity = 1
            self.word_exp = True
            btn_exp.text = '^'

    def expand_word_list(self):
        if self.word_exp: self.exp_w(True)
        else:self.exp_w(False)

    def check_folder_in_folder(self, folder, folder2):
        folder = os.path.abspath(os.path.normcase(folder))
        file = os.path.abspath(os.path.normcase(folder2))
        split = file.split(folder)
        if len(split) != 2: return False
        first_char = split[1][:1]
        if first_char == '\\' or first_char == '/':
            return True
        return False

    def add_folder(self):
        folder = sm.current_screen.ids.folder_txt.text
        folder_list_box = sm.current_screen.ids.folder_box
        if folder == '':
            self.create_simple_notify("Exception empty folder")

            return
        if not os.path.exists(folder):
            self.create_simple_notify ("Exception folder not exists")
            return
        fullpath = os.path.abspath(os.path.normcase(folder))
        if fullpath in self.excluded_folders:
            self.rem_folder()
            return
        for f in self.folders:
            if self.check_folder_in_folder(f, fullpath):
                self.create_simple_notify ("Exception subdirectory already in the list")
                return
        if not fullpath in self.folders:
            cbtn = ButtonList()
            cbtn.text = fullpath
            cbtn.content = 'folder'
            folder_list_box.add_widget(cbtn)
            self.folders.append(fullpath)
        sm.current_screen.ids.folder_txt.text = ''
        self.create_simple_notify('Folder added to search list')

    def exclude_folder(self):
        folder = sm.current_screen.ids.folder_txt.text
        folder_list_box = sm.current_screen.ids.folder_box
        if folder == '':
            self.create_simple_notify ("Exception empty folder")
            return
        if not os.path.exists(folder):
            self.create_simple_notify ("Exception folder not exists")
            return
        fullpath = os.path.abspath(os.path.normcase(folder))
        if fullpath in self.folders:
            self.rem_folder()
            return
        if not fullpath in self.excluded_folders:
            cbtn = ButtonList()
            cbtn.text = '[-] ' + fullpath
            cbtn.content = 'folder'
            folder_list_box.add_widget(cbtn)
            self.excluded_folders.append(fullpath)
        self.exp_f(False)
        sm.current_screen.ids.folder_txt.text = ''

    def find_folder_by_path(self, text):
        folder_list = sm.current_screen.ids.folder_box
        for btn in folder_list.children:
            try:
                if text == btn.text:
                    return btn
            except Exception: pass

    def rem_folder(self):
        folder_list_box = sm.current_screen.ids.folder_box
        folder = sm.current_screen.ids.folder_txt.text
        if folder[:3] == '[-]':
            fullpath = os.path.abspath(os.path.normcase(folder[4:]))
        else:
            fullpath = os.path.abspath(os.path.normcase(folder))
        if fullpath in self.excluded_folders:
            del self.excluded_folders[self.excluded_folders.index(fullpath)]
            btn = self.find_folder_by_path('[-] ' + fullpath)
            folder_list_box.remove_widget(btn)
        else:
            self.create_simple_notify("Exception Folder not listed")
        if fullpath in self.folders:
            del self.folders[self.folders.index(fullpath)]
            btn = self.find_folder_by_path(fullpath)
            folder_list_box.remove_widget(btn)

    def add_word(self):
        if not self.sensitive:
            word = str(sm.current_screen.ids.word_txt.text).lower()
        else: word = str(sm.current_screen.ids.word_txt.text)
        word_list_box = sm.current_screen.ids.word_box
        if word == '':
            self.create_simple_notify("Exception empty folder")
            return
        if word in self.words:
            self.create_simple_notify("Exception folder already in list")
            return
        cbtn = ButtonList()
        cbtn.text = word
        cbtn.content = 'word'
        word_list_box.add_widget(cbtn)
        self.words.append(word)
        sm.current_screen.ids.word_txt.text = ''
        self.create_simple_notify('Word added to search list')

    def find_word_by_str(self, text):
        word_list = sm.current_screen.ids.word_box
        for btn in word_list.children:
            try:
                if text == btn.text:
                    return btn
            except Exception:
                pass

    def rem_word(self):
        if not self.sensitive:
            word = str(sm.current_screen.ids.word_txt.text).lower()
        else: word = str(sm.current_screen.ids.word_txt.text)
        word_list_box = sm.current_screen.ids.word_box
        if word in self.words:
            del self.words[self.words.index(word)]
            btn = self.find_word_by_str(word)
            word_list_box.remove_widget(btn)
            sm.current_screen.ids.word_txt.text = ''
        else:
            self.create_simple_notify("Exception Folder not listed")

    def update_fields(self, bar_value, rel_value, results_value):
        gen = sm.current_screen.ids
        gen.progresso.value = bar_value
        gen.relatorio.text = rel_value
        gen.lbl_results.text = "Results: " + str(results_value)

    def stop(self):
        self.create_simple_notify("Stopping thread...")
        self.keep_alive = False

    def start(self):
        if self.words == [] or self.folders == []:
            self.create_simple_notify ("Exception word and folder must not be empty")
            return
        sm.current_screen.ids.relatorio.text = ''
        thread = threading.Thread(target= self.start_thread)
        thread.start()
        sm.current_screen.ids.stop_btn.disabled = False
        sm.current_screen.ids.start_btn.disabled = True
        self.keep_alive = True

    def save_report(self):
        report_created = filechooser.save_file()
        if report_created == None: return
        report = 'DeepScan Report created\n\n'
        results = self.master_report.get('data')
        errors = self.master_report.get('error')
        info = self.master_report.get('info')
        if not info == None:
            for item in info:
                report += item + '\n'
        if not results == None:
            for item in results:
                report += item + '\n'
        if not errors == None:
            for item in errors:
                report += item + '\n'
        s = open(report_created[0],'w')
        s.write(str(report))
        s.close()
        self.create_simple_notify("Report saved!")

    def show_dir(self):
        s = filechooser.choose_dir()
        if not s == None: sm.current_screen.ids.folder_txt.text = s[0]

    def start_thread(self):
        Clock.schedule_once(partial(sm.current_screen.create_simple_notify,'Verifying all files to search'), 0)
        search = Searcher(self.folders, self.excluded_folders, self.words, self.sensitive)
        search.get_all_files()
        Clock.schedule_once(partial(sm.current_screen.create_simple_notify, 'Search done!'), 0)


class Notification(ModalView):

    duration = None

    def __init__(self, **kwargs):
        super(Notification,self).__init__(**kwargs)

    def on_open(self):
        if not self.duration == None:
            self.auto_dismiss = True
            Clock.schedule_once(self.dismiss, self.duration)
            return
        self.dismiss()

    def open(self, *_args, **kwargs):
        self.pos_hint = {'x' : 0, 'top' : 1.1}
        animation = Animation(pos_hint = {'x' : 0, 'top' : 1}, duration=0.7)
        animation.start(self)
        super(Notification, self).open(*_args, **kwargs)


class Searcher:

    added_files = []
    size_buffer = 1 * 1024 * 1024
    results = 0
    data = ''

    def __init__(self, folders, excluded_folders, words, senstive):
        self.restore_settings()
        self.folders = folders
        self.excluded_folders = excluded_folders
        self.words = words
        self.sensitive = senstive

    def restore_settings(self):
        self.added_files = []
        self.results = 0
        sm.current_screen.master_report = {}
        sm.current_screen.ids.lbl_results.text = "Results: " + str(self.results)
        sm.current_screen.ids.total_files.text = "Total files: " + str(len(self.added_files))

    def check_file_in_folder(self, folder, file):
        folder = os.path.abspath(os.path.normcase(folder))
        file = os.path.abspath(os.path.normcase(file))
        split = file.split(folder)
        if len(split) != 2: return False
        first_char = split[1][:1]
        if first_char == '\\' or first_char == '/':
            return True
        return False

    def add_file(self, file):
        file = os.path.abspath(os.path.normcase(file))
        if not file in self.added_files:
            self.added_files.append(file)

    def get_all_files(self):
        self.start_time = time.time()
        check_ex = False
        if len(self.excluded_folders) != 0:
            check_ex = True
        for folder in self.folders:
            for diretorio_atual, subdiretorios, arquivos in os.walk(folder):
                for arquivo in arquivos:
                    actual_file = os.path.join(diretorio_atual, arquivo)
                    if check_ex:
                        for ex_folder in self.excluded_folders:
                            if not self.check_file_in_folder(ex_folder, actual_file):
                                self.add_file( actual_file)
                    else: self.add_file(actual_file)
        sm.current_screen.ids.total_files.text = "Total files: " + str(len(self.added_files))
        self.reporter('info',"Total files: " + str(len(self.added_files)))
        sm.current_screen.lock_window = False
        self.finder()

    def updater(self, x = None):
        sm.get_screen('tela_operacao').update_fields(self.progress, self.data, self.results)

    def print_info(self, filepath, word, line, x = 0):
        text = "\n[DATA FOUND]"
        text = text + "\nFile location: " + filepath
        text = text + "\nWord: " + word + "\n"
        text = text + str(line)
        text = text + '\n[END]\n'
        self.reporter('data',text)
        self.data = self.data + text
        self.updater()

    def searchword(self, data, word, filepath):
        line_list = grex.find_all_lines(word, data, self.sensitive)
        if not line_list == None:
            for line in line_list:
                Clock.schedule_once(partial(self.print_info,filepath,word,line), 0.1)
                self.results += 1

    def reporter(self, type, log):
        master_report = sm.current_screen.master_report
        if not master_report.get(type):
            master_report[type] = [log]
            return
        master_report[type] += [log]

    def inicial_sets(self):
        screen = sm.current_screen.ids
        screen.start_btn.disabled = False
        screen.stop_btn.disabled = True

    def finder(self):
        count = 0
        n_files = len(self.added_files)
        inf = "Total files: %s/%s" % (n_files, count)
        for file in self.added_files:
            if not sm.current_screen.keep_alive: break
            count +=1
            self.progress = count/n_files
            inf = "Total files: %s/%s" % (n_files,count)
            sm.current_screen.ids.total_files.text = (inf)
            try:
                current_file = open(file, 'rb')
                while sm.current_screen.keep_alive:
                    cdata = current_file.read(self.size_buffer)
                    if not cdata:
                        break
                    for word in self.words:
                        if not self.sensitive: word = word.lower()
                        self.searchword(cdata, word , file)
            except Exception as err:
                self.reporter('error', str(err))
            Clock.schedule_once(lambda x: self.updater(), 0.2)
        self.reporter('info', inf)
        end = time.time() - self.start_time
        inf = 'Total time: ' + str(round(end,2))
        self.reporter('info', inf)
        sm.get_screen('tela_operacao').ids.total_time.text = inf
        self.inicial_sets()


sm = ScreenManager()
sm.add_widget(TelaOperacao(name = 'tela_operacao'))


class DeepScan(App):

    def build(self):
        self.icon = 'icon.icns'
        self.title = "DeepScan"
        return sm

deepscan = DeepScan()
deepscan.run()