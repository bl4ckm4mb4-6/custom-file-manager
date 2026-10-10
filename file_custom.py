# File custom. Estensione .lds (luigi de santis)
# Header + Data
# Header = LDS version 1.1

''' Struttura file:
    Header
    Lunghezza
    Payload
'''

import os
import subprocess
import time
import zlib
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()
path = "files\\lds"
HEADER = b"LDS version 1.1"
HEADER_SIZE = len(HEADER)

# Configurazione combinazione tasti per salvare o annullare
kb = KeyBindings()

# Combinazione per salvare: Ctrl+S
@kb.add('c-s')
def _(event):
    # Premendo Ctrl+S si conferma l'input e si esce dall'editor
    event.app.exit(result=event.app.current_buffer.text)

# Combinazione per salvare: Ctrl+S
@kb.add('c-x')
def _(event):
    # Premendo Ctrl+X si annulla l'inserimento
    event.app.exit(result=None)


if not os.path.exists(path):
    os.makedirs(path)



def write_file():
    filename = input("Inserisci nome file: ")
    filename = filename+".lds"
    file_path = os.path.join(path, filename)
    testo = ""

    try:
        with open(file_path, "xb") as file:
            console.print("\n[bold green]=== LDS Editor ===\n")
            console.print(f"[bold cyan]Premi Ctrl+S per salvare\n")
            console.print(f"[bold cyan]Premi Ctrl+X per annullare\n")
            print("Scrivi il testo da salvare.\n\n")
            testo = prompt("> ", multiline=True, key_bindings=kb)
            
            if testo is None:
                console.print(f"[bold yellow]Operazione annullata!")
                file.close()
                os.remove(file_path)
                return
            
            testo_byte = testo.encode('utf-8')
            lunghezza_testo = len(testo_byte)
            testo_byte = zlib.compress(testo_byte)
    
            # Header
            file.write(HEADER)
            file.write(b"\n")
    
            # Lunghezza payload
            riga_lunghezza = f"Lunghezza = {lunghezza_testo}\n".encode('utf-8')
            file.write(riga_lunghezza)
    
            # Payload
            file.write(testo_byte)

        console.print(f"\n[bold green]File salvato con successo!")
        
    except FileExistsError:
        console.print(f"[bold red]File già esistente!")
    except Exception as e:
        console.print(f"[bold red]Si è verificato un errore durante il salvataggio: {e}")



def read_file():
    filename = input("Inserisci nome file: ")
    filename = filename+".lds"
    file_path = os.path.join(path, filename)

    try:
        with open(file_path, "rb") as file:
            header_letto = file.read(HEADER_SIZE)
            if header_letto != HEADER:
                raise ValueError("Formato file non valido o versione del formato non supportata!")

            # Salta \n dopo l'header
            file.readline()

            # Legge la riga della lunghezza e toglie gli spazi
            lunghezza_testo = file.readline().decode('utf-8').strip()
            pos_numero = len("Lunghezza=")
            pos_numero += 1
            length = int(lunghezza_testo[pos_numero:])

            # Legge il testo
            testo_byte = file.read()
            testo = zlib.decompress(testo_byte).decode('utf-8')

        return length, testo
    
    except FileNotFoundError:
        console.print(f"[bold red]Il file {file_path} non esiste!")
        return None, None
    except ValueError as e:
        console.print(f"[bold red]{e}")
        return None, None
    except Exception as e:
        console.print(f"Si è verificato un errore imprevisto: {e}")
        return None, None



def lds_to_txt():
    filename = input("Inserisci nome file lds da convertire: ")
    filename = filename+".lds"
    file_path = os.path.join(path, filename)
    testo = ""

    try:
        with open(file_path, "rb") as file:
            header_letto = file.read(HEADER_SIZE)
            if header_letto != HEADER:
                raise ValueError("Formato file non valido o versione del formato non supportata!")
    
            # Salta \n dopo l'header
            file.readline()
    
            # Legge la riga della lunghezza
            file.readline()
    
            # Legge il testo
            testo_byte = file.read()
            testo = zlib.decompress(testo_byte).decode('utf-8')
    
    except FileNotFoundError:
        console.print(f"[bold red]Il file {file_path} non esiste!")
        return
    except ValueError as e:
        console.print(f"[bold red]{e}")
        return
    except Exception as e:
        console.print(f"Si è verificato un errore imprevisto: {e}")
        return

    # Creazione file txt
    file_txt = input("Inserisci nome file di testo: ")
    file_txt = file_txt+".txt"
    txt_path = os.path.join(path, file_txt)

    try:
        with open(txt_path, "x") as file:
            file.write(testo)

        console.print(f"\n[bold green]File convertito con successo!")

    except FileExistsError:
        console.print(f"[bold red]File già esistente!")
    except Exception as e:
        console.print(f"[bold red]Si è verificato un errore durante il salvataggio: {e}")



