from ._client import GetimgAutoreg


def autoreg_api_key() -> str:
    with GetimgAutoreg() as getimg_client:
        getimg_client.register_account()
        getimg_client.activate_account()
        api_key = getimg_client.get_api_key()
        return api_key
