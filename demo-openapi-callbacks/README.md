How to show in OpenAPI the schema of your callback requests?

Run `main.py` with:

    pip install fastapi "pydantic>=2.0" uvicorn
    uvicorn main:app --reload

Then go to http://127.0.0.1:8000/docs#/callbacks/post__request_body__webhook_url_

You'll see the callback URL and how it displays the Union of all kinds of schema.

Here's a screenshot of how the callback schema appears in the OpenAPI UI:

![OpenAPI Callback Union Schema](callback-union.jpeg)
