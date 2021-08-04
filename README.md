# onix-splitter
onix-splitter is a tool used for splitting large ONIX collections into 1-item chunks.

It extracts items with specified identifiers and save them as 1-item ONIX collections
in the specified output directory.

## Usage
1. Install the module:
```bash
poetry install
``` 

2. Run the module and create a new ONIX file:
```bash
python -m onix_splitter split \
    --identifiers=<IDENTIFIERS> \
    --metadata-folder=<METADATA_FOLDER> \
    --books-folder=<BOOKS_FOLDER> \
    --covers-folder=<COVERS_FOLDER> \
    --output-folder=<OUTPUT_FOLDER>
``` 
where `<IDENTIFIERS>` is a comma-separated list of identifiers. For example: `9788880638384,9788880639565,9788880638247`.