from flask import Blueprint, request, current_app, url_for
from khs.path import UPDATE_FOLDER
from khs.utils.responses import RespBody, RespCode

update_app = Blueprint('update', __name__)

platform_suffixes = current_app.config['PLATFORM_SUFFIXES']


@update_app.before_request
def before_request():
    UPDATE_FOLDER.mkdir(parents=True, exist_ok=True)


def get_latest_version(platform):
    update_packages = list(UPDATE_FOLDER.glob(f'*{platform}*'))
    if not update_packages:
        return '0.0.0'
    return max(package.name.split('-')[1] for package in update_packages)


@update_app.route('/api/update/check', methods=['GET'])
def check_update():
    response = RespBody({
        'update_available': False,
        'latest_version': '0.0.0',
        'file_name': '',
    })

    try:
        if len(request.args.keys()) != 2:
            raise KeyError
        version = request.args['version']
        platform = request.args['platform'].lower()
    except KeyError:
        response.update(code=RespCode.INVALID_ARGUMENT, msg='Invalid parameter')
        return response.body

    max_version = get_latest_version(platform)
    update_available = version < max_version
    response(
        latest_version=max_version,
        update_available=update_available,
        file_name=f'khs-{max_version}-{platform}{platform_suffixes.get(platform, "")}',
    )
    return response.body


@update_app.route('/api/update/get', methods=['GET'])
def get_update():
    response = RespBody({'url': ''})
    platform = request.args.get('platform', '').lower()
    if platform not in platform_suffixes:
        response.update(code=RespCode.INVALID_ARGUMENT, msg='Invalid parameter')
        return response.body
    latest_version = get_latest_version(platform)
    filename = f'khs-{latest_version}-{platform}{platform_suffixes.get(platform, "")}'
    if not (UPDATE_FOLDER / filename).is_file():
        response.update(code=RespCode.NOT_FOUND, msg='Package not found')
        return response.body
    response(url=url_for(
        'download.download_package',
        version=latest_version,
        platform=platform,
    ))
    return response.body
