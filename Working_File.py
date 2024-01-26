# Dependencies
import requests
import time
from dotenv import load_dotenv
import os
import pandas as pd
import json

# Set environment variables from the .env in the local environment
load_dotenv()


nyt_api_key = os.getenv("NYT_API_KEY")
tmdb_api_key = os.getenv("TMDB_API_KEY")

if not nyt_api_key or not tmdb_api_key:
    print("Error: API keys not loaded properly.")
    # Optionally, raise an exception or exit the script


# Set the base URL
url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"

# Filter for movie reviews with "love" in the headline
# section_name should be "Movies"
# type_of_material should be "Review"
filter_query = 'section_name:"Movies" AND type_of_material:"Review" AND headline:"love"'

# Use a sort filter, sort by newest
sort = "newest"

# Select the following fields to return:
# headline, web_url, snippet, source, keywords, pub_date, byline, word_count
field_list = "headline,web_url,snippet,source,keywords,pub_date,byline,word_count"

# Search for reviews published between a begin and end date
begin_date = "20130101"
end_date = "20230531"

# Build URL
query_url = f"{url}api-key={nyt_api_key}&fq={filter_query}&sort={sort}&begin_date={begin_date}&end_date={end_date}&fl={field_list}"

print(query_url)

# Set the base URL
url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"

# Filter for movie reviews with "love" in the headline
# section_name should be "Movies"
# type_of_material should be "Review"
filter_query = 'section_name:"Movies" AND type_of_material:"Review" AND headline:"love"'

# Use a sort filter, sort by newest
sort = "newest"

# Select the following fields to return:
# headline, web_url, snippet, source, keywords, pub_date, byline, word_count
field_list = "headline,web_url,snippet,source,keywords,pub_date,byline,word_count"

# Search for reviews published between a begin and end date
begin_date = "20130101"
end_date = "20230531"

# Build URL
query_url = f"{url}api-key={nyt_api_key}&fq={filter_query}&sort={sort}&begin_date={begin_date}&end_date={end_date}&fl={field_list}"

print(query_url)

# Create an empty list to store the reviews
reviews_list = []

# Loop through pages 0-19
for page in range(0, 20):
    # Create query with a page number
    query_url = f"{url}api-key={nyt_api_key}&fq={filter_query}&sort={sort}&fl={field_list}&begin_date={begin_date}&end_date={end_date}&page={page}"

    try:
        # Make a GET request and retrieve the JSON
        response = requests.get(query_url).json()

        # Loop through the reviews["response"]["docs"] and append each review to the list
        reviews = response["response"]["docs"]
        reviews_list.extend(reviews)

        # Print the page that was just retrieved
        print(f"Retrieved page {page}")

    except Exception as e:
        # Print the page number that had no results then break from the loop
        print(f"Error retrieving page {page}: {e}")
        break

    # Add a twelve-second interval between queries to stay within API query limits
    time.sleep(12)

# You can then inspect the first few entries of your reviews_list
print(json.dumps(reviews_list[:5], indent=4))  # Prints the first 5 reviews

# Preview the first 5 results in JSON format
# Use json.dumps with argument indent=4 to format data
print(json.dumps(reviews_list[:5], indent=4))

# Convert reviews_list to a Pandas DataFrame
reviews_df = pd.json_normalize(reviews_list)

# Display the first few rows of the DataFrame to verify
print(reviews_df.head())

# Extract the movie title and save to a new column "title"
reviews_df['title'] = reviews_df['headline.main'].apply(lambda st: st[st.find("\u2018")+1:st.find("\u2019")] if " Review" in st else None)

# Display the first few rows to verify the new column
print(reviews_df[['headline.main', 'title']].head())

# Extract 'name' and 'value' from items in "keywords" column
def extract_keywords(keyword_list):
    extracted_keywords = ""
    for item in keyword_list:
        # Extract 'name' and 'value'
        keyword = f"{item['name']}: {item['value']};" 
        # Append the keyword item to the extracted_keywords list
        extracted_keywords += keyword
    return extracted_keywords

# Fix the "keywords" column by converting cells from a list to a string
reviews_df["keywords"] = reviews_df["keywords"].apply(extract_keywords)
print(reviews_df.head())

# Extract the movie title and save to a new column "title"
reviews_df['title'] = reviews_df['headline.main'].apply(
    lambda st: st[st.find("\u2018")+1:st.find("\u2019")] if "\u2018" in st and "\u2019" in st and " Review" in st else None
)

# Create a list of movie titles from the "title" column
titles_list = reviews_df['title'].to_list()

# Print the list
print(titles_list)


