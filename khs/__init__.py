import logging
import sys
from flask import Flask
from logging.handlers import RotatingFileHandler
from khs.path import ROOT

# 配置类型
# development production testing
CONFIG_TYPE = 'development'


def setup_logging(app):
    log_dir = ROOT / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f'{CONFIG_TYPE}.log'

    # 设置基本配置
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        handlers=[logging.StreamHandler(sys.stdout)])

    # 文件日志处理器
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))

    # 将文件日志处理器添加到 Flask 默认日志记录器
    app.logger.addHandler(file_handler)

    # 如果需要，还可以为其他日志记录器添加文件处理器
    # logging.getLogger('werkzeug').addHandler(file_handler)


def register_blueprints(app):
    from khs.apps.update_app import update_app
    app.register_blueprint(update_app)
    from khs.apps.download_app import download_app
    app.register_blueprint(download_app)


def create_app():
    app = Flask(__name__)
    # 安装日志
    setup_logging(app)
    # 配置文件
    config_file = ROOT / 'config/' / (CONFIG_TYPE + '.cfg')
    app.config.from_pyfile(config_file, silent=True)
    # 注册蓝图
    with app.app_context():
        register_blueprints(app)
    return app
