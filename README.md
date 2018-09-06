# datasud_control_dataset
Administration des données publiées sur Datasud

Le script control_datasud.py interroge l'API CKAN de Datasud.fr pour repérer les datasets publiés sans description, sans ressources associées, sans ressources au format brut, et contrôle les ressources publiées en HTML ou ZIP.

Le paramétrage d'un cron quotidien pour faire fonctionner ce script permet de regénérer ces fichiers chaque jour. Ils sont déposés dans le dossier /opendata du SAN.

# results
Il génère un fichier de log et 5 fichiers csv :

* dataset_html_a_verifier.csv :: liste les datasets contenant uniquement des liens HTML et des descriptifs sous format texte -> Vérifier que le lien HTML mène directement à un extracteur ou la possibilité de télécharger le fichier brut ;
* dataset_sans_description.csv :: liste les datasets publiés sans description -> Contacter le producteur pour mettre à jour son dataset ; 
* dataset_sans_ressource.csv :: liste les datasets publiés sans aucune ressource -> Dépublier le jeu de données et contacter le producteur pour mettre à jour son dataset ; 
* dataset_sans_ressource_brute.csv :: liste les datasets publiés sans ressource "brute" mais uniquement avec des formats non exploitables par la plateforme : PDF, DOC, ODT, etc. -> Dépublier le jeu de données et contacter le producteur pour mettre à jour son dataset ; 
* dataset_zip_a_verifier.csv :: liste les datasets publiés contenant une ressource ZIP -> Vérifier que le format ne peut pas être mieux spécifié (SHP, GTFS, Neptune, MAPinfo) pour en améliorer l'indexation ; 
