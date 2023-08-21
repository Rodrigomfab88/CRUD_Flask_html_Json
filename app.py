from flask import Flask, render_template, redirect, request, flash
import json
import ast

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rodrigo'

logado = False

@app.route('/', methods=['GET', 'POST'])
def home():
    global logado
    logado = False
    return render_template("login.html")

@app.route('/adm')
def admin():
    if logado == True:
        with open('usuarios.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)
        return render_template("admin.html", usuarios=usuarios)
    if logado == False:
        return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():

    global logado

    nome= request.form.get('nome')
    senha= request.form.get('senha')
    
    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)

        cont = 0
        for usuario in usuarios:
            cont += 1
            if nome == 'adm' and senha == '000':
                logado = True
                return redirect('/adm')

            if usuario['nome'] == nome and usuario['senha'] == senha:
                return render_template("usuario.html")
            
            if cont >= len(usuarios):
                flash("USUÁRIO INVÁLIDO")
                return redirect("/")
            
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user = []
    nome= request.form.get('nome')
    senha= request.form.get('senha')

    user = [
        {
            "nome": nome,
            "senha": senha
        }
    ]

    with open('usuarios.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
    
    usuarioNovo = usuarios + user

    with open('usuarios.json', 'w') as salvarTemp:
        json.dump(usuarioNovo, salvarTemp, indent=4)
    flash(F'{nome} CADASTRADO(A) COM SUCESSO!')   
    return redirect('/adm')

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuarioDelete')
    usuarioDicionario = ast.literal_eval(usuario)
    nome = usuarioDicionario['nome']
    with open('usuarios.json') as usuariosTemp:
        usuarioJson = json.load(usuariosTemp)
        for c in usuarioJson:
            if c == usuarioDicionario:
                usuarioJson.remove(usuarioDicionario)
                with open('usuarios.json', 'w') as usuariosDeletar:
                    json.dump(usuarioJson, usuariosDeletar, indent=4)

    flash(F'{nome} EXCLUIDO!')
    return redirect('/adm')
 
if __name__ in "__main__":
    app.run(debug=True)

    