# datasud_control_dataset
Administration des données publiées sur Datasud.

Le script control_datasud.py interroge l'API CKAN de Datasud.fr pour repérer les dataset publiés sans organisme, sans description, sans ressources associées et sans ressources au format brut.
Il génère un fichier de log et 4 fichiers csv.

Le paramétrage d'un cron quotidien pour faire fonctionner ce script permet de regénérer ces fichiers chaque jour.
