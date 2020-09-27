#################################
# bot for game 'Рейд на монстров' simple stupid game (https://vk.com/app6759871?cid=0&queue=1&sid=0)
#################################

import requests
import json
import time
url = 'https://79ce.playfabapi.com/Client/LoginWithCustomID?sdk=JavaScriptSDK-1.58.191218' #api's need to update every time or script wont work 
url2 = 'https://79ce.playfabapi.com/Client/ExecuteCloudScript?sdk=JavaScriptSDK-1.58.191218'
login_payload = '{TitleId: "79CE", CustomId: "f3cc8222332e0264ab399810383f1d21", CreateAccount: true}'
get_pvp_payload = '{"FunctionName":"getPvPOpponent","RevisionSelection":"Specific","SpecificRevision":56,"FunctionParameter":null}'

headers = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8'}

answer = requests.post(url, data=login_payload, headers=headers)
print(answer)
response = answer.json()
print(response)


headers2 = {'Content-type': 'application/json',  # Определение типа данных
           'Accept': 'text/plain',
           'Content-Encoding': 'utf-8',
            'X-Authorization': response['data']['SessionTicket']}

reset_payload = '{"FunctionName":"resetPvPLootBox","RevisionSelection":"Specific","SpecificRevision":56,"FunctionParameter":null}'

answer2 = requests.post(url2, data=reset_payload, headers=headers2)
#print(answer2)
response2 = answer2.json()
print(response2)


i = 0
while(i < 200):
    answer2 = requests.post(url2, data=get_pvp_payload, headers=headers2)
    #print(answer2)
    response2 = answer2.json()
    #print(response2)

    enemy_playfabid = response2['data']['FunctionResult']['PlayFabId']
    enemy_socialdata_json  = response2['data']['FunctionResult']['socialData']

    enemy_socialdata=json.loads(enemy_socialdata_json)

    enemy_name = enemy_socialdata['response'][0]['first_name']
    enemy_lastname = enemy_socialdata['response'][0]['last_name']
    enemy_id = enemy_socialdata['response'][0]['id']
    enemy_boardposition = response2['data']['FunctionResult']['Position']

    finish_pvp_payload = '{"FunctionName":"finishPvPBattle","RevisionSelection":"Specific","SpecificRevision":56,"FunctionParameter":{"status":1,"opponentPlayFabId":"' + enemy_playfabid + '","socialId":321938513}}'

    answer2 = requests.post(url2, data=finish_pvp_payload, headers=headers2)
    #print(answer2)
    response2 = answer2.json()
    #print(response2)
    pvp_score = response2['data']['FunctionResult']['pvpScore']
    print(f"Enemy: {enemy_name} {enemy_lastname} id={enemy_id} on positon {enemy_boardposition} defated: score is {pvp_score}; {enemy_playfabid} ")
    i += 1
    time.sleep(1.0)
