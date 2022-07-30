import requests
import json
from bs4 import BeautifulSoup 
import time

blockchain_tx_base = 'https://etherscan.io/tx/'

def get_records(wal_addr)->list:
    global blockchain_tx_base

    c_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
    }
    c_api_key = 'YOUR KEY'

    results = []

    timestamp = str(int(time.time() - 60)) # get the timestamp 1 min ago

    try:
        # get block number from timestamp
        response = requests.get('https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp=' + timestamp + '&closest=before&apikey=' + c_api_key, headers = c_headers)
        block_num = json.loads(response.text).get('result')

        target_wallet_addr = wal_addr

        response = requests.get('https://api.etherscan.io/api?module=account&action=txlist' +
                                '&address=' + target_wallet_addr + 
                                '&startblock=' + block_num + '&endblock=99999999&page=1&offset=10&sort=asc' +
                                '&apikey=' + c_api_key,
                                headers = c_headers)

        records = json.loads(response.text).get('result')
 
        for i in range(len(records)):

            tx = records[i].get('hash')

            response = requests.get(blockchain_tx_base + tx, headers = c_headers)
            soup = BeautifulSoup(response.text, 'lxml')
            html_text = soup.get_text()

            if 'swapExactTokensForTokens' in html_text or '0x414bf389' in html_text:

                action = ''

                for idx in range(html_text.find('Transaction Action'), len(html_text)):
                    if html_text[idx] != '\n':
                        action += html_text[idx]
                    else:
                        break
                # for

                # Tanslate to Mandarin
                action = action.replace('Swap', '將 ').replace('For', ' 交換成 ').replace('On', ' 於 ')
                action = action[action.find('於'):] + '，' + action[action.find('將'):action.find('於') - 1] + '@' + blockchain_tx_base + tx

                results.append(action)
            # if
        # for
        return results
    # try
    except:
        return results
# get_records()
