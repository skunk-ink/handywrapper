import responses
import pytest

BASE = 'http://x:testkey@127.0.0.1:12037'

# Each case: (method, kwargs, http_verb, path, extra)
# extra may contain 'params' (expected query dict subset) or 'rpc_method' (expected
# JSON-RPC "method" field for calls hitting POST /).
REST_CASES = [
    ('getInfo', {}, 'GET', '/', {}),
    ('getMemPool', {}, 'GET', '/mempool', {}),
    # hsd's query-string validator requires lowercase 'true'/'false', not Python's str(True).
    ('getMemPoolInvalid', {'verbose': True}, 'GET', '/mempool/invalid', {'params': {'verbose': 'true'}}),
    ('getMemPoolInvalidHash', {'tx_hash': 'abc'}, 'GET', '/mempool/invalid/abc', {}),
    ('getBlockByHashOrHeight', {'block_hash_or_height': '100'}, 'GET', '/block/100', {}),
    ('getHeaderByHashOrHeight', {'header_hash_or_height': '100'}, 'GET', '/header/100', {}),
    ('broadcast', {'tx_hex': 'deadbeef'}, 'POST', '/broadcast/', {'body': {'tx': 'deadbeef'}}),
    ('broadcastClaim', {'claim': 'deadbeef'}, 'POST', '/claim/', {'body': {'claim': 'deadbeef'}}),
    ('getFeeEstimate', {'blocks': 6}, 'GET', '/fee', {'params': {'blocks': '6'}}),
    ('reset', {'height': 100}, 'POST', '/reset', {'body': {'height': 100}}),
    # Bug-fix regression: was '/coin/' + <builtin hash> + '/' + tx_hash + '/' + index (3 segments, TypeError).
    ('getCoinByHashIndex', {'tx_hash': 'abc', 'index': 3}, 'GET', '/coin/abc/3', {}),
    ('getCoinByAddress', {'address': 'addr1'}, 'GET', '/coin/address/addr1', {}),
    ('getCoinsByAddresses', {'addresses': ['a', 'b']}, 'POST', '/coin/address', {'body': {'addresses': ['a', 'b']}}),
    ('getTxByHash', {'tx_hash': 'abc'}, 'GET', '/tx/abc', {}),
    ('getTxByAddress', {'address': 'addr1'}, 'GET', '/tx/address/addr1', {}),
    ('getTXsByAddresses', {'addresses': ['a', 'b']}, 'POST', '/tx/address', {'body': {'addresses': ['a', 'b']}}),
]

