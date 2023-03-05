from typing import List
from ldap3 import Server, Connection



class ActiveDirectory:
    
    def __init__(self, server: str, username: str, password: str, search_base: str) -> None:
        self.server = server
        self.username = username
        self.password = password
        self.search_base = search_base
    
    def get_user_attr(self, username: str, search_filter: str = None, attributes: List[str] = None) -> dict:
        
        # Create a connection object and perform a search for the given username
        try:
            conn = Connection(Server(self.server), user=self.username, password=self.password)
            conn.bind()
            
            conn.search(
                search_base=self.search_base,
                search_filter=search_filter.format(user=username),
                attributes=attributes
            )
           
        except Exception as e:
            raise ValueError(f"User {self.username} was not able to bind to LDAP server. Error: {str(e)}")

        # If we didn't find any entries based on the given search at Active Directory,
        if len(conn.entries) < 1:
            return {}

        # If there are multiple entries for the username, it may cause issues, thus we handle such case by returning an empty dictionary
        elif len(conn.entries) > 1:
            raise ValueError(f"Multiple entries found for '{username}' in Active Directory.")
            
        entry = conn.entries[0]
        
        # Get all of the attributes that are present on this user's entry 
        # Only retrieves specified attributes while initializing the class object. 
        user_attr = {attribute: entry[attribute].value for attribute in attributes if attribute in entry}
        
        # Return a dictionary containing relevant user attributes.
        return user_attr
