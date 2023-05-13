from setuptools import setup, find_packages

setup(
    name='safeGPT',
    version='0.0.1',
    description='A safer way to use GPT chat models',
    packages=find_packages(),
    install_requires=['openai>=0.27.0'],
    python_requires='>=3.10',
)
