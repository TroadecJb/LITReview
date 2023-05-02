# LITReview

## Objectif

Réaliser un MVP utilisant le framework Django.  
Le produit a pour but de permettre à une communauté d'échanger à propos de livres.  
Les utilisateurs pourront consulter ou demander des critiques les uns aux autres.
- - - 
## Environnement
### Installation:
 
- Clonez le repository sur votre machine.  
`git clone https://github.com/TroadecJb/LITReview.git`

- Accédez au répertoire.  
`$ cd /path/to/project/LITReview`


### Utilisation dans un environnement virtuel:
- Python >= 3.10.6
`$ python -m -venv <environment name>`

- activation windows  
`$ ~env\Scripts\activate.bat`  
- activation macos/linux  
`$ ~source env/bin/activate`

- From terminal  
 `python -m pip install -r requirements.txt`
- To run the program 
```
$ cd /path/to/folder/LITReview/LITReview
$ python manage.py makemigrations
$ python manage.py migrate
$ python -m manage.py runserver
```
- Accédez au site via votre navigateur à l'adresse http://127.0.0.1:8000/
- - - 
## Requirements
asgiref==3.6.0  
Django==4.2  
Pillow==9.5.0  
sqlparse==0.4.3  
- - - 
## Utilisateurs test
utilisateurs / mdp
- admin / sudoadmin
- user_1 / S3crets!
- user_2 / S3crets!
- user_3 / S3crets!
- user_4 / S3crets!

- - - 
Pour avoir une base de données vierge il suffit de supprimer le fichier `db.sqlite3`.  
Ensuite, comme indiqué plus haut:  
```
$ cd /path/to/folder/LITReview/LITReview
$ python manage.py makemigrations
$ python manage.py migrate
$ python -m manage.py runserver
```
Cela créera une nouvelle base de données vierge.
 
