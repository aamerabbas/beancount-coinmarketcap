# Coinmarketcap price source for Beancount

If you use the beancount cli accounting tool (http://furius.ca/beancount/), this price source will let you fetch cryptocurrency prices from coinmarketcap.com. This tool works by scraping the website rather than using the API.

This is **only** intended for personal use and not for scraping at scale. Coinmarketcap will likely block you if you query too frequently and, for this reason, the code is set by default to query no more than 1 time per second. I encourage you to be a good internet citizen and not go any quicker than that or use this tool for anything but limited personal use.

To use this you should:
1. Start by adding the "price_sources" folder here into some location defined in your $PYTHONPATH
2. Go to the commodity definition of your cryptocurrency and add a "price" attribute to refer to this price source. For example, for bitcoin you would add _USD:price_sources.coinmarketcap/bitcoin_
3. You should now be able to use the bean-price tool to fetch prices!

On step 2, please note that the last part that says "bitcoin" is based on the URL used to get the historical prices, not the ticker symbol (in that example, the URL is https://coinmarketcap.com/currencies/bitcoin/historical-data/).
