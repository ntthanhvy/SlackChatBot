from db.connect_db import Server, ServerInfo, ServerOwner, Session, ContactInfo, Escalate
from datetime import datetime


def new_server(session, data):
    '''
    To add new server and its following infos (server info and server owner).

    Params:
    ------------
    session: 
        session of current query 
    data:
        a dictionary that contain server info
        data = {
            server_name: String
            enable: Boolean
            ram: Integer
            cpu: Integer
            owner: List<String>
        }
    '''
    info = [ServerInfo(ram=data['ram'], cpu=data['cpu'])]
    owners = []
    if type(data['owner']) is not str():
        for owner in data['owner']:
            owners.append(ServerOwner(owner_name=owner))
    else:
        raise TypeError("server owner must be list of owners")

    server = Server(name=data['server_name'],
                    enabled=True if not 'enable' in data else data['enable'], info=info, owners=owners)
    session.add(server)
    session.commit()

    return server


def add_contact_info(session, data):
    '''
    Add new contact info for in charge person with specific time of contact.

    Params:
    ---------------
    session: 
        Session() class isntance to do query to db
    data:
        a dictionary with contact_info data.
        data = {
            start_time: DateTime obj,
            end_time: DateTime obj,
            owner_name: String,
            tel: String (owner telephone numbers)
        }
    
    Return:
    ---------------
    contact_info just have been create 
    '''

    contact_info = ContactInfo(
        start_time=data['start_time'], end_time=data['end_time'], owner_name=data['owner_name'], tel=data['tel'])
    session.add(contact_info)
    session.commit()
    return contact_info


def add_escalate(session, data):
    '''
    To store an escalate alert from server and return the time of the escalate
    
    Params:
    ------------
    session:
       Session() class isntance to do query to db
    data:
        a dictionary of escalate data
        data = {
            time: DataTime obj,
            reporter: String,
            type: String (< 10 words)
        }
    
    Return:
    -------------
    time:
        time of the escalate happened
    '''
    escalate = Escalate(time=data['time'], reporter=data['customer'], type=data['type'])
    session.add(escalate)

    return escalate.time
    

