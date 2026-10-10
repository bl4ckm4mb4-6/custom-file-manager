# Custom File Manager

**Custom File Manager** is a Python-based command-line tool designed to manage files in a custom proprietary format: **`.lds` (Luigi De Santis format)**. It features a built-in multi-line terminal editor inspired by GNU Nano, zlib compression for payload storage, and seamless conversion tools between `.lds` and standard `.txt` files.


## Features

- **Integrated LDS Editor (`Ctrl+S` to save, `Ctrl+X` to cancel):** Write text directly into a compressed `.lds` file using interactive terminal shortcuts.
- **File Reader:** Open and decompress `.lds` files to view their metadata (header and length) and payload content.
- **File Converter:** 
  - Convert `.lds` files into standard `.txt` files.
  - Convert standard `.txt` files into compressed `.lds` files.
- **Directory Manager:** List all stored files within the default workspace (`files/lds`).
- **Rich UI:** Clean, color-coded terminal interface powered by `rich` and `prompt_toolkit`.


## `.lds` File Format Specification

An `.lds` file consists of a strict header, a length metadata row, and a compressed binary payload:

```text
LDS version 1.1
Lunghezza = <uncompressed_byte_length>
<zlib_compressed_bytes>
```

1. **Header:** `LDS version 1.1` (identifies the file format version).
2. **Payload Length:** The byte length of the original uncompressed text string.
3. **Payload:** The UTF-8 encoded text string compressed using standard `zlib`.


## Compression details
An `.lds` file can weigh more than a `.txt` file when the texts are short due to the header lines and the payload length. But when texts are medium or long, an `.lds` file can weigh less thanks to payload compression.


## Prerequisites & Dependencies

Make sure you have Python installed along with the required third-party libraries:

```bash
pip install rich prompt_toolkit
```


## Installation & Usage

1. Clone or download the repository containing `file_custom.py`.
2. Run the script from your terminal:

```bash
python file_custom.py
```

3. Follow the interactive main menu options:
   - **1) Scrivi su file:** Create and write to a new `.lds` file using the built-in editor.
   - **2) Leggi da file:** Read and decompress an existing `.lds` file.
   - **3) Vedi file:** List all files currently saved in the `files/lds` directory.
   - **4) Conversione lds -> txt:** Export a `.lds` file into a standard `.txt` file.
   - **5) Conversione txt -> lds:** Import and compress a `.txt` file into the `.lds` format.
   - **6) About:** View author information, library credits, and license details.
   - **7) Exit:** Close the application.


## License

This project is open-source and available under the [MIT License](LICENSE).
