# Publikacja na GitHub — instrukcja

## Co zawiera paczka?

Gotowy szkielet repozytorium z angielskim `README.md`, notebookiem treningowym, zmodyfikowaną aplikacją Streamlit, konfiguracją środowiska, ilustracjami i dokumentacją techniczną. **Bez pełnej wspólnej pracy dyplomowej, zbioru CSV i plików `.pkl`.**

## Wariant A — GitHub przez przeglądarkę

1. Wejdź na `https://github.com/new` po zalogowaniu.
2. Podaj nazwę `traffic-stress-prediction-snowflake` i krótki opis, np. „Snowflake data warehouse, ML model comparison and Streamlit driver stress index predictor”.
3. Wybierz repozytorium **Public**. Na tym etapie nie twórz osobnego README, `.gitignore` ani licencji — masz je w paczce (licencji celowo nie dodajemy).
4. Utwórz repozytorium. Wybierz **uploading an existing file** lub `Add file → Upload files`.
5. **Rozpakuj ZIP** na komputerze. Wgraj **zawartość** folderu `traffic-stress-prediction-snowflake`, zachowując układ katalogów; **nie wgrywaj pliku ZIP jako jedynego pliku w repozytorium**.
6. Upewnij się, że `.gitignore` jest widoczny po uploadzie i że dokument `.docx`, pliki `.pkl` oraz źródłowy CSV nie trafiły do repozytorium.
7. Wybierz `Commit changes` i odśwież stronę repozytorium. Sprawdź, czy README wyświetla diagram i zdjęcia.

## Wariant B — Git w terminalu

Zamiast przeglądarki możesz utworzyć repozytorium i następnie użyć lokalnie `git init`, `git add`, `git commit`, `git branch -M main`, `git remote add origin ...` i `git push -u origin main`, po uprzednim sprawdzeniu zawartości `git status`. Nie umieszczaj tokenów/hasła bezpośrednio w poleceniach ani plikach.

## Co należy jeszcze sprawdzić przed uruchomieniem aplikacji?

- Czy Snowflake Stage zawiera `traffic_stress_best_model.pkl` oraz `preprocessor_20260514_202212.pkl`.
- Czy ten zestaw artefaktów jest zgodny z sześcioma cechami używanymi przez notebook.
- Czy masz uprawnienia do użytkowania bazy danych, stage i Streamlit in Snowflake.
- Czy masz prawo publicznie udostępnić własny kod/notebook/screenshoty w świetle zasad projektu i praw innych współautorów.
- Czy aktualna instancja Snowflake nie będzie generowała nieoczekiwanych kosztów.

## Dlaczego nie zamieszczamy pracy dyplomowej?

Praca została obroniona **w maju 2026**, a w dniu przygotowania paczki (**19 października 2026**) sześć miesięcy od obrony jeszcze nie minęło. Ponadto był to dokument współautorski. Rozważ dodanie całości dopiero po sprawdzeniu dokładnej daty obrony, uprawnienia uczelni i uzyskaniu stosownych zgód współautorek.

## Status

**Paczka przygotowana lokalnie, nie wysłana na GitHub.** Przesłanie wymaga operacji na zalogowanym koncie użytkowniczki.