RPC_CASES = [
    ('rpc_stop', {}, 'stop'),
    ('rpc_getInfo', {}, 'getinfo'),
    ('rpc_getMemoryInfo', {}, 'getmemoryinfo'),
    ('rpc_setLogLevel', {'log_level': 'DEBUG'}, 'setloglevel'),
    # Bug-fix regression: originally sent {"validateaddress": "", ...} instead of {"method": "validateaddress", ...}.
    ('rpc_validateAddress', {'address': 'addr1'}, 'validateaddress'),
    ('rpc_createMultiSig', {'nrequired': 2, 'key_dict': 'keys'}, 'createmultisig'),
    ('rpc_signMessageWithPrivKey', {'private_key': 'pk', 'message': 'm'}, 'signmessagewithprivkey'),
    ('rpc_verifyMessage', {'address': 'a', 'signature': 's', 'message': 'm'}, 'verifymessage'),
    ('rpc_verifyMessageWithName', {'name': 'n', 'signature': 's', 'message': 'm'}, 'verifymessagewithname'),
    ('rpc_setMockTime', {'timestamp': 100}, 'setmocktime'),
    ('rpc_pruneBlockchain', {}, 'pruneblockchain'),
    # Bug-fix regression: originally sent {"method": "", ...} (empty method name).
    ('rpc_invalidateBlock', {'block_hash': 'h'}, 'invalidateblock'),
    ('rpc_reconsiderBlock', {'block_hash': 'h'}, 'reconsiderblock'),
    ('rpc_getBlockchainInfo', {}, 'getblockchaininfo'),
    ('rpc_getBestBlockHash', {}, 'getbestblockhash'),
    ('rpc_getBlockCount', {}, 'getblockcount'),
    ('rpc_getBlock', {'block_hash': 'h'}, 'getblock'),
    ('rpc_getBlockByHeight', {'block_height': 1}, 'getblockbyheight'),
    ('rpc_getBlockHash', {'block_height': 1}, 'getblockhash'),
    ('rpc_getBlockHeader', {'block_hash': 'h'}, 'getblockheader'),
    ('rpc_getChainTips', {}, 'getchaintips'),
    ('rpc_getDifficulty', {}, 'getdifficulty'),
    ('rpc_getMemPoolInfo', {}, 'getmempoolinfo'),
    ('rpc_getMemPoolAncestors', {'tx_hash': 'h'}, 'getmempoolancestors'),
    ('rpc_getMemPoolDescendants', {'tx_hash': 'h'}, 'getmempooldescendants'),
    ('rpc_getMemPoolEntry', {'tx_hash': 'h'}, 'getmempoolentry'),
    ('rpc_getRawMemPool', {}, 'getrawmempool'),
    ('rpc_prioritiseTransaction', {'tx_hash': 'h', 'priority_delta': 1, 'fee_delta': 1}, 'prioritisetransaction'),
    ('rpc_estimateFee', {}, 'estimatefee'),
    ('rpc_estimatePriority', {}, 'estimatepriority'),
    ('rpc_estimateSmartFee', {}, 'estimatesmartfee'),
    ('rpc_estimateSmartPriority', {}, 'estimatesmartpriority'),
    ('rpc_getTxOut', {'tx_hash': 'h', 'index': 0}, 'gettxout'),
    ('rpc_getTxOutSetInfo', {}, 'gettxoutsetinfo'),
    ('rpc_getRawTransaction', {'tx_hash': 'h'}, 'getrawtransaction'),
    ('rpc_decodeRawTransaction', {'raw_tx': 'hex'}, 'decoderawtransaction'),
    ('rpc_decodeScript', {'script': 'hex'}, 'decodescript'),
    ('rpc_sendRawTransaction', {'raw_tx': 'hex'}, 'sendrawtransaction'),
    ('rpc_createRawTransaction', {'tx_hash': 'h', 'tx_index': 0, 'address': 'a', 'amount': 1, 'data': 'd'}, 'createrawtransaction'),
    ('rpc_signRawTransaction', {'raw_tx': 'hex', 'tx_hash': 'h', 'tx_index': 0, 'address': 'a', 'amount': 1, 'private_key': 'pk'}, 'signrawtransaction'),
    ('rpc_getTxOutProof', {'tx_id_list': 'id'}, 'gettxoutproof'),
    ('rpc_verifyTxOutProof', {'proof': 'p'}, 'verifytxoutproof'),
    ('rpc_getNetworkHashPerSec', {}, 'getnetworkhashps'),
    ('rpc_getMiningInfo', {}, 'getmininginfo'),
    # Bug-fix regression: originally sent {"method": "getworklp", ...} (copy-paste from rpc_getWorkLP).
    ('rpc_getWork', {}, 'getwork'),
    ('rpc_getWorkLP', {}, 'getworklp'),
    ('rpc_getBlockTemplate', {}, 'getblocktemplate'),
    ('rpc_submitBlock', {'block_data': 'd'}, 'submitblock'),
    ('rpc_verifyBlock', {'block_data': 'd'}, 'verifyblock'),
    ('rpc_setGenerate', {}, 'setgenerate'),
    ('rpc_getGenerate', {}, 'getgenerate'),
    ('rpc_generate', {}, 'generate'),
    ('rpc_generateToAddress', {'address': 'a'}, 'generatetoaddress'),
    ('rpc_getConnectionCount', {}, 'getconnectioncount'),
    ('rpc_ping', {}, 'ping'),
    ('rpc_getPeerInfo', {}, 'getpeerinfo'),
    ('rpc_addNode', {'node_address': 'a', 'cmd': 'add'}, 'addnode'),
    ('rpc_disconnectNode', {'node_address': 'a'}, 'disconnectnode'),
    ('rpc_getAddedNodeInfo', {'node_address': 'a'}, 'getaddednodeinfo'),
    ('rpc_getNetTotals', {}, 'getnettotals'),
    ('rpc_getNetworkInfo', {}, 'getnetworkinfo'),
    ('rpc_setBan', {'node_address': 'a', 'cmd': 'add'}, 'setban'),
    ('rpc_listBan', {}, 'listbanned'),
    ('rpc_clearBanned', {}, 'clearbanned'),
    ('rpc_getNameInfo', {}, 'getnameinfo'),
    ('rpc_getNameByHash', {}, 'getnamebyhash'),
    ('rpc_getNameResource', {}, 'getnameresource'),
    ('rpc_getNameProof', {}, 'getnameproof'),
    ('rpc_sendRawClaim', {'base64_string': 'b'}, 'sendrawclaim'),
    ('rpc_getDnsSecProof', {}, 'getdnssecproof'),
    ('rpc_sendRawAirdrop', {}, 'sendrawairdrop'),
    ('rpc_grindName', {}, 'grindname'),
]


@pytest.mark.parametrize('method,kwargs,verb,path,extra', REST_CASES)
def test_node_rest_endpoint(hsd_client, method, kwargs, verb, path, extra):
    with responses.RequestsMock() as rsps:
        rsps.add(getattr(responses, verb), BASE + path, json={'ok': True}, status=200)
        getattr(hsd_client, method)(**kwargs)

        req = rsps.calls[0].request
        assert req.method == verb
        assert req.url.split('?')[0] == BASE + path

        if 'params' in extra:
            for key, val in extra['params'].items():
                assert f'{key}={val}' in req.url

        if 'body' in extra:
            import json
            sent = json.loads(req.body)
            for key, val in extra['body'].items():
                assert sent[key] == val


@pytest.mark.parametrize('method,kwargs,rpc_method', RPC_CASES)
def test_node_rpc_method(hsd_client, method, kwargs, rpc_method):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, BASE + '/', json={'result': None}, status=200)
        getattr(hsd_client, method)(**kwargs)

        req = rsps.calls[0].request
        assert req.method == 'POST'
        assert req.url == BASE + '/'

        import json
        sent = json.loads(req.body)
        assert sent['method'] == rpc_method
