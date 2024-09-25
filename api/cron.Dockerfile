FROM trading-api as base

RUN apt-get -y update; apt-get -y install curl

# Latest releases available at https://github.com/aptible/supercronic/releases
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.32/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=7da26ce6ab48d75e97f7204554afe7c80779d4e0

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

# Add crontab file
COPY crontab .

CMD supercronic crontab

# Give execution rights on the cron job
# RUN chmod 0644 /etc/cron.d/crontab

# Create the log file to be able to run tail
# RUN touch /var/log/cron.log

# Start the cron service
# CMD cron && tail -f /var/log/cron.log
