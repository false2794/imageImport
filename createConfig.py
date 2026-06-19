import sys
from main import setLogging

def initiation() -> None:
    logger = setLogging(__name__)
    from main import createDir
    imageRootDirectory = input(f"please insert your desired directory root location for all future image imports: ")
    logger.debug(f"*{sys._getframe().f_code.co_name}*: {imageRootDirectory = }")
    createDir(imageRootDirectory)
    optionsScheme = ["YYYY/MM/DD", "None"]
    print(f"select your desired directory hierachy scheme for all future image imports:\n0: '{optionsScheme[0]}' (default)\n1: '{optionsScheme[1]}'")
    hierarchyScheme = input(f"(enter '0' or '1' or leave blank for default): ").strip() or optionsScheme[0]
    logger.debug(f"*{sys._getframe().f_code.co_name}*: {hierarchyScheme = }")
    config = {
        "rootDir": imageRootDirectory,
        "scheme": hierarchyScheme,
        "validImgFileExt": {
            "Adobe/Universal": [".dng"],
            "Canon": [".cr2", ".cr3", ".crw"],
            "Fujifilm": [".raf"],
            "Nikon": [".nef", ".nrw"],
            "Olympus/OM-System": [".orf"],
            "Panasonic": [".raw", ".rw2"],
            "Sony": [".arw", ".sr2", ".srf"],
            "jpeg": [".jpg", ".jpeg"]
            }
        }
    print(f"by default this script will copy files with following extensions: {config["validImgFileExt"]}")

    writeTOML(config)

def writeTOML(dict):
    logger = setLogging(__name__)
    import tomli_w
    try:
        with open("./config/config.toml", "wb") as f:
            tomli_w.dump(dict, f)
        logger.debug(f"*{sys._getframe().f_code.co_name}*: {dict = }")
    except Exception:
        logger.exception(f"Exception")