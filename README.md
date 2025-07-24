# System Monitor

System Monitor to prosta aplikacja do monitorowania najważniejszych parametrów systemu operacyjnego oraz do rejestrowania alertów przekroczenia wykorzystania CPU, pamięci operacyjnej i masowej.

---

## Wymagania

Brak szczególnych wymagań.

---

## Instalacja

1. Pobierz odpowiedni plik z folderu `dist`:

    - `System Monitor` — dla systemu Linux (Fedora)
    - `System_Monitor.exe` — dla systemu Windows

2. Umieść plik w dowolnym folderze.
3. Uruchom plik.

---

## Konfiguracja

Aby skonfigurować progi przekroczenia alertów, należy ustawić odpowiednie wartości w pliku `config.ini`, który zostanie wygenerowany przy pierwszym uruchomieniu aplikacji.

Przy pierwszym uruchomieniu powstanie także plik bazy danych `alerts`, który rejestruje wykryte alerty w relacji User → Alert.

---

## Opis aplikacji

Aplikacja jest podzielona na 4 główne sekcje:

1. **Alerts**  
   Okno wyświetla ostatnio zarejestrowane alerty przekroczeń.  
   - Przycisk **Refresh** — odświeża zawartość okna alertów.  
   - Przycisk **Clear** — czyści widoczne alerty zarówno z aplikacji, jak i z bazy danych.

2. **Resource Graphs**  
   Okno wyświetla wykresy zużycia CPU, dysku oraz pamięci operacyjnej.

3. **Network**  
   Okno przedstawia statystyki wykorzystania sieci.  
   - Przycisk **Reset Counters** — resetuje statystyki wykorzystania sieci.

4. **Logs**  
   Okno umożliwia przegląd pełnych logów systemowych.

---

## Tech stack

- **Kod:** Python 3.18
- **Baza danych:** SQLite
- **ORM:** Peewee
- **UI:** Tkinter
- **Wykresy:** Matplotlib, NumPy

---

## Licencja

Ten projekt jest dostępny na licencji **UNLICENSED**. Szczegóły znajdują się w pliku `LICENSE`.

---

## Informacje końcowe

Aplikacja została stworzona jako projekt uczelniany i przetestowana na systemach Fedora Linux oraz Windows 10.

Do jej stworzenia wykorzystano m.in. oficjalną dokumentację Pythona, forum Stack Overflow, inne fora tematyczne oraz AI (w stopniu instruktarzowym, np. przy wykorzystaniu słabo udokumentowanych bibliotek i redakcji pliku README).

---
