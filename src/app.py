from flask import Flask, render_template

from config import Config
from prometheus import get_prometheus_events

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    prometheus_object = get_prometheus_events()

    most_sever_alert = prometheus_object['most_sever']

    if most_sever_alert == 'ok':
        background_color = 'background_ok'
    elif most_sever_alert == 'none':
        background_color = 'background_unknown'
    elif most_sever_alert == 'warning':
        background_color = 'background_warning'
    elif most_sever_alert == 'critical':
        background_color = 'background_critical'

    watchdog_alert = [alert for alert in prometheus_object['events'] if alert['alertname'] == 'Watchdog']
    prometheus_object['events'] = \
        [alert for alert in prometheus_object['events'] if not alert['alertname'] == 'Watchdog']

    if watchdog_alert:
        dead_mans_switch = False
    else:
        dead_mans_switch = True
        background_color = 'background_critical'

    return render_template('index.html',
                           events=prometheus_object['events'],
                           refresh_interval=Config.refresh_interval,
                           background_color_class=background_color,
                           dashboard_header=Config.dashboard_header,
                           deadmansswitch=dead_mans_switch)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=Config.flask_debug)
