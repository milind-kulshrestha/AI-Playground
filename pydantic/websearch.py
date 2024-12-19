import os
import exa_py
from datetime import datetime, timedelta
import requests

EXA_API_KEY = os.environ.get('EXA_API_KEY')

class websearch_exa:
    def __init__(self, exa_api_key: str = EXA_API_KEY):
        """Initialize the websearch_exa class.

        Args:
            exa_api_key (str): The API key for Exa (optional).
        """
        self.exa = exa_py.Exa(exa_api_key)

    def get_search_results(self, queries: list[str], links_per_query: int = 2) -> list:
        """Retrieve search results for a list of queries.

        Args:
            queries (list[str]): A list of search queries.
            links_per_query (int): The number of links to retrieve per query.

        Returns:
            list: A list of search results.
        """
        results = []
        for query in queries:
            search_response = self.exa.search_and_contents(query,
                num_results=links_per_query,
                use_autoprompt=False
            )
            results.extend(search_response.results)
        return results

    def get_similar_pages(self, input_url: str, num_results: int = 10, num_sentences: int = 2) -> list:
        """Get similar pages for a given URL.

        Args:
            input_url (str): The URL to find similar pages for.
            num_results (int): The number of similar pages to retrieve.
            num_sentences (int): The number of sentences to highlight.

        Returns:
            list: A list of similar pages.
        """
        search_response = self.exa.find_similar_and_contents(
            input_url,
            highlights={"num_sentences":num_sentences},
            num_results=num_results)
        return search_response

    
    def get_linkedin(self, name: str, school: str = '') -> str:
        """Retrieve LinkedIn profile URL from a name and optional school.

        Args:
            name (str): The name of the person.
            school (str): The school of the person (optional).

        Returns:
            str: The LinkedIn profile URL or None if not found.
        """
        query = f"{name} {school}"
        keyword_search = self.exa.search(query, num_results=1, type="keyword", include_domains=['linkedin.com'])

        if keyword_search.results:
            result = keyword_search.results[0]
            return result.url
        print(f"No LinkedIn found for: {name}")
        return None

    def get_tweet_embed(tweet_url):
        oembed_url = f"https://publish.twitter.com/oembed?url={tweet_url}&hide_thread=true"
        response = requests.get(oembed_url)
        if response.status_code == 200:
            return response.json()['html']
        else:
            return None

    def search_twitter(self, query: str, num_results: int = 10, start_published_date: str = None) -> list:
        """Search for tweets related to a specific query.

        Args:
            query (str): The search query for tweets.
            num_results (int): The number of tweets to retrieve.
            start_published_date (str): The date to filter tweets from (optional).

        Returns:
            list: A list of search results related to the query.
        """
        include_domains = ["twitter.com", "x.com"]
        if start_published_date is None:
            start_published_date = (datetime.now() - timedelta(days=30)).isoformat()

        search_response = self.exa.search_and_contents(
            query,
            include_domains=include_domains,
            num_results=num_results,
            use_autoprompt=True,
            text=True,
            start_published_date=start_published_date
        )
        return search_response.results


#websearch = websearch_exa()
#print("LinkedIn:", websearch.get_linkedin_from_name('Milind Kulshrestha'))
