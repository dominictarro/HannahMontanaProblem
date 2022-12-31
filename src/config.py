"""
Project configuration values.
"""
import os


PROJECT_HOME = os.path.dirname(os.path.dirname(__file__))

RESULT_HOME = os.path.join(PROJECT_HOME, 'Results')
if not os.path.exists(RESULT_HOME):
    os.mkdir(RESULT_HOME)
