# Game prediction

Run all the analysis.ipynb file's cells then `flask --app app run --debug` to start the API.

You'll then have access to:

* `http://127.0.0.1:5000/category_to_games`: This endpoint is about recommending games from a chosen category.

* `http://127.0.0.1:5000/games_prediction`: On this endpoint you can chose video games from a list and you'll have a list of 10 recommended games based on their steam tags. 