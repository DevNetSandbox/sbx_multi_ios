from flask import request, render_template


def monitoring():
    host = request.host
    if ':' in host:
        host = host.split(':')[0]
    grafana_host = host + ":3000"
    return render_template('monitoring.html',
                           grafana_host=grafana_host)
