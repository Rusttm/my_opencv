from OCVYolo8.OCVMainLogger import OCVMainLogger
import os
class OCVMainClass(OCVMainLogger):
    logger_name = f"{os.path.basename(__file__)}"
    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = OCVMainClass()
    connect.logger.info("testing MainClass")
