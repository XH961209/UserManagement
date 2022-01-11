FROM rrrelax/python-redis
COPY . /UserManagement
WORKDIR /UserManagement
RUN chmod +x start.sh
RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 6379
CMD ./start.sh