from rag.loaders.loader_factory import LoaderFactory

from rag.loaders.pdf_loader import PDFLoader
from rag.loaders.docx_loader import DOCXLoader
from rag.loaders.ppt_loader import PPTLoader
from rag.loaders.excel_loader import ExcelLoader
from rag.loaders.csv_loader import CSVLoader
from rag.loaders.text_loader import TextLoader
from rag.loaders.code_loader import CodeLoader

LoaderFactory.register(PDFLoader)
LoaderFactory.register(DOCXLoader)
LoaderFactory.register(PPTLoader)
LoaderFactory.register(ExcelLoader)
LoaderFactory.register(CSVLoader)
LoaderFactory.register(TextLoader)
LoaderFactory.register(CodeLoader)