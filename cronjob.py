import os
import django

from application.services.notification_service import NotificationService

django.setup()

from driven.db.notification.mapper import NotificationDBMapper
from driven.db.user.adapter import UserDBRepositoryAdapter
from driven.db.user.mapper import UserDBMapper
from application.services.mail_services import MailServices
from driven.mail.mail_repository_adapter import MailRepositoryAdapter
from driven.db.mail.adapter import MailDBRepositoryAdapter
from driven.db.ticket.adapter import TicketDBRepositoryAdapter
from driven.db.ticket.mapper import TicketDBMapper
from driving.mails.adapter import MailsAdapter
from driven.firebase.adapter import FirebaseRepositoryAdapter
from driven.db.notification.adapter import NotificationDBRepositoryAdapter
import time


def run_cronjob():
    print("Starting cronjob...")

    mail_repository_adapter = MailRepositoryAdapter()
    ticket_db_repository_adapter = TicketDBRepositoryAdapter(mapper=TicketDBMapper())
    mail_db_repository_adapter = MailDBRepositoryAdapter()
    firebase_repository_adapter = FirebaseRepositoryAdapter()
    user_mapper = UserDBMapper()
    notification_repository_adapter = NotificationDBRepositoryAdapter(mapper=NotificationDBMapper(user_mapper=user_mapper))
    user_repository_adapter = UserDBRepositoryAdapter(mapper=user_mapper)

    notification_service = NotificationService(notification_db=notification_repository_adapter,
                                               firebase=firebase_repository_adapter)

    service = MailServices(mail_repository=mail_repository_adapter,
                           ticket_db_repository=ticket_db_repository_adapter,
                           mail_db_repository=mail_db_repository_adapter,
                           user_db_repository=user_repository_adapter,
                           notification_service=notification_service)

    adapter = MailsAdapter(service=service)
    adapter.schedule_jobs()

    # Simular ejecución periódica
    while True:
        print("Cronjob is running...")
        time.sleep(10)


if __name__ == "__main__":
    run_cronjob()
