import aiohttp, logging
from configs import ADS_WEB_API, ADS_WEB_URL

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

async def get_shortlink(link):
    url = f"{ADS_WEB_URL}"
    params = {
     'api': ADS_WEB_API,
     'url': link,
     'format': 'json'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                data = await response.json(content_type='text/html')
                if data["status"] == "success":
                    return data['shortlink']
                else:
                    logger.error(f"Error: {data['message']}")
                    return f'https://api.shareus.in/directLink?token={ADS_WEB_API}&link={link}'

    except Exception as e:
        logger.error(e)
        return f'https://api.shareus.in/directLink?token={ADS_WEB_API}&link={link}'
