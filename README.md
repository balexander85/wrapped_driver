# WrappedDriver

How to install:

`pip install -e git+https://github.com/balexander85/wrappeddriver.git#egg=wrappeddriver`

```$python
from wrappeddriver import WrappedDriver

CHROME_DRIVER_PATH = "/usr/bin/chromedriver"

driver = WrappedDriver(
            executable_path=CHROME_DRIVER_PATH,
            browser="chrome",
            headless=headless,
         )
```
