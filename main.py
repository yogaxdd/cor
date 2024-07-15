import os
import subprocess
from colorama import Fore, Style, init

# Inisialisasi colorama
init(autoreset=True)

# Daftar file Python yang tersedia untuk dijalankan
file_options = [
    "blum.py",
    "chick_hatch.py",
    "cyberfinance.py",
    "dejen.py",
    "dotcoin.py",
    "hamster.py",
    "matchquest.py",
    "memefi.py",
    "memefi_old.py",
    "pixeltele.py",
    "pixelfight.py",
    "spinner.py",
    "tabi.py",
    "timefarm.py",
    "yescoin.py",
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome_message():
    print(r"""
██╗   ██╗ ██████╗  ██████╗  █████╗ ██╗  ██╗██████╗ 
╚██╗ ██╔╝██╔═══██╗██╔════╝ ██╔══██╗╚██╗██╔╝██╔══██╗
 ╚████╔╝ ██║   ██║██║  ███╗███████║ ╚███╔╝ ██║  ██║
  ╚██╔╝  ██║   ██║██║   ██║██╔══██║ ██╔██╗ ██║  ██║
   ██║   ╚██████╔╝╚██████╔╝██║  ██║██╔╝ ██╗██████╔╝
   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
          """)
    print(Fore.GREEN + Style.BRIGHT + "YogaxD Server Bot Menu")
    print(Fore.BLUE + Style.BRIGHT + "\nJika Ingin Mengganti Query Menuju Ke File Manager Dan Ubah Query Sesuai Dengan Bot Yang Dituju\nMisal : initdata-hamster.txt\n")

def display_menu():
    print(Fore.RED + Style.BRIGHT + "Silakan pilih file yang ingin dijalankan:")
    for i, file in enumerate(file_options, start=1):
        print(f"{i}. {file}")

def run_selected_file(choice):
    try:
        selected_file = file_options[choice - 1]
        subprocess.run(["python", selected_file], check=True)
    except IndexError:
        print("Pilihan tidak valid. Silakan coba lagi.")
    except subprocess.CalledProcessError as e:
        print(f"Terjadi kesalahan saat menjalankan {selected_file}: {e}")

if __name__ == "__main__":
    clear_screen()
    print_welcome_message()
    display_menu()
    try:
        choice = int(input(">> "))
        clear_screen()
        run_selected_file(choice)
    except ValueError:
        print("Masukkan angka yang valid.")
