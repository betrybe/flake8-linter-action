import sys
from github import Github
import os


def format_feedback(flake8_report):
    flake8_report = open(flake8_report, 'r')
    lines = flake8_report.readlines()

    files = {
        'error': {
            'files': {},
            'count': 0
        },
        'warning': {
            'files': {},
            'count': 0
        },
    }
    for line in lines:
        content = line.strip().split(":", 3)
        if len(content) < 4:
            continue

        filename = content[0]
        message = content[-1]
        file_msg = {
            'line': content[1],
            'message': message
        }
        group = 'error'
        if message.lstrip().startswith("W"):
            group = 'warning'

        if filename not in files[group]['files']:
            files[group]['files'][filename] = []

        files[group]['files'][filename].append(file_msg)
        files[group]['count'] += 1

    return files


def build_comment(feedback):
    comment = ''
    for group in feedback:
        label = 'erro'
        if group == 'warning':
            label = 'aviso'
        msg = 'Foram encontrados {} {}s'.format(feedback[group]['count'], label)
        if feedback[group]['count'] == 1:
            msg = 'Foi encontrado 1 {}'.format(label)
        if feedback[group]['count'] == 0:
            msg = 'Nenhum {} foi encontrado'.format(label)

        comment += '### {}.\n'.format(msg)
        if feedback[group]['count'] == 0:
            continue

        for file in feedback[group]['files']:
            comment += '\n#### Arquivo `{}`\n\n'.format(file)
            for error in feedback[group]['files'][file]:
                comment += '- Linha **{}**:{}\n'.format(error['line'], error['message'])
        comment += '\n'

    return comment


def comment_on_pr(comment):
    github = Github(os.getenv('INPUT_TOKEN'))
    repo = github.get_repo(os.getenv('GITHUB_REPOSITORY'))
    pull_request = repo.get_pull(int(os.getenv('INPUT_PR_NUMBER', '1')))

    pull_request.create_issue_comment(comment)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError('You must pass report and requirements files as arguments!')

    feedback = format_feedback(sys.argv[1])
    comment = build_comment(feedback)
    comment_on_pr(comment)

    if len(feedback['error']) > 0:
        raise ValueError()
