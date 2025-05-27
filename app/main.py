from flask import Flask, render_template, request
import os
from weasyprint import HTML
import io


#my packages
from subprocessUtils.subprocess import * #for  subprocess handling
from parsing.whoisParsing import * #to parse whois output
from parsing.nmapParsing import * #to parse nmap
from commandsFunctions.ipFunction import * #logique when only ip is provide
from database.database import * #for db SQLite operations

#fontion for IA
from ai.ai import getResponseFromAI



app = Flask(__name__)
init_db()
base_dir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(base_dir, '..', 'database.db')


@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/home/scans")
def scans():
    scans = getScans(DB_PATH)
    return render_template("scans.html", content = scans )


@app.route("/home/scans/<scanName>", methods=['POST', 'GET'])
def scanDetail(scanName):
    scanDetail = getScansDetails(DB_PATH, scanName)
    scanDetail = convertTuples(scanDetail)

    
    return render_template("scanBase.html", scan = scanName, scansContent = scanDetail)

@app.route("/home/scans/<scanName>/reporting")
def reporting(scanName):
    return render_template("reportingBase.html", scan=scanName)

@app.route("/home/scans/<scanName>/reporting/export")
def export_report(scanName):
    scanDetail = getScansDetails(DB_PATH, scanName)
    scanDetail = convertTuples(scanDetail)
    

    html_content = render_template("scanBase.html", scan=scanName, scansContent=scanDetail)
    pdf_file = HTML(string=html_content).write_pdf()
    return io.BytesIO(pdf_file), 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename="{scanName}_report.pdf"'
    }

@app.route("/home/reports")
def reports():
    return render_template("reportsBase.html")


@app.route("/home/docs")
def documentation():
    return render_template("documentation.html")

if __name__ == "__main__":
    app()

