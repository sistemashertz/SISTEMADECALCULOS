from supabase_client import supabase

def test_connection():
    try:
        response = supabase.table("usuarios").select("*").limit(1).execute()
        print("✅ Conexión exitosa.")
        print("Respuesta:", response.data)
    except Exception as e:
        print("❌ Error al conectar:", e)

test_connection()
