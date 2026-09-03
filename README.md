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

# **Usage**
**Source Code: [`api.py`](handywrapper/api.py)**
> *For more information on using the Handshake API, visit the **[Handshake API Docs](https://hsd-dev.org/api-docs/#introduction)***

```python
# Import
from handywrapper import api
```

```python
# Use default ip and port

hsd = api.hsd('api-key')
hsw = api.hsw('api-key')
```

```python
# Or specify

hsd = api.hsd('api-key', '0.0.0.0', 14037)
hsw = api.hsw('api-key', '0.0.0.0', 14039)
```

```python
# Then use

response = hsd.getInfo()
print(response)

response = hsw.resetAuthToken('primary', 'secret123')
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
