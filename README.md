
    ███╗   ███╗██╗██╗     ██╗  ██╗ ██████╗ ██████╗ ██╗    ██╗
    ████╗ ████║██║██║     ██║ ██╔╝██╔════╝██╔═══██╗██║    ██║
    ██╔████╔██║██║██║     █████╔╝ ██║     ██║   ██║██║ █╗ ██║
    ██║╚██╔╝██║██║██║     ██╔═██╗ ██║     ██║   ██║██║███╗██║
    ██║ ╚═╝ ██║██║███████╗██║  ██╗╚██████╗╚██████╔╝╚███╔███╔╝
    ╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝  ╚══╝╚══╝ 

## v 0.0.10

### Description

A utility for building middleware between programs that use pydantic
and sqlite.

### Core Features
- Creates database tables to store instances of pydantic model objects
- Sends encoded objects to other processes or programs
- Good for piping in live data and forking to one other process and disk

### Limitations
- Only supports one model per database
- Datebase queries available are limited just this one. Key -> list of objects

