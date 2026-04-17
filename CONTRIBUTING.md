# Contributing

## Development

Run the bot locally:

```bash
python -m pilltalks.main --transport=stdin
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Guidelines

- keep changes focused
- preserve bot disclosure behavior
- do not add unsafe financial-advice flows
- do not commit secrets, API keys, or `.env`
- add or update tests when changing reply logic or transport behavior
