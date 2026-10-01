# Réponses

1.

Pour créer une station, il faut utiliser POST avec le code HTTP 201 Created**.

2.

Si la station n'existe pas, il faut renvoyer le code 404 Not Found avec un message indiquant que la station n'a pas été trouvée.

3.

401 signifie que l'utilisateur n'est pas authentifié, tandis que 403 signifie qu'il est authentifié mais n'a pas les droits nécessaires.
Exemple : 401 sans connexion, 403 pour un utilisateur connecté qui n'a pas accès à une ressource.
