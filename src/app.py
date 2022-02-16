
from flask import Flask
from flask.blueprints import Blueprint
from flask_cors import CORS
from anuvaad_auditor.loghandler import log_info
import routes
import config
from utilities import MODULE_CONTEXT
import threading
from kafka_wrapper import KafkaTranslate
from werkzeug.serving import run_simple

server  = Flask(__name__)

def kafka_function():
    log_info('starting kafka from nmt-server on thread-1',MODULE_CONTEXT)
    KafkaTranslate.batch_translator([config.kafka_topic[0]['consumer']])     

if config.bootstrap_server_boolean:
    t1 = threading.Thread(target=kafka_function)
    t1.start()

if config.ENABLE_CORS:
    cors    = CORS(server, resources={r"/api/*": {"origins": "*"}})

for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        server.register_blueprint(blueprint, url_prefix=config.API_URL_PREFIX)

if __name__ == "__main__":
    # from waitress import serve

    log_info('starting server at {} at port {}'.format(config.HOST, config.PORT), MODULE_CONTEXT)
    server.run(host=config.HOST, port=config.PORT, debug=config.DEBUG, threaded=True)
    # server.run(host=config.HOST, port=config.PORT, debug=config.DEBUG, threaded=False, processes=50)
    # serve(server, host=config.HOST, port=config.PORT)
    # run_simple(config.HOST,config.PORT,server,processes=config.concurrent_processes)