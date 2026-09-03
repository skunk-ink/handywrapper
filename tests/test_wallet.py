import json as jsonlib

import responses
import pytest

BASE = 'http://x:testkey@127.0.0.1:12039'

# Each case: (method, kwargs, http_verb, path, extra)
REST_CASES = [
    ('createWallet', {'passphrase': 'p', 'id': 'w1'}, 'PUT', '/wallet/w1', {'body': {'watchOnly': False}}),
    ('resetAuthToken', {'passphrase': 'p', 'id': 'w1'}, 'POST', '/wallet/w1/retoken', {}),
    ('getWalletInfo', {'id': 'w1'}, 'GET', '/wallet/w1', {}),
    ('getMasterHDKey', {'id': 'w1'}, 'GET', '/wallet/w1/master', {}),
    ('changePassword', {'new_passphrase': 'n', 'id': 'w1'}, 'POST', '/wallet/w1/passphrase', {}),
    ('signTransaction', {'passphrase': 'p', 'tx_hex': 'hex', 'id': 'w1'}, 'POST', '/wallet/w1/sign', {}),
    ('sendTransaction', {'id': 'w1', 'passphrase': 'p', 'address': 'addr', 'value': 1},
     'POST', '/wallet/w1/send', {'body': {'outputs': [{'address': 'addr', 'value': 1}]}}),
    ('createTransaction', {'id': 'w1', 'passphrase': 'p', 'address': 'addr', 'value': 1},
     'POST', '/wallet/w1/create', {'body': {'outputs': [{'address': 'addr', 'value': 1}]}}),
    ('zapTransactions', {'account': 'default', 'id': 'w1', 'age': 10}, 'POST', '/wallet/w1/zap',
     {'body': {'account': 'default', 'age': 10}}),
    ('lockWallet', {'id': 'w1'}, 'POST', '/wallet/w1/lock', {}),
    ('unlockWallet', {'passphrase': 'p', 'id': 'w1'}, 'POST', '/wallet/w1/unlock', {}),
    ('importPublicKey', {'account': 'default', 'public_key': 'pk', 'id': 'w1'}, 'POST', '/wallet/w1/import', {}),
    ('importPrivateKey', {'account': 'default', 'private_key': 'pk', 'id': 'w1'}, 'POST', '/wallet/w1/import', {}),
    # Bug-fix regression: originally hardcoded '/wallet/watchonly1/import', ignoring `id`.
    ('importAddress', {'account': 'default', 'address': 'addr', 'id': 'w1'}, 'POST', '/wallet/w1/import', {}),
    ('getBlocksWithWalletTX', {'id': 'w1'}, 'GET', '/wallet/w1/block', {}),
    ('getWalletBlockByHeight', {'height': 1, 'id': 'w1'}, 'GET', '/wallet/w1/block/1', {}),
    # Bug-fix regression: originally hardcoded '/wallet/multisig3/shared-key/', ignoring `id`.
    ('addXPubKey', {'account_key': 'k', 'id': 'w1'}, 'PUT', '/wallet/w1/shared-key', {}),
    ('removeXPubKey', {'account_key': 'k', 'id': 'w1'}, 'DELETE', '/wallet/w1/shared-key', {}),
    ('getPublicKeyByAddress', {'address': 'addr', 'id': 'w1'}, 'GET', '/wallet/w1/key/addr', {}),
    ('getPrivateKeyByAddress', {'address': 'addr', 'passphrase': 'p', 'id': 'w1'}, 'GET', '/wallet/w1/wif/addr',
     {'params': {'passphrase': 'p'}}),
    ('generateReceivingAddress', {'account': 'default', 'id': 'w1'}, 'POST', '/wallet/w1/address', {}),
    ('generateChangeAddress', {'id': 'w1'}, 'POST', '/wallet/w1/change', {}),
    ('getBalance', {'id': 'w1'}, 'GET', '/wallet/w1/balance', {}),
    ('listCoins', {'id': 'w1'}, 'GET', '/wallet/w1/coin', {}),
    ('lockCoinOutpoints', {'tx_hash': 'h', 'id': 'w1'}, 'PUT', '/wallet/w1/locked/h/0', {}),
    ('unlockCoinOutpoints', {'tx_hash': 'h', 'id': 'w1'}, 'DELETE', '/wallet/w1/locked/h/0', {}),
    ('getLockedOutpoints', {'id': 'w1'}, 'GET', '/wallet/w1/locked', {}),
    ('getWalletCoin', {'tx_hash': 'h', 'id': 'w1'}, 'GET', '/wallet/w1/coin/h/0', {}),
    # Bug-fix regression: originally hit the nonexistent '/_rescan/' path.
    ('walletRescan', {'height': 1}, 'POST', '/rescan', {'body': {'height': 1}}),
    ('adminResend', {}, 'POST', '/resend', {}),
    ('walletResend', {'id': 'w1'}, 'POST', '/wallet/w1/resend', {}),
    ('walletBackup', {'path': '/tmp'}, 'POST', '/backup', {}),
    ('walletMasterHDKeyBackup', {'id': 'w1'}, 'GET', '/wallet/w1/master', {}),
    ('listWallets', {}, 'GET', '/wallet/', {}),
    ('getWalletAccountList', {'id': 'w1'}, 'GET', '/wallet/w1/account', {}),
    ('getAccountInfo', {'id': 'w1'}, 'GET', '/wallet/w1/account/default', {}),
    ('createAccount', {'passphrase': 'p', 'id': 'w1', 'account': 'acc1'}, 'PUT', '/wallet/w1/account/acc1', {}),
    ('modifyAccount', {'account': 'acc1', 'id': 'w1', 'lookahead': 5}, 'PATCH', '/wallet/w1/account/acc1',
     {'body': {'lookahead': 5}}),
    ('getWalletTxDetails', {'id': 'w1', 'tx_hash': 'h'}, 'GET', '/wallet/w1/tx/h', {}),
    ('deleteTransaction', {'id': 'w1', 'tx_hash': 'h'}, 'DELETE', '/wallet/w1/tx/h', {}),
    # Breaking change (hsd v7): now paginated via query params instead of a bare GET.
    ('getWalletTxHistory', {'id': 'w1', 'limit': 10, 'reverse': True, 'after': 'h'}, 'GET', '/wallet/w1/tx/history',
     {'params': {'limit': '10', 'reverse': 'true', 'after': 'h'}}),
    ('getPendingTransactions', {'id': 'w1', 'limit': 10}, 'GET', '/wallet/w1/tx/unconfirmed', {'params': {'limit': '10'}}),
    ('getWalletNames', {'id': 'w1'}, 'GET', '/wallet/w1/name', {}),
    # Breaking change (hsd v8): 'own' filter param added.
    ('getWalletName', {'name': 'n', 'id': 'w1', 'own': True}, 'GET', '/wallet/w1/name/n', {'params': {'own': 'true'}}),
    ('getWalletAuctions', {'id': 'w1'}, 'GET', '/wallet/w1/auction', {}),
    ('getWalletAuctionByName', {'name': 'n', 'id': 'w1'}, 'GET', '/wallet/w1/auction/n', {}),
    ('getWalletBids', {'id': 'w1'}, 'GET', '/wallet/w1/bid', {}),
    ('getWalletBidsByName', {'name': 'n', 'id': 'w1'}, 'GET', '/wallet/w1/bid/n', {}),
    ('getWalletReveals', {'id': 'w1'}, 'GET', '/wallet/w1/reveal', {}),
    ('getWalletRevealsByName', {'name': 'n', 'id': 'w1'}, 'GET', '/wallet/w1/reveal/n', {}),
    # Bug-fix regression: originally hit '/wallet/<id>/resource', never including `name`.
    ('getWalletResourceByName', {'name': 'n', 'id': 'w1'}, 'GET', '/wallet/w1/resource/n', {}),
    # Bug-fix regression: originally hit '/nounce/' (typo) instead of '/nonce/'.
    ('getNonceForBid', {'bid': 1.0, 'name': 'n', 'address': 'addr', 'id': 'w1'}, 'GET', '/wallet/w1/nonce/n',
     {'params': {'address': 'addr'}}),
    ('sendOPEN', {'id': 'w1', 'passphrase': 'p', 'name': 'n'}, 'POST', '/wallet/w1/open', {}),
    ('sendBID', {'id': 'w1', 'passphrase': 'p', 'name': 'n', 'bid': 1, 'lockup': 2}, 'POST', '/wallet/w1/bid', {}),
    ('createAuction', {'id': 'w1', 'passphrase': 'p', 'name': 'n', 'bid': 1, 'lockup': 2}, 'POST', '/wallet/w1/auction', {}),
    ('sendREVEAL', {'id': 'w1', 'passphrase': 'p'}, 'POST', '/wallet/w1/reveal', {}),
    ('sendREDEEM', {'id': 'w1', 'passphrase': 'p'}, 'POST', '/wallet/w1/redeem', {}),
    ('sendUPDATE', {'id': 'w1', 'passphrase': 'p', 'name': 'n', 'data': {'a': 1}}, 'POST', '/wallet/w1/update',
     {'body': {'data': {'a': 1}}}),
    ('sendRENEW', {'id': 'w1', 'passphrase': 'p', 'name': 'n'}, 'POST', '/wallet/w1/renewal', {}),
    ('sendTRANSFER', {'id': 'w1', 'passphrase': 'p', 'name': 'n', 'address': 'addr'}, 'POST', '/wallet/w1/transfer', {}),
    ('cancelTRANSFER', {'id': 'w1', 'passphrase': 'p', 'name': 'n'}, 'POST', '/wallet/w1/cancel', {}),
    ('sendFINALIZE', {'id': 'w1', 'passphrase': 'p', 'name': 'n'}, 'POST', '/wallet/w1/finalize', {}),
    ('sendREVOKE', {'id': 'w1', 'passphrase': 'p', 'name': 'n'}, 'POST', '/wallet/w1/revoke', {}),
    ('deepClean', {}, 'POST', '/deepclean', {'body': {'I_HAVE_BACKED_UP_MY_WALLET': False}}),
    ('recalculateBalances', {}, 'POST', '/recalculate-balances', {}),
]

