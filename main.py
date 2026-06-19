import sys
import logging
import logging.config

def createDir(dir):
    try:
        import os
        if not os.path.isdir(dir):
            os.makedirs(dir)
            try:
                logger = setLogging()
                logger.debug(f"*{sys._getframe().f_code.co_name}*: Directory '{dir}' successfully created.")
            except Exception as e:
                print(f"Exception: '{e}' while trying to log the creation of '{dir}'.")
        else:
            try:
                logger = setLogging()
                logger.debug(f"*{sys._getframe().f_code.co_name}*: Directory '{dir}' does already exist.")
            except Exception as e:
                print(f"Directory '{dir}' does already exist.")
    except Exception as e:
        print(f"Exception: '{e}' while trying to create '{dir}'.")

def setLogging(logFile = __name__):
    try:
        logging.config.fileConfig("./config/logging.conf")
        logger = logging.getLogger(logFile)
    except Exception as e:
        print(f"Excpetion: '{e}' while trying to initiate the logger.")
    else:
        return logger

def loadToml() -> dict:
    import tomllib
    try:
        with open("./config/config.toml", "rb") as f:
            tomlData: dict = tomllib.load(f)
            return tomlData
    except Exception:
        logger = setLogging()
        logger.exception(f"Exception")

def main():
    logger = setLogging()
    import os.path
    if not os.path.isfile("./config/config.toml") or (len(sys.argv) >= 2 and sys.argv[1] == "init"):
        from createConfig import initiation
        initiation()
    from doStuff import initImport
    from doStuff import cleanUp
    initImport()
    cleanUp()
    

if __name__ == "__main__":
    createDir("./logs")
    main()