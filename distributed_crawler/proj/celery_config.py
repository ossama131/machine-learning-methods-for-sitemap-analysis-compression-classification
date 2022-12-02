import logging

from celery import Celery
from celery.signals import after_setup_logger

# Init celery app
app = Celery(
    'proj',
    broker='amqp://crawler:crawler@localhost:5672/crawler_vhost',
    include=['proj.tasks']
)


# Update cerly app config
app.conf.update(
    timezone='Europe/Berlin',
    enable_utc=True,
    broker_pool_limit=256,
    worker_prefetch_multiplier=100,
)


logger = logging.getLogger(__name__)

@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # FileHandler
    fh = logging.FileHandler('crawler_logs.log')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

if __name__ == '__main__':
    app.start()