RPC_CASES = [
    ('rpc_getNames', {}, 'getnames'),
    ('rpc_getAuctionInfo', {'name': 'n'}, 'getauctioninfo'),
    ('rpc_getBIDS', {}, 'getbids'),
    ('rpc_getREVEALS', {}, 'getreveals'),
    ('rpc_sendOPEN', {'name': 'n'}, 'sendopen'),
    ('rpc_sendBID', {'name': 'n', 'bid_amount': 1, 'lockup_blind': 2}, 'sendbid'),
    ('rpc_sendREVEAL', {}, 'sendreveal'),
    ('rpc_sendREDEEM', {}, 'sendredeem'),
    ('rpc_sendUPDATE', {'name': 'n', 'data': {'a': 1}}, 'sendupdate'),
    ('rpc_sendRENEWAL', {'name': 'n'}, 'sendrenewal'),
    ('rpc_sendTRANSFER', {'name': 'n', 'address': 'a'}, 'sendtransfer'),
    ('rpc_sendFINALIZE', {'name': 'n'}, 'sendfinalize'),
    ('rpc_sendCANCEL', {'name': 'n'}, 'sendcancel'),
    ('rpc_sendREVOKE', {'name': 'n'}, 'sendrevoke'),
    ('rpc_importNONCE', {'name': 'n', 'address': 'a', '_bidValue': 1}, 'importnonce'),
    ('rpc_createOPEN', {'name': 'n'}, 'createopen'),
    ('rpc_createBID', {'name': 'n', 'bid_amount': 1, 'lockup_blind': 2, 'account': 'a'}, 'createbid'),
    ('rpc_createREVEAL', {}, 'createreveal'),
    ('rpc_createREDEEM', {}, 'createredeem'),
    ('rpc_createUPDATE', {'name': 'n', 'data': {'a': 1}}, 'createupdate'),
    ('rpc_createRENEWAL', {'name': 'n'}, 'createrenewal'),
    ('rpc_createTRANSFER', {'name': 'n', 'address': 'a'}, 'createtransfer'),
    ('rpc_createFINALIZE', {'name': 'n'}, 'createfinalize'),
    ('rpc_createCANCEL', {'name': 'n'}, 'createcancel'),
    ('rpc_createREVOKE', {'name': 'n'}, 'createrevoke'),
    ('rpc_createBatch', {'actions': [['OPEN', 'n']]}, 'createbatch'),
    ('rpc_sendBatch', {'actions': [['OPEN', 'n']]}, 'sendbatch'),
    ('rpc_importName', {'name': 'n'}, 'importname'),
    ('rpc_selectWallet', {'wallet_id': 'w1'}, 'selectwallet'),
    ('rpc_getWalletInfo', {}, 'getwalletinfo'),
    ('rpc_fundRawTransaction', {'tx_hex': 'hex'}, 'fundrawtransaction'),
    ('rpc_resendWalletTransactions', {}, 'resendwallettransactions'),
    ('rpc_abandonTransaction', {'tx_id': 'id'}, 'abandontransaction'),
    ('rpc_backupWallet', {'path': '/tmp'}, 'backupwallet'),
    ('rpc_dumpPrivKey', {'address': 'a'}, 'dumpprivkey'),
    ('rpc_dumpWallet', {'path': '/tmp'}, 'dumpwallet'),
    ('rpc_encryptWallet', {'passphrase': 'p'}, 'encryptwallet'),
    ('rpc_getAccountAddress', {}, 'getaccountaddress'),
    ('rpc_getAccount', {'address': 'a'}, 'getaccount'),
    ('rpc_getAddressesByAccount', {}, 'getaddressesbyaccount'),
    ('rpc_getBalance', {}, 'getbalance'),
    ('rpc_getNewAddress', {}, 'getnewaddress'),
    ('rpc_getRawChangeAddress', {}, 'getrawchangeaddress'),
    ('rpc_getReceivedByAccount', {'account': 'a'}, 'getreceivedbyaccount'),
    ('rpc_getReceivedByAddress', {'address': 'a'}, 'getreceivedbyaddress'),
    ('rpc_getTransaction', {'tx_id': 'id'}, 'gettransaction'),
    ('rpc_getUnconfirmedBalance', {}, 'getunconfirmedbalance'),
    ('rpc_importPrivKey', {'private_key': 'pk'}, 'importprivkey'),
    ('rpc_importWallet', {'wallet_file': 'f'}, 'importwallet'),
    # Bug-fix regression: originally sent {"method": "importwallet", ...} (copy-paste bug).
    ('rpc_importAddress', {'address': 'a'}, 'importaddress'),
    ('rpc_importPrunedFunds', {'tx_hex': 'hex', 'tx_out_proof': 'p'}, 'importprunedfunds'),
    ('rpc_importPubKey', {'public_hex_key': 'k'}, 'importpubkey'),
    ('rpc_listAccounts', {}, 'listaccounts'),
    ('rpc_lockUnspent', {}, 'lockunspent'),
    ('rpc_listLockUnspent', {}, 'listlockunspent'),
    ('rpc_listReceivedByAccount', {}, 'listreceivedbyaccount'),
    ('rpc_listReceivedByAddress', {}, 'listreceivedbyaddress'),
    ('rpc_listSinceBlock', {}, 'listsinceblock'),
    ('rpc_listTransactions', {}, 'listtransactions'),
    ('rpc_listHistory', {}, 'listhistory'),
    ('rpc_listHistoryAfter', {'account': 'a', 'txid': 'h'}, 'listhistoryafter'),
    ('rpc_listHistoryByTime', {'account': 'a', 'timestamp': 1}, 'listhistorybytime'),
    ('rpc_listUnconfirmed', {}, 'listunconfirmed'),
    ('rpc_listUnconfirmedAfter', {'account': 'a', 'txid': 'h'}, 'listunconfirmedafter'),
    ('rpc_listUnconfirmedByTime', {'account': 'a', 'timestamp': 1}, 'listunconfirmedbytime'),
    ('rpc_listUnspent', {}, 'listunspent'),
    ('rpc_sendFrom', {'from_account': 'a', 'to_address': 'b', 'amount': 1}, 'sendfrom'),
    ('rpc_sendMany', {'from_account': 'a', 'outputs': {'addr': 1}}, 'sendmany'),
    ('rpc_createSendToAddress', {'to_address': 'a', 'amount': 1}, 'createsendtoaddress'),
    ('rpc_sendToAddress', {'to_address': 'a', 'amount': 1}, 'sendtoaddress'),
    ('rpc_setTxFee', {}, 'settxfee'),
    ('rpc_signMessage', {'address': 'a', 'message': 'm'}, 'signmessage'),
    ('rpc_signMessageWithName', {'name': 'n', 'message': 'm'}, 'signmessagewithname'),
    ('rpc_walletLock', {}, 'walletlock'),
    ('rpc_walletPasswordChange', {'old_passphrase': 'o', 'new_passphrase': 'n'}, 'walletpassphrasechange'),
    ('rpc_walletPassphrase', {'passphrase': 'p'}, 'walletpassphrase'),
    ('rpc_removePrunedFunds', {'tx_id': 'id'}, 'removeprunedfunds'),
    ('rpc_getMemoryInfo', {}, 'getmemoryinfo'),
    ('rpc_setLogLevel', {}, 'setloglevel'),
    ('rpc_stop', {}, 'stop'),
]


