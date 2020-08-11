"""convert data from a format to another format, read or write from file or database, suitable for iDataAPI"""

from .cli import main
from .source.factory import ParserFactory
from .dest.factory import OutPutFactory

__all__ = ["ParserFactory", "OutPutFactory"]

__version__ = '0.0.1'
