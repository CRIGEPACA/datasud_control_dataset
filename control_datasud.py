#!/usr/bin/python
# -*- coding: utf-8 -*-


###### IMPORT DES DIFFERENTS MODULES ######

import sys
import os
import os, os.path as OP
import re
import json
import urllib
import csv
from datetime import datetime
import string

Now = datetime.now()
Now_w = str(Now.date())+"_"+str(Now.hour)+"-"+str(Now.minute)
Now_date = Now.date()

###### DOSSIER D'ENREGISTREMENT ET FICHIERS DE SORTIE #######

# Repertoires a créer si inexistants
dirScript = OP.abspath(OP.split(__file__)[0])
print dirScript
# dirSrc = "/DATA/fileadmin/opendata/_crawler"
# dirResult = dirScript +"//result_control"
dirResult ="/DATA/fileadmin/opendata/_control_datasud"
if not os.path.exists(dirResult):
    os.makedirs(dirResult)
dirLog = dirScript + "//log"
if not os.path.exists(dirLog):
    os.makedirs(dirLog)
	
# Fichier de log
pathFileLog = dirLog + "//log_%s.txt"%(Now_w)
fileLog = open(pathFileLog, "w")
fileLog.write("Lancement du script de controle le %s \n\nEcriture des fichiers csv \n\n" %(Now))

# Fichier de resultat en csv
	# csv : date publi, organisme, dataset
pathFileCsvOrga = dirResult+"//dataset_sans_orga.csv"
csvOrga = csv.writer(open(pathFileCsvOrga, "wb"), delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL )
	# csv : organisme, dataset, description
pathFileCsvDescr = dirResult+"//dataset_sans_description.csv"
csvDescr = csv.writer(open(pathFileCsvDescr, "wb"), delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL )
	# csv : dataset sans ressources
pathFileCsv0Ress = dirResult+"//dataset_sans_ressource.csv"
csv0Ress = csv.writer(open(pathFileCsv0Ress, "wb"), delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL )	
	# csv : ressources non opendata
pathFileCsvNoBrut = dirResult+"//dataset_sans_ressource_brute.csv"
csvNonBrut = csv.writer(open(pathFileCsvNoBrut, "wb"), delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL )	

# Fonction de récupération d'info d'un dataset
def controlDataset (url):
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	assert data["success"] is True
	dataset = str((data["result"]["title"]).encode('utf-8'))
	datepub = str((data["result"]["metadata_modified"]).encode('utf-8'))
	if data["result"]["organization"] is None :
		orga = "None"
		i_org=0
	else:
		orga = str((data["result"]["organization"]["title"]).encode('utf-8'))
		i_org=1
	if data["result"]["notes"] is None or data["result"]["notes"] =="":
		descr = "None"
		i_des=0
	else:
		descr = str((data["result"]["notes"]).encode('utf-8'))	
		i_des=1
	if data["result"]["num_resources"] ==0:
		i_nb_res = 0
		nb_res = 0
	else:
		i_nb_res = 1
		nb_res = data["result"]["num_resources"]
		format = []
		lstFormat = ["PDF","ODT","HTML","DOC","ZIP"]
		i_format=0
		for i in range(len(data["result"]["resources"])):
			form_res=str((data["result"]["resources"][i]["format"]).encode('utf-8'))
			for y in range(len(lstFormat)):
			    if form_res ==lstFormat[y]:
					i_format+=1
					format.append(form_res)
					pass		
		if i_format == nb_res:
			i_non_brut = 0
		else:
			i_non_brut = 1
	lst_orgdesc=[datepub,orga,dataset,descr]
	lst_nbres=[datepub,orga,dataset]
	lst_res=[datepub,orga,dataset,nb_res,format]
	return (i_org,i_des,i_nb_res,i_non_brut,lst_res,lst_nbres,lst_orgdesc)
	
def ecrit(liste,a,b,com,csv):
	if liste[a]==0:
		fileLog.write("	=>%s\n"%(com))
		lstLine=[]
		for i in range(len(liste[b])):
			lstLine.append(liste[b][i])
		csv.writerow(lstLine)
	
# Fonction ecriture de la ligne si manque d'infos
def Line4Csv(urlFix, URL):
	url = urlFix+URL
	fileLog.write(URL+"\n")
	repcontrol = controlDataset(url)
	print URL
	ecrit(repcontrol,0,-1,"manque organisation",csvOrga)
	ecrit(repcontrol,1,-1,"manque description",csvDescr)
	ecrit(repcontrol,2,-2,"manque ressource",csv0Ress)
	ecrit(repcontrol,3,-3,"manque format brut",csvNonBrut)
	
###### NOMBRE DE DATASET PAR GROUPE #######

fileLog.write ("\n\n#####	  Requetes  #####\n\n")
print "\n\n#####	  Requetes   #####\n\n"

# Récupération de la liste des dataset
urlAPI_listDataset="http://trouver.datasud.fr/api/3/action/package_list"
fileLog.write("Récupération de la liste des dataset grace à la requete de l'API : \n%s\n\n"%(urlAPI_listDataset))
repAPI_listDataset = urllib.urlopen(urlAPI_listDataset)
dataAPI_listDataset=json.loads(repAPI_listDataset.read())
assert dataAPI_listDataset["success"] is True
API_listDataset = dataAPI_listDataset["result"]

# Ecriture de l'entete des csv
entOrga = ['Derniere MAJ du dataset','Organisation','Dataset','Description']
csvOrga.writerow(entOrga)
entDescr = ['Derniere MAJ du dataset','Organisation','Dataset','Description']
csvDescr.writerow(entDescr)
ent0Ress = ['Derniere MAJ du dataset','Organisation','Dataset']
csv0Ress.writerow(ent0Ress)
entNonBrut = ['Derniere MAJ du dataset','Organisation','Dataset','Nombre de ressources','Liste des formats']
csvNonBrut.writerow(entNonBrut)


urlAPI_dataset = "https://trouver.datasud.fr/api/3/action/package_show?id="

for i in range(len(API_listDataset)):
# for i in range(20):
	Line4Csv(urlAPI_dataset,API_listDataset[i])
	
###### ENREGISTREMENT DES FICHIERS #########
fileLog.close()