@pytest.mark.parametrize('method,kwargs,verb,path,extra', REST_CASES)
def test_wallet_rest_endpoint(hsw_client, method, kwargs, verb, path, extra):
    with responses.RequestsMock() as rsps:
        rsps.add(getattr(responses, verb), BASE + path, json={'ok': True}, status=200)
        getattr(hsw_client, method)(**kwargs)

        req = rsps.calls[0].request
        assert req.method == verb
        assert req.url.split('?')[0] == BASE + path

        if 'params' in extra:
            for key, val in extra['params'].items():
                assert f'{key}={val}' in req.url

        if 'body' in extra:
            sent = jsonlib.loads(req.body)
            for key, val in extra['body'].items():
                assert sent[key] == val


@pytest.mark.parametrize('method,kwargs,rpc_method', RPC_CASES)
def test_wallet_rpc_method(hsw_client, method, kwargs, rpc_method):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, BASE + '/', json={'result': None}, status=200)
        getattr(hsw_client, method)(**kwargs)

        req = rsps.calls[0].request
        assert req.method == 'POST'
        assert req.url == BASE + '/'

        sent = jsonlib.loads(req.body)
        assert sent['method'] == rpc_method


def test_get_range_of_transactions_removed(hsw_client):
    # hsd v7 removed GET /wallet/:id/tx/range entirely; the dead method must not come back.
    assert not hasattr(hsw_client, 'getRangeOfTransactions')


