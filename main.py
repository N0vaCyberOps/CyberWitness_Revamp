import configparser
import logging
import json
import asyncio
import aiosqlite
from tenacity import retry, stop_after_attempt, wait_exponential
from traffic_monitor import AdvancedTrafficMonitor

def setupLogging():
    """Set up logging with default configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename='cyber_witness.log'
    )

class DatabaseHandler:
    """Asynchronous handler for SQLite database operations."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = None

    async def connect(self) -> None:
        """Establish database connection."""
        self.db = await aiosqlite.connect(self.db_path)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def execute_query(self, query: str, params: tuple = None) -> None:
        """Execute a database query with retry mechanism."""
        async with self.db as db:
            if params:
                await db.execute(query, params)
            else:
                await db.execute(query)
            await db.commit()

    async def fetch_all(self, query: str, params: tuple = None) -> list:
        """Fetch all results from a query."""
        async with self.db as db:
            cursor = await db.execute(query, params)
            return await cursor.fetchall()

    async def close(self) -> None:
        """Close database connection."""
        if self.db:
            await self.db.close()

class AlertCoordinator:
    """Coordinator for managing alerts with priority queues."""

    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler
        self.high_priority_queue = asyncio.Queue()
        self.low_priority_queue = asyncio.Queue()

    async def add_alert(self, alert_data: dict, priority: str = 'low') -> None:
        """Add alert to appropriate queue based on priority."""
        alert_data['priority'] = priority
        if priority == 'high':
            await self.high_priority_queue.put(alert_data)
            await self.process_alert(alert_data)
        else:
            await self.low_priority_queue.put(alert_data)

    async def process_alert(self, alert_data: dict) -> None:
        """Process and log alert to database."""
        query = "INSERT INTO alerts (data, priority) VALUES (?, ?)"
        await self.db_handler.execute_query(query, (json.dumps(alert_data), alert_data['priority']))

    async def background_processing(self) -> None:
        """Background task for processing low priority alerts."""
        while True:
            try:
                alert_data = await self.low_priority_queue.get()
                await self.process_alert(alert_data)
                self.low_priority_queue.task_done()
            except Exception as e:
                logging.error(f"Error processing low priority alert: {str(e)}")
            await asyncio.sleep(1)

async def main():
    """Main asynchronous function to run the application."""
    config = configparser.ConfigParser()
    config.read('config.ini')

    try:
        setupLogging()
        logging.info("Starting Cyber Witness: Network Sniffer")

        db_path = config.get('database', 'database_file')
        db_handler = DatabaseHandler(db_path)
        await db_handler.connect()

        alert_coordinator = AlertCoordinator(db_handler)
        background_task = asyncio.create_task(alert_coordinator.background_processing())

        interface = config.get('network', 'interface', fallback='')
        traffic_monitor = AdvancedTrafficMonitor(interface, alert_coordinator)
        await traffic_monitor.start_monitoring()

        while True:
            await asyncio.sleep(1)
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        logging.error(f"Configuration error: {str(e)}")
        return 1
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return 1
    finally:
        if 'background_task' in locals():
            background_task.cancel()
        if 'traffic_monitor' in locals():
            await traffic_monitor.stop_monitoring()
        if 'db_handler' in locals():
            await db_handler.close()
        logging.info("Cyber Witness shutdown completed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
        sys.exit(0)