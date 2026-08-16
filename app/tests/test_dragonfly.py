import redis

# Como el script corre dentro de Docker (o puedes cambiarlo a 'localhost' si lo corres directo en tu máquina)
# Si lo pruebas desde fuera de Docker usa 'localhost', si está dentro de la red del compose usa 'dragonfly'
HOST = "dragonfly"
PORT = 6379

def test_dragonfly_connection():
    print(f"[*] Conectando a Dragonfly ({HOST}:{PORT})...")
    
    try:
        # Inicializar cliente de Redis (Dragonfly es 100% compatible con el protocolo Redis)
        r = redis.Redis(host=HOST, port=PORT, decode_responses=True)
        
        # Probar ping
        if r.ping():
            print("[+] ¡Conexión exitosa a Dragonfly!")
            
        # Prueba de escritura
        key = "test_key"
        value = "¡Hola desde Dragonfly y Python!"
        r.set(key, value)
        print(f"[+] Dato guardado -> Clave: '{key}', Valor: '{value}'")
        
        # Prueba de lectura
        retrieved_value = r.get(key)
        print(f"[+] Dato recuperado -> Valor: '{retrieved_value}'")
        
        # Limpieza opcional
        r.delete(key)
        print("[+] Clave de prueba eliminada correctamente.")
        
    except Exception as e:
        print(f"[X] Error al conectar o interactuar con Dragonfly: {e}")

if __name__ == "__main__":
    test_dragonfly_connection()