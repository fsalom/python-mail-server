import re

from application.ports.driven.database.mail.db_repository import MailDBRepositoryPort
from application.ports.driven.database.notification.notification_repository import NotificationDBRepositoryPort
from application.ports.driven.database.ticket.db_repository import TicketDBRepositoryPort
from application.ports.driven.database.user.db_repository import UserDBRepositoryPort
from application.ports.driven.firebase.repository import FirebaseRepositoryPort
from application.ports.driven.mail.mail_repository_port import MailRepositoryPort
from application.ports.driving.mail_service_port import MailServicePort
from domain.notification import Notification
from domain.product import Product
from domain.ticket import Ticket


class MailServices(MailServicePort):
    def __init__(self,
                 mail_repository: MailRepositoryPort,
                 ticket_db_repository: TicketDBRepositoryPort,
                 mail_db_repository: MailDBRepositoryPort,
                 user_db_repository: UserDBRepositoryPort,
                 notification_db_repository: NotificationDBRepositoryPort,
                 firebase_repository: FirebaseRepositoryPort,
                 ):
        self.mail_repository = mail_repository
        self.ticket_db_repository = ticket_db_repository
        self.mail_db_repository = mail_db_repository
        self.notification_db_repository = notification_db_repository
        self.firebase_repository = firebase_repository
        self.user_db_repository = user_db_repository

    def process(self):
        mails = self.mail_repository.read()
        for mail in mails:
            ticket = self.analyze(content=mail.content, email=mail.email)
            self.ticket_db_repository.save(ticket)
            self.send_notification(mail.email)

    def send_notification(self, email: str):
        try:
            user = self.user_db_repository.get(email=email)
            if not user:
                raise ValueError(f"No user found with email: {email}")

            devices = list(self.notification_db_repository.get_devices(user))
            if not devices:
                return

            notification = Notification(
                title="Nuevo ticket",
                content="Estamos procesando tu nuevo ticket",
                created_by=user)

            if len(devices) > 1:
                self.firebase_repository.send_bulk_notification(
                    notification, [device.device_id for device in devices]
                )
            else:
                self.firebase_repository.send_single_notification(
                    notification, devices[0].device_id
                )

        except Exception as e:
            print(f"Error sending notification: {e}")

    def analyze(self, content: str, email: str):
        id_pattern = r"(FACTURA(?: SIMPLIFICADA)?(?:.*?)(\d{4}-\d{3}-\d{6}))"
        id_ticket = re.search(id_pattern, content)
        id_ticket = id_ticket.group(2) if id_ticket else "Número de factura no encontrado"
        # DATE
        date_pattern = r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2})"
        date = re.search(date_pattern, content)
        date = date.group(1) if date else "Fecha no encontrada"
        # PRODUCTS
        products_text = self.extract_products_section(content)
        products = self.get_products(str(products_text))
        # LOCATION
        location_pattern = r"(MERCADONA, S.A. A-\d+)(.*?TELÉFONO: \d+)"
        location_match = re.search(location_pattern, content, re.DOTALL)
        location_info = location_match.group(0) if location_match else "Ubicación no encontrada"
        location_info = location_info.replace("MERCADONA, S.A. A-46103834 ", "")
        # TOTAL
        totals_pattern = r"TOTAL \(€\) (\d+,\d{2})"
        totals_match = re.search(totals_pattern, content)
        total_ticket = totals_match.group(1) if totals_match else "0,0"

        string_number = total_ticket.replace(",", ".")
        float_number = float(string_number)
        print(f"Localización: {location_info}")
        print(f"Ticket: {id_ticket}")
        print(f"Importe: {float_number}")
        print("PRODUCTOS-----")
        for product in products:
            print(
                f"{product.quantity} | {product.name} | ({product.price_per_unit} {product.weight}) = {product.price}")

        return Ticket(id_ticket=id_ticket,
                      products=products,
                      total=float_number,
                      date=date,
                      email=email,
                      location=location_info,
                      iva=0.0)

    def get_products(self, data: str) -> [Product]:
        lines = data.strip().split('\n')
        tokenized_lines = [line.split() for line in lines]

        products = []
        complete_product = None
        for tokens in tokenized_lines:
            total = ""
            float_total = 0.0
            float_price_per_unit = 0.0
            weight = ""
            quantity = tokens[0]
            if complete_product:
                if not self.is_float(text=quantity):
                    weight = tokens[0]
                    price_per_unit = tokens[2]
                    total = tokens[-1]
                    total = total.replace(",", ".")
                    float_total = float(total)
                    price_per_unit = price_per_unit.replace(",", ".")
                    float_price_per_unit = float(price_per_unit)
                complete_product.price_per_unit = float_price_per_unit
                complete_product.price = float_total
                complete_product.weight = weight
                products.append(complete_product)
                complete_product = None
                continue
            if not quantity.isdigit():
                continue

            last_element = tokens[-1]
            name = ' '.join(tokens[1:-1]) if quantity == "1" else ' '.join(tokens[1:-2])
            if ',' in last_element:
                total = last_element
                total = total.replace(",", ".")
                float_total = float(total)
            else:
                name = ' '.join(tokens[1:])
                if not total.strip():
                    complete_product = Product(name=name,
                                               quantity=int(quantity),
                                               price_per_unit=0.0,
                                               price=0.0,
                                               weight="")
                    continue

            product = Product(name=name,
                              quantity=int(quantity),
                              price_per_unit=float_total / int(quantity),
                              price=float_total,
                              weight=weight)
            products.append(product)
        return products

        def test(self):
            content = '''MERCADONA, S.A. A-46103834
    C/ MENÉNDEZ Y PELAYO 35
    46010 VALENCIA
    TELÉFONO: 963613959
    16/09/2024 10:37 OP: 3049233
    FACTURA SIMPLIFICADA: 2475-014-371662
    Descripción P. Unit Importe
    1 ARROZ INTEGRAL 1,10
    1 MOUSSE PROTEIN CHOCO 1,30
    1 BOLSA PLASTICO 0,15
    1 ARÁNDANO 225 GR 3,09
    1 T POLLO NATURAL 1,95
    1 AGUACATE
    0,236 kg 5,10 €/kg 1,20
    1 BOLSA PLASTICO 0,15
    1 +PROT CHOCO-NATA 2,90
    1 + PROTEÍNAS FLAN 2,00
    1 JAMON S. EXTRA FINO 2,45
    1 CALAMAR PEQUEÑO 5,10
    1 ESCALOPIN SALMON 7,76
    1 MOUSSE PROTEIN CHOCO 1,30
    1 GUACAMOLE 200 G 1,85
    2 CLARA LIQUIDA PASTEU 1,55 3,10
    1 ESP VERDE FINO 2,29
    1 OBLEAS PARA HELADO 0,70
    1 3 VEGETALES 1,64
    1 PORCIONES 85% CACAO 3,20
    1 CEBOLLA CARAMELIZADA 1,70
    TOTAL (€) 8,79
    TARJETA BANCARIA 8,79
    IVA BASE IMPONIBLE (€) CUOTA (€)
    0% 4,29 0,00
    10% 3,95 0,40
    21% 0,12 0,03
    TOTAL 8,36 0,43
    TARJ. BANCARIA: **** **** **** 9018
    N.C: 098100902 AUT: 558083
    AID: A0000000041010 ARC: 00
    MASTERCARD
    Importe: 8,79 € MASTERCARD
    SE ADMITEN DEVOLUCIONES CON TICKET
            '''
            ticket = self.analyze(content=content, email="mail")

    @staticmethod
    def extract_products_section(ticket_text):
        products_pattern = r"Descripción(.+?)TOTAL \(\€\)"
        match = re.search(products_pattern, ticket_text, re.DOTALL)

        if match:
            products_section = match.group(1).strip()
            return products_section
        else:
            return None

    @staticmethod
    def is_float(text):
        try:
            float(text)
            return True
        except ValueError:
            return False
