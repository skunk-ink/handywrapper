# Changelog

All notable changes to this project are documented in this file.

## [2.0.0]

Brings `handywrapper` up to date with `hsd` v8.0.0. This is a breaking release.

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
- Tracks `hsd` v8.0.0 (the current tagged release).

## [1.0.6] and earlier

No changelog was kept prior to 2.0.0. See git history.
