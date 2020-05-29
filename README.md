redacto
============
This project defines a webservice that takes PDFs and extracts de-identified data

.
# To run locally

In the base directory, create and activate a virtual environment, per
https://virtualenv.pypa.io/en/stable/user_guide.html

Once set up, run 
```pip install -r app/requirements.txt```
to install dependencies.

Finally to start up the service, run  
```python app/app.py```

We should see logs, ending with  
``` * Running on http://localhost:5000/```

We can now run `curl` commands to get de-identified data:

```
curl --location --request POST 'http://localhost:5000/request' \
--header 'Content-Type: application/pdf' \
--data-binary '@test/example1.pdf'
```

would return

```json
{
    "billing_loc": {
        "City": "London",
        "Country": "United Kingdom",
        "PostalCode": "27475",
        "Region": "England"
    },
    "date_placed": "February 25, 2017",
    "date_shipped": "February 16, 2017",
    "id": "140-2475861-372856",
    "items": [
        {
            "condition": "New",
            "name": "AmazonBasics Wand",
            "price": 108.0,
            "quantity": 1,
            "sold_by": "Amazon.com Services LLC"
        }
    ],
    "order_total": 109.33,
    "payment_method": "Visa",
    "shipping_loc": {
        "City": "London",
        "Country": "United Kingdom",
        "PostalCode": "27475",
        "Region": "England"
    },
    "shipping_speed": "Standard Shipping"
}
```

#Future actions

* Debug and fix pdfminer.six import in docker.
* Have the service write to CSV, or other formats.
* This only works for similar format PDFs. To generalize this, we would need to think slightly different about the algorithm presented here.
* If this service were to be deployed to AWS, we'd recommend this be re-written into a Lambda function. That would allow some architectural flexibility, 
for example having it invoked by write of target files to S3, and final files be written to a different data store, potentially.
