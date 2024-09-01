from typing import List, Dict
import aiohttp

class YandexSpellerService:
    async def check_spelling(self, text: str) -> List[Dict[str, any]]:
        """
        Проверяет орфографию текста и возвращает список ошибок и исправленный текст.
        """
        url = "https://speller.yandex.net/services/spellservice.json/checkText"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    params={"text": text},
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Error: Received status code {response.status}")
                    
                    result = await response.json()
                    
        except aiohttp.ClientError as e:
            raise Exception(f"Network error: {str(e)}")
        except aiohttp.ContentTypeError:
            raise Exception("Error: Received invalid JSON response")

        return [
            {
                'word': error.get('word'),
                'suggestions': error.get('s', [])
            }
            for error in result if error.get('word')
        ]

 
    
