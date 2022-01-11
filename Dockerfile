FROM python:3.8
COPY . /UserManagement
WORKDIR /UserManagement
RUN curl -O https://download.redis.io/releases/redis-6.2.6.tar.gz \
    && tar -zxvf redis-6.2.6.tar.gz \
    && cd redis-6.2.6 \
    && make \
    && make install \
    && cd ../ \
    && chmod +x start.sh
RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 6379
CMD ./start.sh