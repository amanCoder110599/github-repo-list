class Contribution():
    def __init__(self, id, url, commit_count):
        self.__id = id
        self.__url = url
        self.__commit_count = commit_count

    def get_id(self):
        return self.__id

    def get_url(self):
        return self.__url

    def get_commit_count(self):
        return self.__commit_count

