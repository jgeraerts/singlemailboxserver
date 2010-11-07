from setuptools import setup, find_packages

def main():
    setup(
        name="singlemailboxserver",
        version="0.1",
        description=("This is a simple email server which accepts all incoming mail and drops it in a single mailbox"),
        author="Jo Geraerts",
        author_email="jo@umask.net",
        license="MIT",
        url="https://github.com/jgeraerts/singlemailboxserver",
        packages=find_packages()+ ['twisted/plugins'],
        install_requires=["Twisted>=10.1.0"],
        zip_safe=False
    )

if __name__ == "__main__":
    main()
