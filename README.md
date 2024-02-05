# webloc2html



Treating URL's as Files is fun. But it is not cross-platform. This Script helps.

Convert all webloc files in the current directory (including subdirectories) to html:

``````shell
webloc2html .
``````

Stop it from asking for confirmation (DANGER!):

``` shell
webloc2html  /some/path --silent
```

for more details:

```
webloc2html --help
```


## Roadmap

- Validate Links (check their HTTP Return Code)
- Delete Invalid Links
