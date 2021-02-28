class ModelNotFoundError(Exception):
    """Raised when there aren't models in the DB to fill the criteria"""
    print("One or more models doesn't exist in the DB")
    pass
