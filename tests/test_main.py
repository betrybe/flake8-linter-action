import os
import tempfile
import pytest
from unittest.mock import MagicMock
from src import main
from github.GithubException import UnknownObjectException
from github import Github, Repository, PullRequest

CURRENT_PATH = os.path.dirname(__file__)


def test_format_feedback():
    mock_report = os.path.join(CURRENT_PATH, 'fixture', 'flake8.log')

    feedback = main.format_feedback(mock_report)
    assert 'error' in feedback
    assert 'warning' in feedback
    assert feedback['error']['count'] == 6
    assert feedback['warning']['count'] == 2
    assert './python/scripts/githubsearch.py' in feedback['error']['files']
    file_errors = feedback['error']['files']['./python/scripts/githubsearch.py']
    assert len(file_errors) == 4
    assert file_errors[0]['line'] == '4'
    assert file_errors[0]['message'] == ' F401 \'json\' imported but unused'
    assert file_errors[1]['line'] == '12'
    assert file_errors[1]['message'] == ' E302 expected 2 blank lines, found 1'
    assert file_errors[2]['line'] == '145'
    assert file_errors[2]['message'] == ' E501 line too long (88 > 79 characters)'
    assert file_errors[3]['line'] == '161'
    assert file_errors[3]['message'] == ' E303 too many blank lines (2)'
    assert './python/scripts/main.py' in feedback['error']['files']
    file_errors = feedback['error']['files']['./python/scripts/main.py']
    assert len(file_errors) == 2
    assert file_errors[0]['line'] == '33'
    assert file_errors[0]['message'] == ' E711 comparison to None should be \'if cond is None:\''
    assert file_errors[1]['line'] == '40'
    assert file_errors[1]['message'] == ' F841 local variable \'datetime_object\' is assigned to but never used'
    assert './python/scripts/main.py' in feedback['warning']['files']
    file_warnings = feedback['warning']['files']['./python/scripts/main.py']
    assert len(file_warnings) == 2
    assert file_warnings[0]['line'] == '48'
    assert file_warnings[0]['message'] == ' W292 no newline at end of file'
    assert file_warnings[1]['line'] == '52'
    assert file_warnings[1]['message'] == ' W291 trailing whitespace'


def test_format_feedback_with_file_not_found():
    mock_report = os.path.join(CURRENT_PATH, 'fixture', 'unexistent.log')
    with pytest.raises(FileNotFoundError):
        main.format_feedback(mock_report)


def test_format_feedback_with_invalid_file():
    mock_report = os.path.join(CURRENT_PATH, 'fixture', 'expected_comment.md')
    feedback = main.format_feedback(mock_report)

    assert 'error' in feedback
    assert feedback['error']['count'] == 0
    assert len(feedback['error']['files']) == 0
    assert 'warning' in feedback
    assert feedback['warning']['count'] == 0
    assert len(feedback['warning']['files']) == 0


def test_format_feedback_with_empty_file():
    empty_file = os.path.join(tempfile.gettempdir(), 'empty.log')
    file = open(empty_file, 'w+')
    file.flush()
    file.close()

    feedback = main.format_feedback(empty_file)

    assert 'error' in feedback
    assert feedback['error']['count'] == 0
    assert len(feedback['error']['files']) == 0
    assert 'warning' in feedback
    assert feedback['warning']['count'] == 0
    assert len(feedback['warning']['files']) == 0


def test_build_comment_with_errors_and_warnings():
    mock_comment = os.path.join(CURRENT_PATH, 'fixture', 'expected_comment.md')
    fp = open(mock_comment, "r")
    comment_expected = fp.read()
    fp.close()

    mock_report = os.path.join(CURRENT_PATH, 'fixture', 'flake8.log')
    feedback = main.format_feedback(mock_report)
    comment = main.build_comment(feedback)
    assert comment == comment_expected


def test_build_comment_with_0_errors_0_warnings_found():
    feedback = {
        'error': {
            'files': {},
            'count': 0
        },
        'warning': {
            'files': {},
            'count': 0
        },
    }
    comment = main.build_comment(feedback)
    expected = '### Nenhum erro foi encontrado.\n'
    expected += '### Nenhum aviso foi encontrado.\n'
    assert comment == expected


def test_build_comment_with_1_error_0_warning_found():
    feedback = {
        'error': {
            'files': {
                './src/main.py': [
                    {
                        'line': '66',
                        'message': 'E000 Lorem ipsum'
                    }
                ]
            },
            'count': 1
        },
        'warning': {
            'files': {},
            'count': 0
        },
    }

    comment = main.build_comment(feedback)
    assert '### Foi encontrado 1 erro.\n' in comment
    assert '### Nenhum aviso foi encontrado.\n' in comment


def test_build_comment_with_0_error_1_warning_found():
    feedback = {
        'error': {
            'files': {},
            'count': 0
        },
        'warning': {
            'files': {
                './src/main.py': [
                    {
                        'line': '66',
                        'message': 'E000 Lorem ipsum'
                    }
                ]
            },
            'count': 1
        },
    }
    comment = main.build_comment(feedback)
    assert '### Nenhum erro foi encontrado.\n' in comment
    assert '### Foi encontrado 1 aviso.\n' in comment


def test_comment_on_pr_with_repository_not_found(mocker):
    get_repo_mock = mocker.patch.object(Github, "get_repo", autospec=True)
    get_repo_mock.side_effect = UnknownObjectException(mocker.Mock(status=404), 'not found', [])

    with pytest.raises(UnknownObjectException):
        main.comment_on_pr('')


def test_comment_on_pr_with_pull_request_not_found(mocker):
    get_repo_mock = mocker.patch.object(Github, "get_repo", autospec=True)
    repo_mock = MagicMock(wrap=Repository.Repository)
    repo_mock.owner = 'org'
    repo_mock.repo = 'trybe'
    repo_mock.get_pull = MagicMock(
        autospec=True,
        side_effect=UnknownObjectException(mocker.Mock(status=404), 'not found', [])
    )

    get_repo_mock.return_value = repo_mock

    with pytest.raises(UnknownObjectException):
        main.comment_on_pr('')


def test_comment_on_pr(mocker):
    get_repo_mock = mocker.patch.object(Github, "get_repo", autospec=True)
    repo_mock = MagicMock(wrap=Repository.Repository)
    repo_mock.owner = 'betrybe'
    repo_mock.repo = 'flake8-linter'
    pr_mock = MagicMock(wrap=PullRequest.PullRequest)
    repo_mock.get_pull = MagicMock(autospec=True, return_value=pr_mock)

    get_repo_mock.return_value = repo_mock

    main.comment_on_pr('### Lorem')

    pr_mock.create_issue_comment.assert_called_once_with('### Lorem')
