# Youtube-Listener

This project is a video synchronization service that fetches the latest videos related to a specified topic from YouTube and stores them in a local database. This README provides an overview of the functionalities and endpoints available in this application.

## Local Setup

### Virtual Environment
1. Clone repo and navigate to project root.

```
python3 -m venv .venv
```
2. activate the virtual environment
```
source .venv/bin/activate
```
### Install Dependencies
We will be using poetry to install the packages.

4. Navigate to the project directory (if not already) and Run `make setup` to install dependencies and packages.

### Database Setup
1. Previous command should have created `.env` file, populate it with relevant fields. No need to change `SECRET_KEY`.
2. Setup the db credentials in the `.env` following the example in `.env.example`. I'm using redditMQ for my celery broker and results of celery can be stored in table of choice.
3. create a table for the django project using psql in terminal
```createdb -U abhi -h localhost yt_listener ``` db name can be your choice. please use your db credentials for this command.
4. Run `make db` to migrate changes to db.
5. Add API keys separated by a comma to use with the app.
6. I have left my keys for an example.

### Run the server and celery task

You will need to open three terminals, after that
- start django server using `python3 manage.py runserver`
- start celery broker using `celery -A yt_listener worker -l info  --pool=solo`
- start celery scheduler using `celery -A yt_listener beat -l info`

## Optimisations made

- Used bulk create when storing data in db of the records of video data. refer `api.services.sync.video.syncRecordsToDB`
- stores 10,000 entries at once.
- created indexes using `video_id` and `channel_id`
- used unique constraint on the combination of video_id and channel_id fields. This constraint prevents duplicate videos (with the same video_id and channel_id) from being inserted into the database. The name attribute is used to define the name of the constraint in the database.

## Key Features

### Pagination
The list API is fully paginated with a default page size of 10. This prevents fetching all results from the DB at once. Helpful when the list API have to get a lot of rows.
### Api with proper filters.
The `localhost:8000/api/search/` is configured to accept params that can be used to filter the data. Helpful for using in dashboard

### Supports Multiple Youtube API KEYS
- The yt api keys can be added in .env file, separated by commas, which allows the script to switch to next key when quota of one key is exhausted.
- The cost of a search list request is 100 units and we have around 10k units for a day.

## API Spec

### List Video Data (GET)
- endpoint = `localhost:8000/api/search/`
- fetches data from the db in a paginated response containing 10 items per page. It contains links to next and previous pages along with the video data payload.

- query_params can be added in the request to filter data, they are:
    - video_id (string):- returns response containing the details of the specific video found using video_id

    - channel_id (string) :- returns response containing the details of the videos found using channel_id.
    - channel_title (string) :- returns response containing the details of the videos found using channel_title.

    from_date (epoch format):- takes in a date value and returns videos published after from_date.
    to_date (epoch format):- takes in a date value adn returns videos published till to_date.

    Example of a curl request with few params
    ```bash
    curl --location 'localhost:8000/api/search/?channel_title=cricbaziwithalpesh&from_date=1711042727&video_id=DgAm0CS66xc'```

### Add task to queue forcefully (POST)
- endpoint = `localhost:8000/api/trigger-fetch-yt/`
- simply adds task to celery broker to hit youtube api and fetch data and store it in db.
```bash
curl --location --request POST 'localhost:8000/api/trigger-fetch-yt/'```
