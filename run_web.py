from web import app
import logging

# Log to file
FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(filename='log/web.log',level=logging.DEBUG, format=FORMAT)

# Log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# Start web server
app.run(port=80, debug=True)