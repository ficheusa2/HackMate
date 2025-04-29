# main.py
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from db.db_connector import fetch_users
from matcher.matcher import matching_algorithm

logging.basicConfig(level=logging.INFO)

async def batch_matching():
    logging.info("Ejecutando batch de matching...")
    users = fetch_users() 
    matches = matching_algorithm(users)
    # Aquí añadirás la lógica para guardar los matches en la base de datos
    logging.info(f"Matches encontrados: {matches}")

def main():
    scheduler = AsyncIOScheduler()
    # Programa la tarea para que se ejecute cada 60 minutos (3600 segundos)
    scheduler.add_job(batch_matching, 'interval', seconds=3600)
    scheduler.start()
    logging.info("Scheduler iniciado, el batch se ejecutará cada 60 minutos.")

    # Mantén el loop asíncrono corriendo
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()
