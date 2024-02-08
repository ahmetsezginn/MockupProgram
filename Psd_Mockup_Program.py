import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from file_operations import FileOperations
from app_operations import AppOperations
from PIL import Image, ImageTk
import os

class Psd_Mockup_Program:
    def __init__(self):
        self.app = TkinterDnD.Tk()
        self.app.title('Program Arayüzü')
        self.file_ops = FileOperations()
        self.app_ops = AppOperations()
        self.setup_ui()
        self.image_references = []

    def setup_ui(self):
        self.drag_file_button = tk.Button(self.app, text="Dosya Sürükle", command=self.open_file_drag_window)
        self.drag_file_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.drag_folder_button = tk.Button(self.app, text="Klasör Sürükle", command=self.open_folder_drag_window)
        self.drag_folder_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        
        self.psd_file_button = tk.Button(self.app, text="PSD Kaynak", command=self.psd_file)
        self.psd_file_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        
        self.reset_button=tk.Button(self.app,text="içerikleri sıfırla", command=self.reset_contents)
        self.reset_button.pack(side=tk.LEFT,padx=10,pady=10)
        
        
        self.run_button = tk.Button(self.app, text="Run", command=self.run)
        self.run_button.pack(side=tk.LEFT, padx=10, pady=10)
        
    def open_file_drag_window(self):
        self.file_drag_window = tk.Toplevel(self.app)
        self.file_drag_window.title("Dosya Sürükle")

        # Canvas ve Scrollbar için konteyner frame oluştur
        self.canvas_frame = tk.Frame(self.file_drag_window)
        self.canvas_frame.pack(fill="both", expand=True)

        # Canvas oluştur ve frame içine yerleştir (başlangıç boyutları belirlendi)
        canvas_width = 400  # Örnek genişlik değeri
        canvas_height = 300  # Örnek yükseklik değeri
        self.preview_canvas = tk.Canvas(self.canvas_frame, bg='white', width=canvas_width, height=canvas_height)
        self.preview_canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar oluştur ve Canvas ile ilişkilendir
        self.scrollbar = tk.Scrollbar(self.canvas_frame, command=self.preview_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.preview_canvas.config(yscrollcommand=self.scrollbar.set)
        # Canvas üzerinde bir etiket oluşturacak Frame oluştur
        self.header_frame = tk.Frame(self.preview_canvas, bg='lightgrey', height=50)
        self.header_frame.pack_propagate(False)  # Frame'in boyutunu koru, içindeki widget'ların boyutuna göre değişmesin
        label = tk.Label(self.header_frame, text="Buraya Dosyaları Sürükleyin", bg='lightgrey')
        label.pack(side="top", fill="both", expand=True)
        self.header_frame.pack(fill="x")
        # Canvas üzerinde bir window oluştur ve header frame'i içine yerleştir
        self.header_frame_window = self.preview_canvas.create_window(0, 0, window=self.header_frame, anchor='nw', width=self.preview_canvas.winfo_reqwidth())

        # Canvas'ın boyutu değiştiğinde etiketi ve dikdörtgeni güncelle
        self.preview_canvas.bind('<Configure>', self.on_canvas_configure)

        # Drop işlevselliğini etkinleştir
        self.header_frame.drop_target_register(DND_FILES)
        self.header_frame.dnd_bind('<<Drop>>', self.file_dragged)

    def update_drop_area(self, event):
        # Canvas'ın genişliğini al ve dikdörtgenin boyutunu güncelle
        new_width = event.width
        self.preview_canvas.coords(self.drop_area_rect, 0, 0, new_width, 50)
        # Etiketi yeni genişliğin ortasına taşı
        self.preview_canvas.coords(self.drop_area_label, new_width // 2, 25)
        # Etiketi ön plana getir
        self.preview_canvas.tag_raise(self.drop_area_label, self.drop_area_rect)
    def on_canvas_configure(self, event):
        # 'header' tag'ine sahip öğeleri güncelle
        self.preview_canvas.coords('header', 0, 0, event.width, 50)
        self.preview_canvas.tag_raise('header')

    def file_dragged(self, event):
        self.file_ops.handle_dragged_files(event)
        self.update_dragged_files_list()
        self.file_drag_window.update_idletasks()  # Pencerenin boyutunu güncelle
        self.update_dragged_files_list()
    def update_dragged_files_list(self):
        # Canvas'ı temizle ve resim referanslarını sıfırla
        self.preview_canvas.delete("all")

        # Header frame'ini yeniden paketle
        self.header_frame.pack(fill="x")

        # Header frame'ini canvas üzerinde bir window olarak yeniden oluştur
        self.header_frame_window = self.preview_canvas.create_window(
            0, 0, window=self.header_frame, anchor='nw', width=self.preview_canvas.winfo_reqwidth()
        )

        # Başlangıç koordinatları ve satır yüksekliği
        padding_1 = 10
        padding_2 =60
        padding=10
        image_width, image_height = 100, 100
        text_width_limit = 100  # Metin genişliği sınırlaması
        x, y = padding_1, padding_2
        next_x, next_y = x, y  # Sonraki resim/metin için koordinatlar
        row_height = 0  # Satır yüksekliği

        for file_path in self.file_ops.dragged_files:
            try:
                # Resmi aç ve boyutlandır
                image = Image.open(file_path)
                image.thumbnail((image_width, image_height))  # Image.ANTIALIAS kaldırıldı
                photo = ImageTk.PhotoImage(image)
                self.image_references.append(photo)

                # Resmi canvas'a ekle
                self.preview_canvas.create_image(next_x, next_y, image=photo, anchor='nw')

                # Metni canvas'a ekle ve genişliği sınırla
                filename = os.path.splitext(os.path.basename(file_path))[0]
                text_id = self.preview_canvas.create_text(next_x, next_y + image_height + padding, text=filename, anchor='nw', width=text_width_limit)
                
                # Metin boyutlarını al ve row_height ayarla
                text_bbox = self.preview_canvas.bbox(text_id)
                text_height = text_bbox[3] - text_bbox[1]
                row_height = max(row_height, image_height + text_height + padding)

                # Sonraki öğenin x koordinatını güncelle
                next_x += max(image_width, text_width_limit) + padding

                # Eğer canvas genişliğini aşarsa, yeni satıra geç
                if next_x + max(image_width, text_width_limit) > self.preview_canvas.winfo_width():
                    next_x = padding
                    next_y += row_height + padding
                    row_height = 0  # Satır yüksekliğini sıfırla

            except Exception as e:
                print(f"Hata: {e}")
        self.preview_canvas.tag_raise('header')
    def open_folder_drag_window(self):
        self.folder_drag_window = tk.Toplevel(self.app)
        self.folder_drag_window.title("Klasör Sürükle")
        label = tk.Label(self.folder_drag_window, text='Buraya Klasörü Sürükleyin')
        label.pack(padx=10, pady=10)
        label.drop_target_register(DND_FILES)
        label.dnd_bind('<<Drop>>', self.folder_dragged)

    def folder_dragged(self, event):
        self.file_ops.handle_dragged_folder(event)

    def psd_file(self):
        self.file_ops.psd_file()
    def reset_contents(self):
        self.file_ops.dragged_files.clear()
        self.file_ops.dragged_folder = None
        FileOperations.count=1
        tk.messagebox.showinfo("showinfo", "All Content Has Been Reset")
    def run(self):
        psd_selected = self.file_ops.psd_selected
        dragged_files = self.file_ops.dragged_files
        dragged_folder = self.file_ops.dragged_folder
        self.app_ops.run(psd_selected, dragged_files, dragged_folder)
        tk.messagebox.showinfo("Showinfo", "Your All File Has Been Mockup")

    def start(self):
        self.app.mainloop()

def start_main_interface():
    interface = Psd_Mockup_Program()
    interface.start()

if __name__ == "__main__":
    start_main_interface()
