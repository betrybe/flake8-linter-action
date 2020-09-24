import os
from src import main

CURRENT_PATH = os.path.dirname(__file__)


def test_format_feedback():
    mock_report = os.path.join(CURRENT_PATH, 'fixture', 'flake8.log')

    feedback = main.format_feedback(mock_report)
    assert 'count' in feedback
    assert feedback['count'] == 6
    assert 'files' in feedback
    assert './python/scripts/githubsearch.py' in feedback['files']
    file_errors = feedback['files']['./python/scripts/githubsearch.py']
    assert len(file_errors) == 4
    assert file_errors[0]['line'] == '4'
    assert file_errors[0]['message'] == ' F401 \'json\' imported but unused'
    assert file_errors[1]['line'] == '12'
    assert file_errors[1]['message'] == ' E302 expected 2 blank lines, found 1'
    assert file_errors[2]['line'] == '145'
    assert file_errors[2]['message'] == ' E501 line too long (88 > 79 characters)'
    assert file_errors[3]['line'] == '161'
    assert file_errors[3]['message'] == ' E303 too many blank lines (2)'
    assert './python/scripts/main.py' in feedback['files']
    file_errors = feedback['files']['./python/scripts/main.py']
    assert len(file_errors) == 2
    assert file_errors[0]['line'] == '33'
    assert file_errors[0]['message'] == ' E711 comparison to None should be \'if cond is None:\''
    assert file_errors[1]['line'] == '40'
    assert file_errors[1]['message'] == ' F841 local variable \'datetime_object\' is assigned to but never used'


def test_build_comment():
    mock_comment = os.path.join(CURRENT_PATH, 'fixture', 'expected_comment.md')
    fp = open(mock_comment, "r")
    comment_expected = fp.read()
    fp.close()

    mock_report = os.path.join(CURRENT_PATH, 'fixture', 'flake8.log')
    feedback = main.format_feedback(mock_report)
    comment = main.build_comment(feedback)
    assert comment == comment_expected


def test_comment_on_pr():
    mock_comment = os.path.join(CURRENT_PATH, 'fixture', 'expected_comment.md')
    fp = open(mock_comment, "r")
    comment_mock = fp.read()
    fp.close()

    main.comment_on_pr(comment_mock)