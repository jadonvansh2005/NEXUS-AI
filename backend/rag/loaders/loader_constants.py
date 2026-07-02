from enum import Enum


# --------------------------------------------------
# Document Types
# --------------------------------------------------

class DocumentType(

    Enum

):

    PDF = "pdf"

    DOCX = "docx"

    PPTX = "pptx"

    XLSX = "xlsx"

    CSV = "csv"

    TXT = "txt"

    CODE = "code"


# --------------------------------------------------
# Supported Extensions
# --------------------------------------------------

PDF_EXTENSIONS = [

    ".pdf"

]

DOCX_EXTENSIONS = [

    ".docx"

]

PPTX_EXTENSIONS = [

    ".pptx"

]

EXCEL_EXTENSIONS = [

    ".xlsx",

    ".xls"

]

CSV_EXTENSIONS = [

    ".csv"

]

TEXT_EXTENSIONS = [

    ".txt",

    ".md",

    ".rst"

]

CODE_EXTENSIONS = [

    ".py",

    ".js",

    ".jsx",

    ".ts",

    ".tsx",

    ".java",

    ".cpp",

    ".c",

    ".cc",

    ".cs",

    ".go",

    ".rs",

    ".php",

    ".rb",

    ".swift",

    ".kt",

    ".scala",

    ".sql",

    ".html",

    ".css",

    ".scss",

    ".json",

    ".xml",

    ".yaml",

    ".yml",

    ".toml",

    ".ini",

    ".cfg",

    ".sh",

    ".bat",

    ".ps1"

]


# --------------------------------------------------
# Combined Extensions
# --------------------------------------------------

SUPPORTED_EXTENSIONS = (

    PDF_EXTENSIONS

    +

    DOCX_EXTENSIONS

    +

    PPTX_EXTENSIONS

    +

    EXCEL_EXTENSIONS

    +

    CSV_EXTENSIONS

    +

    TEXT_EXTENSIONS

    +

    CODE_EXTENSIONS

)