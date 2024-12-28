# BPSKmodulation
programme télécom qui simule une modulation numérique de phase phase shift key modulation 

La modulation par décalage de phase (Phase Shift Keying, PSK) est une technique de modulation numérique qui modifie la phase d'une porteuse pour représenter les données numériques. Il existe plusieurs types de PSK, tels que BPSK (Binary Phase Shift Keying), QPSK (Quadrature Phase Shift Keying), et d'autres variantes plus complexes.

Pour illustrer cela, nous allons écrire un programme en Python qui simule la modulation BPSK, qui est la forme la plus simple de PSK. Nous utiliserons des bibliothèques comme NumPy pour les calculs numériques et Matplotlib pour la visualisation.

Exemple de Code
Prérequis
Installer les bibliothèques nécessaires :
pip install numpy matplotlib

Explications
Importation des Bibliothèques :

numpy pour les calculs numériques.
matplotlib.pyplot pour la visualisation.
Fonction bpsk_modulation :

Prend en entrée une séquence de bits, la fréquence de la porteuse, le taux d'échantillonnage et la durée de chaque bit.
Crée un vecteur de temps t pour la durée totale du signal.
Génère une porteuse cosinus.
Modifie la phase de la porteuse en fonction des bits : un bit 0 inverse la phase (multiplie par -1), un bit 1 conserve la phase.
Retourne le vecteur de temps et le signal modulé.
Fonction main :

Définit les paramètres de la simulation : séquence de bits, fréquence de la porteuse, taux d'échantillonnage, et durée de chaque bit.
Appelle la fonction bpsk_modulation pour générer le signal modulé.
Affiche le signal modulé en utilisant Matplotlib.
Utilisation
Exécutez le script Python.
Le programme affichera le signal modulé BPSK correspondant à la séquence de bits spécifiée.
Ce programme fournit une simulation de base de la modulation BPSK en Python, avec une visualisation du signal modulé. Vous pouvez ajuster les paramètres et la séquence de bits pour explorer différents scénarios de modulation.
