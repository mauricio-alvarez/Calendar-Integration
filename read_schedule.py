# importing required modules 
from datetime import datetime
import pytz
from pypdf import PdfReader 
'''
event = {
            'summary': 'Reunión de prueba',
            'description': 'Reunión de prueba con Google Calendar API',
            'start': {
                'dateTime': '2024-06-19T09:00:00-05:00',
                'timeZone': 'America/Lima',
            },
            'end': {
                'dateTime': '2024-06-19T11:00:00-05:00',
                'timeZone': 'America/Lima',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;COUNT=2'
            ],
            'attendees': [
                {'email': 'mauricio.alvarez@utec.edu.pe'},
            ],
            'reminders': {
                'useDefault': True
            },
        }
'''
def edit_time(date_format, hours):
    date_format = date_format[:-14] + hours + ':00' + date_format[-6:]
    return date_format
def edit_date(date_format, day_diff):
    date_format = date_format[:-17] + str(int(date_format[-17:-15])+day_diff) + date_format[-15:]
    return date_format

def create_event(day, hours, where):
    timezone = pytz.timezone('America/Lima')
    # Obtén la fecha y hora actuales con la zona horaria definida
    now = datetime.now(timezone)
    # Formatea la fecha y hora en el formato ISO 8601
    weekday_name = now.strftime('%A')
    date_format = now.strftime('%Y-%m-%dT%H:%M:%S%z')
    date_format = date_format[:-2] + ':' + date_format[-2:]
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    days_spanish = {"Lunes": 0, "Martes":1, "Miércoles": 2, "Jueves": 3, "Viernes": 4, "Sábado":5}
    
    hours = hours.strip()
    timezone = pytz.timezone('America/Lima')
    # Obtén la fecha y hora actuales con la zona horaria definida
    now = datetime.now(timezone)
    # Formatea la fecha y hora en el formato ISO 8601
    weekday_name = now.strftime('%A')
    day_diff = days_spanish[day] - days_of_week.index(weekday_name)
    start_date = edit_time(date_format, hours[0:5])
    if day_diff == 0:
        end_date = edit_time(start_date, hours[6:])
    elif  day_diff > 0:
        start_date = edit_date(start_date, day_diff)
        end_date = edit_time(start_date, hours[6:])
        pass
    else:
        start_date = edit_date(start_date, 7+day_diff)
        end_date = edit_time(start_date, hours[6:])
        pass
    event = {
        'summary': 'Clase en: '+where,
        'description': 'Clase de prueba con Google Calendar API',
        'start': {
            'dateTime': f'{start_date.replace(" ", "")}',
            'timeZone': 'America/Lima',
        },
        'end': {
            'dateTime': f'{end_date.replace(" ", "")}',
            'timeZone': 'America/Lima',
        },
        'recurrence': [
            'RRULE:FREQ=WEEKLY;COUNT=16'
        ],
        'attendees': {
            'email': ''
        },
        'reminders': {
            'useDefault': True
        },
        
    }
    return event

def get_classes():
    event_list = []
    schedule = []
    # creating a pdf reader object 
    reader = PdfReader('horario.pdf') 
    cnt=0
    for i in range(0,reader.get_num_pages()):
        # getting a specific page from the pdf file 
        page = reader.pages[i] 

        # extracting text from page 
        text = page.extract_text() 
        # identify new line and print until the end
        text = text.split("\n")
        found = False

        for line in text:
            index = line.find("Semana General")
            if (found and index==-1):
                schedule[cnt-1] = schedule[cnt-1] + " " + line
                found=False
            if (index != -1):
                index += len("Semana General")+1
                schedule.append(line[index:])
                found = True
                cnt = cnt + 1

                

    for day_of_class in schedule:

            day_index = max(day_of_class.find("Teoría"),day_of_class.find("Laboratorio"))
            day = day_of_class[:day_index-1]
            hour_from = day_of_class.find(":")-2
            # length(19:00-20:00) = 12
            hour_to = hour_from+12
            hour = day_of_class[hour_from:hour_to]
            where = hour_to
            where = day_of_class[where:-4]
            #print(day, hour, where)
            event_list.append(create_event(day, hour, where))

    return event_list
            
if __name__ == '__main__':
    get_classes()