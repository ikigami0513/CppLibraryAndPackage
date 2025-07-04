import PyInstaller.__main__

PyInstaller.__main__.run([
    'clap_cli/main.py',          # Chemin vers ton point d'entrée
    '--name=clap',               # Nom de l'exécutable généré
    '--onefile',                 # Tout dans un seul exécutable
    '--console',                 # Affiche la console (utile pour un CLI)
    '--clean',                   # Nettoie les anciens builds
])
