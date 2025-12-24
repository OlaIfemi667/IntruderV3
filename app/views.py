from flask import Blueprint, render_template, request, flash, redirect, url_for
from datetime import datetime
import threading
import os
import io
import sqlite3

from . import db
from .models import Scan
from flask_login import login_required, current_user
from database.database import *
from weasyprint import HTML
from parsing.nmapParsing import convertTuples, isIP
from ai.ai import getResponseFromAI
from commandsFunctions.ipFunction import *

base_dir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(base_dir, '..', 'database.db')

views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home")
@login_required
def index():
    return render_template("index.html", user=current_user)


@views.route("/home/scans")
@login_required
def scans():
    # Utilise  le modèle SQLAlchemy Scan pour récupérer les scans de l'utilisateur
    user_scans = Scan.query.filter_by(userId=current_user.id).order_by(Scan.date.desc()).all()
    scan_names = [scan.scanName for scan in user_scans]

    # Statut simple basé sur la présence des résultats dans PROCESSES
    statuses = {}
    for s in user_scans:
        status = getScanStatus(s.scanName, current_user.id)
        if status == "finished":
            label = "Terminé"
        elif status == "running":
            label = "En cours"
        elif status == "pending":
            label = "En attente"
        else:
            label = "Inconnu"
        statuses[s.scanName] = label

    return render_template("scans.html", content=scan_names, statuses=statuses, user=current_user)

@views.route("/home/newscan", methods=['POST', 'GET'])
@login_required
def newScan():
    if request.method == "POST":
        ip = request.form.get("target")
        scanName = request.form.get("scanName") 
        if not ip:
            flash("L'adresse IP cible est requise.", category='error')
            return redirect(url_for('views.newScan'))

        if not isIP(ip):
            flash("Format d'adresse IP invalide.", category='error')
            return redirect(url_for('views.newScan'))

        
        if checkScanExists(scanName, DB_PATH):
            flash(f"Un scan nommé {scanName} existe déjà.", category='error')
            return redirect(url_for('views.newScan'))

        flash(f"Scan {scanName} créé avec succès. Le scan est en cours, consulte l'historique pour suivre les résultats.", category='success')


        # Capture les valeurs AVANT de quitter le contexte Flask
        # parce que si j'avais utilisé current_user.zapApi directement dans la fonction ipAi,
        # il aurait été vide car le contexte Flask n'est plus actif.
        user_id = current_user.id
        zap_api = current_user.zapApi

        threading.Thread(
            target=lambda: asyncio.run(ipAi(ip, scanName, "", user_id, zap_api))
        ).start()
        print(f"view {target}")
        return redirect(url_for('views.scanDetail', scanName=scanName))
    return render_template("newscan.html", user=current_user)

@views.route("/home/scans/<scanName>", methods=['POST', 'GET'])
@login_required
def scanDetail(scanName):
    scanDetail = getScansDetails(DB_PATH, scanName, current_user.id)
    scanDetail = convertTuples(scanDetail)
    apiKey = current_user.groqApi if current_user.groqApi else None
    if request.method == 'POST':
        if "asking" in request.form:
            print("Form submitted")
            question = request.form.get("iaInput")
            print(apiKey)
            response = getResponseFromAI(question, scanDetail, apiKey)
            return render_template("scanBase.html", scan=scanName, scansContent=scanDetail, response=response, question=question, user=current_user)
    return render_template("scanBase.html", scan = scanName, scansContent = scanDetail, user=current_user)

@views.route("/home/scans/<scanName>/export")
@login_required
def export_report(scanName):
    ##on converti en pdf grace a l'objet HTML de weasyprint
    scanDetail = getScansDetails(DB_PATH, scanName, current_user.id)
    scanDetail = convertTuples(scanDetail)
    

    html_content = render_template("report.html", scan=scanName, scansContent=scanDetail, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"))
    pdf_file = HTML(string=html_content).write_pdf()
    return io.BytesIO(pdf_file), 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename="{scanName}_report.pdf"'
    }

@views.route("/home/docs")
def documentation():
    return render_template("documentation.html", user=current_user)


@views.route("/home/scans/<scanName>/delete", methods=["POST"])
@login_required
def delete_scan(scanName):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Ne supprime que les données appartenant à l'utilisateur courant
        cursor.execute(
            "DELETE FROM PROCESSES WHERE nameScan = ? AND userId = ?",
            (scanName, current_user.id),
        )
        cursor.execute(
            "DELETE FROM SCANS WHERE scanName = ? AND userId = ?",
            (scanName, current_user.id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for('views.scans'))
    except Exception as e:
        return f"Error deleting scan: {e}"


@views.route("/home/scans/delete_all", methods=["POST"])
@login_required
def delete_all_scans():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Ne supprime que les scans de l'utilisateur courant
        cursor.execute("DELETE FROM PROCESSES WHERE userId = ?", (current_user.id,))
        cursor.execute("DELETE FROM SCANS WHERE userId = ?", (current_user.id,))
        conn.commit()
        conn.close()
        return redirect(url_for('views.scans'))
    except Exception as e:
        return f"Error deleting all scans: {e}"



