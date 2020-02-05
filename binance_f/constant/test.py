import os
if(os.path.exists("binance_f/privateconfig.py")):
    from binance_f.privateconfig import *
    g_api_key = p_api_key
    g_secret_key = p_secret_key
else:
    g_api_key = "57b9858d-f489-41a0-91b9-b926742b30be"
    g_secret_key = "61792E270589F5ACEE74259EE584FFA6"


g_account_id = 12345678



