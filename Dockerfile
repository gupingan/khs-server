# 使用官方Python基础镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /khs-backend

# 安装pipenv
RUN pip install --no-cache-dir pipenv

# 将Pipfile复制到工作目录并安装依赖项
COPY Pipfile* /khs-backend/
RUN pipenv install --system --deploy

# 将当前目录的内容复制到容器中的工作目录
COPY . /khs-backend

# 允许外部访问容器的端口
EXPOSE 5000

# 定义环境变量
ENV FLASK_APP=run.py

# 运行Flask应用程序
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "run:app"]

