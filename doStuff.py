import sys
from main import setLogging
import string
from pathlib import Path

dateFormatISO8601 = "YYYY/MM/DD"
incidents: list[dict] = []

def initImport() -> None:
    logger = setLogging(__name__)
    from main import loadToml
    drives = getDrives()
    print(f"select the device from which you are planning to import images:")
    for i, drive in enumerate(drives):
        print(f"{i}: {drive}:/")
    importDeviceLetter = drives[int(input(f"(enter the corresponding number of the desired drive): ")).strip()]
    logger.debug(f"*{sys._getframe().f_code.co_name}*: {importDeviceLetter = }")
    config = loadToml()
    copyImages(config, importDeviceLetter)
    incidentReport(incidents)
    

def getDrives() -> list:
    logger = setLogging(__name__)
    from ctypes import windll
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    logger.debug(f"*{sys._getframe().f_code.co_name}*: {drives = }")
    return drives

def getFileDate(file) -> list[float|str]:
    logger = setLogging(__name__)
    import os
    from datetime import datetime
    stat = os.stat(file)
    try:
        formattedDate = datetime.fromtimestamp(stat.st_birthtime).strftime("%Y/%m/%d")
        logger.debug(f"*{sys._getframe().f_code.co_name}*: '{file}': {stat.st_birthtime};  {formattedDate}")
        return [stat.st_birthtime, formattedDate]
    except AttributeError:
        logger.exception(f"Exception")
        from statx import statx
        btime = statx(file).btime
        if btime:
            formattedDate = datetime.fromtimestamp(btime).strftime("%Y/%m/%d")
            logger.debug(f"*{sys._getframe().f_code.co_name}*: '{file}': {btime};  {formattedDate}")
            return [btime, formattedDate]
    rawDate = os.path.getmtime(file)
    formattedDate = datetime.fromtimestamp(rawDate).strftime("%Y/%m/%d")
    logger.debug(f"*{sys._getframe().f_code.co_name}*: '{file}': {rawDate};  {formattedDate}")
    return [rawDate, formattedDate]

def randomStringGen(length = 12, alphabet = string.ascii_letters) -> str:
    logger = setLogging(__name__)
    import random
    randomString = "".join(random.choice(alphabet) for _ in range(length))
    logger.debug(f"*{sys._getframe().f_code.co_name}*: {randomString = }")
    return randomString

def copyImages(config: dict, device: str) -> None:
    logger = setLogging(__name__)
    import shutil
    from main import createDir
    if config["schema"] == dateFormatISO8601:
        for brand in config["validImgFileExt"]:
            for imgFileExt in config["validImgFileExt"][brand]:
                for pathToImage in list(Path(f"{device}:/").glob(f"**/*{imgFileExt}")):
                    imageDate: str = getFileDate(pathToImage)[1]
                    targetPath = Path(config["rootDir"]).joinpath(imageDate)
                    createDir(targetPath)
                    if not raiseIncident(pathToImage, targetPath):
                        logger.debug(f"*{sys._getframe().f_code.co_name}*: {pathToImage} -> {targetPath.joinpath(pathToImage.name)}")
                        shutil.copyfile(pathToImage, targetPath.joinpath(pathToImage.name))
                        print(f"copied '{pathToImage}' to '{targetPath.joinpath(pathToImage.name)}'")
    elif config["schema"] == "Insanity":
        subDir = randomStringGen()
        targetPath = Path(config["rootDir"]).joinpath(subDir)
        createDir(targetPath)
        for brand in config["validImgFileExt"]:
            for imgFileExt in config["validImgFileExt"][brand]:
                for pathToImage in list(Path(f"{device}:/").glob(f"**/*{imgFileExt}")):
                    if not raiseIncident(pathToImage, targetPath):
                        logger.debug(f"*{sys._getframe().f_code.co_name}*: {pathToImage} -> {targetPath.joinpath(pathToImage.name)}")
                        shutil.copyfile(pathToImage, targetPath.joinpath(pathToImage.name))
                        print(f"copied '{pathToImage}' to '{targetPath.joinpath(pathToImage.name)}'")

