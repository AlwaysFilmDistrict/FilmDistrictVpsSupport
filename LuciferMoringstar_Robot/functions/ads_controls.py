import aiohttp, logging
from configs import ADS_WEB_API, ADS_WEB_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

async def get_shortlink(link):
    https = link.split(":")[0]
    if "https" == https:
        https = "https"
        link = link.replace("http", https)
    url = ADS_WEB_URL
    params = {'api': ADS_WEB_API,
              'url': link,
              }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                data = await response.json()
                if data["status"] == "success":
                    return data['shortenedUrl']
                else:
                    logger.error(f"Error: {data['message']}")
                    return f'https://{ADS_WEB_URL}/api?api={ADS_WEB_API}&link={link}'

    except Exception as e:
        logger.error(e)
        return f'{ADS_WEB_URL}/api?api={ADS_WEB_API}&link={link}'

