from __future__ import print_function

import inspect, os.path, re, shlex, sys, traceback, unittest

try:
    import StringIO
except ImportError:
    import io as StringIO

from aiclass import search, naive, propositional, plan, network, data
from aiclass.command import BaseCommand, get_command_from_args


class TestFailure(AssertionError):

    def __init__(self, filename, lineno, error):
        self.filename = filename
        self.lineno = lineno
        self.error = error

    def __str__(self):
        return "File '{filename}' line {lineno}\n{error}".format(
            filename = self.filename.encode('string_escape'),
            lineno = self.lineno,
            error = self.error)


FAILURE_TEMPLATE = '-'*70 + '''
Failed example in File '{filename}' line {lineno}
Trying:

    >>> {input}

Expected:

    {expected}

Got:

    {output}
'''

EXCEPTION_TEMPLATE = '-'*70 + '''
Failed example in File '{filename}' line {lineno}
Trying:

    >>> {input}

Exception Raised:
'''



class TestCase(unittest.TestCase):

    def __init__(self, filename, lineno, arguments, examples):
        unittest.TestCase.__init__(self)

        self.filename = filename
        self.lineno = lineno
        self.arguments = arguments
        self.examples = examples


    def __str__(self):
        return 'aiclass ' + self.arguments


    def runTest(self):
        tries = 0
        failures = 0
        out = StringIO.StringIO()

        try:
            cmd = get_command_from_args(shlex.split(self.arguments))
        except Exception:
            raise TestFailure(
                self.filename,
                self.lineno,
                'Command Argument Error:\n    {args}'.format(
                    args='aiclass ' + self.arguments))
            

        for input, expected, start in self.examples:
            tries += 1

            try:
                output = str(cmd.call(input))
                if output != expected:
                    failures += 1

                    print(
                        FAILURE_TEMPLATE.format(
                            filename = self.filename,
                            lineno = start,
                            input = input,
                            expected = '\n    '.join(expected.split('\n')),
                            output = '\n    '.join(output.split('\n'))), 
                        file = out)
                    
            except Exception:
                failures += 1

                print(
                    EXCEPTION_TEMPLATE.format(
                        filename = self.filename,
                        lineno = start,
                        input = input),
                    file = out)

                traceback.print_exception(*sys.exc_info(), file=out)
                out.write('\n')

        if failures:
            raise TestFailure(
                self.filename,
                self.lineno,
                out.getvalue())


    def shortDescription(self):
        return 'aiclass ' + self.arguments



def find_command_tests(command):
    if not command.__doc__:
        return []

    path = inspect.getsourcefile(command)
    relpath = os.path.relpath(path)
    if not relpath.startswith('..'):
        path = relpath

    lineno = inspect.getsourcelines(command)[1] + 1

    docstring = command.__doc__.expandtabs()
    indent = min(len(spaces) for spaces in re.findall(r'^ *(?=\S)', docstring, re.M))
    docstring = '\n'.join(line[indent:] for line in docstring.splitlines())

    arguments = [ 
        ( m.group(1), m.start(), m.end() ) 
        for m in re.finditer(r'^\$ +aiclass +(.*)$', docstring, re.M) ]

    tests = []

    for i, (arg, start, end) in enumerate(arguments):
        next_start = arguments[i+1][1] if i+1 < len(arguments) else None
        string = docstring[end+1:next_start]

        examples = []

        for m in re.finditer(
            r'^>>> +(?P<input>[^\n]*)(?P<output>(?:\n(?:(?! *$)(?!>>> .*$).*$))*)', 
            string, re.M):
            result = m.groupdict()

            example = (
                result['input'],
                result['output'][1:],
                lineno + docstring.count('\n', 0, end + 1 + m.start()))

            examples += [example]

        tests.append(
            TestCase(
                path,
                lineno + docstring.count('\n', 0, start),
                arg,
                examples))

    return tests



def find_module_tests(module):
    tests = []
 
    for k,v in module.__dict__.items():
        if isinstance(v, type) and issubclass(v, BaseCommand) and v != BaseCommand:
            tests += find_command_tests(v)

    return tests
    


def suite():
    suite = unittest.TestSuite()

    for module in [ search, naive, propositional, plan, network ]:
        suite.addTests(find_module_tests(module))
    
    return suite



