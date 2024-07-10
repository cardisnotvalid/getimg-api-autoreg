# Getimg API Autoreg

`getimg_api_autoreg` ‒ это простая библиотека на Python для получения API ключа путем автоматической регистрации на сайте генерации изображений [Dashboard Getimg](https://dashboard.getimg.ai/).

## Установка

Вы можете установить библиотеку с помощью pip:

```bash
$ pip install git+https://github.com/cardisnotvalid/getimg-api-autoreg
```

### Зависимости

- `disposablemail` ‒ библиотека для работы с временным почтовым сервисом. Подробнее с ней можно ознакомиться по ссылке [disposablemail](https://github.com/cardisnotvalid/disposablemail-api).

## Использование

```python
from getimg_api_autoreg import autoreg_api_key

api_key = autoreg_api_key()
print(api_key)
```

Этот код автоматически зарегистрируется на сайте Getimg и выведет полученный API ключ.

## Лицензия

Этот проект лицензируется в соответствии с условиями [LICENSE](LICENSE).
