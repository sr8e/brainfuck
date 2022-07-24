## brainfuck interpreter written in python

### Usage
`$ python plain_bf_interpreter.py <filename> [options]`

### Options
| flag | description |
| :-- | :-- |
| -d | Enable to dump memory address/value if it encounters `!` character |
| -m=\<memory size\> | Set memory size to specified value (default: 100)
| -i=\<input string\> | Give input string

### Behavior

- each memory element has type of unsigned byte (0x00-0xff)
- incrementing 0xff will get 0
- decrementing 0 will get 0xff
- memory address must be non-negative and smaller than given memory size, otherwise it will raise `PointerUnderFlowError` and `PointerOverFlowError`, respectively
- if input stream is empty, `,` command will do nothing