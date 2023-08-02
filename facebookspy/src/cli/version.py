from rich import print as rprint


VERSION = "0.4"


def return_version_info():
    """
    Return the version of the package.
    """
    text = f"You are using {VERSION} version of the facebook spy. For more info visit https://github.com/DEENUU1/facebook-spy"
    rprint(text)
