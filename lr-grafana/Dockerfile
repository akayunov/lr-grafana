FROM debian:13-slim

ENV DEBIAN_FRONTEND=noninteractive

#RUN apt-get update && apt-get install -y --no-install-recommends \
#    apt-transport-https \
#    ca-certificates \
#    curl \
#    gnupg \
#    && mkdir -p /etc/apt/keyrings \
#    # Используем curl вместо wget:
#    && curl -fsSL https://grafana.com -o /etc/apt/keyrings/grafana.asc \
#    && chmod 644 /etc/apt/keyrings/grafana.asc \
#    && echo "deb [signed-by=/etc/apt/keyrings/grafana.asc] https://grafana.com stable main" | tee /etc/apt/sources.list.d/grafana.list \
#    && apt-get update \
#    && apt-get install -y --no-install-recommends grafana-enterprise \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

# work around

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    libcap2-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r -g 472 grafana && \
    useradd -r -u 472 -g grafana -d /usr/share/grafana -s /sbin/nologin grafana


RUN --mount=type=bind,source=grafana-enterprise_13.1.0_28013217238_linux_amd64.deb,target=/tmp/grafana.deb \
    apt-get update && \
    dpkg -i /tmp/grafana.deb || apt-get install -f -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chown -R grafana:grafana /etc/grafana /var/lib/grafana /usr/share/grafana /var/log/grafana

RUN setcap 'cap_net_bind_service=+ep' /usr/share/grafana/bin/grafana

USER grafana

CMD ["/usr/share/grafana/bin/grafana", "server", "--config=/etc/grafana/grafana.ini", "--homepath=/usr/share/grafana"]
