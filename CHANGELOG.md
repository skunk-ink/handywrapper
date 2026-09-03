# Changelog

All notable changes to this project are documented in this file.

## [2.0.0]

Brings `handywrapper` up to date with `hsd` v8.0.0. This is a breaking release.
Existing code pinned to `handywrapper<2.0.0` is unaffected — nothing here changes
until you explicitly upgrade.

### Upgrading from 1.x

Most code needs no changes at all. Check for these three specifically:

1. **Error handling.** Every method used to swallow all failures and return
   `{'error': '...'}` instead of raising. That's gone — methods now raise
   `HandywrapperAPIError`, `HandywrapperConnectionError`, or
   `HandywrapperDecodeError`. If you have code like:
   ```python
   result = hsd.getInfo()
   if 'error' in result:
       ...
   ```
   wrap the call in a `try/except` instead (see the README's Error Handling
   section), or check `HandywrapperAPIError.body` for the same information
   hsd previously returned.
2. **`hsw.getRangeOfTransactions` was removed** (hsd v7 removed the underlying
   endpoint). Replace it with `hsw.getWalletTxHistory(after=..., limit=...)`.
3. **`hsw.walletResend()` was renamed to `hsw.adminResend()`.**
   `hsw.walletResend(id=...)` now refers to a different, per-wallet endpoint
   that hsd added in v7 — same method name, different behavior. If you call
   `walletResend()`, change it to `adminResend()` to keep the old behavior.

Everything else is additive or an internal shape fix — see Fixed/Added below
for the full list, but nothing else requires a code change to keep working.

### Breaking

- Replaced the blanket `try/except: return {'error': ...}` on every method with real
  exceptions: `HandywrapperAPIError` (non-2xx response, carries `.status_code`, `.url`,
  `.body`), `HandywrapperConnectionError` (node/wallet unreachable), and
  `HandywrapperDecodeError` (2xx response with a non-JSON body). Previously, every
  failure — including bugs internal to handywrapper itself — was silently swallowed
  into an indistinguishable dict.
- `hsw.getRangeOfTransactions` removed. hsd v7 removed the underlying
  `GET /wallet/:id/tx/range` endpoint entirely. Use `hsw.getWalletTxHistory(after=...,
  limit=...)` instead.
- `hsw.getWalletTxHistory` and `hsw.getPendingTransactions` gained pagination kwargs
  (`account`, `reverse`, `limit`, `after`, `time`) to match hsd v7's paginated
  `tx/history`/`tx/unconfirmed` endpoints; they no longer take a bare wallet id only.
- `hsw.walletResend()` (the top-level admin endpoint, `POST /resend`) has been renamed
  to `hsw.adminResend()`. `hsw.walletResend(id='primary')` now refers to the distinct,
  non-admin, per-wallet `POST /wallet/:id/resend` endpoint added in hsd v7.
- `hsw.rpc_createOPEN` dropped its `force` parameter — hsd v6 removed `force` from the
  `createopen`/`sendopen` RPCs server-side.
- The library is now split into a small package (`node.py`, `wallet.py`, `_http.py`,
  `exceptions.py`) instead of a single `api.py` file. `from handywrapper import api;
  api.hsd(...)` / `api.hsw(...)` continue to work via a compatibility shim; `from
  handywrapper import hsd, hsw` also now works directly.
- `hsw.rpc_listTransactions` is deprecated upstream (hsd v3+ raises a deprecation
  error for it server-side). Use `hsw.rpc_listHistory`, `rpc_listHistoryAfter`, or
  `rpc_listHistoryByTime` instead.

### Fixed

- `hsd.getCoinByHashIndex` referenced the Python builtin `hash` instead of building
  `/coin/<tx_hash>/<index>` — every call raised `TypeError`.
- `hsw.importAddress` hardcoded `/wallet/watchonly1/import`, ignoring the caller's
  wallet `id`.
- `hsw.addXPubKey`/`removeXPubKey` hardcoded `/wallet/multisig3/shared-key/`, ignoring
  the caller's wallet `id`.
- `hsw.getNonceForBid` hit `/nounce/` (typo) instead of hsd's real `/nonce/` route —
  every call 404'd.
- `hsw.getWalletResourceByName` never included `name` in its path, hitting
  `/wallet/<id>/resource` instead of `/wallet/<id>/resource/<name>`.
- `hsw.walletRescan` hit the nonexistent `/_rescan/` path instead of hsd's real
  admin-only `/rescan` route.
- `hsd.rpc_generateToAddress` had a bare `except KeyError` that printed to stdout and
  swallowed the error, plus a convoluted retry path; replaced with a single
  straightforward RPC call.
- `hsw.createWallet`'s `PUT /wallet/:id` body used the field name `_watch_only`
  instead of hsd's real `watchOnly`.
- `hsd.rpc_validateAddress` sent `{"validateaddress": "", ...}` instead of
  `{"method": "validateaddress", ...}`.
- `hsd.rpc_invalidateBlock` sent an empty `"method": ""` instead of `"invalidateblock"`.
- `hsd.rpc_getWork` sent `"method": "getworklp"` (copy-paste from `rpc_getWorkLP`)
  instead of `"getwork"`.
- `hsw.rpc_importAddress` sent `"method": "importwallet"` (copy-paste bug) instead of
  `"importaddress"`.
- `hsw.sendTransaction`/`createTransaction` built a malformed, doubly-nested `outputs`
  array with transaction options (rate, smart, selection, etc.) incorrectly nested
  *inside* each output object instead of at the top level of the request body, and
  left a stray debug `print()` statement in the send path. Both now build the request
  body matching hsd's actual `TransactionOptions` shape.
