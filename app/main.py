from flask import Flask, render_template, request
from weasyprint import HTML
import io
from flask_sqlalchemy import SQLAlchemy

from .models import User
from . import create_app

#my packages
from subprocessUtils.subprocess import * #for  subprocess handling
from parsing.whoisParsing import * #to parse whois output
from parsing.nmapParsing import * #to parse nmap
from commandsFunctions.ipFunction import * #logique when only ip is provide
from database.database import * #for db SQLite operations


#fontion for IA
from ai.ai import getResponseFromAI

#obtenir le chemin de la base de données


app = create_app()

# initialisation de la base de données
init_db() # ceci est ma fonction pour créer les tables si elle n'existe pas
insertBuiltinTools() # insérer les outils par défaut dans la base de données








if __name__ == "__main__":
    app.run(debug=True)

