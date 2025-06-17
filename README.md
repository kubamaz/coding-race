# 🏎️ Code-Racing

**Code-Racing** to dynamiczna gra wyścigowa, w której dwaj studenci ścigają się 
swoimi samochodzikami po torze pełnym pytań. 
Rozgrywka łączy zręcznościowe omijanie przeszkód z zadaniami, 
które mogą wpłynąć na prędkość pojazdu.


---

## 🎮 Funkcje gry

- 🚗 Sterowanie samochodem z prostą fizyką
- 🖱️ Graficzny interfejs użytkownika
- 🎵 Efekty dźwiękowe i muzyka w tle
- ⏱️ Licznik okrążeń

---

## 🕹️ Jak uruchomić grę

### Wymagania

- Python 3.12 lub nowszy
- Pygame
- pygame_gui

### Instalacja i uruchomienie

1. Po uruchomieniu PyCharma sklonuj repozytorium:

   ```bash
   git clone https://github.com/kubamaz/coding-race.git
   cd coding-race

2. Zainstaluj wymagane biblioteki:

   ```bash
   pip install pygame pygame_gui

3. Uruchom serwer (może to zrobić dowolna osoba):

   ```bash
   cd server
   python server.py
   cd ..

4. Uruchom grę (koniecznie przy uruchomionym serwerze!):

   ```bash
   cd client
   python main.py
   
---

## 🕹️ Sterowanie samochodem:

- ⬆️⬇️⬅️➡️ lub WSAD - kierunek jazdy
- spacja - uruchomienie boosta
