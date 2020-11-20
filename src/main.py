import sys
from github import Github
import os


def format_feedback(flake8_report):
    flake8_report = open(flake8_report, 'r')
    lines = flake8_report.readlines()

    files = {}
    err_count = 0
    warn_count = 0
    for line in lines:
        content = line.strip().split(":", 3)
        if len(content) < 4:
            continue

        filename = content[0]
        if filename not in files:
            files[filename] = []

        message = content[-1]
        files[filename].append({
            'line': content[1],
            'message': message
        })

        if message.lstrip().startswith("W"):
            warn_count += 1
        else:
            err_count += 1

    return {
        'error_count': err_count,
        'warning_count': warn_count,
        'files': files,
    }


def build_comment(feedback):
    err_msg = 'Foram encontrados {} erros'.format(feedback['error_count'])
    warn_msg = 'Foram encontrados {} avisos'.format(feedback['warning_count'])
    if feedback['error_count'] == 1:
        err_msg = 'Foi encontrado 1 erro'
    if feedback['warning_count'] == 1:
        warn_msg = 'Foi encontrado 1 aviso'
    if feedback['error_count'] == 0:
        err_msg = 'Nenhum erro foi encontrado'
    if feedback['warning_count'] == 0:
        warn_msg = 'Nenhum aviso foi encontrado'

    comment = '### {}.\n'.format(err_msg)
    comment += '### {}.\n'.format(warn_msg)

    if len(feedback['files']) == 0:
        return comment

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

    if feedback['error_count'] > 0:
        raise ValueError()
