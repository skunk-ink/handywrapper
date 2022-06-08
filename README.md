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

# **Usage**
**Source Code: [`api.py`](handshake/api.py)**
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