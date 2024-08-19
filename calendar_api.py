import datetime
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from read_schedule import *
# Alcances requeridos por la API de Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Muestra la lista de eventos de Google Calendar."""
    creds = None
    # El archivo token.json almacena el token de acceso y refresco del usuario, y es
    # creado automáticamente cuando el flujo de autorización es completado por primera vez.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si no hay credenciales válidas disponibles, permite al usuario iniciar sesión.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Guarda las credenciales para la próxima ejecución
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    #events = main()
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Crea un nuevo evento
        try:
            events = get_classes()
            for event in events:
                event = service.events().insert(calendarId='primary', body=event).execute()
                print(f'Evento creado: {event.get("htmlLink")}')
        except:
            print("No hay eventos")

    except HttpError as error:
        print(f'Ocurrió un error: {error}')

if __name__ == '__main__':
    main()
