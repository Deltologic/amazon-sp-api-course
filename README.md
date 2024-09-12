# Amazon SP-API course
Welcome to SP-API course repository! This repository is part of the Amazon SP-API course available at: https://courses.deltologic.com/
It contains examples of the use of the *python-amazon-sp-api* library, which facilitates the use of SP-API in the Python language.

## Prepare virtual environment
Create virtual environment
```bash
python3 -m venv venv
```

Activate the environment
```bash
source venv/bin/activate
```

Install the packages listed in requirements.txt file
```bash
pip install -r requirements.txt
```

Set environment variable which should be:
```bash
export PYTHONPATH=$PYTHONPATH:/the/path/to/amazon-sp-api-course/project/directory
```

Running the code from a specific directory, for example FeedsAPI, needs to add this directory to the PYTHONPATH environment variable too. This is indicated by the Readme.md file located in such a directory.

## Prepare .env file
Create a .env file.
Copy the contents of .env.example file and fill it with your credentials:
```bash
lwa_app_id=''
lwa_client_secret=''
refresh_token=''

order_id=''
seller_id=''

# Needed for Notifications API:
AWS_SQS_NAME=''
AWS_EVENTBRIDGE_DESTINATION_NAME=''
AWS_SQS_ARN=''
ACCOUNT_ID=''
```
## What the repository offers
We have made an effort to demonstrate the handling of various endpoints on the basis of specific use cases. For example, we use the searchCatalogItems operation to calculate the average weight of products that appear as search results for selected keywords.

In ReportsAPI, scripts can be run either in ‘create report’ or ‘download report’ mode - depending on whether you specify a report identifier or leave it empty. In addition, in the ReportsAPI, you can set the report options to suit your needs (in the <input part>).

In FeedsAPI, there are also two modes of running the script available - either to create the feed or to retrieve the result of the feed creation (to check whether the feed was created successfully). The Feeds API itself offers many possibilities, but currently there are two types of feeds available in the repository: POST_PRODUCT_PRICING_DATA (to update product’s price) and POST_INVENTORY_AVAILABILITY_DATA (to update product’s inventory).

## Django Amazon OAuth App
```bash
# To run the app, you need to migrate the database and run the server
./manage.py migrate
./manage.py runserver

```
