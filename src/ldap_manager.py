from ldap3 import Server, Connection


class ActiveDirectory():
    def __init__(self, server, username, password, search_base):
        self.server = server
        self.username = username
        self.password = password
        self.search_base = search_base

    def get_user_attr(self, username, search_filter=None, attributes=None):
        with Connection(Server(self.server), self.username, self.password, auto_bind=True) as conn:
            conn.search(
                search_base=self.search_base,
                search_filter=search_filter.format(user=username),
                attributes=attributes
            )
            if conn.entries:
                entry = conn.entries[0]
                user_attr = {attribute: entry[attribute].value for attribute in attributes if attribute in entry}
                return user_attr
