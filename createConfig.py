import sys
from main import setLogging

def initiation() -> None:
    logger = setLogging(__name__)
    from main import createDir
    imageRootDirectory = input(f"please insert your desired directory root location for all future image imports: ").strip
    logger.debug(f"*{sys._getframe().f_code.co_name}*: {imageRootDirectory = }")
    createDir(imageRootDirectory)
    optionsSchema = ["YYYY/MM/DD", "Insanity"]
    print(f"select your desired directory hierachy schema for all future image imports:\n0: '{optionsSchema[0]}' (default)\n1: '{optionsSchema[1]}'")
    hierarchySchema = optionsSchema[int(input(f"(enter '0' or '1' or leave blank for default): ").strip())] or optionsSchema[0]
    logger.debug(f"*{sys._getframe().f_code.co_name}*: {hierarchySchema = }")
    config = {
        "rootDir": imageRootDirectory,
        "schema": hierarchySchema,
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

def writeTOML(dict) -> None:
    logger = setLogging(__name__)
    import tomli_w
    try:
        with open("./config/config.toml", "wb") as f:
            tomli_w.dump(dict, f)
        logger.debug(f"*{sys._getframe().f_code.co_name}*: {dict = }")
    except Exception:
        logger.exception(f"Exception")