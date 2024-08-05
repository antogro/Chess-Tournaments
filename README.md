# Chess-Tournaments
Creation of a software for counting points and round results for a chess tournament


## Description
L'application de gestion de tournoi d'échec "Chess-Tournaments" permet au organisateur de pouvoir ajouter des joueurs dans une base de donné, puis la possiblité de créer des tournois ou les pairs seront assemblés pour les différents rounds et trié en fonction de leurs scores et ainsi avoir des adversaires adapté à leur niveau. Les tournois peuvent être mise sur pause, permettant le gestion de plusieur tournois en simultané.
Il est également possible de réaliser un rapport du tournoi sèlectionné, ou tout les rounds et les adversaire seront affiché, mais également la liste des joueurs rangé dans l'ordre des vainqueurs.


## Installation

Pour installer le projet, il faut cloner le repository, soit en utilisant la clé SSH, ou en téléchargeant le dossier zipper du repository. 
[lien du repository :](https://github.com/antogro/Chess-Tournaments.git)
**Pour chaque ligne de commande, veuillez appuyer sur Entrée après avoir collé le code dans l'invite de commande.**


### 1 - Git clone (cloner le repository)

Pour cloner le repository il va vous falloir ouvrir l'inviter de commande (CMD), si cette méthode n'est pas fonctionnel,
veuillez suivre l'étape du téléchargement du repository.
Puis Copier/Coller le bout de code suivant dans l'invité de commande.
```bash
git@github.com:antogro/Chess-Tournaments.git
```

Après clonage du repository, retournez dans votre invité de commande, puis positionnez-vous dans le dossier contenant l'application
    Pour cela, utilisez la commande suivante:
```bash
cd chess-tournaments
```

### 1 bis - Téléchargement du repository compressé (zipper)

[lien du repository :](https://github.com/antogro/Chess-Tournaments.git)
Télécharger le code grâce au lien du repository, en cliquant sur le bouton **<> Code** tout en haut de la page, puis sur **Download ZIP** ou **Télécharger le ZIP**
Ensuite, vous devrez extraire le document, ouvrir le dossier puis glisser le fichier dans le dossier sélectionné.



## Usage

### Etape 1: Installer Pyhton et créer son environnement virtuel

Il vous faut installer Python 3.12.4 ou plus pour faire fonctionner le programme.  
[Lien pour télécharger la dernière version de python](https://www.python.org/downloads/)

Pour créer votre environnement virtuel, il faut vous placer dans l'inviter de commande (CMD) ouvert précédement.
Pour cela utilisé la commance *cd*

```cd C:\Users\anton\Bureau\openclassroom\``` 

utilisez la commande suivante dans votre invité de commande pour créer votre environnement:

```bash
python -m venv env

```

Puis Activer votre environnement virtuelle:
```bash
env\scripts\activate
```


### Etape 2: Installer les packages
Les packages permettent un bon fonctionnement de l'application, ne les oubliez pas.
```bash
pip install -r requirements.txt
```

### Etape 3: Lancer l'application
- Enfin, pour lancer l'application,
lancez le programme avec la commande suivante:

```bash
python main.py
```
                        
Voilà votre programme est maintenant opérationnel, vous n'avez plus qu'à suivre les consignes.


## Exemple d'utilisation

Pour lancer l'application, il vous faut taper la commande suivante:

sur Window/mac

```bash
python -m chess
```
sur Linux
```bash
python3 -m chess
```

Après le lancement de l'application, il vous sera proposé 2 choix,

- Gestion des tournois
--> La gestion des tournois permet de créée des tournois (Nom, date de début, description, nombre de rounds, participant, lieu du tournoi), de générer des rapport, de continuer des tournois déjà créé, et d'afficher les liste de tout les tournois (en cours, en paused, ou fini).
- Gestion des joueurs
--> La gestion des joueurs permet de créer des joueurs (Nom et prénom, date de naissance, l'identifiant national d'échec), mais également d'affiché la liste des joueurs enregistrer par ordre alphabetique.


## Auteurs

- [@antogro](https://www.github.com/antogro)