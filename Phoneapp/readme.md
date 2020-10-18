# Design

The most challenging requirement is to be able to search by phone number prefix on hundreds of millions of records. This suggests using a database capable of storing this data in tries (prefix trees) for quick retrieval. It is also necessary to push the heavy lifting to the database itself, rather than processing the data in API services.

For my design I have chosen to use an indexed table in a SQLite databse for my design because:
 - Traditional SQL database b-tree indexes store data in prefix tree format, as we require
 - They typically have acceptable efficiency in query for string prefixes by b-tree index
 - They are mature, robust products and will not present unexpected difficulties doing create/read/update/delete or administration and maintenance
 - They have a standardized API and the specific data technology used is easily replaceable

Other architectural choices are not so impactful. I have used 2 standard RESTful json services for the data layer and the API layer, and I have implemented them in python with flask. I have allowed the database to create an auto-incremented customer ID.

The data API, in accordance with the above, pushes all the work to the database, and the API layer is a thin wrapper on it, doing little more than some more informative error reporting and validation in this version.

The data layer search function is restricted to 100 results, and the API layer search is restricted to 10.

## Data layer - Create customer
---|---
Url|POST /customer/create
Posted data|{"customerName": "<string 1-200 chars>", "customerPhoneNumber": "<11 digits>"}
Action|validate input, insert customer record in SQL database
Response|200 OK

## Data layer - Customer search by phone prefix 
---|---
Url|GET /customer/search-by-phone-prefix
Query string|phonePrefix=<prefix string>, (optional) maxResults=<integer>
Action|validate input, treat maxResults as 100 if it is missing, <=0 or >100, perform search, return top results ordered by phone number (via SQL query)
Response|list of {"customerId": <int>, "customerName": <string>, "customerPhoneNumber": <string>}

## API layer - Create customer
---|---
Url|POST /phoneAPI/create-customer
Posted data|{"customerName": "<string 1-200 chars>", "customerPhoneNumber": "<11 digits>"}
Action|invoke data API to create customer
Response|200 OK, or informative validation error message

## API layer - Customer search by phone prefix
---|---
Url|GET /customer/search-by-phone-prefix
Query string|phonePrefix=<prefix string>, (optional) maxResults=<integer>
Action|validate input, treat maxResults as 10 if it is missing, <=0 or >10, invoke data API, return results
Response|list of {"customerId": <int>, "customerName": <string>, "customerPhoneNumber": <string>}

# How to run
Apologies, haven't had time to dockerize this.

 - install python 3 and run its command prompt
 - `pip install -r requirements.txt`
 - `flask init-db` to initialize the database
 - `flask run` to run the web service (it'll run on port 5000)

I have also provided a test suite that can be run with `flask smash-db` - this will populate the databse with >20 million records, then run a query on it and measure how long it takes. On my machine it's 4 seconds.

