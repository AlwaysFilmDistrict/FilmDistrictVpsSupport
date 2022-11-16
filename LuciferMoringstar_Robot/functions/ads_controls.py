import aiohttp, logging
from configs import ADS_WEB_API, ADS_WEB_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

async def get_shortlink(link):
    url = f"{URL_SHORTNER_WEBSITE}/api"
    params = {
     'api': URL_SHORTNER_WEBSITE_API,
     'url': link,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            if data["status"] == "success":
                return data['shortenedUrl']
            else:
                return f"Error: {data['message']}"
