from invoke import task

# poetry run invoke start
@task
def start(ctx):
    ctx.run("python3 src/main.py", pty=True)

# poetry run invoke test
@task
def test(ctx):
    ctx.run("pytest src", pty=True)


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)


@task
def format(ctx):  # pylint: disable=redefined-builtin
    ctx.run("autopep8 --in-place --recursive src", pty=True)


@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)

@task
def check(ctx):
    """Suorita kaikki tarkistukset"""
    lint(ctx)
    test(ctx)
    coverage(ctx)

@task
def build(ctx):
    ctx.run("python3 src/ui/build.py", pty=True)
    