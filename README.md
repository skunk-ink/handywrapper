# Skunk Works
```
                         _..._ ___
                       .:::::::.  `"-._.-''.
                  ,   /:::::::::\     ':    \                     _._
                  \:-::::::::::::\     :.    |     /|.-'         /:::\ 
                   \::::::::\:::::|    ':     |   |  /           |:::|
                    `:::::::|:::::\     ':    |   `\ |    __     |\::/\ 
                       -:::-|::::::|    ':    |  .`\ .\_.'  `.__/      |
                            |::::::\    ':.   |   \ ';:: /.-._   ,    /
                            |:::::::|    :.   /   ,`\;:: \'./0)  |_.-/
                            ;:::::::|    ':  |    \.`;::.   ``   |  |
                             \::::::/    :'  /     _\::::'      /  /
                              \::::|   :'   /    ,=:;::/           |
                               \:::|   :'  |    (='` //        /   |
                                \::\   `:  /     '--' |       /\   |
  GITHUB.COM/SKUNK-INK           \:::.  `:_|.-"`"-.    \__.-'/::\  |
░▒█▀▀▀█░▒█░▄▀░▒█░▒█░▒█▄░▒█░▒█░▄▀  '::::.:::...:::. '.       /:::|  |
░░▀▀▀▄▄░▒█▀▄░░▒█░▒█░▒█▒█▒█░▒█▀▄░   '::/::::::::::::. '-.__.:::::|  |
░▒█▄▄▄█░▒█░▒█░░▀▄▄▀░▒█░░▀█░▒█░▒█     |::::::::::::\::..../::::::| /
                                     |:::::::::::::|::::/::::::://
  ░▒█░░▒█░▒█▀▀▀█░▒█▀▀▄░▒█░▄▀░▒█▀▀▀█  \:::::::::::::|'::/::::::::/
  ░▒█▒█▒█░▒█░░▒█░▒█▄▄▀░▒█▀▄░░░▀▀▀▄▄  /\::::::::::::/  /:::::::/:|
  ░▒▀▄▀▄▀░▒█▄▄▄█░▒█░▒█░▒█░▒█░▒█▄▄▄█ |::';:::::::::/   |::::::/::;
              HANDSHAKE API WRAPPER |:::/`-:::::;;-._ |:::::/::/
                                    |:::|  `-::::\   `|::::/::/
                                    |:::|     \:::\   \:::/::/
                                   /:::/       \:::\   \:/\:/
                                  (_::/         \:::;__ \\_\\___
                                  (_:/           \::):):)\:::):):)
                                   `"             `""""`  `""""""`      
```
# **Install**
Install the `handywrapper` package using PIP:
```
pip install handywrapper
```

Tracks the [`hsd`](https://github.com/handshake-org/hsd) v8.0.0 API surface. Requires Python 3.6+.

**From source**, for development:
```
git clone https://github.com/skunk-ink/handywrapper.git
cd handywrapper
pip install -e .[test]
```

# **Project Layout**
The `handywrapper` package is split into a few small modules:

| Module | Contents |
|---|---|
| [`handywrapper/node.py`](handywrapper/node.py) | `hsd` — full-node REST + RPC client |
| [`handywrapper/wallet.py`](handywrapper/wallet.py) | `hsw` — wallet REST + RPC client |
| [`handywrapper/_http.py`](handywrapper/_http.py) | Shared `get`/`post`/`put`/`patch`/`delete` primitives both classes build on |
| [`handywrapper/exceptions.py`](handywrapper/exceptions.py) | `HandywrapperAPIError`, `HandywrapperConnectionError`, `HandywrapperDecodeError` |
| [`handywrapper/api.py`](handywrapper/api.py) | Compatibility shim — `from handywrapper import api; api.hsd(...)` still works |

`hsd` and `hsw` can also be imported directly: `from handywrapper import hsd, hsw`.

See [`CHANGELOG.md`](CHANGELOG.md) for what changed since 1.x — the 2.0.0 release is a breaking rewrite to match `hsd` v8.0.0.

# **Usage**
> *For more information on using the Handshake API, visit the **[Handshake API Docs](https://hsd-dev.org/api-docs/#introduction)***

```python
# Import — either style works
from handywrapper import hsd, hsw
# from handywrapper import api  (back-compat: api.hsd(...), api.hsw(...))
```

```python
# Use default ip and port

node = hsd('api-key')
wallet = hsw('api-key')
```

```python
# Or specify host, port, and request timeout (seconds, default 30)

node = hsd('api-key', '0.0.0.0', 14037, timeout=10)
wallet = hsw('api-key', '0.0.0.0', 14039, timeout=10)
```

```python
# Then use

response = node.getInfo()
print(response)

response = wallet.resetAuthToken(passphrase='secret123', id='primary')
print(response)

```

# **Error Handling**
Failed requests raise an exception instead of returning an error dict:

- `HandywrapperAPIError` — hsd/hsw returned a non-2xx response. Carries `.status_code`, `.url`, and `.body` (the parsed error payload, when available).
- `HandywrapperConnectionError` — the node/wallet could not be reached.
- `HandywrapperDecodeError` — a 2xx response body wasn't valid JSON.

```python
from handywrapper import hsd, HandywrapperAPIError

node = hsd('api-key')

try:
    response = node.getBlockByHashOrHeight('not-a-real-block')
except HandywrapperAPIError as e:
    print(e.status_code, e.body)
```

# **Testing**
```
pip install -e .[test]
pytest
```

The suite mocks HTTP (via [`responses`](https://github.com/getsentry/responses)) and covers every public method on both `hsd` and `hsw`, asserting the exact verb, path, query params, and body each one sends.
