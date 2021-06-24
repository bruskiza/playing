import setuptools


setuptools.setup(
    name="cortexutil",
    version="0.0.1",
    author="Bruce McIntyre",
    author_email="bruce.mcintyre@gmail.com",
    description="A Cortex example program",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'cortexutil = cortexutil.guesser:cli',
        ],
    },
)
