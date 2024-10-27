#Scraper for <ecoventure.ch>

## Architecture

The scraper uses pydantic.BaseModel as the data model for Project. Each scraper for a specific website consists of a directory in sites/. the command line interface ```scrape.py``` can be used to test and develop scrapers. Run ```./scrape.py list``` to see which scrapers are in sites. To develop a new scraper create a new directory in sites/ and in that a new python script. The python script should contain a ```main()``` function that returns a ```list[Project]```. To run the script use for example:

```./scrape.py run econeers```

Each scraper has it's own ```pydantic.BaseModel``` which greatly helps parsing json data and validating it. A quick approach is to have a ```convert()``` method of this data model, that converts to a ```Project```. See existing scrapers in sites. For example [/sites/econeers/main.py](/sites/econeers/main.py) .
