from __future__ import print_function

try:
    import readline
except ImportError:
    pass

from aiclass.command import get_command_from_args

def main():
    command = get_command_from_args()
    command.loop()
    print('quit')


    
if __name__ == '__main__':
    main()


