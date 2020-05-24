# Final Year Project News Crawler
## Setup
Make sure python 3.6 and virtualenv are installed and that the URL pointing to the common repository is replaced by your own URL.

Run the following:
```sh
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Files Required
Please add all these files to your folder with the missing parts filled in.
### set_env.sh
```sh
source ./venv/bin/activate
export PYTHON_ENV="DEVELOPMENT" # DEVELOPMENT / PRODUCTION

# Secrets
export NEWS_API_KEY="" # Your key

# Mongo
export MONGO_URL='mongodb://localhost:27017'
export MONGO_DATABASE_NAME='default_db'

# Celery
export BROKER_URL="amqp://guest:guest@localhost:5672"

```
