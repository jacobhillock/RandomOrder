# Random Order Note Taker
Version: v0.1.1
## What it is

## Required files
`./.people.txt` - a list of people to order separated by new lines
`./.tokens.json` - a JSON object with `TOKEN`: `VALUE` pairs

## How to use
The following commands will use `python` to run this app, but we require python 3.10+ to run

help: `python main.py -h`
- this gives you all available commands to use

enable testing features: `python main.py -t`
- this enables testing features and outputs to a testing document

hide people: `python main.py [PERSON,]`
- From the input list in `.people.txt` this hides exact matches

fuzzy hide: `python main.py -f [PERSON,]`
- From the input list in `.people.txt` this hides partial matches if exactly one match
  - eg `moh` matches `Mohammed`

random only: `python main.py -r`
- Only print the random order

specify person file: `python main.py --file FILE_NAME`
- if flag is `abc` for example, program will look for
  - `abc.people.txt` and `abc.tokens.json`

## During note taking
use tokens:
- if you have a token `PR` we will replace it for the following
  - `> PR`
  - `> PR.`
  - `> Some PR`
  - `> This PR, and that`
- it will note replace
  - `> PRs`
  - `> pr`

note commands:
- having two back-to-back inputs that are blank go to the next person
- having two back-to-back inputs that are `g` then `b` (go back) go to the previous person
