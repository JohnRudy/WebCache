# WebCacheClient

create a virtual env if you so please.

Set environment varialbe "WEBCACHE_URL" to point towards the webcache api.

wcc.sh 
```
#!/usr/bin/env bash

# modify the path to suit your paths
# Activate virtual environment if done, can be ommitted if used system packages.
source /path/to/your/.venv/bin/activate

# point towards the client folder in WebCacheClient of repo root
python /path/to/project/client/wcc "$@"
```

.bashrc
```
# point towards the .sh file
alias wcc='f() { /path/to/wcc.sh "$@"; }; f'
```

```
Commands:
  cache-file
  cache-value
  delete
  fetch-file
  fetch-value
  keys
```