- Numerous hand-built JSON strings across both classes broke on values containing
  quotes, or crashed the error-formatting code itself when concatenating strings with
  non-string values (e.g. `"..." + n_blocks + "..."` where `n_blocks` is an `int`).
  Resolved across the board by building request bodies as plain Python dicts, which
  `requests` now serializes safely.
- Any boolean query parameter (`hsd.getMemPoolInvalid`'s `verbose`; `hsw`'s
  `getWalletTxHistory`/`getPendingTransactions`'s `reverse`; `getWalletName`'s `own`;
  `getWalletBids`/`getWalletBidsByName`/`getWalletReveals`/`getWalletRevealsByName`'s
  `own`) serialized as Python's `"True"`/`"False"` instead of the lowercase
  `"true"`/`"false"` hsd's query validator requires — fixed once at the shared HTTP
  primitive rather than per call site.
- `hsd.rpc_getTxOutProof` sent `tx_id_list` as a bare string instead of an array,
  which hsd's `gettxoutproof` rejects with "Param #0 must be a array."
- `hsw.createWallet`/`createAccount` sent `accountKey`/`master`/`mnemonic` as empty
  strings when not provided instead of omitting them, crashing hsd's base58 key
  decoder with "Out of bounds read." `createWallet`'s `watch_only` default also
  changed from `True` to `False`, and `passphrase` is now genuinely optional
  (omitting it creates an unencrypted wallet, matching hsd's own behavior).
- `hsw.rpc_listHistory`/`rpc_listHistoryAfter`/`rpc_listHistoryByTime`/
  `rpc_listUnconfirmed`/`rpc_listUnconfirmedAfter`/`rpc_listUnconfirmedByTime` sent an
  options object as a positional param instead of hsd's actual flat positional params
  (`account, limit, reverse`), and defaulted `account` to `''` instead of `'*'`
  (hsd's "all accounts" sentinel) — both rejected by hsd.
- `hsd.rpc_createRawTransaction` always included an empty `data` output field, which
  hsd's nulldata decoder rejects rather than ignores; now omitted unless given.
- `hsw.rpc_createOPEN`/`rpc_createREVEAL`/`rpc_createREDEEM`/`rpc_createUPDATE`/
  `rpc_createRENEWAL`/`rpc_createTRANSFER`/`rpc_createFINALIZE`/`rpc_createCANCEL`/
  `rpc_createREVOKE` defaulted `account` to `''` and always included it, which hsd's
  account lookup rejects with "Invalid type for database key" — now omitted unless
  given.

### Added

- `hsw.modifyAccount` — `PATCH /wallet/:id/account/:account` (hsd v6).
- `hsw.unlockWallet` — `POST /wallet/:id/unlock`.
- `hsw.deepClean` — `POST /deepclean` (admin-only).
- `hsw.recalculateBalances` — `POST /recalculate-balances` (admin-only, hsd v8).
- `hsw.createAuction` — `POST /wallet/:id/auction`, combined BID+REVEAL in one call.
- `hsw.walletResend(id)` — per-wallet, non-admin resend (see Breaking, above).
- `hsd.getCoinsByAddresses`/`hsd.getTXsByAddresses` — bulk `POST /coin/address` and
  `POST /tx/address` variants of the existing single-address GET routes.
- `hsw.rpc_createBatch`/`hsw.rpc_sendBatch` — batch covenant-action RPCs (hsd v5+).
- `hsw.rpc_listHistory`, `rpc_listHistoryAfter`, `rpc_listHistoryByTime`,
  `rpc_listUnconfirmed`, `rpc_listUnconfirmedAfter`, `rpc_listUnconfirmedByTime` — the
  hsd v7 replacements for the deprecated `listtransactions` RPC.
- `hsw.getWalletName` gained an `own` filter kwarg (hsd v8).
- All `TransactionOptions`-shaped send/create methods gained `hard_fee` and an
  expanded `selection` value set (`db-value` [hsd v8's new default], `db-age`,
  `db-all`, `db-sweepdust`) plus `sweepdustMinValue` where applicable.
- A `tests/` suite (via `pip install -e .[test]`) covering every public method on both
  `hsd` and `hsw` with mocked HTTP responses.
- Request timeouts (`timeout` kwarg, default 30s, on both `hsd`/`hsw` constructors) —
  previously requests could hang indefinitely.

### Notes

- `hsw.zapTransactions`'s underlying endpoint response now includes a `zapped: <int>`
  count (hsd v8) — no request-side change.
- hsd v6 changed validation-error HTTP responses from 500 to 400 on both APIs; this
  surfaces as `HandywrapperAPIError.status_code` accordingly.
- Verified end-to-end against a live regtest hsd v8.0.0+ node, not just the mocked
  test suite: the full name-auction lifecycle (OPEN → BID → REVEAL → REGISTER →
  UPDATE → RENEW → TRANSFER → FINALIZE/CANCEL/REVOKE, plus REDEEM for a losing bid)
  via the REST methods, the RPC `send*` methods, and the RPC `create*` + sign +
  broadcast methods; multisig xpub exchange between two wallets; watch-only key/
  address imports; batch RPC (`createBatch`/`sendBatch`); and the admin-only
  endpoints (`deepClean`, `reset`, `pruneBlockchain`, `walletRescan`,
  `recalculateBalances`).
- Tracks `hsd` v8.0.0 (the current tagged release).

## [1.0.6] and earlier

No changelog was kept prior to 2.0.0. See git history.
