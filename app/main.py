from flask import Flask, render_template, request


#my packages
from subprocessUtils.subprocess import * #for  subprocess handling
from parsing.whoisParsing import * #to parse whois output
from parsing.nmapParsing import * #to parse nmap
from commandsFunctions.ipFunction import * #logique when only ip is provide
from database.database import * #for db SQLite operations


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")


@app.route("/home/scans")
def scans():
    return render_template("scans.html")


@app.route("/home/scans/<scanName>")
def scanDetail(scanName):
    return render_template("scanBase.html")

@app.route("/home/scans/<scanName>/reporting")
def reporting(scanName):
    return render_template("reportingBase.html")



@app.route("/home/reports")
def reports():
    return render_template("reportsBase.html")


if __name__ == "__main__":
    app()
