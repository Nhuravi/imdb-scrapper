# IMDb Web Scraper

Program Python ini mengambil data mengenai 250 film teratas dari IMDb dan memperbarui data yang ada pada database MySQL dengan judul dan peringkat film.

## Instalasi

1. Clone repository:

    ```bash
    git clone https://github.com/GROSANIA/imdb-webscraps.git
    cd imdb-web-scraper
    ```

2. Install packages yang sudah di cantumkan:

    ```bash
    pip install -r requirements.txt
    ```

3. Siapkan MySQL database:

    - Buat database bernama `imdb_scrapping`.
    - Lalu Import `movies.sql` pada database `imdb_scrapping`.
    - Update detail koneksi database pada `app.py` (host, user, password).


## Penggunaaan

1. Eksekusi program menggunakan perintah dibawah ini:

    ```bash
    python app.py
    ```

    Perintah Ini akan memulai Program, dan Anda dapat mengakses hasil data film-film top yang diambil di `http://127.0.0.1:5000/top_movies`.

2. Database MySQL 'imdb_scrapping' akan diisi dengan 250 film teratas. Jika film sudah ada di database, maka akan diperbarui.

## Catatan

- Program ini berjalan pada versi Python 3.12
- Pastikan server MySQL Anda berjalan sebelum menjalankan scraper.
- Pastikan Anda memiliki versi ChromeDriver yang benar untuk browser Chrome Anda.

## Extra

Dibuat oleh Nhuravi