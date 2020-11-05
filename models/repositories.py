class Repository:
    def __init__(self, id, url, fork_count, contributors):
        self.__id = id
        self.__url = url
        self.__fork_count = fork_count
        self.__contributors = contributors
    
    def get_id(self):
        return self.__id

    def get_url(self):
        return self.__url

    def get_fork_count(self):
        return self.__fork_count

    def get_contributors(self):
        return self.__contributors
