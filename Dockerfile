FROM python:3.11-slim-buster

COPY requirements.txt /tmp/

RUN apt-get update && apt-get install -y libpq-dev gcc python-dev supervisor nginx && \
  pip install --upgrade pip && \
  pip install --upgrade --force-reinstall -r /tmp/requirements.txt -i https://pypi.org/simple/ --extra-index-url https://test.pypi.org/simple/ &&\
  groupadd -r -g 55020 appuser && \
  useradd -u 55020 -g 55020 --create-home appuser

# Supervisor to run and manage multiple apps in the same container
ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD supervisord_filelog.conf /etc/supervisor/conf.d/supervisord_filelog.conf

# Copy code into the image
COPY --chown=appuser ./app /home/appuser/app
COPY --chown=appuser ./scripts /home/appuser/scripts
COPY --chown=appuser webapp.conf.example /home/appuser/webapp.conf.example
COPY --chown=appuser gunicorn.conf.py /home/appuser/gunicorn.conf.py
COPY --chown=appuser celeryconfig.py /home/appuser/celeryconfig.py
COPY --chown=appuser conditional_start_script.sh /home/appuser/conditional_start_script.sh

RUN rm -f /etc/nginx/sites-enabled/default && \
    rm -f /etc/service/nginx/down && \
    mkdir -p /data/nginx/cache && \
    mv /home/appuser/webapp.conf.example /etc/nginx/conf.d/webapp.conf && \
    chown -R appuser /var/log/nginx && \
    chown -R appuser /var/lib/nginx && \
    chown -R appuser /data && \
    chown -R appuser /run

WORKDIR /home/appuser
USER appuser

CMD ["bash", "conditional_start_script.sh"]