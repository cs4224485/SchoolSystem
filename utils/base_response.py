class BaseResponse(object):
    def __init__(self):
        self.code = None
        self.state = False
        self.msg = None
        self.data = None

    @property
    def get_dict(self):
        return self.__dict__


