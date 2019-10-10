FROM python: 3

RUN pip install requests

COPY publish.py /publish.py 

#TODO: unsure if additional logic should be handled in entrypoint.sh or if we should just do everything inside of python
COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
