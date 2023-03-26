This repo exists to report a bug, it doesn't do anything else.

First become convinced that as-is, there is no error:

```
% nix develop
$ rm -rf .venv
$ poetry env use $(which python)
$ poetry install
$ poetry run python mypkg/app.py	# no error
$ exit
%
```

Then, edit `flake.nix`

```
devShells.default = pkgs.mkShell {
  packages = [

    poetry2nix.packages.${system}.poetry
    pkgs.python311Packages.psycopg
    # pkgs.pre-commit  # uncomment this line

  ];
};
```

Then, repeat the above commands:

```
% nix develop
$ rm -rf .venv
$ poetry env use $(which python)
$ poetry install
$ poetry run python mypkg/app.py	# now there's an error
$ exit
%
```


The error looks like this:
```
Traceback (most recent call last):
  File "/home/matt/src/mypkg/mypkg/app.py", line 2, in <module>
    create_engine(
  File "<string>", line 2, in create_engine
  File "/home/matt/src/mypkg/.venv/lib/python3.11/site-packages/sqlalchemy/util/deprecations.py", line 277, in warned
    return fn(*args, **kwargs)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^
  File "/home/matt/src/mypkg/.venv/lib/python3.11/site-packages/sqlalchemy/engine/create.py", line 600, in create_engine
    dbapi = dbapi_meth(**dbapi_args)
            ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/matt/src/mypkg/.venv/lib/python3.11/site-packages/sqlalchemy/dialects/postgresql/psycopg.py", line 370, in import_dbapi
    import psycopg
  File "/home/matt/src/mypkg/.venv/lib/python3.11/site-packages/psycopg/__init__.py", line 9, in <module>
    from . import pq  # noqa: F401 import early to stabilize side effects
    ^^^^^^^^^^^^^^^^
  File "/home/matt/src/mypkg/.venv/lib/python3.11/site-packages/psycopg/pq/__init__.py", line 114, in <module>
    import_from_libpq()
  File "/home/matt/src/mypkg/.venv/lib/python3.11/site-packages/psycopg/pq/__init__.py", line 106, in import_from_libpq
    raise ImportError(
ImportError: no pq wrapper available.
Attempts made:
- couldn't import psycopg 'c' implementation: No module named 'psycopg_c'
- couldn't import psycopg 'binary' implementation: No module named 'psycopg_binary'
- couldn't import psycopg 'python' implementation: libpq library not found
```

What is it about pkgs.pre-commit that prevents pkgs.python311Packages.psycopg from being able to find libpq?


I suspect it might be [this](https://github.com/NixOS/nixpkgs/issues/223275)
