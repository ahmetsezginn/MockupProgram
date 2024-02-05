
#app_operations.py

import subprocess
import os
from time import sleep
from file_operations import FileOperations

class AppOperations:
    def __init__(self):
        self.program_record_file = os.path.join(os.path.dirname(__file__), "program_yerleştirme.app")
        self.fixed_file = os.path.join(os.path.dirname(__file__), "kayıt_program.png")
        self.fixed_program = os.path.join(os.path.dirname(__file__), "program_kayıt.app")
    def run(self, psd_selected, dragged_files, dragged_folder):
        # Önce seçilen dosyayı Photoshop ile aç
        for psd_file in psd_selected:
            if psd_file:
                self.open_file_with_app(psd_file, "/Applications/Adobe Photoshop (Beta)/Adobe Photoshop (Beta).app")

            # Sürüklenen dosyaları işle
            if dragged_files:
                for file in dragged_files:
                    self.open_file_with_app(file, self.program_record_file)

            # Sürüklenen klasörü işle
            if dragged_folder:
                file_list = [os.path.join(dragged_folder, f) for f in os.listdir(dragged_folder) if os.path.isfile(os.path.join(dragged_folder, f))]
                file_list.sort()
                for file_path in file_list:
                    self.open_file_with_app(file_path, self.program_record_file)

            # Sabit dosya ve programı aç
            self.open_file_with_app(self.fixed_file, self.fixed_program)

            # Sürüklenen dosya veya klasör adını al ve .jpg dosyasının adını değiştir
            if dragged_files:
                for file in dragged_files:
                    file_name_without_extension =os.path.splitext(os.path.basename(file))[0]
                    file_name_extension =os.path.splitext(os.path.basename(file))[1]
                target_file = "/Users/ahmetsezgin/Desktop/yerleştirme_kayıt/mockup.jpg"
                FileOperations.rename_file(psd_selected,target_file, file_name_without_extension,file_name_extension)
            elif dragged_folder:
                folder_name_without_extension =os.path.splitext(os.path.basename(file))[0]
                folder_name_extension =os.path.splitext(os.path.basename(file))[0]
                target_file = "/Users/ahmetsezgin/Desktop/yerleştirme_kayıt/mockup.jpg"
                FileOperations.rename_file(psd_selected,target_file, folder_name_without_extension,folder_name_extension)
            FileOperations.count+=1

    @staticmethod
    def open_file_with_app(file_path, app_path):
        subprocess.run(["open", "-a", app_path, file_path])
        sleep(5)

