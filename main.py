from fastapi import FastAPI
import mysql.connector

app = FastAPI()

@app.post("/token")
def token():
    return {
        "access_token": "teste_token",
        "type": "Bearer",
        "expires_in": "300",
        "refresh_token": "NaN"
    }

@app.get("/user/list")
def user_list():
    # conexao com o banco de dado
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='micklindo',
        database='poc_api_php'
    )
    cursor = conexao.cursor(dictionary=True)
    # consulta ao banco de dados
    cursor.execute("SELECT * FROM poc_api_php.users")
    resultados = cursor.fetchall()
    # Fecha a conexao com o bamco de dados
    cursor.close()
    conexao.close()
    return {"users": resultados}

