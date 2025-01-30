from setuptools import setup, find_packages

setup(
    name="equation_solver",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'PySide2>=5.15.2',
        'matplotlib>=3.5.2',
        'numpy>=1.23.1',
        'sympy>=1.10.1',
    ],
    extras_require={
        'test': ['pytest>=7.1.2', 'pytest-qt>=4.1.0'],
    },
)