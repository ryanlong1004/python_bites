logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    handlers=[
        logging.FileHandler("test_esmf.log"),
        logging.StreamHandler()
    ]
)
