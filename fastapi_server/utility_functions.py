import aiofiles.os as aos
import aiofiles
import aiohttp
import constants
import pathlib



async def dowload_file(file_id, shop_id=6808139269, bot_token=constants.TG_API_KEY): #TODO const.DEFAULT_SHOP
    async with aiohttp.ClientSession() as session:
        file_info = await session.request('get', f'{constants.TELEGRAM_API_ENDPOINT}bot{bot_token}/getFile?file_id={file_id}')
        jsoned = await file_info.json()

        if jsoned['ok']:
            file_path: str = jsoned['result']['file_path']
            path = file_path.split('/')[0]
            ext = file_path.split('/')[-1].split('.')[-1]
            uniq = jsoned['result']['file_unique_id']
            file_obj = await session.request('get', f'{constants.TELEGRAM_API_ENDPOINT}file/bot{bot_token}/{file_path}')
            file = await file_obj.read()
            await aos.makedirs(f'files/{shop_id}/{path}', exist_ok=True)
            async with aiofiles.open(f'files/{shop_id}/{path}/{uniq}.{ext}', "wb+") as f:
                res = await f.write(file) # TODO  success ? ... : ...
                return f'images/{shop_id}/{uniq}.{ext}'
        else:
            return ''






