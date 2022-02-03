# Project

Project contains of [server part](https://github.com/kiarro/Crossplatform_Server) and [client part](https://github.com/kiarro/Crossplatform_Client).

## Info

Server execute python code with parameters and returns result to client.

Sevrer executable might be created with command

``` cmd
dotnet publish -c Release -o Release -p:PublishSingleFile=true -p:PublishTrimmed=true -r win-x64
```

or other `dotnet publish` commands.

## Connection and Interactions

Server and client use tcp sockets to connect

Message from client to server is json string ends with 0000:

``` json
{
    "Command": "command",
    "Proc": "name",
    "Data": "data"
}
```

where `command` is command name, `name` is filename with python script, `data` is string with arguments for script.

Message from server to client is json string ends with 0000:

``` json
{
    "Error": "error",
    "Result": "result",
    "Axe1Name":"axe1",
    "Axe2Name":"axe2",
    "Values": [
        {
            "Series": [
                {
                    "X": Xvalue,
                    "Y": Yvalue
                },
            ],
            "Name": "name"
        }
    ]
}
```

where `error` is error message, `result` is text result, `axe1` is horizontal axis label, `axe2` is vertical axis label, `Xvalue` is point horizontal coordinate, `Yvalue` is point vertical coordinate, `name` is series label. `"Values"` may contain more than 1 series. `"Series"` may contain more than 1 points.

## Python scripts

Python scripts for server should return info about script when run with argument `info` and json string (as server to client message) when run with argument `eval`. Script results should be printed to standert output stream.

## Launch server

Server might be launched with options:

``` text
      --ip                   ip address for server
  -f                         path to directory with python scripts
  -p                         path to python interpreter;
  -h, --help                 show this message and exit
```
