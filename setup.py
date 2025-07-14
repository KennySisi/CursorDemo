from setuptools import setup, find_packages

# 读取README文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取requirements文件
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="devops-demo-api",
    version="1.0.0",
    author="DevOps Team",
    author_email="devops@company.com",
    description="一个用于演示CI/CD流程的FastAPI应用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/company/devops-demo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Framework :: FastAPI",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ]
    },
    entry_points={
        "console_scripts": [
            "devops-demo-api=app.main:main",
        ],
    },
)