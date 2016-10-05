m = {u'_text': u'g\u0142o\u015bno\u015b\u0107 80',
     u'entities': {u'intent': [{u'confidence': 0.9976977303950855,
                                u'value': u'set_volume'}],
                   u'value': [{u'confidence': 0.7869300663111243,
                               u'suggested': True,
                               u'type': u'value',
                               u'value': u'80'}]},
     u'msg_id': u'c61357ce-ef77-4d85-9195-1ffa404896e1'}

m2 = {u'_text': u'musisz 55',
      u'entities': {u'intent': [{u'confidence': 0.5197958326992627,
                                u'value': u'set_volume'}],
                    u'value': [{u'confidence': 0.8307277847045514,
                                u'type': u'value',
                                u'value': u'55'}]},
      u'msg_id': u'a84b08c2-748d-45a4-8c04-139de404b254'}

print(str(m2['entities']['value'][0]['value']))
