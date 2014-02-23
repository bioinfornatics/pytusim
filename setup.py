from distutils.core import setup
from os import listdir
from os.path import join, isdir

data_files = []
data_dir   = "share/pytusim"
cards_dir  = join(data_dir, "cards" )
for faction in filter( lambda x: isdir( join(cards_dir, x) ) , listdir( cards_dir )):
        data_files.append(
            (
                join( cards_dir, faction ),
                [join( cards_dir, faction, card ) for card in listdir( join( cards_dir, faction ) )],
            )
        )

setup(
    name            = "pytusim",
    version         = "0.1.0",
    description     = "Another Tyrant Unleashed simulator",
    author          = "Jonathan Mercier aka bioinfornatics",
    author_email    = "bioinfornatics at fedoraproject dot org",
    url             = "https://github.com/bioinfornatics/pytusim",
    download_url    = "https://github.com/bioinfornatics/pytusim/archive/master.zip",
    keywords        = ["Tyrant Unleashed", "game", "simulator"],
    classifiers     = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment :: Simulation"
        "Topic :: Games/Entertainment :: Turn Based Strategy"
        ],
    requires        = [ "BeautifulSoup (> 4.0.0)" ],
    packages        = [ "pytusim", "pytusim.cards", "pytusim.wikia", "pytusim.engine" ],
    data_files      = data_files,
    scripts         = [ "bin/pytusim" ]
)
