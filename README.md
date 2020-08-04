# fooddata

Download, build, and query the USDA food database.

Do you know what you are putting in your body?

## Installation

```shell script
$ pip install fooddata --upgrade
```

## Usage

```shell script
$ fooddata build
```

```shell script
$ fooddata query "SELECT * from foods WHERE category_id IS NOT NULL LIMIT 100;" --json | jq .
```

```shell script
$ fooddata query "SELECT * from foods WHERE category_id IS NOT NULL LIMIT 100;" --json > output2.json
```

```shell script
$ fooddata query "SELECT * from food_nutrients_v WHERE food_type IS NOT NULL AND food_category IS NOT NULL LIMIT 1000;" --json | jq .
```

## Update Database

To update the database, just run the first command again:

```shell script
$ fooddata build
```

## Note

The data comes from the USDA website:
[https://fdc.nal.usda.gov/download-datasets.html](https://fdc.nal.usda.gov/download-datasets.html)
