from setuptools import setup, find_packages

setup(
    name="story-agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "openai>=1.0.0",
        "python-dotenv"
    ],
) 