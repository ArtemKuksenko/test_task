from setuptools import setup, find_packages

setup(
    name="run_single_generator",
    version="0.0.1",
    packages=find_packages(),
    description="""
        Starts only one generator.
        If called again, it will kill the old call and start calculating again.
    """,
    install_requires=[
        'aioredis==2.0.1'
    ],
    author="kuksenko_ab",
    author_email="kuksenko.artem@gmail.com"
)
