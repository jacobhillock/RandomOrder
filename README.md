# Random Order Note Taker
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
  - eg `Moh` matches `Mohammed`
