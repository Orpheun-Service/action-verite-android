# Action & Vérité — version Android

Cette version utilise Kivy au lieu de CustomTkinter.
Elle est conçue pour être empaquetée en APK avec Buildozer/python-for-android.

## Test sur PC
pip install -r requirements.txt
python main.py

## Génération APK
Buildozer fonctionne principalement sous Linux/WSL.

1. Installer WSL2/Ubuntu si tu es sous Windows.
2. Installer les dépendances Buildozer.
3. Dans ce dossier :
   buildozer -v android debug
4. L'APK sera généré dans le dossier `bin/`.

La base SQLite est enregistrée dans le dossier de données privé de l'application Android,
via `App.user_data_dir`, donc elle n'est pas placée dans un chemin Windows.