@pytest.mark.parametrize('method,kwargs,expected_params', [
    # Bug-fix regression: hsd's listhistory/listunconfirmed RPC family takes flat
    # positional params (account, limit, reverse) or (account, cursor, limit,
    # reverse) -- NOT (account, {limit, reverse}). Found via live testing: hsd
    # rejected the options-object shape with "Param #1 must be a int."
    ('rpc_listHistory', {'account': 'default'}, ['default']),
    ('rpc_listHistory', {'account': 'default', 'limit': 5}, ['default', 5]),
    ('rpc_listHistory', {'account': 'default', 'reverse': True}, ['default', None, True]),
    ('rpc_listHistoryAfter', {'account': 'default', 'txid': 'h'}, ['default', 'h']),
    ('rpc_listHistoryAfter', {'account': 'default', 'txid': 'h', 'limit': 5, 'reverse': True}, ['default', 'h', 5, True]),
    ('rpc_listHistoryByTime', {'account': 'default', 'timestamp': 100}, ['default', 100]),
    ('rpc_listUnconfirmed', {'account': 'default'}, ['default']),
    ('rpc_listUnconfirmed', {'account': 'default', 'limit': 5}, ['default', 5]),
    ('rpc_listUnconfirmedAfter', {'account': 'default', 'txid': 'h'}, ['default', 'h']),
    ('rpc_listUnconfirmedByTime', {'account': 'default', 'timestamp': 100}, ['default', 100]),
    # Bug-fix regression: an empty-string account isn't hsd's "all accounts"
    # sentinel -- hsd looks up an account literally named '' and 404s with
    # "Account not found." hsd's own CLI/RPC convention for "all accounts" is
    # the literal string '*', which the default must produce.
    ('rpc_listHistory', {}, ['*']),
    ('rpc_listUnconfirmed', {}, ['*']),
])
def test_history_rpc_uses_positional_params(hsw_client, method, kwargs, expected_params):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, BASE + '/', json={'result': None}, status=200)
        getattr(hsw_client, method)(**kwargs)

        sent = jsonlib.loads(rsps.calls[0].request.body)
        assert sent['params'] == expected_params


