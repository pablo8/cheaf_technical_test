import os
import subprocess
import time

def run_command(command, wait=True, capture_output=False):
    """Ejecuta un comando en la terminal y muestra su salida en tiempo real."""
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None,
        text=True
    )

    if wait and capture_output:  # Captura y muestra la salida en tiempo real
        for line in process.stdout:
            print(line, end='')
        for line in process.stderr:
            print(line, end='')
        process.wait()

    return process  # Retorna el proceso si no queremos esperar

def run_simulation():
    print("🧹 Limpiando Base de Datos...")
    run_command("python xscripts/clean_db.py", capture_output=True)
    run_command("python xscripts/populate_db.py", capture_output=True)

    print("🚀 Iniciando Redis en Docker...")
    run_command("docker start redis-server", capture_output=True)

    print("📡 Iniciando Celery Worker en segundo plano...")
    celery_worker = run_command("celery -A apps.core worker --pool=solo --loglevel=info", wait=False)

    time.sleep(5)  # Espera para asegurar que Celery se inicie correctamente

    print("🔄 Ejecutando Simulación...")
    run_command("celery -A apps.core call apps.alerts.tasks.simulate_notifications", capture_output=True)

    print("✅ Simulación Finalizada. Limpiando Celery...")
    run_command("celery -A apps.core purge", capture_output=True)

    print("🔁 Reiniciando Base de Datos para otra prueba...")
    run_command("python xscripts/clean_db.py", capture_output=True)
    run_command("python xscripts/populate_db.py", capture_output=True)

    print("🔥 Todo listo para una nueva simulación.")

    print("🛑 Deteniendo Celery Worker...")
    celery_worker.terminate()  # Detenemos Celery Worker


if __name__ == "__main__":
    run_simulation()
