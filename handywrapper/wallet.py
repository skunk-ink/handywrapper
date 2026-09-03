from ._http import HTTPClient


def _compact(d):
    return {k: v for k, v in d.items() if v is not None}


class hsw(HTTPClient):

    def __init__(self, api_key:str, ip_address:str='127.0.0.1', port:int=12039, timeout:int=30):
        """
        DESCRIPTION:

            Initialization of the hsw class

        PARAMS:

        (*) Denotes required argument

        (*) api_key    : HSW API key.

        ( ) ip_address : HSW node ip. Default = '127.0.0.1'.

        ( ) port       : HSW node port. Default = 12039

        ( ) timeout    : Request timeout in seconds. Default = 30
        """

        super().__init__(api_key, ip_address, port, timeout)
    ### END METHOD ################################### __init__(self, api_key:str, ip_address:str='127.0.0.1', port:int=12039, timeout:int=30):

    def createWallet(self, passphrase:str, id:str='primary', account_key:str=None, type:str='pubkeyhash',
                    mnemonic:str=None, master:str=None, watch_only:bool=False, m:int=1, n:int=1):
        """
        DESCRIPTION:

            Create a new wallet with a specified ID.

        PARAMS:

            (*) Denotes required argument

            (*) id          : Wallet ID (used for storage).

            ( ) type        : Type of wallet (pubkeyhash, multisig). Default is 'pubkeyhash'

            ( ) master      : Master HD key. If not present, it will be generated.

            ( ) mnemonic    : A mnemonic phrase to use to instantiate an hd private key. One will be generated if none provided.

            ( ) m           : 'm' value for multisig (m-of-n).

            ( ) n           : 'n' value for multisig (m-of-n)

            (*) passphrase  : A strong passphrase used to encrypt the wallet.

            ( ) watch_only  : Whether to create a watch-only wallet. Default = False

            ( ) account_key : The extended public key for the primary account in the new wallet.
                              Required if watch_only is True; ignored otherwise. Sending an empty
                              string here crashes hsd's key decoder, so it's omitted unless given.
        """

        body = _compact({
            'passphrase': passphrase,
            'watchOnly': watch_only,
            'accountKey': account_key,
            'type': type,
            'master': master,
            'm': m,
            'n': n,
            'mnemonic': mnemonic,
        })
        return self.put(f'/wallet/{id}', body)
    ### END METHOD ################################### createWallet(self, id:str='primary', passphrase:str, account_key:str=None, type:str='pubkeyhash',
    #                                                               mnemonic:str=None, master:str=None, watch_only:bool=False, m:int=1, n:int=1)

    def resetAuthToken(self, passphrase:str, id:str='primary'):
        """
        DESCRIPTION:

            Create a new wallet with a specified ID.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : A strong passphrase used to encrypt the wallet.
        """

        return self.post(f'/wallet/{id}/retoken', {'passphrase': passphrase})
    ### END METHOD ################################### resetAuthToken(self, id:str='primary', passphrase:str)

    def getWalletInfo(self, id:str=''):
        """
        DESCRIPTION:

            Get wallet info by ID. If no id is passed in the CLI it assumes an id of primary.

        PARAMS:

            (*) Denotes required argument

            ( ) id : Name of the wallet whose info you would like to retrieve.
        """

        return self.get(f'/wallet/{id}')
    ### END METHOD ################################### getWalletInfo(self, id:str='')

    def getMasterHDKey(self, id:str='primary'):
        """
        DESCRIPTION:

            Get wallet master HD key. This is normally censored in the
            wallet info route.The provided API key must have admin access.

        PARAMS:

            (*) Denotes required argument

            (*) id : Name of the wallet whose info you would like to retrieve.
        """

        return self.get(f'/wallet/{id}/master')
    ### END METHOD ################################### getMasterHDKey(self, id:str='')

    def changePassword(self, new_passphrase:str, id:str='primary', old_passphrase:str=''):
        """
        DESCRIPTION:

            Change wallet passphrase. Encrypt if unencrypted.

        PARAMS:

            (*) Denotes required argument

            (*) id             : Wallet ID.

            ( ) old_passphrase : Old passphrase. Pass in empty string if none.

            (*) new_passphrase : New passphrase.
        """

        return self.post(f'/wallet/{id}/passphrase', {'old': old_passphrase, 'passphrase': new_passphrase})
    ### END METHOD ################################### changePassword(self, id:str='primary', new_passphrase:str, old_passphrase:str='')

    def signTransaction(self, passphrase:str, tx_hex:str, id:str='primary'):
        """
        DESCRIPTION:

            Sign a templated transaction (useful for multisig).

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            (*) tx_hex     : The (hex) of the transaction you would like to sign.
        """

        return self.post(f'/wallet/{id}/sign', {'tx': tx_hex, 'passphrase': passphrase})
    ### END METHOD ################################### signTransaction(self, id:str='primary', passphrase:str, tx_hex:str)

    def sendTransaction(self, id:str, passphrase:str, rate:int=None, value:float=None, address:str=None, smart:bool=None,
                        blocks:int=None, max_fee:int=None, hard_fee:int=None, subtract_fee:bool=None,
                        subtract_index:int=None, selection:str=None, depth:int=None):
        """
        Description:

            Create, sign, and send a transaction.

        Params:

            (*) Denotes required argument

            (*) id             : Account to use for transaction.

            (*) passphrase     : Passphrase to unlock the account.

            ( ) rate           : The rate for transaction fees. Denominated in subunits per kb.

            ( ) value          : Value to send in subunits (or whole HNS, see warning above).

            ( ) address        : Destination address for transaction.

            ( ) smart          : Whether or not to choose smart coins, will also used unconfirmed transactions.

            ( ) blocks         : Number of blocks to use for fee estimation.

            ( ) max_fee        : Maximum fee you're willing to pay.

            ( ) hard_fee       : Set an exact fee for the transaction.

            ( ) subtract_fee   : Whether to subtract fee from outputs (evenly).

            ( ) subtract_index : Subtract only from specified output index.

            ( ) selection      : How to select coins ('value', 'age', 'all', 'sweepdust', 'db-value', 'db-age', 'db-all', 'db-sweepdust').

            ( ) depth          : Number of confirmation for coins to spend.
        """

        body = _compact({
            'passphrase': passphrase,
            'rate': rate,
            'outputs': [{'address': address, 'value': value}] if address is not None else None,
            'smart': smart,
            'blocks': blocks,
            'maxFee': max_fee,
            'hardFee': hard_fee,
            'subtractFee': subtract_fee,
            'subtractIndex': subtract_index,
            'selection': selection,
            'depth': depth,
        })
        return self.post(f'/wallet/{id}/send', body)
    ### END METHOD ################################### def sendTransaction(self, id:str, new_passphrase:str, old_passphrase:str='')

    def createTransaction(self, id:str, passphrase:str, rate:int=None, value:float=None, address:str=None, smart:bool=None,
                        blocks:int=None, max_fee:int=None, hard_fee:int=None, subtract_fee:bool=None,
                        subtract_index:int=None, selection:str=None, depth:int=None):
        """
        Description:

            Create and template a transaction (useful for multisig). Does not broadcast or add to wallet.

        Params:

            (*) Denotes required argument

            (*) id             : Account to use for transaction.

            (*) passphrase     : Passphrase to unlock the account.

            ( ) rate           : The rate for transaction fees. Denominated in subunits per kb.

            ( ) value          : Value to send in subunits (or whole HNS, see warning above).

            ( ) address        : Destination address for transaction.

            ( ) smart          : Whether or not to choose smart coins, will also used unconfirmed transactions.

            ( ) blocks         : Number of blocks to use for fee estimation.

            ( ) max_fee        : Maximum fee you're willing to pay.

            ( ) hard_fee       : Set an exact fee for the transaction.

            ( ) subtract_fee   : Whether to subtract fee from outputs (evenly).

            ( ) subtract_index : Subtract only from specified output index.

            ( ) selection      : How to select coins ('value', 'age', 'all', 'sweepdust', 'db-value', 'db-age', 'db-all', 'db-sweepdust').

            ( ) depth          : Number of confirmation for coins to spend.
        """

        body = _compact({
            'passphrase': passphrase,
            'rate': rate,
            'outputs': [{'address': address, 'value': value}] if address is not None else None,
            'smart': smart,
            'blocks': blocks,
            'maxFee': max_fee,
            'hardFee': hard_fee,
            'subtractFee': subtract_fee,
            'subtractIndex': subtract_index,
            'selection': selection,
            'depth': depth,
        })
        return self.post(f'/wallet/{id}/create', body)
    ### END METHOD ################################### createTransaction(self, id:str, passphrase:str, rate:int=None, value:float=None, smart:bool=None, blocks:int=None, max_fee:int=None, subtract_fee:bool=None,
    #                                                                        subtract_index:int=None, selection:str='all', depth:int=None, address:str=''):

    def zapTransactions(self, account:str, id:str='primary', age:int=0):
        """
        DESCRIPTION:

            Remove all pending transactions older than a specified age.

        PARAMS:

            (*) Denotes required argument

            (*) id      : Wallet ID.

            ( ) account : Account to zap from.

            (*) age     : Age threshold to zap up to (seconds).
        """

        return self.post(f'/wallet/{id}/zap', {'account': account, 'age': age})
    ### END METHOD ################################### zapTransactions(self, account:str, id:str='primary', age:int=0)

    def lockWallet(self, id:str='primary'):
        """
        DESCRIPTION:

            If unlock was called, zero the derived AES key and revert to normal behavior.

        PARAMS:

            (*) Denotes required argument

            ( ) id : Name ID of wallet to lock.
        """

        return self.post(f'/wallet/{id}/lock')
    ### END METHOD ################################### lockWallet(self, id:str='primary')

    def unlockWallet(self, passphrase:str, timeout:int=60, id:str='primary'):
        """
        DESCRIPTION:

            Unlock the wallet, decrypting keys for the specified timeout period.

        PARAMS:

            (*) Denotes required argument

            (*) passphrase : Passphrase to unlock the wallet.

            ( ) timeout    : Number of seconds to keep the wallet unlocked. Default = 60

            ( ) id         : Name ID of wallet to unlock. Default = 'primary'
        """

        return self.post(f'/wallet/{id}/unlock', {'passphrase': passphrase, 'timeout': timeout})
    ### END METHOD ################################### unlockWallet(self, passphrase:str, timeout:int=60, id:str='primary')

    def importPublicKey(self, account:str, public_key:str, id:str='primary'):
        """
        DESCRIPTION:

            Import a standard (public) WIF key.

            A _rescan will be required to see any transaction history associated with the key.

            Note: Imported keys do not exist anywhere in the wallet's HD tree.They can be
                  associated with accounts but will not be properly backed up with only the
                  mnemonic.

        PARAMS:

            (*) Denotes required argument

            (*) id         : ID of target wallet to import key into.

            ( ) public_key : Hex encoded public key.
        """

        return self.post(f'/wallet/{id}/import', {'account': account, 'publicKey': public_key})
    ### END METHOD ################################### importPublicKey(self, account:str, public_key:str, id:str='primary')

    def importPrivateKey(self, account:str, private_key:str, id:str='primary'):
        """
        DESCRIPTION:

            Import a standard (private) WIF key.

            A _rescan will be required to see any transaction history associated with the key.

            Note: Imported keys do not exist anywhere in the wallet's HD tree.They can be
                  associated with accounts but will not be properly backed up with only the
                  mnemonic.

        PARAMS:

            (*) Denotes required argument

            (*) id          : ID of target wallet to import key into.

            ( ) private_key : Hex encoded public key.
        """

        return self.post(f'/wallet/{id}/import', {'account': account, 'privateKey': private_key})
    ### END METHOD ################################### importPrivateKey(self, account:str, private_key:str, id:str='primary')

    def importAddress(self, account:str, address:str, id:str='primary'):
        """
        Description:

            Import a Bech32 encoded address. Addresses (like public keys)
            can only be imported into watch-only wallets

            The HTTP endpoint is the same as for key imports.

        Params:

            (*) Denotes required argument

            (*) account : Account to import the address into.

            ( ) address : Hex encoded public key.

            ( ) id      : ID of target wallet to import address into. Default = 'primary'
        """

        return self.post(f'/wallet/{id}/import', {'account': account, 'address': address})
    ### END METHOD ################################### importAddress(self, account:str, address:str, id:str='primary')

    def getBlocksWithWalletTX(self, id:str='primary'):
        """
        DESCRIPTION:

            List all block heights which contain any wallet transactions. Returns an array of block heights.

        PARAMS:

            (*) Denotes required argument

            (*) id : Name of the wallet.
        """

        return self.get(f'/wallet/{id}/block')
    ### END METHOD ################################### getBlocksWithWalletTX(self, id:str='primary')

    def getWalletBlockByHeight(self, height:int, id:str='primary'):
        """
        DESCRIPTION:

            Get block info by height.

        PARAMS:

            (*) Denotes required argument

            (*) height : Height of block being queried.

            ( ) id     : Name of the wallet.
        """

        return self.get(f'/wallet/{id}/block/{height}')
    ### END METHOD ################################### getWalletBlockByHeight(self, height:int, id:str='primary')

    def addXPubKey(self, account_key:str, account:str='default', id:str='primary'):
        """
        DESCRIPTION:

            Add a shared xpubkey to wallet. Must be a multisig wallet.

            Note: Since it must be a multisig, the wallet on creation should
            be set with `m` and `n` where `n` is greater than 1 (since the first key
            is always that wallet's own xpubkey). Creating new addresses from
            this account will not be possible until `n` number of xpubkeys are
            added to the account.

            Response will return `addedKey: true` if key was added on this
            request. Returns `addedKey: false` if key already added, but
            will still return `success: true` with status `200`.

        PARAMS:

            (*) Denotes required argument

            (*) account_key : xpubkey to add to the multisig wallet.

            ( ) account     : Multisig account to add the xpubkey to (default='default').

            ( ) id          : ID of the multisig wallet. Default = 'primary'
        """

        return self.put(f'/wallet/{id}/shared-key', {'accountKey': account_key, 'account': account})
    ### END METHOD ################################### addXPubKey(self, account_key:str, account:str='default', id:str='primary')

    def removeXPubKey(self, account_key:str, account:str='default', id:str='primary'):
        """
        DESCRIPTION:

            Remove shared xpubkey from wallet if present.

            Response will return `removedKey: true` if key was removed on
            this request. Returns `removedKey: false` if key was already removed, but will
            still return `success: true` with status `200`.

            Note: Remove Key is only available to a multisig wallet that is
            not yet "complete" -- as in, `n-1` number of keys have not yet been
            added to the wallet's own original key. Once a multisig wallet
            has the right number of keys to create m-of-n addresses, this
            function will return an error

        PARAMS:

            (*) Denotes required argument

            (*) account_key : xpubkey to add to the multisig wallet.

            ( ) account     : Multisig account to remove the xpubkey from (default='default').

            ( ) id          : ID of the multisig wallet. Default = 'primary'
        """

        return self.delete(f'/wallet/{id}/shared-key', {'accountKey': account_key, 'account': account})
    ### END METHOD ################################### removeXPubKey(self, account_key:str, account:str='default', id:str='primary')

    def getPublicKeyByAddress(self, address:str, id:str='primary'):
        """
        DESCRIPTION:

            Get wallet key by address. Returns wallet information with address and public key.

        PARAMS:

            (*) Denotes required argument

            (*) address : Bech32 encoded address to get corresponding public key for.

            ( ) id      : Name of wallet.
        """

        return self.get(f'/wallet/{id}/key/{address}')
    ### END METHOD ################################### getPublicKeyByAddress(self, address:str, id:str='primary')

    def getPrivateKeyByAddress(self, address:str, passphrase:str, id:str='primary'):
        """
        DESCRIPTION:

            Get wallet private key (WIF format) by address. Returns just the private key.

        PARAMS:

            (*) Denotes required argument

            (*) address    : Address to get corresponding private key for.

            (*) passphrase : Passphrase of wallet.

            ( ) id         : Name of wallet.
        """

        return self.get(f'/wallet/{id}/wif/{address}', params={'passphrase': passphrase})
    ### END METHOD ################################### getPrivateKeyByAddress(self, address:str, passphrase:str, id:str='primary')

    def generateReceivingAddress(self, account:str, id:str='primary'):
        """
        DESCRIPTION:

            Derive new receiving address for account.

        PARAMS:

            (*) Denotes required argument

            (*) id       : Name of wallet.

            ( ) account  : BIP44 account to generate address from.
        """

        return self.post(f'/wallet/{id}/address', {'account': account})
    ### END METHOD ################################### generateReceivingAddress(self, account:str, id:str='primary')

    def generateChangeAddress(self, account:str='default', id:str='primary'):
        """
        DESCRIPTION:

            Derive new change address for account.

        PARAMS:

            (*) Denotes required argument

            ( ) id       : Name of wallet.

            ( ) account  : BIP44 account to generate address from. Default = 'defualt'
        """

        return self.post(f'/wallet/{id}/change', {'account': account})
    ### END METHOD ################################### generateChangeAddress(self, account:str='default', id:str='primary')

    def getBalance(self, account:str='', id:str='primary'):
        """
        DESCRIPTION:

            Get wallet or account balance. If no account option is passed,
            the call defaults to wallet balance (with account index of -1).
            Balance values for `unconfirmed` and `confirmed` are expressed in
            subunits.

        PARAMS:

            (*) Denotes required argument

            (*) account    : Address to get corresponding private key for.

            ( ) id         : Wallet ID.
        """

        return self.get(f'/wallet/{id}/balance', params={'account': account})
    ### END METHOD ################################### getBalance(self, account:str='', id:str='primary')

    def listCoins(self, id:str='primary'):
        """
        DESCRIPTION:

            List all wallet coins available.

        PARAMS:

            (*) Denotes required argument

            ( ) id : Wallet ID.
        """

        return self.get(f'/wallet/{id}/coin')
    ### END METHOD ################################### listCoins(self, id:str='primary')

    def lockCoinOutpoints(self, tx_hash:str, index:str='0', id:str='primary'):
        """
        DESCRIPTION:

            Lock outpoints.

        PARAMS:

            (*) Denotes required argument

            (*) tx_hash : Hash of transaction that created the outpoint.

            ( ) index   : Index of the output in the transaction being referenced. Default = '0'

            ( ) id      : ID of wallet that contains the outpoint. Default = 'primary'
        """

        return self.put(f'/wallet/{id}/locked/{tx_hash}/{index}')
    ### END METHOD ################################### lockCoinOutpoints(self, tx_hash:str, index:str='0', id:str='primary')

    def unlockCoinOutpoints(self, tx_hash:str, index:str='0', id:str='primary'):
        """
        DESCRIPTION:

            Unlock outpoints.

        PARAMS:

            (*) Denotes required argument

            (*) tx_hash : Hash of transaction that created the outpoint.

            ( ) index   : Index of the output in the transaction being referenced. Default = '0'

            ( ) id      : ID of wallet that contains the outpoint. Default = 'primary'
        """

        return self.delete(f'/wallet/{id}/locked/{tx_hash}/{index}')
    ### END METHOD ################################### unlockCoinOutpoints(self, tx_hash:str, index:str='0', id:str='primary')

    def getLockedOutpoints(self, id:str='primary'):
        """
        DESCRIPTION:

            Get all locked outpoints.

        PARAMS:

            (*) Denotes required argument

            ( ) id : ID of wallet to check for outpoints.
        """

        return self.get(f'/wallet/{id}/locked')
    ### END METHOD ################################### getLockedOutpoints(self, id:str='primary')

    def getWalletCoin(self, tx_hash:str, index:str='0', id:str='primary'):
        """
        DESCRIPTION:

            Get wallet coin.

        PARAMS:

            (*) Denotes required argument

            (*) tx_hash : ID of wallet that contains the outpoint.

            ( ) index   : Hash of transaction that created the outpoint.

            ( ) id      : Index of the output in the transaction being referenced.
        """

        return self.get(f'/wallet/{id}/coin/{tx_hash}/{index}')
    ### END METHOD ################################### getWalletCoin(self, tx_hash:str, index:str='0', id:str='primary')

    def walletRescan(self, height:int):
        """
        DESCRIPTION:

            Initiates a blockchain rescan for the walletdb. Wallets will
            be rolled back to the specified height (transactions above
            this height will be unconfirmed). Requires an admin API key.

        PARAMS:

            (*) Denotes required argument

            (*) height : Height to roll the walletdb back to.
        """

        return self.post('/rescan', {'height': height})
    ### END METHOD ################################### walletRescan(self, height:int)

    def adminResend(self):
        """
        DESCRIPTION:

            Rebroadcast all pending transactions in all wallets. Requires an admin API key.

        PARAMS:

            None.
        """

        return self.post('/resend')
    ### END METHOD ################################### adminResend(self)

    def walletResend(self, id:str='primary'):
        """
        DESCRIPTION:

            Rebroadcast all pending transactions for a single wallet.

        PARAMS:

            (*) Denotes required argument

            ( ) id : ID of wallet to resend pending transactions for. Default = 'primary'
        """

        return self.post(f'/wallet/{id}/resend')
    ### END METHOD ################################### walletResend(self, id:str='primary')

    def walletBackup(self, path:str=''):
        """
        DESCRIPTION:

            Safely backup the wallet database to specified path (creates a clone of the database).

        PARAMS:

            (*) Denotes required argument

            (*) path : Local directory to save backup.
        """

        return self.post('/backup', {'path': path})
    ### END METHOD ################################### walletBackup(self, path:str='')

    def walletMasterHDKeyBackup(self, id:str='primary'):
        """
        DESCRIPTION:

            Export the wallet's master hd private key. This is normally
            censored in the wallet info route. The provided API key must
            have admin access.

            Note: Once a passphrase has been set for a wallet, the API
            will not reveal the unencrypted master hd private key or seed
            phrase. Be sure you back it up right away!

        PARAMS:

            (*) Denotes required argument

            ( ) id : Wallet ID. Default = 'primary'
        """

        return self.get(f'/wallet/{id}/master')
    ### END METHOD ################################### walletMasterHDKeyBackup(self, id:str='primary')

    def listWallets(self):
        """
        DESCRIPTION:

            List all wallet IDs. Returns an array of strings.

        PARAMS:

            None.
        """

        return self.get('/wallet/')
    ### END METHOD ################################### listWallets(self)

    def getWalletAccountList(self, id:str='primary'):
        """
        DESCRIPTION:

            List all account names (array indices map directly to bip44
            account indices) associated with a specific wallet id.

        PARAMS:

            (*) Denotes required argument

            ( ) id : ID of wallet you would like to retrieve the account list for. Default = 'primary'
        """

        return self.get(f'/wallet/{id}/account')
    ### END METHOD ################################### getWalletAccountList(self, id:str='primary')

    def getAccountInfo(self, id:str='primary', account:str='default'):
        """
        DESCRIPTION:

            Get account info.

        PARAMS:

            (*) Denotes required argument

            ( ) id : ID of wallet you would like to query. Default = 'primary'
            ( ) account : ID of account you would to retrieve information for. Default = 'default'
        """

        return self.get(f'/wallet/{id}/account/{account}')
    ### END METHOD ################################### getAccountInfo(self, id:str='primary', account:str='default')

    def createAccount(self, passphrase:str, id:str, account:str, account_key:str=None, type:str='pubkeyhash', m:int=1, n:int=1):
        """
        DESCRIPTION:

            Create account with specified account name.

        PARAMS:

            (*) Denotes required argument

            (*) id          : Wallet ID (used for storage).

            (*) passphrase  : A strong passphrase used to encrypt the wallet.

            (*) account     : Name to give the account.

            ( ) account_key : The extended public key for the account. This is ignored for
                              non watch only wallets. Watch only accounts can't accept private
                              keys for import (or sign transactions). Sending an empty string
                              here crashes hsd's key decoder, so it's omitted unless given.

            ( ) type        : Type of wallet (pubkeyhash, multisig). Default is 'pubkeyhash'

            ( ) m           : 'm' value for multisig (m-of-n).

            ( ) n           : 'n' value for multisig (m-of-n)
        """

        body = _compact({'type': type, 'passphrase': passphrase, 'accountKey': account_key, 'm': m, 'n': n})
        return self.put(f'/wallet/{id}/account/{account}', body)
    ### END METHOD ################################### createAccount(self, passphrase:str, id:str, account:str,
    #                                                                      account_key:str='', type:str='pubkeyhash',
    #                                                                      m:int=1, n:int=1)

    def modifyAccount(self, account:str, lookahead:int=None, passphrase:str=None, id:str='primary'):
        """
        DESCRIPTION:

            Modify an existing account (currently only `lookahead` is supported).

        PARAMS:

            (*) Denotes required argument

            (*) account    : Name of the account to modify.

            ( ) lookahead  : New lookahead value for the account.

            ( ) passphrase : Passphrase to unlock the wallet, if encrypted.

            ( ) id         : Wallet ID. Default = 'primary'
        """

        body = _compact({'lookahead': lookahead, 'passphrase': passphrase})
        return self.patch(f'/wallet/{id}/account/{account}', body)
    ### END METHOD ################################### modifyAccount(self, account:str, lookahead:int=None, passphrase:str=None, id:str='primary')

    def getWalletTxDetails(self, id:str='primary', tx_hash:str=''):
        """
        DESCRIPTION:

            Get wallet transaction details.

        PARAMS:

            (*) Denotes required argument

            ( ) id      : ID of wallet that handled the transaction. Default = 'primary'
            (*) tx_hash : ID of account you would to retrieve information for.
        """

        return self.get(f'/wallet/{id}/tx/{tx_hash}')
    ### END METHOD ################################### getWalletTxDetails(self, id:str='primary', tx_hash:str='')

    def deleteTransaction(self, id:str='primary', tx_hash:str=''):
        """
        DESCRIPTION:

            Abandon single pending transaction. Confirmed transactions
            will throw an error. `TX not eligible`

        PARAMS:

            (*) Denotes required argument

            ( ) id      : ID of wallet where the transaction is that you want to remove.

            (*) tx_hash : Hash of transaction you would like to remove.
        """

        return self.delete(f'/wallet/{id}/tx/{tx_hash}')
    ### END METHOD ################################### deleteTransaction(self, id:str='primary', tx_hash:str='')

    def getWalletTxHistory(self, id:str='primary', account:str=None, reverse:bool=False, limit:int=None, after:str=None, time:int=None):
        """
        DESCRIPTION:

            Get wallet TX history. Returns array of tx details, paginated
            by `limit`/`after`/`time`.

        PARAMS:

            (*) Denotes required argument

            ( ) id      : ID of wallet to get history of. Default = 'primary'

            ( ) account : Account to filter by.

            ( ) reverse : Return results in reverse order. Default = False

            ( ) limit   : Maximum number of results to return.

            ( ) after   : Return results after this tx hash (cursor).

            ( ) time    : Return results after this timestamp.
        """

        params = _compact({'account': account, 'limit': limit, 'after': after, 'time': time})
        if reverse:
            params['reverse'] = True
        return self.get(f'/wallet/{id}/tx/history', params=params)
    ### END METHOD ################################### getWalletTxHistory(self, id:str='primary', account:str=None, reverse:bool=False, limit:int=None, after:str=None, time:int=None)

    def getPendingTransactions(self, id:str='primary', account:str=None, reverse:bool=False, limit:int=None, after:str=None, time:int=None):
        """
        DESCRIPTION:

            Get pending wallet transactions. Returns array of tx details,
            paginated by `limit`/`after`/`time`.

        PARAMS:

            (*) Denotes required argument

            ( ) id      : ID of wallet to get pending/unconfirmed transactions. Default = 'primary'

            ( ) account : Account to filter by.

            ( ) reverse : Return results in reverse order. Default = False

            ( ) limit   : Maximum number of results to return.

            ( ) after   : Return results after this tx hash (cursor).

            ( ) time    : Return results after this timestamp.
        """

        params = _compact({'account': account, 'limit': limit, 'after': after, 'time': time})
        if reverse:
            params['reverse'] = True
        return self.get(f'/wallet/{id}/tx/unconfirmed', params=params)
    ### END METHOD ################################### getPendingTransactions(self, id:str='primary', account:str=None, reverse:bool=False, limit:int=None, after:str=None, time:int=None)

    def getWalletNames(self, id:str='primary'):
        """
        DESCRIPTION:

            List the states of all names known to the wallet.

            Note: If no wallet ID is given, the names of the `primary` wallet
                  will be returned.

        PARAMS:

            (*) Denotes required argument

            ( ) id : ID of wallet to get transactions from. Default = 'primary'
        """

        return self.get(f'/wallet/{id}/name')
    ### END METHOD ################################### getWalletNames(self, id:str='primary')

    def getWalletName(self, name:str='', id:str='primary', own:bool=False):
        """
        DESCRIPTION:

            List the status of a single name known to the wallet.

        PARAMS:

            (*) Denotes required argument

            (*) name : Name of wallet.

            (*) id   : ID of wallet. Default = 'primary'

            ( ) own  : Only return the name state if this wallet owns it. Default = False
        """

        params = {'own': True} if own else {}
        return self.get(f'/wallet/{id}/name/{name}', params=params)
    ### END METHOD ################################### getWalletName(self, name:str='', id:str='primary', own:bool=False)

    def getWalletAuctions(self, id:str='primary'):
        """
        DESCRIPTION:

            List the states of all auctions known to the wallet.

            Note: If no wallet is specified, all auctions for the
                  `primary` wallet will be returned by default.

        PARAMS:

            (*) Denotes required argument

            ( ) id : ID of wallet. Default = 'primary'
        """

        return self.get(f'/wallet/{id}/auction')
    ### END METHOD ################################### getWalletAuctions(self, id:str='primary')

    def getWalletAuctionByName(self, name:str='', id:str='primary'):
        """
        DESCRIPTION:

            List the states of all auctions known to the wallet.

        PARAMS:

            (*) Denotes required argument

            (*) name : Name of wallet.

            ( ) id   : ID of wallet. Default = 'primary'
        """

        return self.get(f'/wallet/{id}/auction/{name}')
    ### END METHOD ################################### getWalletAuctionByName(self, name:str='', id:str='primary')

    def getWalletBids(self, id:str='primary', own:bool=True):
        """
        DESCRIPTION:

            List all bids for all names known to the wallet.

            Note: If no wallet is specified bids for the `primary`
                  wallet will be returned.

        PARAMS:

            (*) Denotes required argument

            ( ) id  : ID of wallet. Default = 'primary'

            ( ) own : Whether to only show bids from this wallet. Default = True
        """

        return self.get(f'/wallet/{id}/bid', params={'own': own})
    ### END METHOD ################################### getWalletBids(self, id:str='primary', own:bool=True)

    def getWalletBidsByName(self, name:str='', id:str='primary', own:bool=False):
        """
        DESCRIPTION:

            List all bids for all names known to the wallet.

        PARAMS:

            (*) Denotes required argument

            (*) name : Name of domain to display bids for.

            ( ) id   : ID of wallet. Default = 'primary'

            ( ) own  : Whether to only show bids from this wallet. Default = False
        """

        return self.get(f'/wallet/{id}/bid/{name}', params={'own': own})
    ### END METHOD ################################### getWalletBidsByName(self, name:str='', id:str='primary', own:bool=False)

    def getWalletReveals(self, id:str='primary', own:bool=False):
        """
        DESCRIPTION:

            List all reveals for all names known to the wallet.

        PARAMS:

            (*) Denotes required argument

            ( ) id  : ID of wallet. Default = 'primary'

            ( ) own : Whether to only show reveals from this wallet. Default = False
        """

        return self.get(f'/wallet/{id}/reveal', params={'own': own})
    ### END METHOD ################################### getWalletReveals(self, id:str='primary', own:bool=False)

    def getWalletRevealsByName(self, name:str, id:str='primary', own:bool=False):
        """
        DESCRIPTION:

            List all reveals for all names known to the wallet.

        PARAMS:

            (*) Denotes required argument

            (*) name : Name of domain to get reveals for.

            ( ) id   : ID of wallet. Default = 'primary'

            ( ) own  : Whether to only show reveals from this wallet. Default = False
        """

        return self.get(f'/wallet/{id}/reveal/{name}', params={'own': own})
    ### END METHOD ################################### getWalletRevealsByName(self, name:str='', id:str='primary', own:bool=False)

    def getWalletResourceByName(self, name:str, id:str='primary'):
        """
        DESCRIPTION:

            Get the data resource associated with a name.

        PARAMS:

            (*) Denotes required argument

            (*) name : Name of domain.

            ( ) id   : ID of wallet. Default = 'primary'
        """

        return self.get(f'/wallet/{id}/resource/{name}')
    ### END METHOD ################################### getWalletResourceByName(self, name:str='', id:str='primary')

    def getNonceForBid(self, bid:float, name:str, address:str, id:str='primary'):
        """
        DESCRIPTION:

            Deterministically generate a nonce to blind a bid.

            Note: This command involves entering HNS values, be careful
                  with different formats of values for different APIs.

        PARAMS:

            (*) Denotes required argument

            (*) bid     : Value of bid to blind.

            (*) name    : Name of domain.

            (*) address : Address controlling bid.

            ( ) id      : ID of wallet. Default = 'primary'
        """

        return self.get(f'/wallet/{id}/nonce/{name}', params={'address': address, 'bid': bid})
    ### END METHOD ################################### getNonceForBid(self, bid:float, name:str, address:str, id:str='primary')

    def sendOPEN(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a name OPEN.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            (*) name       : Name to OPEN.

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign}
        return self.post(f'/wallet/{id}/open', body)
    ### END METHOD ################################### sendOPEN(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True)

    def sendBID(self, id:str, passphrase:str, name:str, bid:int, lockup:int, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a name BID.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            (*) name       : Name to BID on.

            (*) bid        : Value (in dollarydoos) to bid for name.

            (*) lockup     : Value (in dollarydoos) to actually send in the transaction, blinding the actual bid value.

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign, 'bid': bid, 'lockup': lockup}
        return self.post(f'/wallet/{id}/bid', body)
    ### END METHOD ################################### sendBID(self, id:str, passphrase:str, name:str, bid:int, lockup:int, sign:bool=True, broadcast:bool=True)

    def createAuction(self, id:str, passphrase:str, name:str, bid:int, lockup:int, broadcast_bid:bool=True, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and (optionally) broadcast a BID and REVEAL together in one call.

        PARAMS:

            (*) Denotes required argument

            (*) id            : Wallet ID.

            (*) passphrase    : Passphrase to unlock the wallet.

            (*) name          : Name to bid on.

            (*) bid           : Value (in dollarydoos) to bid for name.

            (*) lockup        : Value (in dollarydoos) to actually send in the transaction, blinding the actual bid value.

            ( ) broadcast_bid : Whether to broadcast the BID transaction before creating the REVEAL. Default = True

            ( ) sign          : Whether to sign the transactions. Default = True

            ( ) broadcast     : Whether to broadcast the REVEAL transaction (must sign if true). Default = True
        """

        body = {
            'passphrase': passphrase,
            'name': name,
            'bid': bid,
            'lockup': lockup,
            'broadcastBid': broadcast_bid,
            'sign': sign,
            'broadcast': broadcast,
        }
        return self.post(f'/wallet/{id}/auction', body)
    ### END METHOD ################################### createAuction(self, id:str, passphrase:str, name:str, bid:int, lockup:int, broadcast_bid:bool=True, sign:bool=True, broadcast:bool=True)

    def sendREVEAL(self, id:str, passphrase:str, name:str='', sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a name REVEAL. If multiple bids were placed on a name,
            all bids will be revealed by this transaction. If no value is passed in for
            `name`, all reveals for all names in the wallet will be sent.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            ( ) name       : Name to REVEAL bids for (or `null` for all names).

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign}
        return self.post(f'/wallet/{id}/reveal', body)
    ### END METHOD ################################### sendREVEAL(self, id:str, passphrase:str, name:str='', sign:bool=True, broadcast:bool=True)

    def sendREDEEM(self, id:str, passphrase:str, name:str='', sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a REDEEM. This transaction sweeps the value
            from losing bids back into the wallet. If multiple bids (and reveals)
            were placed on a name, all losing bids will be redeemed by this
            ransaction. If no value is passed in for `name`, all qualifying bids
            are redeemed.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            ( ) name       : Name to REDEEM bids for (or null for all names).

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign}
        return self.post(f'/wallet/{id}/redeem', body)
    ### END METHOD ################################### sendREDEEM(self, id:str, passphrase:str, name:str='', sign:bool=True, broadcast:bool=True)

    def sendUPDATE(self, id:str, passphrase:str, name:str, data:dict, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send an UPDATE. This transaction updates
            the resource data associated with a given name.

            Note: Due to behavior of some shells like bash, if your TXT
                  value contains spaces you may need to add additional
                  quotes like this: "'"$value"'"

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            ( ) name       : Name to UPDATE.

            ( ) data       : JSON object containing an array of DNS records (resource object).
                              See https://hsd-dev.org/api-docs/#resource-object for more information.

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign, 'data': data}
        return self.post(f'/wallet/{id}/update', body)
    ### END METHOD ################################### sendUPDATE(self, id:str, passphrase:str, name:str, data:str, sign:bool=True, broadcast:bool=True)

    def sendRENEW(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a RENEW.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            ( ) name       : Name to RENEW.

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign}
        return self.post(f'/wallet/{id}/renewal', body)
    ### END METHOD ################################### sendRENEW(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True)

    def sendTRANSFER(self, id:str, passphrase:str, name:str, address:str, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a TRANSFER.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            ( ) name       : Name to TRANSFER.

            ( ) address    : Address to transfer name ownership to.

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign, 'address': address}
        return self.post(f'/wallet/{id}/transfer', body)
    ### END METHOD ################################### sendTRANSFER(self, id:str, passphrase:str, name:str, address:str, sign:bool=True, broadcast:bool=True)

    def cancelTRANSFER(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a transaction that cancels a TRANSFER.

            This transaction is not a unique covenant type, but spends from
            a TRANSFER to an UPDATE covenant (with an empty resource object)
            in order to cancel a transfer already in progress.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            (*) name       : Name in transferred state to cancel transfer for.

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign}
        return self.post(f'/wallet/{id}/cancel', body)
    ### END METHOD ################################### cancelTRANSFER(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True)

    def sendFINALIZE(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a FINALIZE.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            (*) name       : Name in transferred state to finalize transfer for.

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign}
        return self.post(f'/wallet/{id}/finalize', body)
    ### END METHOD ################################### sendFINALIZE(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True)

    def sendREVOKE(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True):
        """
        DESCRIPTION:

            Create, sign, and send a REVOKE.

            This method is a fail-safe for name owners whose keys
            are compromised and lose control of their name. Before
            the transfer is finalized, a REVOKE can be sent that not
            only cancels the transfer, but burns the name preventing
            any further updates or transfers. The name can be
            reopened with a new auction after a set time.

        PARAMS:

            (*) Denotes required argument

            (*) id         : Wallet ID.

            (*) passphrase : Passphrase to unlock the wallet.

            (*) name       : Name in transferred state to REVOKE transfer for.

            ( ) sign       : Whether to sign the transaction. Default = True

            ( ) broadcast  : Whether to broadcast the transaction (must sign if true). Default = True
        """

        body = {'passphrase': passphrase, 'name': name, 'broadcast': broadcast, 'sign': sign}
        return self.post(f'/wallet/{id}/revoke', body)
    ### END METHOD ################################### sendREVOKE(self, id:str, passphrase:str, name:str, sign:bool=True, broadcast:bool=True)

    def deepClean(self, confirm:bool=False):
        """
        DESCRIPTION:

            Wipe wallet balance and transaction history, keeping keys intact.
            Requires an admin API key.

        PARAMS:

            ( ) confirm : Must be explicitly set to True to confirm the wipe. Default = False
        """

        return self.post('/deepclean', {'I_HAVE_BACKED_UP_MY_WALLET': confirm})
    ### END METHOD ################################### deepClean(self, confirm:bool=False)

    def recalculateBalances(self):
        """
        DESCRIPTION:

            Force the walletdb to recalculate all wallet balances.
            Requires an admin API key.

        PARAMS:

            None.
        """

        return self.post('/recalculate-balances')
    ### END METHOD ################################### recalculateBalances(self)

    def rpc_getNames(self):
        """
        DESCRIPTION:

            Returns the domain names associated with your wallet.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'getnames', 'params': []})
    ### END METHOD ################################### rpc_getNames(self)

    def rpc_getAuctionInfo(self, name:str):
        """
        DESCRIPTION:

            Returns information on auction.

        PARAMS:
            (*) Denotes required argument

            (*) name : Name to get auction information for.
        """

        return self.post('/', {'method': 'getauctioninfo', 'params': [name]})
    ### END METHOD ################################### rpc_getAuctionInfo(self, name:str)

    def rpc_getBIDS(self):
        """
        DESCRIPTION:

            Returns list of `BID`s placed by your wallet.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'getbids', 'params': []})
    ### END METHOD ################################### rpc_getBIDS(self)

    def rpc_getREVEALS(self):
        """
        DESCRIPTION:

            Returns all the `REVEAL` transactions sent by the wallet.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'getreveals', 'params': []})
    ### END METHOD ################################### rpc_getREVEALS(self)

    def rpc_sendOPEN(self, name:str):
        """
        DESCRIPTION:

            Once a name is available, a sendopen transaction starts the opening phase.

        PARAMS:

            (*) Denotes required argument

            (*) name : Domain name to send `OPEN` transaction for.
        """

        return self.post('/', {'method': 'sendopen', 'params': [name]})
    ### END METHOD ################################### rpc_sendOPEN(self, name:str)

    def rpc_sendBID(self, name:str, bid_amount:float, lockup_blind:float, account:str='default'):
        """
        DESCRIPTION:

            The `OPEN` period is followed by the `BID` period. Use `rpc_sendBID` to place a bid.

            Note: This command involves entering HNS values, be careful with different formats
                  of values for different APIs. See https://hsd-dev.org/api-docs/?shell--curl#values
                  to learn more.


        PARAMS:

            (*) Denotes required argument

            (*) name        : Domain name to to bid on.

            (*) bid_amount   : Amount to bid (in HNS).

            (*) lockup_blind : Amount to lock up to blind your bid (must be greater than bid amount).

            ( ) account     : Wallet account to use. Default = 'default'
        """

        return self.post('/', {'method': 'sendbid', 'params': [name, bid_amount, lockup_blind, account]})
    ### END METHOD ################################### rpc_sendBID(self, name:str, bid_amount:float, lockup_blind:float, account:str='default')

    def rpc_sendREVEAL(self, name:str=''):
        """
        DESCRIPTION:

            The `BID` period is followed by the `REVEAL` period, during which bidders
            must reveal their bids.

            Note: If not domain name is specified then a `REVEAL` will be sent to all names.

        PARAMS:

            (*) Denotes required argument

            ( ) name : Domain name to `REVEAL` bid for (`null` for all names).
        """

        params = [name] if name else []
        return self.post('/', {'method': 'sendreveal', 'params': params})
    ### END METHOD ################################### rpc_sendREVEAL(self, name:str='')

    def rpc_sendREDEEM(self, name:str=''):
        """
        DESCRIPTION:

            After the `REVEAL` period, the auction is `CLOSED`. The value locked
            up by losing bids can be spent using a `REDEEM` covenant like any
            other coin. The winning bid can not be redeemed.

        PARAMS:

            (*) Denotes required argument

            ( ) name : Domain name to `REDEEM` bid for (`null` for all names).
        """

        params = [name] if name else []
        return self.post('/', {'method': 'sendredeem', 'params': params})
    ### END METHOD ################################### rpc_sendREDEEM(self, name:str='')

    def rpc_sendUPDATE(self, name:str, data:dict):
        """
        DESCRIPTION:

            After the `REVEAL` period, the auction is `CLOSED`. The value
            locked up by the winning bid is locked forever, although
            the name owner and the name state can still change. The
            winning bidder can update the data resource associated with
            their name by sending an `UPDATE`.

        PARAMS:

            (*) Denotes required argument

            (*) name       : Domain name to `UPDATE`.

            (*) data       : JSON-encoded resource object.
                              See https://hsd-dev.org/api-docs/#resource-object for more information.
        """

        return self.post('/', {'method': 'sendupdate', 'params': [name, data]})
    ### END METHOD ################################### rpc_sendUPDATE(self, name:str, data:dict)

    def rpc_sendRENEWAL(self, name:str):
        """
        DESCRIPTION:

            On mainnet, name ownership expires after two years. If the name
            owner does not `RENEW` the name, it can be re-opened by any user.
            `RENEW` covenants commit to a a recent block hash to prevent
            pre-signing and prove physical ownership of controlling keys.
            There is no cost besides the miner fee.

        PARAMS:

            (*) Denotes required argument

            (*) name : Domain name to `RENEW` ownership of.
        """

        return self.post('/', {'method': 'sendrenewal', 'params': [name]})
    ### END METHOD ################################### rpc_sendRENEWAL(self, name:str)

    def rpc_sendTRANSFER(self, name:str, address:str):
        """
        DESCRIPTION:

            `TRANSFER` a name to a new address. Note that the output value
            of the UTXO still does not change. On mainnet, the `TRANSFER`
            period lasts two days, after which the original owner can
            `FINALIZE` the transfer. Any time before it is final, the
            original owner can still `CANCEL` or `REVOKE` the transfer.

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to `TRANSFER`.

            (*) address : Address to `TRANSFER` name ownership to.
        """

        return self.post('/', {'method': 'sendtransfer', 'params': [name, address]})
    ### END METHOD ################################### rpc_sendTRANSFER(self, name:str, address:str)

    def rpc_sendFINALIZE(self, name:str):
        """
        DESCRIPTION:

            About 48 hours after a TRANSFER, the original owner can send a
            `FINALIZE` transaction, completing the transfer to a new address.
            The output address of the `FINALIZE` is the new owner's address.

        PARAMS:

            (*) Denotes required argument

            (*) name : Domain name to `FINALIZE`.
        """

        return self.post('/', {'method': 'sendfinalize', 'params': [name]})
    ### END METHOD ################################### rpc_sendFINALIZE(self, name:str)

    def rpc_sendCANCEL(self, name:str):
        """
        DESCRIPTION:

            After sending a `TRANSFER` but before sending a `FINALIZE`,
            the original owner can `CANCEL` the transfer. The owner will
            retain control of the name. This is the recommended means
            of canceling a transfer. Not to be confused with a `REVOKE`,
            which is only to be used in the case of a stolen key. There
            is no `CANCEL` covenant -- this transaction actually sends
            an `UPDATE`.

        PARAMS:

            (*) Denotes required argument

            (*) name : Domain name to `CANCEL` the in-progress transfer of.
        """

        return self.post('/', {'method': 'sendcancel', 'params': [name]})
    ### END METHOD ################################### rpc_sendCANCEL(self, name:str)

    def rpc_sendREVOKE(self, name:str):
        """
        DESCRIPTION:

            After sending a `TRANSFER` but before sending a `FINALIZE`,
            the original owner can `REVOKE` the name transfer. This
            renders the name's output forever unspendable, and puts the
            name back up for bidding. This is intended as an action of
            last resort in the case that the owner's key has been
            compromised, leading to a grief battle between an attacker
            and the owner.

        PARAMS:

            (*) Denotes required argument

            (*) name : Domain name to `REVOKE` the in-progress transfer of.
        """

        return self.post('/', {'method': 'sendrevoke', 'params': [name]})
    ### END METHOD ################################### rpc_sendREVOKE(self, name:str)

    def rpc_importNONCE(self, name:str, address:str, _bidValue:float):
        """
        DESCRIPTION:

            Deterministically regenerate the nonce for a bid.

            Note: This command involves entering HNS values, be careful with different formats
                  of values for different APIs. See https://hsd-dev.org/api-docs/?shell--curl#values
                  to learn more.

        PARAMS:

            (*) Denotes required argument

            (*) name     : Domain name bid on.

            (*) address  : Address submitting the bid.

            (*) _bidValue : Value of the bid (in HNS).
        """

        return self.post('/', {'method': 'importnonce', 'params': [name, address, _bidValue]})
    ### END METHOD ################################### rpc_importNONCE(self, name:str, address:str, _bidValue:float)

    def rpc_createOPEN(self, name:str, account:str=''):
        """
        DESCRIPTION:

            Creates `OPEN` transaction without signing or broadcasting it.

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to `OPEN` bidding on.

            (*) account : Account to use.
        """

        return self.post('/', {'method': 'createopen', 'params': [name, account]})
    ### END METHOD ################################### rpc_createOPEN(self, name:str, account:str='')

    def rpc_createBID(self, name:str, bid_amount:float, lockup_blind:float, account:str):
        """
        DESCRIPTION:

            Create `BID` transaction without signing or broadcasting it.

            Note: This command involves entering HNS values, be careful with different formats
                  of values for different APIs. See https://hsd-dev.org/api-docs/?shell--curl#values
                  to learn more.

        PARAMS:

            (*) Denotes required argument

            (*) name        : Domain name bid on.

            (*) bid_amount   : Amount to bid (in HNS).

            (*) lockup_blind : Amount to lock up to blind your bid, must be greater than `bid_amount`).

            (*) address     : Address submitting the bid.
        """

        return self.post('/', {'method': 'createbid', 'params': [name, bid_amount, lockup_blind, account]})
    ### END METHOD ################################### rpc_createBID(self, name:str, bid_amount:float, lockup_blind:float, account:str)

    def rpc_createREVEAL(self, name:str='', account:str=''):
        """
        DESCRIPTION:

            Create `REVEAL` transaction without signing or broadcasting it.

            Note: If no name is specified a `REVEAL` transaction will be
                  created for all names.

        PARAMS:

            (*) Denotes required argument

            ( ) name    : Domain name to `REVEAL` bid for (`null` for all names).

            ( ) account : Account to use.
        """

        return self.post('/', {'method': 'createreveal', 'params': [name, account]})
    ### END METHOD ################################### rpc_createREVEAL(self, name:str='', account:str='')

    def rpc_createREDEEM(self, name:str='', account:str=''):
        """
        DESCRIPTION:

            Create `REDEEM` transaction without signing or broadcasting it.

            Note: If no name is specified all names will have their loosing
                  bids redeemed.

        PARAMS:

            (*) Denotes required argument

            ( ) name    : Domain name to `REDEEM` a losing bid for (null for all names).

            ( ) account : Account to use.
        """

        return self.post('/', {'method': 'createredeem', 'params': [name, account]})
    ### END METHOD ################################### rpc_createREDEEM(self, name:str='', account:str='')

    def rpc_createUPDATE(self, name:str, data:dict, account:str=''):
        """
        DESCRIPTION:

            Create `UPDATE` transaction without signing or broadcasting it.

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to `UPDATE` the data for.

            (*) data    : JSON-encoded resource object.
                           See https://hsd-dev.org/api-docs/#resource-object for more information.

            ( ) account : Account to use.
        """

        return self.post('/', {'method': 'createupdate', 'params': [name, data, account]})
    ### END METHOD ################################### rpc_createUPDATE(self, name:str, data:dict, account:str='')

    def rpc_createRENEWAL(self, name:str, account:str=''):
        """
        DESCRIPTION:

            Create `RENEW` transaction without signing or broadcasting it.

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to `RENEW` ownership of.

            ( ) account : Account to use.
        """

        return self.post('/', {'method': 'createrenewal', 'params': [name, account]})
    ### END METHOD ################################### rpc_createRENEWAL(self, name:str, account:str='')

    def rpc_createTRANSFER(self, name:str, address:str, account:str=''):
        """
        DESCRIPTION:

            Create `TRANSFER` transaction without signing or broadcasting it.

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to `TRANSFER` ownership of.

            (*) address : Address to transfer name ownership to.

            ( ) account : Account to use.
        """

        return self.post('/', {'method': 'createtransfer', 'params': [name, address, account]})
    ### END METHOD ################################### rpc_createTRANSFER(self, name:str, address:str, account:str='')

    def rpc_createFINALIZE(self, name:str, account:str=''):
        """
        DESCRIPTION:

            Create `FINALIZE` transaction without signing or broadcasting it.

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to `FINALIZE`.

            ( ) account : Account to use.
        """

        return self.post('/', {'method': 'createfinalize', 'params': [name, account]})
    ### END METHOD ################################### rpc_createFINALIZE(self, name:str, account:str='')

    def rpc_createCANCEL(self, name:str, account:str=''):
        """
        DESCRIPTION:

            Create `CANCEL` transaction without signing or broadcasting it.

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to `CANCEL` the in-progress transfer of.

            ( ) account : Account to use.
        """

        return self.post('/', {'method': 'createcancel', 'params': [name, account]})
    ### END METHOD ################################### rpc_createCANCEL(self, name:str, account:str='')

    def rpc_createREVOKE(self, name:str, account:str=''):
        """
        DESCRIPTION:

            Create `REVOKE` transaction without signing or broadcasting it.

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to `REVOKE` the in-progress transfer of.

            ( ) account : Account to use.
        """

        return self.post('/', {'method': 'createrevoke', 'params': [name, account]})
    ### END METHOD ################################### rpc_createREVOKE(self, name:str, account:str='')

    def rpc_createBatch(self, actions:list, options:dict=None):
        """
        DESCRIPTION:

            Create a batch of covenant actions in a single transaction,
            without signing or broadcasting it.

            Each action is a list in the form `[type, ...args]`, where `type`
            is one of `NONE`, `OPEN`, `BID`, `REVEAL`, `REDEEM`, `UPDATE`,
            `RENEW`, `TRANSFER`, `FINALIZE`, `CANCEL`, `REVOKE`, and `args`
            matches the arguments of the corresponding `create*`/`send*` RPC.

        PARAMS:

            (*) Denotes required argument

            (*) actions : List of `[type, ...args]` covenant actions.

            ( ) options : TransactionOptions object (rate, account, etc.).
        """

        params = [actions, options] if options is not None else [actions]
        return self.post('/', {'method': 'createbatch', 'params': params})
    ### END METHOD ################################### rpc_createBatch(self, actions:list, options:dict=None)

    def rpc_sendBatch(self, actions:list, options:dict=None):
        """
        DESCRIPTION:

            Create, sign, and send a batch of covenant actions in a single
            transaction.

            Each action is a list in the form `[type, ...args]`, where `type`
            is one of `NONE`, `OPEN`, `BID`, `REVEAL`, `REDEEM`, `UPDATE`,
            `RENEW`, `TRANSFER`, `FINALIZE`, `CANCEL`, `REVOKE`, and `args`
            matches the arguments of the corresponding `create*`/`send*` RPC.

        PARAMS:

            (*) Denotes required argument

            (*) actions : List of `[type, ...args]` covenant actions.

            ( ) options : TransactionOptions object (rate, account, etc.).
        """

        params = [actions, options] if options is not None else [actions]
        return self.post('/', {'method': 'sendbatch', 'params': params})
    ### END METHOD ################################### rpc_sendBatch(self, actions:list, options:dict=None)

    def rpc_importName(self, name:str, rescan_height:int=None):
        """
        DESCRIPTION:

            Add a name to the wallet "watchlist" without sending a transaction. Optionally
            _rescan the blockchain to recover `OPEN` and `BID`s for the name. This action will
            fail if the name already exists in the wallet.

            The purpose of this action is to "subscribe" to `BID`s for a name auction before
            participating in that auction. If a user is interested in `BID`s that have already
            been placed on a name they are interested in bidding on themselves, they may
            execute this RPC call and include a `height` parameter, which should be any block
            before the OPEN for the name was confirmed. The `OPEN` transaction must be included
            in the _rescan or the wallet will not track `BID`s on the name.

            Once the auction is rescanned, `rpc_getBIDS` can be used to return all current BIDs
            on a name, even if the wallet has not placed any BIDs itself.

        PARAMS:

            (*) Denotes required argument

            (*) name         : Domain name to import.

            ( ) rescan_height : If present, perform a wallet _rescan from specified height.
        """

        params = [name] if rescan_height is None else [name, rescan_height]
        return self.post('/', {'method': 'importname', 'params': params})
    ### END METHOD ################################### rpc_importName(self, name:str, rescan_height:int=None)

    def rpc_selectWallet(self, wallet_id:str):
        """
        DESCRIPTION:

            Switch target wallet for all future RPC calls.

        PARAMS:

            (*) Denotes required argument

            (*) wallet_id : ID of selected wallet.
        """

        return self.post('/', {'method': 'selectwallet', 'params': [wallet_id]})
    ### END METHOD ################################### rpc_selectWallet(self, wallet_id:str)

    def rpc_getWalletInfo(self):
        """
        DESCRIPTION:

            Get basic wallet details.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'getwalletinfo'})
    ### END METHOD ################################### rpc_getWalletInfo(self)

    def rpc_fundRawTransaction(self, tx_hex:str, fee_rate:float=None, change_address:str=None):
        """
        DESCRIPTION:

            Add inputs to a transaction until it has enough in value to meet its out value.

        PARAMS:

            (*) Denotes required argument

            (*) tx_hex         : Raw transaction (hex).

            ( ) fee_rate       : Sets fee rate for transaction in HNS/kb.

            ( ) change_address : Handshake address for change output of transaction.
        """

        options = _compact({'feeRate': fee_rate, 'changeAddress': change_address})
        params = [tx_hex] if not options else [tx_hex, options]
        return self.post('/', {'method': 'fundrawtransaction', 'params': params})
    ### END METHOD ################################### rpc_fundRawTransaction(self, tx_hex:str, fee_rate:float=None, change_address:str=None)

    def rpc_resendWalletTransactions(self):
        """
        DESCRIPTION:

            Re-broadcasts all unconfirmed transactions to the network.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'resendwallettransactions'})
    ### END METHOD ################################### rpc_resendWalletTransactions(self)

    def rpc_abandonTransaction(self, tx_id:str):
        """
        DESCRIPTION:

            Remove transaction from the database. This allows "stuck" coins to be respent.

        PARAMS:

            (*) Denotes required argument

            (*) tx_id : Transaction ID to remove.
        """

        return self.post('/', {'method': 'abandontransaction', 'params': [tx_id]})
    ### END METHOD ################################### rpc_abandonTransaction(self, tx_id:str)

    def rpc_backupWallet(self, path:str):
        """
        DESCRIPTION:

            Back up wallet database and files to directory created at specified path.

        PARAMS:

            (*) Denotes required argument

            (*) path : Absolute path (including directories and filename) to write backup file.
        """

        return self.post('/', {'method': 'backupwallet', 'params': [path]})
    ### END METHOD ################################### rpc_backupWallet(self, path:str)

    def rpc_dumpPrivKey(self, address:str):
        """
        DESCRIPTION:

            Get the private key (WIF format) corresponding to specified
            address. Also see `hsw.rpc_importPrivKey`.

        PARAMS:

            (*) Denotes required argument

            (*) address : Reveal the private key for this Handshake address.
        """

        return self.post('/', {'method': 'dumpprivkey', 'params': [address]})
    ### END METHOD ################################### rpc_dumpPrivKey(self, address:str)

    def rpc_dumpWallet(self, path:str):
        """
        DESCRIPTION:

            Creates a new human-readable file at specified path with
            all wallet private keys in Wallet Import Format (base58).

        PARAMS:

            (*) Denotes required argument

            (*) path : Absolute path (including directories and filename) to write backup file.
        """

        return self.post('/', {'method': 'dumpwallet', 'params': [path]})
    ### END METHOD ################################### rpc_dumpWallet(self, path:str)

    def rpc_encryptWallet(self, passphrase:str):
        """
        DESCRIPTION:

            Encrypts wallet with provided passphrase. This action
            can only be done once on an unencrypted wallet. See
            `hsw.rpc_walletPasswordChange()` or `hsw.changePassword()`
            if wallet has already been encrypted.

        PARAMS:

            (*) Denotes required argument

            (*) passphrase : Absolute path (including directories and filename) to write backup file.
        """

        return self.post('/', {'method': 'encryptwallet', 'params': [passphrase]})
    ### END METHOD ################################### rpc_encryptWallet(self, passphrase:str)

    def rpc_getAccountAddress(self, account:str='default'):
        """
        DESCRIPTION:

            Get the current receiving address for specified account.

            Note: If no account is specified, the receiving address
                  for the account `default` will be returned.

        PARAMS:

            (*) Denotes required argument

            ( ) account : Account to retrieve address from.
        """

        return self.post('/', {'method': 'getaccountaddress', 'params': [account]})
    ### END METHOD ################################### rpc_getAccountAddress(self, account:str)

    def rpc_getAccount(self, address:str):
        """
        DESCRIPTION:

            Get the account associated with a specified address.

        PARAMS:

            (*) Denotes required argument

            (*) address : Address to search for.
        """

        return self.post('/', {'method': 'getaccount', 'params': [address]})
    ### END METHOD ################################### rpc_getAccount(self, address:str)

    def rpc_getAddressesByAccount(self, account:str='default'):
        """
        DESCRIPTION:

            Get all addresses for a specified account.

            Note: If no account is specified, then the addresses
                  for the account `default` will be returned.

        PARAMS:

            (*) Denotes required argument

            ( ) account : Account to retrieve addresses from.
        """

        return self.post('/', {'method': 'getaddressesbyaccount', 'params': [account]})
    ### END METHOD ################################### rpc_getAddressesByAccount(self, account:str='default')

    def rpc_getBalance(self, account:str=None):
        """
        DESCRIPTION:

            Get total balance for entire wallet or a single, specified account.

            Note: If no account is specified, then the balance of
                  the entire wallet will be returned

        PARAMS:

            (*) Denotes required argument

            ( ) account : Account to return balance of.
        """

        params = [] if account is None else [account]
        return self.post('/', {'method': 'getbalance', 'params': params})
    ### END METHOD ################################### rpc_getBalance(self, account:str=None)

    def rpc_getNewAddress(self, account:str=''):
        """
        DESCRIPTION:

            Get the next receiving address from specified account, or default account.

        PARAMS:

            (*) Denotes required argument

            ( ) account : Account name. Default = 'defualt'
        """

        return self.post('/', {'method': 'getnewaddress', 'params': [account]})
    ### END METHOD ################################### rpc_getNewAddress(self, account:str='')

    def rpc_getRawChangeAddress(self):
        """
        DESCRIPTION:

            Get the next change address from specified account.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'getrawchangeaddress'})
    ### END METHOD ################################### rpc_getRawChangeAddress(self)

    def rpc_getReceivedByAccount(self, account:str, min_confirm:int=None):
        """
        DESCRIPTION:

            Get total amount received by specified account. Optionally
            only count transactions with `min_confirm` number of confirmations.

        PARAMS:

            (*) Denotes required argument

            (*) account    : Account name.

            ( ) min_confirm : Only include transactions with this many confirmations.
        """

        params = [account] if min_confirm is None else [account, min_confirm]
        return self.post('/', {'method': 'getreceivedbyaccount', 'params': params})
    ### END METHOD ################################### rpc_getReceivedByAccount(self, account:str, min_confirm:int=None)

    def rpc_getReceivedByAddress(self, address:str, min_confirm:int=None):
        """
        DESCRIPTION:

            Get total amount received by specified address. Optionally
            only count transactions with `min_confirm` number of confirmations.

        PARAMS:

            (*) Denotes required argument

            (*) address    : Address to request balance of.

            ( ) min_confirm : Only include transactions with this many confirmations.
        """

        params = [address] if min_confirm is None else [address, min_confirm]
        return self.post('/', {'method': 'getreceivedbyaddress', 'params': params})
    ### END METHOD ################################### rpc_getReceivedByAddress(self, account:str, min_confirm:int=None)

    def rpc_getTransaction(self, tx_id:str, watch_only:bool=None):
        """
        DESCRIPTION:

            Get details about a transaction in the wallet.

        PARAMS:

            (*) Denotes required argument

            (*) tx_id      : ID of transaction to fetch.

            ( ) watch_only : (bool) Whether to include watch-only addresses in balance details.
        """

        params = [tx_id] if watch_only is None else [tx_id, watch_only]
        return self.post('/', {'method': 'gettransaction', 'params': params})
    ### END METHOD ################################### rpc_getTransaction(self, tx_id:str, watch_only:bool=None)

    def rpc_getUnconfirmedBalance(self):
        """
        DESCRIPTION:

            Get the unconfirmed balance from the wallet.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'getunconfirmedbalance'})
    ### END METHOD ################################### rpc_getUnconfirmedBalance(self)

    def rpc_importPrivKey(self, private_key:str, label:str=None, rescan:bool=None):
        """
        DESCRIPTION:

            Import a private key into wallet. Also see `hsw.rpc_dumpPrivKey`.

        PARAMS:

            (*) Denotes required argument

            (*) private_key : Private key to import (WIF format).

            ( ) label   : Ignored but required if additional parameters are passed.

            ( ) rescan  : (bool) Whether to _rescan wallet after importing.
        """

        if label is None and rescan is None:
            params = [private_key]
        else:
            params = [private_key, label or 'Unlabeled', bool(rescan)]

        return self.post('/', {'method': 'importprivkey', 'params': params})
    ### END METHOD ################################### rpc_importPrivKey(self, private_key:str, label:str=None, rescan:bool=None)

    def rpc_importWallet(self, wallet_file:str, rescan:bool=False):
        """
        DESCRIPTION:

            Import all keys from a wallet backup file. Also see `hsw.rpc_dumpWallet`.

        PARAMS:

            (*) Denotes required argument

            (*) wallet_file : Path to wallet file.

            ( ) rescan  : (bool) Whether to _rescan wallet after importing.
        """

        return self.post('/', {'method': 'importwallet', 'params': [wallet_file, rescan]})
    ### END METHOD ################################### rpc_importWallet(self, wallet_file:str, rescan:bool=False)

    def rpc_importAddress(self, address:str, label:str=None, rescan:bool=None, p2sh:bool=None):
        """
        DESCRIPTION:

            Import address to a watch-only wallet. May also import a
            Handshake output script (in hex) as pay-to-script-hash
            (P2WSH) address.

        PARAMS:

            (*) Denotes required argument

            (*) address : Address to watch in wallet.

            ( ) label   : Ignored but required if additional parameters are passed.

            ( ) rescan  : (bool) Whether to _rescan wallet after importing.

            ( ) p2sh    : (bool) Whether to generate P2SH address from given script.
        """

        if rescan is None and p2sh is None:
            params = [address]
        else:
            params = [address, label or 'Unlabeled', bool(rescan), bool(p2sh)]

        return self.post('/', {'method': 'importaddress', 'params': params})
    ### END METHOD ################################### rpc_importAddress(self, address:str, label:str=None, rescan:bool=None, p2sh:bool=None)

    def rpc_importPrunedFunds(self, tx_hex:str, tx_out_proof:str):
        """
        DESCRIPTION:

            Imports funds (without _rescan) into pruned wallets.
            Corresponding address or script must previously be
            included in wallet. Does NOT check if imported coins
            are already spent, _rescan may be required after the
            point in time in which the specified transaciton was
            included in the blockchain. See `hsd.rpc_getTxOutProof` and
            `hsw.rpc_removePrunedFunds`.

        PARAMS:

            (*) Denotes required argument

            (*) tx_hex : Raw transaction in hex that funds an address already in the wallet.

            (*) tx_out_proof : Hex output from `hsd.rpc_getTxOutProof` containing the tx.
        """

        return self.post('/', {'method': 'importprunedfunds', 'params': [tx_hex, tx_out_proof]})
    ### END METHOD ################################### rpc_importPrunedFunds(self, tx_hex:str, tx_out_proof:str)

    def rpc_importPubKey(self, public_hex_key:str, label:str=None, rescan:bool=None):
        """
        DESCRIPTION:

            Import public key to a watch-only wallet.

        PARAMS:

            (*) Denotes required argument

            (*) public_hex_key : Hex-encoded public key.

            ( ) label   : Ignored but required if additional parameters are passed.

            ( ) rescan  : (bool) Whether to _rescan wallet after importing.
        """

        if rescan is None:
            params = [public_hex_key]
        else:
            params = [public_hex_key, label or 'Unlabeled', bool(rescan)]

        return self.post('/', {'method': 'importpubkey', 'params': params})
    ### END METHOD ################################### rpc_importPubKey(self, public_hex_key:str, label:str=None, rescan:bool=None)

    def rpc_listAccounts(self, min_confirm:int=None, watch_only:bool=None):
        """
        DESCRIPTION:

            Get list of account names and balances.

        PARAMS:

            (*) Denotes required argument

            ( ) min_confirm : Minimum confirmations for transaction to be included in balance.

            ( ) watch_only  : (bool) Include watch-only addresses.
        """

        if min_confirm is None and watch_only is None:
            params = []
        else:
            params = [min_confirm or 0, bool(watch_only)]

        return self.post('/', {'method': 'listaccounts', 'params': params})
    ### END METHOD ################################### rpc_listAccounts(self, min_confirm:int=None, watch_only:bool=None)

    def rpc_lockUnspent(self, lock:bool=True, outputs:list=None):
        """
        DESCRIPTION:

            Lock or unlock specified transaction outputs. If no outputs are
            specified, ALL coins will be unlocked (`unlock` only).

            Note: If no paramaters are passed `lock` will default to `True`

        PARAMS:

            (*) Denotes required argument

            ( ) lock : (bool) `True` = lock coins, `False` = unlock coins. Default = `True`.

            ( ) outputs  : (bool) Array of outputs to lock or unlock.
        """

        params = [not lock] if outputs is None else [not lock, outputs]
        return self.post('/', {'method': 'lockunspent', 'params': params})
    ### END METHOD ################################### rpc_lockUnspent(self, lock:bool=True, outputs:list=None)

    def rpc_listLockUnspent(self):
        """
        DESCRIPTION:

            Get list of currently locked (unspendable) outputs.
            See `hsw.rpc_lockUnspent` and `hsw.lockCoinOutpoints`.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'listlockunspent'})
    ### END METHOD ################################### rpc_listLockUnspent(self)

    def rpc_listReceivedByAccount(self, min_confirm:int=None, include_empty:bool=None, watch_only:bool=None):
        """
        DESCRIPTION:

            Get balances for all accounts in wallet.

        PARAMS:

            (*) Denotes required argument

            ( ) min_confirm   : Minimum confirmations required to count a transaction.

            ( ) include_empty : (bool) Whether to include accounts with zero balance. Default = `False`.

            ( ) watch_only    : (bool) Whether to include watch-only addresses. Default = `False`.
        """

        if min_confirm is None and include_empty is None and watch_only is None:
            params = []
        else:
            params = [min_confirm or 0, bool(include_empty), bool(watch_only)]

        return self.post('/', {'method': 'listreceivedbyaccount', 'params': params})
    ### END METHOD ################################### rpc_listReceivedByAccount(self, min_confirm:int=None, include_empty:bool=None, watch_only:bool=None)

    def rpc_listReceivedByAddress(self, min_confirm:int=None, include_empty:bool=None, watch_only:bool=None):
        """
        DESCRIPTION:

            Get balances for all addresses in wallet.

        PARAMS:

            (*) Denotes required argument

            ( ) min_confirm   : Minimum confirmations required to count a transaction.

            ( ) include_empty : (bool) Whether to include addresses with zero balance. Default = `False`.

            ( ) watch_only    : (bool) Whether to include watch-only addresses. Default = `False`.
        """

        if min_confirm is None and include_empty is None and watch_only is None:
            params = []
        else:
            params = [min_confirm or 0, bool(include_empty), bool(watch_only)]

        return self.post('/', {'method': 'listreceivedbyaddress', 'params': params})
    ### END METHOD ################################### rpc_listReceivedByAddress(self, min_confirm:int=None, include_empty:bool=None, watch_only:bool=None)

    def rpc_listSinceBlock(self, block_hash:str=None, min_confirm:int=None, watch_only:bool=None):
        """
        DESCRIPTION:

            Get all transactions in blocks since a block specified by
            hash, or all transactions if no block is specifiied.

        PARAMS:

            (*) Denotes required argument

            ( ) block_hash    : Hash of earliest block to start listing from.

            ( ) min_confirm   : Minimum confirmations required to count a transaction.

            ( ) watch_only    : (bool) Whether to include watch-only addresses. Default = `False`.
        """

        if block_hash is None and min_confirm is None and watch_only is None:
            params = []
        else:
            params = [block_hash, min_confirm or 0, bool(watch_only)]

        return self.post('/', {'method': 'listsinceblock', 'params': params})
    ### END METHOD ################################### rpc_listSinceBlock(self, block_hash:str=None, min_confirm:int=None, watch_only:bool=None)

    def rpc_listTransactions(self, account:str='', count:int=0, start_from:int=0, watch_only:bool=None):
        """
        DESCRIPTION:

            Get all recent transactions for specified account up
            to a limit, starting from a specified index.

            Deprecated upstream since hsd v7 in favor of `rpc_listHistory`,
            `rpc_listHistoryAfter`, and `rpc_listHistoryByTime`.

        PARAMS:

            (*) Denotes required argument

            ( ) account    : Account name.

            ( ) count      : Max number of transactions to return.

            ( ) start_from : Number of oldest transactions to skip.

            ( ) watch_only : (bool) Whether to include watch-only addresses. Default = `False`.
        """

        if account == '' and count == 0 and start_from == 0 and watch_only is None:
            params = []
        else:
            params = [account, count, start_from, bool(watch_only)]

        return self.post('/', {'method': 'listtransactions', 'params': params})
    ### END METHOD ################################### rpc_listTransactions(self, account:str='', count:int=0, start_from:int=0, watch_only:bool=None)

    def rpc_listHistory(self, account:str='', limit:int=None, reverse:bool=False):
        """
        DESCRIPTION:

            Get confirmed and unconfirmed wallet transaction history.

        PARAMS:

            ( ) account : Account name.

            ( ) limit   : Maximum number of results to return.

            ( ) reverse : Return results in reverse order. Default = False
        """

        options = _compact({'limit': limit})
        if reverse:
            options['reverse'] = True
        return self.post('/', {'method': 'listhistory', 'params': [account, options]})
    ### END METHOD ################################### rpc_listHistory(self, account:str='', limit:int=None, reverse:bool=False)

    def rpc_listHistoryAfter(self, account:str, txid:str, limit:int=None, reverse:bool=False):
        """
        DESCRIPTION:

            Get confirmed and unconfirmed wallet transaction history after a given tx hash (cursor).

        PARAMS:

            (*) Denotes required argument

            (*) account : Account name.

            (*) txid    : Transaction hash cursor to start after.

            ( ) limit   : Maximum number of results to return.

            ( ) reverse : Return results in reverse order. Default = False
        """

        options = _compact({'hash': txid, 'limit': limit})
        if reverse:
            options['reverse'] = True
        return self.post('/', {'method': 'listhistoryafter', 'params': [account, options]})
    ### END METHOD ################################### rpc_listHistoryAfter(self, account:str, txid:str, limit:int=None, reverse:bool=False)

    def rpc_listHistoryByTime(self, account:str, timestamp:int, limit:int=None, reverse:bool=False):
        """
        DESCRIPTION:

            Get confirmed and unconfirmed wallet transaction history after a given timestamp.

        PARAMS:

            (*) Denotes required argument

            (*) account   : Account name.

            (*) timestamp : Unix timestamp to start after.

            ( ) limit     : Maximum number of results to return.

            ( ) reverse   : Return results in reverse order. Default = False
        """

        options = _compact({'time': timestamp, 'limit': limit})
        if reverse:
            options['reverse'] = True
        return self.post('/', {'method': 'listhistorybytime', 'params': [account, options]})
    ### END METHOD ################################### rpc_listHistoryByTime(self, account:str, timestamp:int, limit:int=None, reverse:bool=False)

    def rpc_listUnconfirmed(self, account:str='', limit:int=None, reverse:bool=False):
        """
        DESCRIPTION:

            Get unconfirmed wallet transactions.

        PARAMS:

            ( ) account : Account name.

            ( ) limit   : Maximum number of results to return.

            ( ) reverse : Return results in reverse order. Default = False
        """

        options = _compact({'limit': limit})
        if reverse:
            options['reverse'] = True
        return self.post('/', {'method': 'listunconfirmed', 'params': [account, options]})
    ### END METHOD ################################### rpc_listUnconfirmed(self, account:str='', limit:int=None, reverse:bool=False)

    def rpc_listUnconfirmedAfter(self, account:str, txid:str, limit:int=None, reverse:bool=False):
        """
        DESCRIPTION:

            Get unconfirmed wallet transactions after a given tx hash (cursor).

        PARAMS:

            (*) Denotes required argument

            (*) account : Account name.

            (*) txid    : Transaction hash cursor to start after.

            ( ) limit   : Maximum number of results to return.

            ( ) reverse : Return results in reverse order. Default = False
        """

        options = _compact({'hash': txid, 'limit': limit})
        if reverse:
            options['reverse'] = True
        return self.post('/', {'method': 'listunconfirmedafter', 'params': [account, options]})
    ### END METHOD ################################### rpc_listUnconfirmedAfter(self, account:str, txid:str, limit:int=None, reverse:bool=False)

    def rpc_listUnconfirmedByTime(self, account:str, timestamp:int, limit:int=None, reverse:bool=False):
        """
        DESCRIPTION:

            Get unconfirmed wallet transactions after a given timestamp.

        PARAMS:

            (*) Denotes required argument

            (*) account   : Account name.

            (*) timestamp : Unix timestamp to start after.

            ( ) limit     : Maximum number of results to return.

            ( ) reverse   : Return results in reverse order. Default = False
        """

        options = _compact({'time': timestamp, 'limit': limit})
        if reverse:
            options['reverse'] = True
        return self.post('/', {'method': 'listunconfirmedbytime', 'params': [account, options]})
    ### END METHOD ################################### rpc_listUnconfirmedByTime(self, account:str, timestamp:int, limit:int=None, reverse:bool=False)

    def rpc_listUnspent(self, min_confirm:int=None, max_confirm:int=None, addresses:list=None):
        """
        DESCRIPTION:

            Get unsepnt transaction outputs from all addreses,
            or a specific set of addresses.

        PARAMS:

            (*) Denotes required argument

            ( ) min_confirm : Minimum confirmations required to return tx.

            ( ) max_confirm : Maximum confirmations required to return tx.

            ( ) addresses   : Array of addresses to filter.
        """

        if min_confirm is None and max_confirm is None and addresses is None:
            params = []
        else:
            params = [min_confirm or 0, max_confirm or 0, list(addresses) if addresses else []]

        return self.post('/', {'method': 'listunspent', 'params': params})
    ### END METHOD ################################### rpc_listUnspent(self, min_confirm:int=None, max_confirm:int=None, addresses=None)

    def rpc_sendFrom(self, from_account:str, to_address:str, amount:float, min_confirm:int=None):
        """
        DESCRIPTION:

            Send HNS from an account to an address.

            Note: This command involves entering HNS values, be careful with different formats
                  of values for different APIs. See https://hsd-dev.org/api-docs/?shell--curl#values
                  to learn more.

        PARAMS:

            (*) Denotes required argument

            (*) from_account : Wallet account to spend outputs from.

            (*) to_address   : Handshake address to send funds to.

            (*) amount       : Amount (in HNS) to send.

            ( ) min_confirm  : Minimum confirmations for output to be spent from.
        """

        params = [from_account, to_address, amount] if min_confirm is None else [from_account, to_address, amount, min_confirm]
        return self.post('/', {'method': 'sendfrom', 'params': params})
    ### END METHOD ################################### rpc_sendFrom(self, from_account:str, to_address:str, amount:float, min_confirm:int=None)

    def rpc_sendMany(self, from_account:str, outputs:dict, min_confirm:int=None, subtract_fee:bool=None, label:str=None):
        """
        DESCRIPTION:

            Send different amounts of HNS from an account to multiple addresses.

            Note: This command involves entering HNS values, be careful with different formats
                  of values for different APIs. See https://hsd-dev.org/api-docs/?shell--curl#values
                  to learn more.

        PARAMS:

            (*) Denotes required argument

            (*) from_account : Wallet account to spend outputs from.

            (*) outputs      : (json) of Handshake addresses and amounts to send.

            ( ) min_confirm  : Minimum confirmations for output to be spent from.

            ( ) subtract_fee : (bool) Subtract the transaction fee equally from the output amounts.

            ( ) label        : Ignored but required if additional parameters are passed.
        """

        if min_confirm is None and label is None and subtract_fee is None:
            params = [from_account, outputs]
        else:
            params = [from_account, outputs, min_confirm or 0, label or 'Unlabeled Transaction', bool(subtract_fee)]

        return self.post('/', {'method': 'sendmany', 'params': params})
    ### END METHOD ################################### rpc_sendMany(self, from_account:str, outputs:dict, min_confirm:int=None, subtract_fee:bool=None, label:str=None)

    def rpc_createSendToAddress(self, to_address:str, amount:float, subtract_fee:bool=None, comment:str=None, comment_to:str=None):
        """
        DESCRIPTION:

            Create transaction sending HNS to a given address without signing or broadcasting it.

            Note: This command involves entering HNS values, be careful with different formats
                  of values for different APIs. See https://hsd-dev.org/api-docs/?shell--curl#values
                  to learn more.

        PARAMS:

            (*) Denotes required argument

            (*) to_address   : Handshake address to send funds to.

            (*) amount       : Amount (in HNS) to send.

            ( ) subtract_fee : (bool) Subtract the transaction fee equally from the output amount.

            ( ) comment      : Ignored but required if additional parameters are passed.

            ( ) comment_to   : Ignored but required if additional parameters are passed.
        """

        if subtract_fee is None and comment is None and comment_to is None:
            params = [to_address, amount]
        else:
            params = [to_address, amount, comment or 'No Comment.', comment_to or 'No Comment.', bool(subtract_fee)]

        return self.post('/', {'method': 'createsendtoaddress', 'params': params})
    ### END METHOD ################################### rpc_createSendToAddress(self, to_address:str, amount:float, subtract_fee:bool=None, comment:str=None, comment_to:str=None)

    def rpc_sendToAddress(self, to_address:str, amount:float, subtract_fee:bool=None, comment:str=None, comment_to:str=None):
        """
        DESCRIPTION:

            Send HNS to an address.

            Note: This command involves entering HNS values, be careful with different formats
                  of values for different APIs. See https://hsd-dev.org/api-docs/?shell--curl#values
                  to learn more.

        PARAMS:

            (*) Denotes required argument

            (*) to_address   : Handshake address to send funds to.

            (*) amount       : Amount (in HNS) to send.

            ( ) subtract_fee : (bool) Subtract the transaction fee equally from the output amount.

            ( ) comment      : Ignored but required if additional parameters are passed.

            ( ) comment_to   : Ignored but required if additional parameters are passed.
        """

        if subtract_fee is None and comment is None and comment_to is None:
            params = [to_address, amount]
        else:
            params = [to_address, amount, comment or 'No Comment.', comment_to or 'No Comment.', bool(subtract_fee)]

        return self.post('/', {'method': 'sendtoaddress', 'params': params})
    ### END METHOD ################################### rpc_sendToAddress(self, to_address:str, amount:float, subtract_fee:bool=None, comment:str=None, comment_to:str=None)

    def rpc_setTxFee(self, tx_fee:float=0):
        """
        DESCRIPTION:

            Set the fee rate for all new transactions until the fee is changed
            again, or set to `0` (will return to automatic fee).

            Note: This command involves entering HNS values, be careful with different formats
                  of values for different APIs. See https://hsd-dev.org/api-docs/?shell--curl#values
                  to learn more.

        PARAMS:

            (*) Denotes required argument

            ( ) tx_fee : Fee rate in HNS/kB. Default = `0`
        """

        return self.post('/', {'method': 'settxfee', 'params': [tx_fee]})
    ### END METHOD ################################### rpc_setTxFee(self, tx_fee:float=0)

    def rpc_signMessage(self, address:str, message:str):
        """
        DESCRIPTION:

            Sign an arbitrary message with the private key corresponding to a
            specified Handshake address in the wallet.

            Note: Due to behavior of some shells like bash, if your message
            contains spaces you may need to add additional quotes like
            this: `"'"$message"'"`

        PARAMS:

            (*) Denotes required argument

            (*) address : Wallet address to use for signing.

            (*) message : The message to sign.
        """

        return self.post('/', {'method': 'signmessage', 'params': [address, message]})
    ### END METHOD ################################### rpc_signMessage(self, address:str, message:str)

    def rpc_signMessageWithName(self, name:str, message:str):
        """
        DESCRIPTION:

            Sign an arbitrary message with the private key corresponding to
            a Handshake address that owns the specified name in the wallet.

            Note: Due to behavior of some shells like bash, if your message
            contains spaces you may need to add additional quotes like
            this: `"'"$message"'"`

        PARAMS:

            (*) Denotes required argument

            (*) name    : Domain name to use for signing.

            (*) message : The message to sign.
        """

        return self.post('/', {'method': 'signmessagewithname', 'params': [name, message]})
    ### END METHOD ################################### rpc_signMessageWithName(self, name:str, message:str)

    def rpc_walletLock(self):
        """
        DESCRIPTION:

            Locks the wallet by removing the decryption key from memory.
            See `hsw.rpc_walletPassphrase`.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'walletlock'})
    ### END METHOD ################################### rpc_walletLock(self)

    def rpc_walletPasswordChange(self, old_passphrase:str, new_passphrase:str):
        """
        DESCRIPTION:

            Change the wallet encryption pasphrase.

        PARAMS:

            (*) Denotes required argument

            (*) old_passphrase : The current wallet passphrase.

            (*) new_passphrase : New passphrase.
        """

        return self.post('/', {'method': 'walletpassphrasechange', 'params': [old_passphrase, new_passphrase]})
    ### END METHOD ################################### rpc_walletPasswordChange(self, old_passphrase:str, new_passphrase:str)

    def rpc_walletPassphrase(self, passphrase:str, timeout:int=600):
        """
        DESCRIPTION:

            Store wallet decryption key in memory, unlocking the wallet keys.

        PARAMS:

            (*) Denotes required argument

            (*) passphrase : The current wallet passphrase.

            ( ) timeout    : Amount of time in seconds decryption key will stay in memory. Default = `600`
        """

        return self.post('/', {'method': 'walletpassphrase', 'params': [passphrase, timeout]})
    ### END METHOD ################################### rpc_walletPassphrase(self, passphrase:str, timeout:int=600)

    def rpc_removePrunedFunds(self, tx_id:str):
        """
        DESCRIPTION:

            Deletes the specified transaction from the wallet database.
            See `hsw.rpc_importPrunedFunds`.

        PARAMS:

            (*) Denotes required argument

            (*) tx_id : ID of the transaction to remove.
        """

        return self.post('/', {'method': 'removeprunedfunds', 'params': [tx_id]})
    ### END METHOD ################################### rpc_removePrunedFunds(self, tx_id:str)

    def rpc_getMemoryInfo(self):
        """
        DESCRIPTION:

            Get information about memory usage. Identical to
            node RPC call `hsd.rpc_getMemoryInfo`.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'getmemoryinfo'})
    ### END METHOD ################################### rpc_getMemoryInfo(self)

    def rpc_setLogLevel(self, log_level:str='NONE'):
        """
        DESCRIPTION:

            Change Log level of the running node.

            Levels are: `NONE`, `ERROR`, `WARNING`, `INFO`, `DEBUG`, `SPAM`

        PARAMS:

            (*) Denotes required argument

            ( ) log_level : Level for the logger. Default = `NONE`
        """

        return self.post('/', {'method': 'setloglevel', 'params': [log_level]})
    ### END METHOD ################################### rpc_setLogLevel(self, log_level:str='NONE')

    def rpc_stop(self):
        """
        DESCRIPTION:

            Closes the wallet database.

        PARAMS:

            None.
        """

        return self.post('/', {'method': 'stop'})
    ### END METHOD ################################### rpc_stop(self)
