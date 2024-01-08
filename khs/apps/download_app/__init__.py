from flask import Blueprint, send_from_directory, current_app, abort
from khs.path import UPDATE_FOLDER

download_app = Blueprint('download', __name__)

platform_suffixes = current_app.config['PLATFORM_SUFFIXES']


@download_app.route('/api/download/<version>/<platform>', methods=['GET'])
def download_package(version: str, platform: str):
    filename = f'khs-{version}-{platform}{platform_suffixes.get(platform, "")}'
    if not (UPDATE_FOLDER / filename).is_file():
        abort(404)
    return send_from_directory(UPDATE_FOLDER, filename, as_attachment=True)
