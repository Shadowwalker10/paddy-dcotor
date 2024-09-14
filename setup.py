import setuptools
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.0"

REPO_NAME = "paddy-doctor"
AUTH_USER_NAME = "Shadowwalker10"
SRC_REPO_NAME = "paddy-doctor"

setuptools.setup(name = SRC_REPO_NAME,
                version = __version__, 
                long_description = long_description, 
                long_description_content_type = "text/markdown",
                author = AUTH_USER_NAME,url = f"https://github.com/{AUTH_USER_NAME}/{REPO_NAME}",
                project_urls = {
                    "Bug Tracker": f"https://github.com/{AUTH_USER_NAME}/{REPO_NAME}/issues"
                    },
                package_dir = {"":"src"},
                packages = setuptools.find_packages(where = "src"))