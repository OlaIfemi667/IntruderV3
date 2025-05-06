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
    return "TEst"


if __name__ == "__main__":
    app()
