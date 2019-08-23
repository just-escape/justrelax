from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DataBaseAccess:
    _engine = None
    _session_maker = None

    @staticmethod
    def init_engine(
        protocol,
        user=None, password=None,
        host=None, port=None, base=None
    ):
        url = '{}://'.format(protocol)

        if user is not None:
            credentials = user
            if password is not None:
                credentials = '{}:{}'.format(credentials, password)
            url = '{}{}@'.format(url, credentials)

        if host is not None:
            socket = host
            if port is not None:
                socket = '{}:{}'.format(socket, port)
            url = '{}{}'.format(url, socket)

        if base is not None:
            url = '{}/{}'.format(url, base)

        DataBaseAccess._engine = create_engine(url)

    @staticmethod
    def get_engine():
        if DataBaseAccess._engine is None:
            # If create engine has not been called before, use an SQLite in RAM
            DataBaseAccess.init_engine(protocol='sqlite')
            #TODO: in this case create all databases (and add some fixtures?)

        return DataBaseAccess._engine

    @staticmethod
    def get_session_maker():
        if DataBaseAccess._session_maker is None:
            DataBaseAccess._session_maker = sessionmaker(
                bind=DataBaseAccess.get_engine())

        return DataBaseAccess._session_maker

    @staticmethod
    def get_session():
        return DataBaseAccess.get_session_maker()()


def get_session():
    return DataBaseAccess.get_session()
