from db.connect_db import Server, ServerInfo, ServerOwner, Session


def new_server(session, data):
    '''
    To add new server and its following infos (server info and server owner).

    Params:
    ------------
    session: 
        session of current query 
    data:
        a dictionary that contain server info, included: server_name, enabled, ram, cpu, owner
    '''
    info = [ServerInfo(ram=data['ram'], cpu=data['cpu'])]
    owners = []
    for owner in data['owner']:
        owners.append(ServerOwner(owner_name=owner))

    server = Server(name=data['server_name'], enabled=True if not 'enable' in data else data['enable'], info=info, owners=owners)
    session.add(server)
    session.commit()

    return server


def get_all_server(session):
    return session.query(Server).all()


if __name__ == "__main__":
    # data = {
    #     'server_name': 'test_server2',
    #     'ram': 2,
    #     'cpu': 4,
    #     "owner": ['nthien', 'tmduc']
    # }
    # server = new_server(Session(), data)

    print(get_all_server(Session()))