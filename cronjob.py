import os
import time
import django
from application.services.mail_services import MailServices
from driven.mail.mail_repository_adapter import MailRepositoryAdapter
from driven.db.mail.adapter import MailDBRepositoryAdapter
from driven.db.ticket.adapter import TicketDBRepositoryAdapter
from driven.db.ticket.mapper import TicketDBMapper
from driving.mails.adapter import MailsAdapter

def run_cronjob():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.django.settings')
    django.setup()

    print("Starting cronjob...")

    mail_repository_adapter = MailRepositoryAdapter()
    ticket_db_repository_adapter = TicketDBRepositoryAdapter(mapper=TicketDBMapper())
    mail_db_repository_adapter = MailDBRepositoryAdapter()

    service = MailServices(mail_repository=mail_repository_adapter,
                           ticket_db_repository=ticket_db_repository_adapter,
                           mail_db_repository=mail_db_repository_adapter)

    adapter = MailsAdapter(service=service)
    adapter.schedule_jobs()

    # Simular ejecución periódica
    while True:
        print("Cronjob is running...")
        time.sleep(10)


if __name__ == "__main__":
    run_cronjob()
