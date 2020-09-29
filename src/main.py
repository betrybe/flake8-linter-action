import sys
from github import Github
import os


def format_feedback(flake8_report):
    flake8_report = open(flake8_report, 'r')
    lines = flake8_report.readlines()

    files = {}
    count = 0
    for line in lines:
        content = line.strip().split(":", 3)
        if len(content) < 4:
            continue

        filename = content[0]
        if filename not in files:
            files[filename] = []
        files[filename].append({
            'line': content[1],
            'message': content[-1]
        })
        count += 1

    return {
        'count': count,
        'files': files,
    }


def build_comment(feedback):
    if feedback['count'] == 0:
        return '### Nenhum erro foi encontrado.\n'

    msg = 'Foram encontrados {} erros'.format(feedback['count'])
    if feedback['count'] == 1:
        msg = 'Foi encontrado 1 erro'
    comment = '### {}.\n'.format(msg)

    for file in feedback['files']:
        comment += '\n#### Arquivo `{}`\n\n'.format(file)
        for error in feedback['files'][file]:
            comment += '- Linha **{}**:{}\n'.format(error['line'], error['message'])

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
