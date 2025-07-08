from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask_login import login_user, login_required, logout_user, current_user
from database.database import *
from weasyprint import HTML
import io
import os
from parsing.nmapParsing  import convertTuples, isIP
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
    scans = getScans(DB_PATH, current_user.id)
    return render_template("scans.html", content = scans, user=current_user)

@views.route("/home/newscan", methods=['POST', 'GET'])
@login_required
def newScan():
    if request.method == "POST":
        
        target = request.form.get("target")
        scanName = request.form.get("scanName")  # Default scan name if not provided
        if not target:
            flash("Target IP address is required.", category='error')
            return redirect(url_for('views.newScan'))

        if not isIP(target):
            flash("Invalid IP address format.", category='error')
            return redirect(url_for('views.newScan'))

        
        if checkScanExists(scanName, DB_PATH):
            flash(f"Scan with name {scanName} already exists.", category='error')
            return redirect(url_for('views.newScan'))

        flash(f"Scan {scanName} created successfully.", category='success')
        
        return redirect(url_for('views.scanDetail', scanName=scanName)), asyncio.run(ipAi(target, scanName, "", current_user.id))
    return render_template("newscan.html", user=current_user)

@views.route("/home/scans/<scanName>", methods=['POST', 'GET'])
@login_required
def scanDetail(scanName):
    scanDetail = getScansDetails(DB_PATH, scanName)
    scanDetail = convertTuples(scanDetail)

    if request.method == 'POST':
        if "asking" in request.form:
            print("Form submitted")
            question = request.form.get("iaInput")
            response = getResponseFromAI(question, scanDetail)
            return render_template("scanBase.html", scan=scanName, scansContent=scanDetail, response=response, question=question)
    return render_template("scanBase.html", scan = scanName, scansContent = scanDetail, user=current_user)

""" @app.route("/home/scans/<scanName>/reporting")
def reporting(scanName):
    return render_template("reportingBase.html", scan=scanName) """

@views.route("/home/scans/<scanName>/export")
@login_required
def export_report(scanName):
    scanDetail = getScansDetails(DB_PATH, scanName)
    scanDetail = convertTuples(scanDetail)
    

    html_content = render_template("scanBase.html", scan=scanName, scansContent=scanDetail)
    pdf_file = HTML(string=html_content).write_pdf()
    return io.BytesIO(pdf_file), 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename="{scanName}_report.pdf"'
    }

""" @app.route("/home/reports")
def reports():
    return render_template("reportsBase.html") """


@views.route("/home/docs")
def documentation():
    return render_template("documentation.html", user=current_user)


@views.route("/home/scans/<scanName>/delete", methods=["POST"])
@login_required
def delete_scan(scanName):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PROCESSES WHERE nameScan = ?", (scanName,))
        cursor.execute("DELETE FROM SCANS WHERE scanName = ?", (scanName,))
        conn.commit()
        conn.close()
        return render_template("scans.html", content=getScans(DB_PATH), user=current_user)
    except Exception as e:
        return f"Error deleting scan: {e}"


@views.route("/home/scans/delete_all", methods=["POST"])
@login_required
def delete_all_scans():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PROCESSES")
        cursor.execute("DELETE FROM SCANS")
        conn.commit()
        conn.close()
        return render_template("scans.html", content=getScans(DB_PATH), user=current_user)
    except Exception as e:
        return f"Error deleting all scans: {e}"
