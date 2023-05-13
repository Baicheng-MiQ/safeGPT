from setuptools import setup, find_packages

setup(
    name='safeGPT',
    version='0.0.1',
    description='A safer way to use GPT chat models',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=['openai>=0.27.0'],
    python_requires='>=3.10',
    url="https://github.com/Baicheng-MiQ/safeGPT"
)
