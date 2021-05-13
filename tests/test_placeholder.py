import pytest
from majortom_scripting import ScriptingAPI
import logging

def test_logging_output():
    # A simple test to see what output is being captured
    logging.debug("DEBUG: Testing")
    logging.info("INFO: Testing")
    logging.warning("WARN: Testing")
    logging.error("ERROR: Testing")
    print("PRINT: Testing")

def test_required_args():
    with pytest.raises(TypeError):
        ScriptingAPI()
