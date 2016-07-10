# CTIP
Configuration Testing In Parallel

CTIP is a general, extensible tool for running batches of configurable jobs in
parallel on a variety of environments from your local machine to a remote server.

By relying on the end-user to specify what to run and how to run it, CTIP is a
very general solution for optimizing and experimenting on programs that use
configuration files to determine behavior. CTIP provides the infrastructure for
generating and passing configurations to user-adapted classes that setup and run
a given program. It also provides tools for tracking job status when jobs are run
locally.

## Install

See the [INSTALL](INSTALL.md) file for more detailed information.

Via pip:

``` bash
$ pip install ctip
```

Configure ctip installation by setting paths to directories containing all user
defined ``Experiments`` and ``Environments``:

''' bash
$ ctip set experiment-dir ~/research/ctip-exp
$ ctip set environment-dir ~/research/ctip-env
'''

## Usage

For complete documentation of ctip, browse the docs folder or go to the future and
visit a website I will make with all the documentation.

For a concise summary of all available commands, run:

```bash
$ ctip help
```

Run configurations for the ``Doodle`` experiment in the ``Local`` environment as
specified in a genfile named ``doodle_configs.gen``:

``` bash
$ ctip run gen doodle_configs.gen --experiment Doodle --environment Local
```

**Note:** During development, avoid constant re-installation by using
``python ctip-runner.py ...`` instead of the ``ctip`` command.

## Change log

Please see [CHANGELOG](CHANGELOG.md) for information about what has changed recently.

## Testing

From the root ctip directory run:

``` bash
$ py.test
```

## Security

If you discover any security related issues, please email [me](aminor65ii@gmail.com)
instead of using the issue tracker.

With that being said, any communication ctip does with the outside world is through
user provided Environment classes and thus most security vulnerabilities will likely
be the responsibility of the end-user.

Also sql injection through the optional 'where' clause is not only possible but is
considered a feature. The only database malicious queries effect is the ctip
database which only ever holds information you put in it... so go ahead.

## Credits

Thanks to the Hintze Lab at Michigan State University for being a willing guinea pig.

## License

The MIT License (MIT). Please see [License File](LICENSE) for more information.
