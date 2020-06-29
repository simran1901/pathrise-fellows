# pathrise-fellows
**Automatic connect and endorse profiles in a CSV**

![Alt Text](https://github.com/jzisheng/pathrise-fellows/blob/testing/demo.gif)

### Instructions for installation: 

Make sure to download the appropriate chromedriver [here](https://chromedriver.chromium.org/downloads)

For MacOS, install chromedriver through homebrew (recommended) 

`brew cask install chromedriver`

For authentication, create a new directory:
`resources/`

Store the `resources/fellows at pathrise.csv` CSV here, as well as authentication details in `resources/auth.txt` as follows:

```
your@email.com
yourPassword
```

### Running:
```
usage: script.py [-h] loginPath fellowsCsvPath
loginPath: path to plaintxt containing login info
fellowsCsvPath: path to csv of desired candidates
```

In commandline run `python3 script.py resources/auth.txt resources/fellows.csv`, this should start the selenium chrome driver, automatically log in using `resources/auth.txt`, and iterate through `resources/fellows.csv`


### Requirements
 * python3
 * panda
 * selenium webdriver(chrome)
