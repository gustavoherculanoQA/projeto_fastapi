from binascii import Error
from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel, ValidationError


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
    # Fecha a conexao com o banco de dados
    cursor.close()
    conexao.close()
    return {"users": resultados}

@app.get("/user/details/{id_user}")
def user_details(id_user: int):
    # conexao com o banco de dado
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='micklindo',
        database='poc_api_php'
    )
    cursor = conexao.cursor(dictionary=True)
    # Consulta segura usando parâmetros
    cursor.execute("SELECT * FROM poc_api_php.users WHERE id = %s", (id_user,))
    resultado = cursor.fetchone()
    # Fecha a conexao com o bamco de dados
    cursor.close()
    conexao.close()
    if resultado:
        return resultado
    else:
        return {"error": "Usuário não encontrado"}, 404

@app.delete("/user/delete/{id_user}", status_code=200)
def delete_user(id_user: int):
    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='micklindo',
        database='poc_api_php'
    )
    cursor = conexao.cursor()
    try:
        cursor.execute("DELETE FROM poc_api_php.users WHERE id = %s", (id_user,))
        conexao.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"detail": "Usuário apagado com sucesso"}
    finally:
        cursor.close()
        conexao.close()

#Essa misera vai fazer a validacao dos dados com base nesse modelo
class User(BaseModel):
    name: str
    email: str
    password: str

@app.post("/user/create", status_code=201)
def create_user(user: User):
    try:
        # Conexão com o banco de dados MySQL
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='micklindo',
            database='poc_api_php'
        )
        if conexao.is_connected():
            cursor = conexao.cursor()
            
            if not user.name or not user.email or not user.password:
             raise HTTPException(
            status_code=400,
            detail="Os campos 'name', 'email' e 'password' são obrigatórios e não podem estar vazios."
        )

            # Verificar se o nome já existe
            cursor.execute("SELECT COUNT(*) FROM users WHERE name = %s", (user.name,))
            name_exists = cursor.fetchone()[0]

            # Verificar se o email já existe
            cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (user.email,))
            email_exists = cursor.fetchone()[0]

            if name_exists > 0:
                raise HTTPException(status_code=400, detail="Nome já está em uso meu queridão, tente outro ")
            if email_exists > 0:
                raise HTTPException(status_code=400, detail="Email já está em uso, sei que voce gosta desse email, mas não vai dar não :( ")

        if conexao.is_connected():
            cursor = conexao.cursor()

            # Inserção dos dados do usuário
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            values = (user.name, user.email, user.password)

            cursor.execute(query, values)
            conexao.commit()

            return {"message": "Usuário criado com sucesso!"}
        
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar ao banco de dados: {e}")
    finally:
        if conexao.is_connected():
            cursor.close()
            conexao.close()
    