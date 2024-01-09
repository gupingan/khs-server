import logging
import sys

from flask import Flask
from khs.path import ROOT

# 配置类型
# development production testing
CONFIG_TYPE = 'development'


def register_blueprints(app):
    from khs.apps.update_app import update_app
    app.register_blueprint(update_app)
    from khs.apps.download_app import download_app
    app.register_blueprint(download_app)


def create_app():
    app = Flask(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # 配置文件
    config_file = ROOT / 'config/' / (CONFIG_TYPE + '.cfg')
    app.config.from_pyfile(config_file, silent=True)
    # 注册蓝图
    with app.app_context():
        register_blueprints(app)
    return app
