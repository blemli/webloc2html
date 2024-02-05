# webloc2html



Treating URL's as Files is fun. But it is not cross-platform. This Script helps.

Convert all webloc files in the current directory (including subdirectories) to html:

``````shell
webloc2html .
``````

Also delete unreachable links and don't ask for confirmation (DANGER!):

``` shell
webloc2html  /some/path --silent --validate --delete-unreachable
```

for more details:

```
webloc2html --help
```

