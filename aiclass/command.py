import sys

if (sys.version_info > (3,0)):
    raw_input = input
import traceback


class BaseCommand(object):
    name = None
    description = None
    help = None

    @classmethod
    def get_data(cls, location):
        import aiclass.data
        if location.startswith('data:'):
            return getattr(aiclass.data, location[5:].upper().replace('-', '_')+'_DATA')

        with open(location, 'r') as f:
            return f.read()
    
    @classmethod
    def configure_parser(cls, parser):
        pass
    
    @classmethod
    def create_from_args(cls, args):
        return cls()

    def call(self, string):
        raise NotImplementedError

    def loop(self):
        while True:
            string = raw_input('>>> ')
            try:
                if self.call(string):
                    break
            except Exception as e:
                traceback.print_exception(*sys.exc_info())



