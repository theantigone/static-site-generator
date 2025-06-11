<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
# Static Site Generator

**Table of Contents**

- [How to run the website (server) locally](#how-to-run-the-website-server-locally)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### How to run the website (server) locally

1. Change directories to the `public` directory, and use Python's built-in [HTTP server](https://docs.python.org/3/library/http.server.html#command-line-interface) to serve the contents of the `public` directory:
```bash
cd public
python3 -m http.server 8888
```
2. Open the browser, and paste in the URL of your server ([`http://localhost:8888/`](http://localhost:8888/) if you used port `8888` as suggested in the code snippet above) into the address bar.
3. You should now see the files rendered as a web page(s)!

> [!NOTE]
> _You can kill the server with `Ctrl+C`. To restart it, simply type in:_
> ```bash
> python3 -m http.server 8888
> ```
