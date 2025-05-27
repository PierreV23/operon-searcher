# operon-searcher

## Installation
python 3.10 - 3.13 should work
`pip install git+https://github.com/PierreV23/operon-searcher.git`
This installs the package straight into your python version, so that you can call it using `python -m operon_searcher`

## Usage
`python -m operon_searcher <Folder_Name>`
- `<Folder_Name>` requires a fimo.gff and genomic.gff present.
- `-v` visualizes found operons and writes these out to a folder called "output"
- `-p` prints out found operons
- `--export <File_Name>` exports the found operons as a json file
- `--help` use this to display all available command arguments

You can specify a fimo and gene file seperately, you won't have to specify the `<Folder_Name>` then. For example:
- `python -m operon_searcher <Folder_Name>`
or
- `python -m operon_searhcer --fimo fimo.gff --genes genomic.gff`

If you visualize, the pictures can be found by default in the folder `output`, but a custom folder can be specified using `--output`.

fimo.gff can be found by running a MEME motif on your genome using the FIMO tool online. genomic.gff (or a name alike) can usually be obtained from online databases, these contain the positions of genes.

Use `--help` to see all options: `python -m operon_searcher --help`


# Support
If you have any questions or errors you can use the Issues tab of this repository.