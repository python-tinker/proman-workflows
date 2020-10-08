'''Test git hooks pipeline.'''

from git_tools.message import MessageParser
from textwrap import dedent

message = '''fix(example): test a message

Reviewed-by: Jesse P Johnson <jpj6652@gmail.com>
Refs #123
Fix #124
BREAKING CHANGE: This could change things
'''


def test_footer_trailer():
    '''Test footer trailer.'''
    parser = MessageParser()
    parser.parse(message)
    assert parser.footer['trailer']['token'] == 'Reviewed-by'
    assert parser.footer['trailer']['name'] == 'Jesse P Johnson '
    assert parser.footer['trailer']['email'] == 'jpj6652@gmail.com'


def test_footer_issues():
    '''Test footer issues.'''
    parser = MessageParser()
    parser.parse(message)
    assert parser.footer['issues'][0]['Refs'] == '123'
    assert parser.footer['issues'][1]['Fix'] == '124'


def test_footer_breaking_change():
    '''test footer breaking change.'''
    parser = MessageParser()
    parser.parse(message)
    assert parser.footer['breaking_change'] == 'This could change things'
