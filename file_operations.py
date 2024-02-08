#file_operations.py


import os
from tkinter import filedialog
class FileOperations:
    count=1
    def __init__(self):
        self.psd_selected = None
        self.dragged_files = []
        self.dragged_folder = None

    def psd_file(self):
        mockup_folder_path = os.path.join(os.path.dirname(__file__), "new_A_PSD_MOCKUP")
        # askopenfilenames ile çoklu seçim yapılmasına izin veriliyor
        self.psd_selected = filedialog.askopenfilenames(initialdir=mockup_folder_path,title="Select PSD Files", filetypes=(("PSD files", "*.psd"), ("All files", "*.*")))
    def handle_dragged_files(self, event):
        files_string = event.data

        # Süslü parantezlerle ayrılmış dosya yollarını ayrıştır
        if files_string.startswith('{') and files_string.endswith('}'):
            files_string = files_string[1:-1]  # Süslü parantezleri kaldır
            files_list = files_string.split('} {')  # Dosya yollarını ayır
        else:
            files_list = [files_string]

        # Her dosya için kontrol yap
        for file_path in files_list:
            file_path = file_path.strip()

            # Dosya yolu geçerliyse listeye ekle
            if os.path.isfile(file_path):
                self.dragged_files.append(file_path)
                print("Eklenen dosya:", file_path)  # Hata ayıklama için eklenen satır
    def handle_dragged_folder(self, event):
        folder_path = event.data
        if folder_path.startswith("{") and folder_path.endswith("}"):
            folder_path = folder_path[1:-1]

        if os.path.isdir(folder_path):
            self.dragged_folder = folder_path
        else:
            self.dragged_folder = None
    
    @staticmethod
    def rename_file(psd_selected, target_file_path, new_name_basename,file_extension):
        if not target_file_path.endswith(".jpg"):
            print("Hedef dosya .jpg uzantılı değil.")
            return

        file_folder = os.path.dirname(target_file_path)

        # Yeni dosya adını uzantı ile birlikte oluştur
        new_file_path = os.path.join(file_folder, f"{new_name_basename}_{str(FileOperations.count)}{file_extension}")
        os.rename(target_file_path, new_file_path)
        print(f"'{target_file_path}' dosyasının yeni adı: '{new_file_path}'")

