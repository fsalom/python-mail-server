import os
import django
from starlette.middleware.cors import CORSMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.django.settings')
django.setup()

from fastapi import FastAPI
from driving.api_rest.router import add_routers
from driving.api_rest.containers import add_containers

app = FastAPI()
origins = [
    "http://localhost:3000",  # Origen de desarrollo
    "https://tickets.rudo.es"   # Puedes añadir otros orígenes de producción aquí
]

# Agrega el middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,                # Permite estos orígenes
    allow_credentials=True,                # Permitir cookies y autenticación
    allow_methods=["*"],                   # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],                   # Permitir todos los headers
)
add_routers(app)
add_containers(app)