def test_create_wallet_omits_unset_key_fields(hsw_client):
    # Bug-fix regression: createWallet used to always send accountKey/master/mnemonic
    # as '' when not provided. hsd's watch-only account path does
    # `if (typeof key === 'string') key = HDPublicKey.fromBase58(key)` unconditionally
    # once accountKey is a string at all, so an empty string crashes hsd's base58
    # decoder with a 500 "Out of bounds read" instead of cleanly omitting the field.
    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT, BASE + '/wallet/w1', json={'ok': True}, status=200)
        hsw_client.createWallet(passphrase='p', id='w1')

        sent = jsonlib.loads(rsps.calls[0].request.body)
        assert 'accountKey' not in sent
        assert 'master' not in sent
        assert 'mnemonic' not in sent
        assert sent['watchOnly'] is False


def test_create_wallet_passphrase_is_optional(hsw_client):
    # hsd genuinely treats `passphrase` as optional (omitting it creates an
    # unencrypted wallet) -- the Python signature must allow that too, not
    # force every caller to supply one.
    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT, BASE + '/wallet/w1', json={'ok': True}, status=200)
        hsw_client.createWallet(id='w1')

        sent = jsonlib.loads(rsps.calls[0].request.body)
        assert 'passphrase' not in sent


@pytest.mark.parametrize('method,kwargs,expected_params', [
    # Bug-fix regression: hsd's create*/covenant RPCs reject an empty-string
    # `account` with "Invalid type for database key" (found live: an actual
    # rpc_createREVEAL call 500'd this way). The account positional param
    # must be omitted entirely when not given, not sent as ''.
    ('rpc_createOPEN', {'name': 'n'}, ['n']),
    ('rpc_createOPEN', {'name': 'n', 'account': 'default'}, ['n', 'default']),
    ('rpc_createREVEAL', {}, ['']),
    ('rpc_createREVEAL', {'name': 'n', 'account': 'default'}, ['n', 'default']),
    ('rpc_createREDEEM', {}, ['']),
    ('rpc_createUPDATE', {'name': 'n', 'data': {'a': 1}}, ['n', {'a': 1}]),
    ('rpc_createUPDATE', {'name': 'n', 'data': {'a': 1}, 'account': 'default'}, ['n', {'a': 1}, 'default']),
    ('rpc_createRENEWAL', {'name': 'n'}, ['n']),
    ('rpc_createTRANSFER', {'name': 'n', 'address': 'a'}, ['n', 'a']),
    ('rpc_createFINALIZE', {'name': 'n'}, ['n']),
    ('rpc_createCANCEL', {'name': 'n'}, ['n']),
    ('rpc_createREVOKE', {'name': 'n'}, ['n']),
])
def test_create_rpc_omits_unset_account(hsw_client, method, kwargs, expected_params):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, BASE + '/', json={'result': None}, status=200)
        getattr(hsw_client, method)(**kwargs)

        sent = jsonlib.loads(rsps.calls[0].request.body)
        assert sent['params'] == expected_params


def test_create_account_omits_unset_account_key(hsw_client):
    # Same bug, same fix, on the account-creation endpoint.
    with responses.RequestsMock() as rsps:
        rsps.add(responses.PUT, BASE + '/wallet/w1/account/acc1', json={'ok': True}, status=200)
        hsw_client.createAccount(passphrase='p', id='w1', account='acc1')

        sent = jsonlib.loads(rsps.calls[0].request.body)
        assert 'accountKey' not in sent
