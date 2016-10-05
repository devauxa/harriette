Welcome to Harriette !
===================

Harriette est un programme permettant de détecter la présence d'utilisateur en fonction de leur présence sur un wifi.

Il utilise Jarvis pour la voix, et des scripts ad-hoc pour les modules porte/lumière

Si vous faites partie des administrateurs, vous serez contacter par mail lors d'une détection d'un utilisateur, vous pouvez donc accepter ou non l'ouverture de la porte

----------



Installation
-------------

- `cp install.sh.template install.sh`
- editer les CHANGEME dans install.sh
- `sh install.sh`
- ajouter des users dans user.json
- N'oublier pas de mettre en ip static vos users


Configuration
-------------

#### Utilisateur
> **user.json:**

> Contient une liste d'utilisateur avec pour format
> - **mac** :  "adresse mac"
> - **ip** : "adresse ip static"
> - **name** : liste de nom de l'utilisateur (utilisé aléatoirement par harriette)
> - **tel** : "téléphone" (si présent, l'utilisateur est considéré comme **admin**) [TODO]
> - **email** : "email" (si présent, l'utilisateur est considéré comme **admin**))

#### Config
> **config.json:**

> Contient un dictionnaire de config avec pour format
> - **lang** :  "la langue d'harriette"
> - **light** : "le path du binaire permettant une gestion des lumières"
> - **light_info** : "le path du binaire permettant d'avoir les informations des lumières"
> - **door** : "le path du binaire permettant une ouverture de la porte"
> - **jarvis** : "le path du binaire de [jarvis](https://github.com/alexylem/jarvis))

#### Langage
> **lang.json:**

> Contient la langue d'harriette

Autre
-------------
Un exemple de ces scripts sont dans le dossier script
#### Porte

Script permettant l'ouverture d'une porte

#### Lumière
##### light.py
Gestion de la lumière avec comme paramètre l'intensité souhaité (0 ou 100)
##### info.py
Retourne un json avec les informations des lumières
#### Jarvis
voir [Jarvis](https://github.com/alexylem/jarvis)

----------

TODO
-------------

| Tache     | Importance | Info   |
| :------- | :----: | :--- |
| Sécurité     | 100    |  Interdit la tentative de connexion avec des ip/mac differente |
| SMS    | 20   |  Utilisation d'sms en plus de l'envois de mail pour la l'ouverture   |
| Camera    | 2   |  Ajout des cameras dans le mail   |
| Fix jarvis | 1 |  Problème lorsque l'on veux parler exactement en même temps (use queue)  |
