from db.connect_db import ContactInfo, ServerInfo, ServerOwner, Server


def get_contact_info(session, time):
    contact_info = session.query(ContactInfo.owner_name, ContactInfo.tel)\
        .filter(time >= ContactInfo.start_time)\
        .filter(time <= ContactInfo.end_time)\
        .all()

    return contact_info


def get_server_info(session, server_name=None):
    if server_name:
        server_info = session.query(Server).filter_by(name=server_name).join('info').join('owners').all()
        return server_info
    else:
        return session.query(Server).join('info').join('owners').all()
    return None
