from ._http import HTTPClient


class hsd(HTTPClient):

    def __init__(self, api_key:str, ip_address:str='127.0.0.1', port:int=12037, timeout:int=30):
        """
        DESCRIPTION:

            Initialization of the hsd class

        PARAMS:

        (*) Denotes required argument

        (*) api_key    : HSD API key.

        ( ) ip_address : HSD node ip. Default = '127.0.0.1'.

        ( ) port       : HSD node port. Default = 12037

        ( ) timeout    : Request timeout in seconds. Default = 30
        """

        super().__init__(api_key, ip_address, port, timeout)
    ### END METHOD ################################### __init__(self, api_key:str, ip_address:str='127.0.0.1', port:int=12037, timeout:int=30)

    def getInfo(self):
        """
        DESCRIPTION:

            Get server Info.

        PARAMS:

            None
        """

        return self.get('/')
    ### END METHOD ################################### getInfo(self)

    def getMemPool(self):
        """
        DESCRIPTION:

            Get mempool snapshot (array of json txs).

        PARAMS:

            None
        """

        return self.get('/mempool')
    ### END METHOD ################################### getMemPool(self)

    def getMemPoolInvalid(self, verbose:bool=False):
        """
        DESCRIPTION:

            Get mempool rejects filter (a Bloom filter used to store rejected TX hashes).


        PARAMS:

        (*) Denotes required argument

        ( ) verbose : (bool) Returns entire Bloom Filter in filter property, hex-encoded.
        """

        return self.get('/mempool/invalid', params={'verbose': verbose})
    ### END METHOD ################################### getMemPoolInvalid(self, verbose:bool=False)

    def getMemPoolInvalidHash(self, tx_hash:str):
        """
        DESCRIPTION:

            Test a TX hash against the mempool rejects filter.


        PARAMS:

        (*) Denotes required argument

        (*) tx_hash : Transaction hash.
        """

        return self.get(f'/mempool/invalid/{tx_hash}')
    ### END METHOD ################################### getMemPoolInvalidHash(self, tx_hash:str)

    def getBlockByHashOrHeight(self, block_hash_or_height:str):
        """
        DESCRIPTION:

            Returns block info by block hash or height.

        PARAMS:

        (*) Denotes required argument

        (*) block_hash_or_height : Hash or Height of block.
        """

        return self.get(f'/block/{block_hash_or_height}')
    ### END METHOD ################################### getBlockByHashOrHeight(self, block_hash_or_height:str)

    def getHeaderByHashOrHeight(self, header_hash_or_height:str):
        """
        DESCRIPTION:

            Returns block header by block hash or height.

        PARAMS:

        (*) Denotes required argument

        (*) header_hash_or_height : Hash or Height of block.
        """

        return self.get(f'/header/{header_hash_or_height}')
    ### END METHOD ################################### getHeaderByHashOrHeight(self, header_hash_or_height:str)

    def broadcast(self, tx_hex:str):
        """
        DESCRIPTION:

            Broadcast a transaction by adding it to the node's mempool.
            If mempool verification fails, the node will still forcefully
            advertise and relay the transaction for the next 60 seconds.

        PARAMS:

        (*) Denotes required argument

        (*) tx_hex : Raw transaction in hex.
        """

        return self.post('/broadcast/', {'tx': tx_hex})
    ### END METHOD ################################### broadcast(self, tx_hex:str)

    def broadcastClaim(self, claim:str):
        """
        DESCRIPTION:

            Broadcast a claim by adding it to the node's mempool.

        PARAMS:

        (*) Denotes required argument

        (*) claim : Raw claim in hex.
        """

        return self.post('/claim/', {'claim': claim})
    ### END METHOD ################################### broadcastClaim(self, claim:str)

    def getFeeEstimate(self, blocks:int):
        """
        DESCRIPTION:

            Estimate the fee required (in dollarydoos per kB) for a
            transaction to be confirmed by the network within a targeted
            number of blocks (default 1).

        PARAMS:

        (*) Denotes required argument

        (*) blocks : Number of blocks to target confirmation.
        """

        return self.get('/fee', params={'blocks': blocks})
    ### END METHOD ################################### getFeeEstimate(self, blocks:int)

    def reset(self, height:int):
        """
        DESCRIPTION:

            Triggers a hard-reset of the blockchain. All blocks are disconnected
            from the tip down to the provided height. Indexes and Chain Entries
            are removed. Useful for "rescanning" an SPV wallet. Since there are
            no blocks stored on disk, the only way to _rescan the blockchain is to
            re-request [merkle]blocks from peers.

        PARAMS:

        (*) Denotes required argument

        (*) height : Block height to reset chain to.
        """

        return self.post('/reset', {'height': height})
    ### END METHOD ################################### reset(self, height:int)

    def getCoinByHashIndex(self, tx_hash:str, index:int):
        """
        DESCRIPTION:

            Get coin by outpoint (hash and index). Returns coin in hsd coin
            JSON format. value is always expressed in subunits.

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash : Hash of tx.

        (*) index   : Output's index in tx.
        """

        return self.get(f'/coin/{tx_hash}/{index}')
    ### END METHOD ################################### getCoinByHashIndex(self, tx_hash:str, index:int)

    def getCoinByAddress(self, address:str):
        """
        DESCRIPTION:

            Get coin objects array by address.

        PARAMS:

        (*) Denotes required argument

        (*) address : Handshake address.
        """

        return self.get(f'/coin/address/{address}')
    ### END METHOD ################################### getCoinByAddress(self, address:str)

    def getCoinsByAddresses(self, addresses:list):
        """
        DESCRIPTION:

            Get coin objects array for a bulk list of addresses. Note: hsd
            marks this endpoint for eventual deprecation upstream.

        PARAMS:

        (*) Denotes required argument

        (*) addresses : List array of Handshake addresses.
        """

        return self.post('/coin/address', {'addresses': addresses})
    ### END METHOD ################################### getCoinsByAddresses(self, addresses:list)

    def getTxByHash(self, tx_hash:str):
        """
        DESCRIPTION:

           Returns transaction objects array by hash

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash : Transaction hash.
        """

        return self.get(f'/tx/{tx_hash}')
    ### END METHOD ################################### getTxByHash(self, tx_hash:str)

    def getTxByAddress(self, address:str):
        """
        DESCRIPTION:

           Returns transaction objects array by address.

        PARAMS:

        (*) Denotes required argument

        (*) address : Handshake address.
        """

        return self.get(f'/tx/address/{address}')
    ### END METHOD ################################### getTxByAddress(self, address:str)

    def getTXsByAddresses(self, addresses:list):
        """
        DESCRIPTION:

           Returns transaction objects array for a bulk list of addresses.
           Note: hsd marks this endpoint for eventual deprecation upstream.

        PARAMS:

        (*) Denotes required argument

        (*) addresses : List array of Handshake addresses.
        """

        return self.post('/tx/address', {'addresses': addresses})
    ### END METHOD ################################### getTXsByAddresses(self, addresses:list)

    def rpc_stop(self):
        """
        DESCRIPTION:

            Stops the running node.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'stop'})
    ### END METHOD ################################### rpc_stop(self)

    def rpc_getInfo(self):
        """
        DESCRIPTION:

            Returns general info.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getinfo'})
    ### END METHOD ################################### rpc_getInfo(self)

    def rpc_getMemoryInfo(self):
        """
        DESCRIPTION:

            Returns Memory usage info.

        PARAMS:

            None
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

    def rpc_validateAddress(self, address:str):
        """
        DESCRIPTION:

            Validates address.

        PARAMS:

        (*) Denotes required argument

        (*) address : Address to validate.
        """

        return self.post('/', {'method': 'validateaddress', 'params': [address]})
    ### END METHOD ################################### rpc_validateAddress(self, address:str)

    def rpc_createMultiSig(self, nrequired:int, key_dict:str):
        """
        DESCRIPTION:

            Create multisig address.

        PARAMS:

        (*) Denotes required argument

        (*) nrequired : Required number of approvals for spending.

        (*) key_dict  : List array of public keys.
        """

        return self.post('/', {'method': 'createmultisig', 'params': [nrequired, key_dict]})
    ### END METHOD ################################### rpc_createMultiSig(self, nrequired:int, key_dict:str)

    def rpc_signMessageWithPrivKey(self, private_key:str, message:str):
        """
        DESCRIPTION:

            Signs message with private key.

        PARAMS:
        (*) Denotes required argument

        (*) private_key : Private key.

        (*) message : Message you want to sign.
        """

        return self.post('/', {'method': 'signmessagewithprivkey', 'params': [private_key, message]})
    ### END METHOD ################################### rpc_signMessageWithPrivKey(self, private_key:str, message:str)

    def rpc_verifyMessage(self, address:str, signature:str, message:str):
        """
        DESCRIPTION:

            Verify signature.

        PARAMS:

        (*) Denotes required argument

        (*) address   : Address of the signer.

        (*) signature : Signature of signed message.

        (*) message   : Message that was signed.
        """

        return self.post('/', {'method': 'verifymessage', 'params': [address, signature, message]})
    ### END METHOD ################################### rpc_verifyMessage(self, address:str, signature:str, message:str)

    def rpc_verifyMessageWithName(self, name:str, signature:str, message:str):
        """
        DESCRIPTION:

            Retrieves the address that owns a name and verifies signature.

        PARAMS:

        (*) Denotes required argument

        (*) name      : Name to retrieve the address used to sign.

        (*) signature : Signature of signed message.

        (*) message   : Message that was signed.
        """

        return self.post('/', {'method': 'verifymessagewithname', 'params': [name, signature, message]})
    ### END METHOD ################################### rpc_verifyMessageWithName(self, name:str, signature:str, message:str)

    def rpc_setMockTime(self, timestamp:int):
        """
        DESCRIPTION:

            Changes network time (This is consensus-critical)

        PARAMS:

        (*) Denotes required argument

        (*) timestamp : Timestamp to change to.
        """

        return self.post('/', {'method': 'setmocktime', 'params': [timestamp]})
    ### END METHOD ################################### rpc_setMockTime(self, timestamp:int)

    def rpc_pruneBlockchain(self):
        """
        DESCRIPTION:

            Prunes the blockchain, it will keep blocks specified in Network Configurations.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'pruneblockchain', 'params': []})
    ### END METHOD ################################### rpc_pruneBlockchain(self)

    def rpc_invalidateBlock(self, block_hash:str):
        """
        DESCRIPTION:

            Invalidates the block in the chain. It will rewind network to
            blockhash and invalidate it. It won't accept that block as valid.
            Invalidation will work while running,restarting node will remove
            invalid block from list.

        PARAMS:

        (*) Denotes required argument

        (*) block_hash : Block's hash.
        """

        return self.post('/', {'method': 'invalidateblock', 'params': [block_hash]})
    ### END METHOD ################################### rpc_invalidateBlock(self, block_hash:str)

    def rpc_reconsiderBlock(self, block_hash:str):
        """
        DESCRIPTION:

            This rpc command will remove block from invalid block set.

        PARAMS:

        (*) Denotes required argument

        (*) block_hash : Block's hash.
        """

        return self.post('/', {'method': 'reconsiderblock', 'params': [block_hash]})
    ### END METHOD ################################### rpc_reconsiderBlock(self, block_hash:str)

    def rpc_getBlockchainInfo(self):
        """
        DESCRIPTION:

            Returns blockchain information.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getblockchaininfo'})
    ### END METHOD ################################### rpc_getBlockchainInfo(self)

    def rpc_getBestBlockHash(self):
        """
        DESCRIPTION:

            Returns Block Hash of the tip.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getbestblockhash'})
    ### END METHOD ################################### rpc_getBestBlockHash(self)

    def rpc_getBlockCount(self):
        """
        DESCRIPTION:

            Returns block count.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getblockcount'})
    ### END METHOD ################################### rpc_getBlockCount(self)

    def rpc_getBlock(self, block_hash:str, verbose:bool=True, details:bool=False):
        """
        DESCRIPTION:

            Returns information about block.

        PARAMS:

        (*) Denotes required argument

        (*) block_hash : Hash of the block.

        ( ) verbose    : (bool) If set to False, it will return hex of the block.

        ( ) details    : (bool) If set to True, it will return transaction details too.
        """

        return self.post('/', {'method': 'getblock', 'params': [block_hash, verbose, details]})
    ### END METHOD ################################### rpc_getBlock(self, block_hash:str, verbose:bool=True, details:bool=False)

    def rpc_getBlockByHeight(self, block_height:int, verbose:bool=True, details:bool=False):
        """
        DESCRIPTION:

            Returns information about block by height.

        PARAMS:

        (*) Denotes required argument

        (*) block_height : Height of the block in the blockchain.

        ( ) verbose      : (bool) If set to True, it will return hex of the block.

        ( ) details      : (bool) If set to True, it will return transaction details too.
        """

        return self.post('/', {'method': 'getblockbyheight', 'params': [block_height, verbose, details]})
    ### END METHOD ################################### rpc_getBlockByHeight(self, block_height:int, verbose:bool=True, details:bool=False)

    def rpc_getBlockHash(self, block_height:int):
        """
        DESCRIPTION:

            Returns block's hash given its height.

        PARAMS:

        (*) Denotes required argument

        (*) block_height : Height of the block in the blockchain.
        """

        return self.post('/', {'method': 'getblockhash', 'params': [block_height]})
    ### END METHOD ################################### rpc_getBlockHash(self, block_height:int)

    def rpc_getBlockHeader(self, block_hash:str, verbose:bool=True):
        """
        DESCRIPTION:

            Returns a block's header given its hash.

        PARAMS:

        (*) Denotes required argument

        (*) block_hash : Hash of the block in the blockchain.

        ( ) verbose    : If set to False, it will return (hex) of the block.
        """

        return self.post('/', {'method': 'getblockheader', 'params': [block_hash, verbose]})
    ### END METHOD ################################### rpc_getBlockHeader(self, block_hash:str, verbose:bool=True)

    def rpc_getChainTips(self):
        """
        DESCRIPTION:

            Returns chaintips.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getchaintips'})
    ### END METHOD ################################### rpc_getChainTips(self)

    def rpc_getDifficulty(self):
        """
        DESCRIPTION:

            Returns current difficulty level.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getdifficulty'})
    ### END METHOD ################################### rpc_getDifficulty(self)

    def rpc_getMemPoolInfo(self):
        """
        DESCRIPTION:

            Returns informations about mempool.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getmempoolinfo'})
    ### END METHOD ################################### rpc_getMemPoolInfo(self)

    def rpc_getMemPoolAncestors(self, tx_hash:str, verbose:bool=False):
        """
        DESCRIPTION:

            Returns all in-mempool ancestors for a transaction in the mempool.

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash  : Transaction Hash.

        ( ) verbose : False returns only tx hashs, true - returns dependency tx info.
        """

        return self.post('/', {'method': 'getmempoolancestors', 'params': [tx_hash, verbose]})
    ### END METHOD ################################### rpc_getMemPoolAncestors(self, tx_hash:str, verbose:bool=False)

    def rpc_getMemPoolDescendants(self, tx_hash:str, verbose:bool=False):
        """
        DESCRIPTION:

            Returns all in-mempool descendants for a transaction in the mempool.

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash  : Transaction Hash.

        ( ) verbose : False returns only tx hashs, true - returns dependency tx info.
        """

        return self.post('/', {'method': 'getmempooldescendants', 'params': [tx_hash, verbose]})
    ### END METHOD ################################### rpc_getMemPoolDescendants(self, tx_hash:str, verbose:bool=False)

    def rpc_getMemPoolEntry(self, tx_hash:str):
        """
        DESCRIPTION:

            Returns mempool transaction info by its hash.

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash : Transaction Hash.
        """

        return self.post('/', {'method': 'getmempoolentry', 'params': [tx_hash]})
    ### END METHOD ################################### rpc_getMemPoolEntry(self, tx_hash:str)

    def rpc_getRawMemPool(self, verbose:bool=False):
        """
        DESCRIPTION:

            Returns mempool detailed information (on verbose). Or mempool tx list.

        PARAMS:

        (*) Denotes required argument

        ( ) verbose : False returns only tx hashs, true - returns full tx info.
        """

        return self.post('/', {'method': 'getrawmempool', 'params': [verbose]})
    ### END METHOD ################################### rpc_getRawMemPool(self, verbose:bool=False)

    def rpc_prioritiseTransaction(self, tx_hash:str, priority_delta:int, fee_delta:int):
        """
        DESCRIPTION:

            Prioritises the transaction.

            Note: Changing fee or priority will only trick local miner (using this mempool) into
                accepting Transaction(s) into the block. (even if Priority/Fee doen't qualify)

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash        : Transaction hash.

        (*) priority_delta : Virtual priority to add/subtract to the entry.

        (*) fee_delta      : Virtual fee to add/subtract to the entry.
        """

        return self.post('/', {'method': 'prioritisetransaction', 'params': [tx_hash, priority_delta, fee_delta]})
    ### END METHOD ################################### rpc_prioritiseTransaction(self, tx_hash:str, priority_delta:int, fee_delta:int)

    def rpc_estimateFee(self, n_blocks:int=1):
        """
        DESCRIPTION:

            Estimates fee to be paid for transaction.

        PARAMS:

        (*) Denotes required argument

        ( ) n_blocks : Number of blocks to check for estimation.
        """

        return self.post('/', {'method': 'estimatefee', 'params': [n_blocks]})
    ### END METHOD ################################### rpc_estimateFee(self, n_blocks:int=1)

    def rpc_estimatePriority(self, n_blocks:int=1):
        """
        DESCRIPTION:

            Estimates the priority (coin age) that a transaction
            needs in order to be included within a certain number
            of blocks as a free high-priority transaction.

        PARAMS:

        (*) Denotes required argument

        ( ) n_blocks : Number of blocks to check for estimation.
        """

        return self.post('/', {'method': 'estimatepriority', 'params': [n_blocks]})
    ### END METHOD ################################### rpc_estimatePriority(self, n_blocks:int=1)

    def rpc_estimateSmartFee(self, n_blocks:int=1):
        """
        DESCRIPTION:

            Estimates smart fee to be paid for transaction.

        PARAMS:

        (*) Denotes required argument

        ( ) n_blocks : Number of blocks to check for estimation.
        """

        return self.post('/', {'method': 'estimatesmartfee', 'params': [n_blocks]})
    ### END METHOD ################################### rpc_estimateSmartFee(self, n_blocks:int=1)

    def rpc_estimateSmartPriority(self, n_blocks:int=1):
        """
        DESCRIPTION:

            Estimates smart priority (coin age) that a transaction
            needs in order to be included within a certain number
            of blocks as a free high-priority transaction.

        PARAMS:

        (*) Denotes required argument

        (*) n_blocks : Number of blocks to check for estimation.
        """

        return self.post('/', {'method': 'estimatesmartpriority', 'params': [n_blocks]})
    ### END METHOD ################################### rpc_estimateSmartPriority(self, n_blocks:int=1)

    def rpc_getTxOut(self, tx_hash:str, index:int, include_mempool:int=1):
        """
        DESCRIPTION:

            Get outpoint of the transaction.

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash         : Transaction hash.

        (*) index           : Index of the outpoint tx.

        ( ) include_mempool : Whether to include mempool transactions.
        """

        return self.post('/', {'method': 'gettxout', 'params': [tx_hash, index, include_mempool]})
    ### END METHOD ################################### rpc_getTxOut(self, tx_hash:str, index:int, include_mempool:int=1)

    def rpc_getTxOutSetInfo(self):
        """
        DESCRIPTION:

            Returns information about UTXO's from Chain.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'gettxoutsetinfo', 'params': []})
    ### END METHOD ################################### rpc_getTxOutSetInfo(self)

    def rpc_getRawTransaction(self, tx_hash:str, verbose:bool=False):
        """
        DESCRIPTION:

            Returns raw transaction

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash  : Transaction hash.

        ( ) verbose : Returns json formatted if true.
        """

        return self.post('/', {'method': 'getrawtransaction', 'params': [tx_hash, verbose]})
    ### END METHOD ################################### rpc_getRawTransaction(self, tx_hash:str, verbose:bool=False)

    def rpc_decodeRawTransaction(self, raw_tx:str):
        """
        DESCRIPTION:

            Decodes raw tx and provide chain info.

        PARAMS:

        (*) Denotes required argument

        (*) raw_tx : Raw transaction hex.
        """

        return self.post('/', {'method': 'decoderawtransaction', 'params': [raw_tx]})
    ### END METHOD ################################### rpc_decodeRawTransaction(self, raw_tx:str)

    def rpc_decodeScript(self, script:str):
        """
        DESCRIPTION:

            Decodes script.

        PARAMS:

        (*) Denotes required argument

        (*) script : Script hex.
        """

        return self.post('/', {'method': 'decodescript', 'params': [script]})
    ### END METHOD ################################### rpc_decodeScript(self, script:str)

    def rpc_sendRawTransaction(self, raw_tx:str):
        """
        DESCRIPTION:

            Sends raw transaction without verification.

        PARAMS:

        (*) Denotes required argument

        (*) raw_tx : Raw transaction hex.
        """

        return self.post('/', {'method': 'sendrawtransaction', 'params': [raw_tx]})
    ### END METHOD ################################### rpc_sendRawTransaction(self, raw_tx:str)

    def rpc_createRawTransaction(self, tx_hash:str, tx_index:int, address:str, amount:int, data:str=None):
        """
        DESCRIPTION:

            Creates raw, unsigned transaction without any formal verification.

        PARAMS:

        (*) Denotes required argument

        (*) tx_hash  : Transaction hash.

        (*) tx_index : Transaction outpoint index.

        (*) address  : Recipient address.

        (*) amount   : Amount to send in HNS (float).

        ( ) data     : Hex-encoded nulldata to attach as an extra output.
                       hsd rejects an empty string here ("Hash is the wrong
                       size"), so it's omitted unless given.
        """

        inputs = [{'txid': tx_hash, 'vout': tx_index}]
        outputs = {address: amount}
        if data:
            outputs['data'] = data
        return self.post('/', {'method': 'createrawtransaction', 'params': [inputs, outputs]})
    ### END METHOD ################################### rpc_createRawTransaction(self, tx_hash:str, tx_index:int, address:str, amount:int, data:str)

    def rpc_signRawTransaction(self, raw_tx:str, tx_hash:str, tx_index:int, address:str, amount:int, private_key:str):
        """
        DESCRIPTION:

            Signs raw transaction.

        PARAMS:

        (*) Denotes required argument

        (*) raw_tx      : Raw transaction.

        (*) tx_hash     : Transaction hash.

        (*) tx_index    : Transaction outpoint index.

        (*) address     : Address which received the output you're going to sign.

        (*) amount      : Amount the output is worth.

        ( ) private_key : List of private keys.
        """

        prevtxs = [{'txid': tx_hash, 'vout': tx_index, 'address': address, 'amount': amount}]
        return self.post('/', {'method': 'signrawtransaction', 'params': [raw_tx, prevtxs, [private_key]]})
    ### END METHOD ################################### rpc_signRawTransaction(self, raw_tx:str, tx_hash:str, tx_index:int, address:str, amount:int, private_key:str)

    def rpc_getTxOutProof(self, tx_id_list:list, block_hash:str=None):
        """
        DESCRIPTION:

            Checks if transactions are within block. Returns proof of transaction inclusion (raw MerkleBlock).

        PARAMS:

        (*) Denotes required argument

        (*) tx_id_list : List array of transaction ID's

        ( ) block_hash : Hash of the block to search (searches the whole chain if omitted).
        """

        params = [tx_id_list] if block_hash is None else [tx_id_list, block_hash]
        return self.post('/', {'method': 'gettxoutproof', 'params': params})
    ### END METHOD ################################### rpc_getTxOutProof(self, tx_id_list:list, block_hash:str=None)

    def rpc_verifyTxOutProof(self, proof:str):
        """
        DESCRIPTION:

            Checks the proof for transaction inclusion. Returns transaction hash if valid.

        PARAMS:

        (*) Denotes required argument

        (*) proof : Proof of transaction inclusion (raw MerkleBlock).
        """

        return self.post('/', {'method': 'verifytxoutproof', 'params': [proof]})
    ### END METHOD ################################### rpc_verifyTxOutProof(self, proof)

    def rpc_getNetworkHashPerSec(self, blocks:int=120, height:int=1):
        """
        DESCRIPTION:

            Returns the estimated current or historical network hashes per second, based on last blocks.

        PARAMS:

        (*) Denotes required argument

        (*) blocks : Number of blocks to lookup.

        (*) height : Starting height for calculations.
        """

        return self.post('/', {'method': 'getnetworkhashps', 'params': [blocks, height]})
    ### END METHOD ################################### rpc_getNetworkHashPerSec(self, blocks:int=120, height:int=1)

    def rpc_getMiningInfo(self):
        """
        DESCRIPTION:

            Returns mining info.

            Note: currentblocksize, currentblockweight, currentblocktx, difficulty are
                  returned when there's active work. generate - is true when hsd itself
                  is mining.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getmininginfo', 'params': []})
    ### END METHOD ################################### rpc_getMiningInfo(self)

    def rpc_getWork(self, data:str=None):
        """
        DESCRIPTION:

            Returns hashing work to be solved by miner. Or submits solved block.

        PARAMS:

        (*) Denotes required argument

        ( ) data : Data to be submitted to the network.
        """

        params = [data] if data is not None else []
        return self.post('/', {'method': 'getwork', 'params': params})
    ### END METHOD ################################### rpc_getWork(self, data:str=None)

    def rpc_getWorkLP(self):
        """
        DESCRIPTION:

            Long polling for new work.

            Returns new work, whenever new TX is received in the mempoolor new
            block has been discovered. So miner can restart mining on new data.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getworklp', 'params': []})
    ### END METHOD ################################### rpc_getWorkLP(self)

    def rpc_getBlockTemplate(self):
        """
        DESCRIPTION:

            Returns block template or proposal for use with mining. Also validates proposal if mode is specified as proposal.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getblocktemplate', 'params': []})
    ### END METHOD ################################### rpc_getBlockTemplate(self):

    def rpc_submitBlock(self, block_data:str):
        """
        DESCRIPTION:

            Adds block to chain.

        PARAMS:

        (*) Denotes required argument

        (*) block_data : Mined block data (hex).
        """

        return self.post('/', {'method': 'submitblock', 'params': [block_data]})
    ### END METHOD ################################### rpc_submitBlock(self, block_data:str)

    def rpc_verifyBlock(self, block_data:str):
        """
        DESCRIPTION:

            Verifies the block data.

        PARAMS:
        (*) Denotes required argument

        (*) block_data : Mined block data (hex).
        """

        return self.post('/', {'method': 'verifyblock', 'params': [block_data]})
    ### END METHOD ################################### rpc_verifyBlock(self, block_data:str)

    def rpc_setGenerate(self, mining:int=0, proc_limit:int=0):
        """
        DESCRIPTION:

            Will start the mining on CPU.

        PARAMS:

        (*) Denotes required argument

        ( ) mining    : 1 will start mining, 0 will stop. Default = 0

        ( ) proc_limit : 1 will set processor limit, 0 will remove limit. Default = 0
        """

        return self.post('/', {'method': 'setgenerate', 'params': [mining, proc_limit]})
    ### END METHOD ################################### rpc_setGenerate(self, mining:int=0, proc_limit:int=0)

    def rpc_getGenerate(self):
        """
        DESCRIPTION:

            Returns status of mining on Node.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getgenerate', 'params': []})
    ### END METHOD ################################### rpc_getGenerate(self)

    def rpc_generate(self, num_blocks:int=1):
        """
        DESCRIPTION:

            Mines numblocks number of blocks. Will return once all blocks are mined. CLI command may timeout before that happens.

        PARAMS:
        (*) Denotes required argument

        ( ) num_blocks : Number of blocks to mine.
        """

        return self.post('/', {'method': 'generate', 'params': [num_blocks]})
    ### END METHOD ################################### rpc_generate(self, num_blocks:int=1)

    def rpc_generateToAddress(self, address:str, num_blocks:int=1):
        """
        DESCRIPTION:

            Mines numblocks blocks, with address as coinbase.

        PARAMS:

        (*) Denotes required argument

        (*) address   : Coinbase address for new blocks.

        ( ) num_blocks : Number of blocks to mine.
        """

        return self.post('/', {'method': 'generatetoaddress', 'params': [num_blocks, address]})
    ### END METHOD ################################### rpc_generateToAddress(self, address:str, num_blocks:int=1)

    def rpc_getConnectionCount(self):
        """
        DESCRIPTION:

            Returns connection count.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getconnectioncount', 'params': []})
    ### END METHOD ################################### rpc_getConnectionCount(self)

    def rpc_ping(self):
        """
        DESCRIPTION:

            Will send ping request to every connected peer.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'ping', 'params': []})
    ### END METHOD ################################### rpc_ping(self)

    def rpc_getPeerInfo(self):
        """
        DESCRIPTION:

            Returns information about all connected peers.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getpeerinfo', 'params': []})
    ### END METHOD ################################### rpc_getPeerInfo(self)

    def rpc_addNode(self, node_address:str, cmd:str):
        """
        DESCRIPTION:

            Adds or removes peers in Host List.

        PARAMS:

        (*) Denotes required argument

        (*) node_address : IP Address of the Node. Eg. '127.0.0.1:14038'

        (*) cmd          : 'add' - Adds node to Host List and connects to it.

                           'onetry' - Tries to connect to the given node.

                           'remove' - Removes node from host list.
        """

        return self.post('/', {'method': 'addnode', 'params': [node_address, cmd]})
    ### END METHOD ################################### rpc_addNode(self, node_address:str, cmd:str)

    def rpc_disconnectNode(self, node_address:str):
        """
        DESCRIPTION:

            Disconnects node.

        PARAMS:

        (*) Denotes required argument

        (*) address : IP Address of the Node. Eg. '127.0.0.1:14038'
        """

        return self.post('/', {'method': 'disconnectnode', 'params': [node_address]})
    ### END METHOD ################################### rpc_disconnectNode(self, node_address:str)

    def rpc_getAddedNodeInfo(self, node_address:str):
        """
        DESCRIPTION:

            Returns node information from host list.

        PARAMS:

        (*) Denotes required argument

        (*) address : IP Address of the Node. Eg. '127.0.0.1:14038'
        """

        return self.post('/', {'method': 'getaddednodeinfo', 'params': [node_address]})
    ### END METHOD ################################### rpc_getAddedNodeInfo(self, node_address:str)

    def rpc_getNetTotals(self):
        """
        DESCRIPTION:

            Returns information about used network resources.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getnettotals', 'params': []})
    ### END METHOD ################################### rpc_getNetTotals(self)

    def rpc_getNetworkInfo(self):
        """
        DESCRIPTION:

            Returns local node's network information.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'getnetworkinfo', 'params': []})
    ### END METHOD ################################### def rpc_getNetworkInfo(self)

    def rpc_setBan(self, node_address:str, cmd:str):
        """
        DESCRIPTION:

            Adds or removes nodes from banlist.

        PARAMS:

        (*) Denotes required argument

        (*) node_address : IP Address of the Node. Eg. '127.0.0.1:14038'

        (*) cmd         : 'add' - Adds node to ban list, removes from host list, disconnects.

                           'remove' - Removes node from ban list.
        """

        return self.post('/', {'method': 'setban', 'params': [node_address, cmd]})
    ### END METHOD ################################### rpc_setBan(self, node_address:str, cmd:str)

    def rpc_listBan(self):
        """
        DESCRIPTION:

            Lists all banned peers.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'listbanned', 'params': []})
    ### END METHOD ################################### rpc_listBan(self)

    def rpc_clearBanned(self):
        """
        DESCRIPTION:

            Removes all banned peers.

        PARAMS:

            None
        """

        return self.post('/', {'method': 'clearbanned', 'params': []})
    ### END METHOD ################################### rpc_clearBanned(self)

    def rpc_getNameInfo(self, name:str=''):
        """
        DESCRIPTION:

            Returns information on a given name. Use this function to query any name in any state.

        PARAMS:

        (*) Denotes required argument

        (*) name : Name you wish to look up.
        """

        return self.post('/', {'method': 'getnameinfo', 'params': [name]})
    ### END METHOD ################################### rpc_getNameInfo(self, name:str='')

    def rpc_getNameByHash(self, name_hash:str=''):
        """
        DESCRIPTION:

            Returns the name for a from a given name hash.

        PARAMS:

        (*) Denotes required argument

        (*) name_hash : Name hash you wish to look up.
        """

        return self.post('/', {'method': 'getnamebyhash', 'params': [name_hash]})
    ### END METHOD ###################################  rpc_getNameByHash(self, name_hash:str='')

    def rpc_getNameResource(self, name:str=''):
        """
        DESCRIPTION:

            Returns the resource records for the given name (added to the trie by the name owner using sendupdate).

        PARAMS:

        (*) Denotes required argument

        (*) name : Name for resource records.
        """

        return self.post('/', {'method': 'getnameresource', 'params': [name]})
    ### END METHOD ################################### rpc_getNameResource(self, name:str='')

    def rpc_getNameProof(self, name:str=''):
        """
        DESCRIPTION:

            Returns the merkle tree proof for a given name.

        PARAMS:

        (*) Denotes required argument

        (*) name : Domain name you to retreive the proof for.
        """

        return self.post('/', {'method': 'getnameproof', 'params': [name]})
    ### END METHOD ################################### rpc_getNameProof(self, name:str='')

    def rpc_sendRawClaim(self, base64_string:str):
        """
        DESCRIPTION:

            If you already have DNSSEC setup, you can avoid publishing a
            TXT record publicly by creating the proof locally. This requires
            that you have direct access to your zone-signing keys. The
            private keys themselves must be stored in BIND's private key
            format and naming convention.

        PARAMS:

        (*) Denotes required argument

        (*) base64_string : Raw serialized base64-string.
        """

        return self.post('/', {'method': 'sendrawclaim', 'params': [base64_string]})
    ### END METHOD ################################### rpc_sendRawClaim(self, base64_string:str='')

    def rpc_getDnsSecProof(self, name:str='', estimate:bool=False, verbose:bool=True):
        """
        DESCRIPTION:

            Adds or removes nodes from banlist.

        PARAMS:

        (*) Denotes required argument

        (*) name     : Domain name.

        ( ) estimate : No validation when True.

        ( ) verbose  : Returns (hex) when False.
        """

        return self.post('/', {'method': 'getdnssecproof', 'params': [name, estimate, verbose]})
    ### END METHOD ################################### rpc_getDnsSecProof(self, name:str='', estimate:bool=False, verbose:bool=True)

    def rpc_sendRawAirdrop(self, base64_string:str=''):
        """
        DESCRIPTION:

            Airdrop proofs create brand new coins directly
            to a Handshake address.

        PARAMS:

        (*) Denotes required argument

        (*) base64_string : Raw serialized base64-string.
        """

        return self.post('/', {'method': 'sendrawairdrop', 'params': [base64_string]})
    ### END METHOD ################################### rpc_sendRawAirdrop(self, base64_string:str='')

    def rpc_grindName(self, length:int=10):
        """
        DESCRIPTION:

            Grind a rolled-out available name.

        PARAMS:

        (*) Denotes required argument

        (*) length : Length of name to generate.
        """

        return self.post('/', {'method': 'grindname', 'params': [length]})
    ### END METHOD ################################### rpc_grindName(self, length:int=10)