def txt_to_lds():
    file_txt = input("Inserisci nome file di testo da convertire: ")
    file_txt = file_txt+".txt"
    txt_path = os.path.join(path, file_txt)
    testo = ""
    
    try:
        with open(txt_path, "r") as file:
            testo = file.read()
    
    except FileNotFoundError:
        console.print(f"[bold red]Il file {txt_path} non esiste!")
        return
    except Exception as e:
        console.print(f"[bold red]Si è verificato un errore durante l'apertura del file: {e}")

    # Creazione file lds
    filename = input("Inserisci nome file lds: ")
    filename = filename+".lds"
    file_path = os.path.join(path, filename)

    try:
        with open(file_path, "xb") as file:
            file.write(HEADER)
            file.write(b"\n")

            testo_byte = testo.encode('utf-8')
            lunghezza_testo = len(testo_byte)
            riga_lunghezza = f"Lunghezza = {lunghezza_testo}\n".encode('utf-8')
            testo_byte = zlib.compress(testo_byte)

            file.write(riga_lunghezza)
            file.write(testo_byte)

        console.print(f"\n[bold green]File convertito con successo!")

    except FileExistsError:
        console.print(f"[bold red]File già esistente!")
    except Exception as e:
        console.print(f"[bold red]Si è verificato un errore durante il salvataggio: {e}")



def about():
    about_txt = '''
    [bold dark_orange]LDS File Manager v1.0[/bold dark_orange]
    Questo tool è un file manager per il formato proprietario LDS (Luigi De Santis).
    Permette di scrivere file tramite un editor integrato, leggere file .lds, 
    convertire file lds in txt e viceversa.
    I file hanno estensioni .lds.

    [bold]Author:[/bold] Luigi De Santis
    [bold]Github:[/bold] https://github.com/bl4ckm4mb4-6

    --------------------------------------------------
    [bold green]CREDITS[/bold green]

    • [bold]Python Libraries:[/bold]
    - [cyan]rich[/cyan] (Will McGugan) - Per l'interfaccia grafica e i colori nel terminale.
    - [cyan]prompt_toolkit[/cyan] (Jonathan Slenders) - Per la gestione dell'editor multiriga e scorciatoie
      da tastiera.

    • [bold]LDS Editor integrato:[/bold]
    - Interfaccia e scorciatoie da tastiera ispirate a [bold]GNU Nano[/bold].

    • [bold]Licenza:[/bold] MIT License
    '''

    console.print("\n")
    console.print(Panel(about_txt, title="[bold white]About & Credits[/bold white]", expand=False))
    
    console.print("\n[dim]Premere Invio per tornare al menu...[/dim]")
    input()



def view_file():
    if os.path.exists(path):
        files = os.listdir(path)
        print(f"\nFile presenti in {path}:\n")

        for file in files:
            print(f"- {file}")



def main():
    while(True):
        subprocess.run('cls', shell=True)
        console.print("\n")
        testo = Text("LDS File Manager",style="bold dodger_blue1", justify="center")
        pannello = Panel(testo, subtitle="1.0", style="bold dodger_blue1", padding=(0, 4) ,expand=False)
        console.print(Align.center(pannello))
        console.print(f"\nBenvenuto in LDS File Manager!")

        console.print(f"\n[bold green1]=== MENU ===")
        console.print(f"[bold red1]1[/bold red1]) Scrivi su file")
        console.print(f"[bold red1]2[/bold red1]) Leggi da file")
        console.print(f"[bold red1]3[/bold red1]) Vedi file")
        console.print(f"[bold red1]4[/bold red1]) Conversione lds -> txt")
        console.print(f"[bold red1]5[/bold red1]) Conversione txt -> lds")
        console.print(f"[bold red1]6[/bold red1]) About")
        console.print(f"[bold red1]7[/bold red1]) Exit\n")
        scelta = int(input("Scegli un'opzione dal menù: "))

        match(scelta):
            case 1:
                print()
                write_file()
                console.print("\n[dim]Premere Invio per tornare al menu...[/dim]")
                input()
            case 2:
                print()
                lunghezza, testo = read_file()
                if lunghezza and testo != None:
                    print("\nLunghezza testo: ")
                    print(lunghezza)
                    console.print("\n[bold white]Testo:\n")
                    print(testo)

                console.print("\n[dim]Premere Invio per tornare al menu...[/dim]")
                input()
            case 3:
                print()
                view_file()
                console.print("\n[dim]Premere Invio per tornare al menu...[/dim]")
                input()
            case 4:
                print()
                lds_to_txt()
                console.print("\n[dim]Premere Invio per tornare al menu...[/dim]")
                input()
            case 5:
                print()
                txt_to_lds()
                console.print("\n[dim]Premere Invio per tornare al menu...[/dim]")
                input()
            case 6:
                about()
            case 7:
                break

        if scelta == 7:
            break

        if scelta < 1 or scelta > 7:
            console.print("[bold bright_red]Operazione non consentita. Scegli un'opzione dal menù")
            console.print("\n[dim]Premere Invio per tornare al menu...[/dim]")
            input()


    console.print(f"\n[bold yellow]Uscita dal programma", end="")
    for i in range(3):
        time.sleep(0.7)
        console.print(f".", end="")

    print()
    time.sleep(0.3)


if __name__ == "__main__":
    main()