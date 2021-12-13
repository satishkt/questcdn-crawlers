# questcdn-crawlers

Scrapy project to set up crawlers for the Quest CDN project.

To setup on local machine do the following

1. Clone the git repository and checkout the develop branch. That has the latest and the most stable code.
2. On a new python virtual environment run pip install -r requirements.txt
3. Create a database with a schema in mysql.
4. Run the insert script [data_aggregator_agent_inserts.sql](sql/data_aggregator_agent_inserts.sql) to insert the
   allowed urls into the agent table. Modify the schema name if needed.
5. Update the [settings.py](questcdn/settings.py) CONNECTION_URL string to reflect the database properties.
6. Download and install geckodriver for your OS from [here](https://github.com/mozilla/geckodriver/releases)
7. Update the variables FIREFOX_PATH and GECKODRIVER_PATH in [settings.py](questcdn/settings.py) to reflect the actual
   values on your machine.
8. From the top level folder run scrapy crawl planet_bid_spider.
9. You should see console logs, and an entry in the agent_tracking table.