def raiseIncident(pathToImage: Path, targetPath: Path) -> bool:
    logger = setLogging(__name__)
    import os
    targetPathToImage = targetPath.joinpath(pathToImage.name)
    if os.path.exists(targetPathToImage):
        incidents.append({"src": pathToImage, "tar": targetPathToImage})
        print(f"{pathToImage} was added to the incident Report.")
        logger.debug(f"*{sys._getframe().f_code.co_name}*: {pathToImage} was added to the incident Report.")
        return True
    else:
        return False

def incidentReport(incidents: list[dict]) -> None:
    logger = setLogging(__name__)
    if len(incidents) > 0:
        print(f"{len(incidents)} incidents occured while trying to import images.")
        writeOrShow = input("Do you want to see the incident-report or shall i create a file containing the output? (show/file/both): ").strip()
        if (writeOrShow.lower() == "show") or (writeOrShow.lower() == "both"):
            print(f"Following files seem to already exist. None of the affected files were copied or replaced. Please check the incident and decide how to proceed:")
            for i, v in enumerate(incidents):
                print(f"{i+1}: '{v["src"]}' vs. '{v["tar"]}'")
        if (writeOrShow.lower() == "file") or (writeOrShow.lower() == "both"):
            from datetime import datetime
            from main import createDir
            timestamp = datetime.now().strftime("%Y%m%d_%H-%M-%S")
            reportOutputLocation = Path(input("Please enter the desired directory for the incident output file. Defaults to the root directory of this script.: ").strip() or Path.cwd()).joinpath("incidentReports")
            createDir(reportOutputLocation)
            with open(reportOutputLocation.joinpath(f"report_{timestamp}.txt"), "w") as f:
                f.write(f"{len(incidents)} incidents occured while trying to import images.\n")
                f.write(f"Following files seem to already exist. None of the affected files were copied or replaced. Please check the incident and decide how to proceed:\n")
                for i, v in enumerate(incidents):
                    f.write(f"{i+1}: '{v["src"]}' vs. '{v["tar"]}'\n")
    else:
        print("no incidents occured. Everything should be fine. Make me a sandwich.")

def cleanUp(dir = "./logs") -> None:
    logger = setLogging(__name__)
    from datetime import timedelta
    from datetime import date
    import os
    delta0 = timedelta(days = 3)
    delta1 = timedelta(weeks = 4)
    delta2 = timedelta(weeks = 12)
    today = date.today()
    size = {"max": 20000000, "min": 4000000} # 20mb, 4mb
    for logFile in list(Path().cwd().joinpath(dir).glob(f"**/*.log")):
        fileDate = date.fromtimestamp(getFileDate(logFile)[0])
        fileSize = os.stat(logFile).st_size
        if today - fileDate >= delta2:
            if os.path.exists(logFile):
                logger.debug(f"*{sys._getframe().f_code.co_name}*: deleted '{logFile}' after {today - fileDate} days with a filesize of {round(fileSize/1000, 2)} kb.")
                os.remove(logFile)
        if (today - fileDate >= delta1) and (fileSize >= size["min"]):
            if os.path.exists(logFile):
                logger.debug(f"*{sys._getframe().f_code.co_name}*: deleted '{logFile}' after {today - fileDate} days with a filesize of {round(fileSize/1000000, 2)} mb.")
                os.remove(logFile)
        if (today - fileDate >= delta0) and (fileSize >= size["max"]):
            if os.path.exists(logFile):
                logger.debug(f"*{sys._getframe().f_code.co_name}*: deleted '{logFile}' after {today - fileDate} days with a filesize of {round(fileSize/1000000, 2)} mb.")
                os.remove(logFile)