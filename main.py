from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient, ASCENDING, DESCENDING
#from pymongo.server_api import ServerApi
import os
import json 
import ast
from datetime import datetime, time
import requests

ARDUINO_IP = ""

uri = "mongodb+srv://rrddamazio:vQ4lM2M1zErxlIFY@bdprojfinalmic.rgwiall.mongodb.net/?retryWrites=true&w=majority&appName=bdProjFinalMic"
cliente = MongoClient(uri, 27017)
'''
try:
    cliente = MongoClient(uri, 27017)
    banco = cliente["banco_proj_final"]
    colecaoBandejao = banco["bandejao"]
    print("Conexão estabelecida com sucesso.")
    for doc in colecaoBandejao.find():
        print(doc)
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
'''

banco = cliente["banco_proj_IOT"]

colecaoBandejao = banco["bandejao"]

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 #limite de 16mb
print(app.config)
# nome, cpf, curso, foto            

@app.route("/", methods = ["GET", "POST"]) #mudado
@app.route("/index.html", methods = ["GET", "POST"])
def menu():    
    lPessoas = []
        
    for aluno in colecaoBandejao.find():
        lPessoas.append(aluno)
    
    return render_template("index.html", lPessoas = lPessoas)

@app.route("/favicon.ico", methods = ["GET", "POST"]) #mudado
@app.route("/index/favicon.ico.html", methods = ["GET", "POST"])
def favico():
    return redirect(url_for("menu"))

@app.route("/cadastramento.html", methods = ["GET", "POST"]) #mudado
def cadastra():
    lCadastro = ["", "", "", ""]
    if request.method == "POST":
        nome = request.form.get("fNome")
        cpf = request.form.get("fcpf")
        saldo = request.form.get("fsaldo")
        senha = request.form.get("fsenha")
        #foto = request.files.get("fFoto")

        ind = colecaoBandejao.find_one({"cpf" : cpf})
        print(ind)
        print(type(ind))

        if ind != None:           
            lCadastro[0] = nome
            lCadastro[1] = cpf
            lCadastro[2] = saldo
            lCadastro[3] = senha
            return render_template("cadastramento.html", error = True, lCadastro = lCadastro)
        
        else:
            colecaoBandejao.insert_one({"nome":nome, "cpf" : cpf, "saldo" : saldo, "senha" : senha, "uid" : ""})
        return redirect(url_for("menu"))
    else:
        return render_template("cadastramento.html", lCadastro = lCadastro)
    
@app.route("/exclui/<num>.html", methods = ["GET", "POST"]) #mudado
def exclui(num):  
    colecaoBandejao.delete_one({"cpf" : num})
    return redirect(url_for("menu"))
    
@app.route("/edita/<num>.html", methods = ["GET", "POST"]) #mudado
def edita(num):
    print("entrei na edita")
    print(num)
    aluno = colecaoBandejao.find_one({"cpf" : num})
    print(aluno)
    lEdita = ["", "", ""]
    lEdita[0] = aluno["nome"]
    lEdita[1] = aluno["saldo"]
    print(lEdita[0])

    if request.method == "POST":
        nome = request.form.get("fNome")
        saldo = request.form.get("fsaldo")
        
        print({"cpf" : num}, {"nome": nome, "saldo" : saldo})
        colecaoBandejao.update_one({"cpf" : num}, {"$set":{"nome": nome, "saldo" : saldo}})
        print("dentro")
        return redirect(url_for("menu"))
    #return redirect(url_for("edita", lEdita = lEdita, num = num, turma = turma))
    print(lEdita)
    return render_template("edita.html", lEdita = lEdita, num = num)

#if __name__ == '__main__':
app.run(port=5002, debug=False)