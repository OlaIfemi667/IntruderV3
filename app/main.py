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

    if request.method == 'POST':
        if "asking" in request.form:
            print("Form submitted")
            question = request.form.get("iaInput")
            response = getResponseFromAI(question, scanDetail)
            return render_template("scanBase.html", scan=scanName, scansContent=scanDetail, response=response, question=question)
    return render_template("scanBase.html", scan = scanName, scansContent = scanDetail)

""" @app.route("/home/scans/<scanName>/reporting")
def reporting(scanName):
    return render_template("reportingBase.html", scan=scanName) """

@app.route("/home/scans/<scanName>/export")
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


@app.route("/home/docs")
def documentation():
    return render_template("documentation.html")


@app.route("/home/scans/<scanName>/delete", methods=["POST"])
def delete_scan(scanName):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PROCESSES WHERE nameScan = ?", (scanName,))
        cursor.execute("DELETE FROM SCANS WHERE scanName = ?", (scanName,))
        conn.commit()
        conn.close()
        return render_template("scans.html", content=getScans(DB_PATH))
    except Exception as e:
        return f"Error deleting scan: {e}"


@app.route("/home/scans/delete_all", methods=["POST"])
def delete_all_scans():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PROCESSES")
        cursor.execute("DELETE FROM SCANS")
        conn.commit()
        conn.close()
        return render_template("scans.html", content=getScans(DB_PATH))
    except Exception as e:
        return f"Error deleting all scans: {e}"



@app.route("/login")
def login():
    pass    

@app.route("/logout")
def logout():
    pass

@app.route("/register")
def register():
    pass


if __name__ == "__main__":
    app()

