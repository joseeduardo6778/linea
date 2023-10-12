from pymongo import MongoClient
import certifi

MONGO= 'mongodb+srv://VictorR:gUsah8Myag0rAHcj@cluster0.96qc520.mongodb.net/?retryWrites=true&w=majority'
certificado = certifi.where()

def conexion():
    try:
        client = MongoClient(MONGO, tlsCAFile=certificado)
        bd = client["caso_uso"]
    except ConnectionError:
        print('Error de Conexión')
    return bd 