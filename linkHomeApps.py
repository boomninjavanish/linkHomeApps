from os import system
from pathlib import Path

homeDirectory = Path.home()
mainAppsPath = '/Applications'
homeAppsPath = homeDirectory / 'Applications'

# get the files
listOfHomeApps = Path(homeAppsPath).rglob('*.app')
listOfMainApps = Path(mainAppsPath).glob('*.app')


# terminal colors
class TermColors:
    red = '\033[31m'
    green = '\033[32m'
    white = '\033[37m'


# add soft links from ~/Applications to /Applications
if listOfHomeApps:
    print('Linking any apps that do not exist in the main app directory...')
    for app in listOfHomeApps:
        # see if link exists
        link = Path(mainAppsPath) / app.name
        linkExist = Path(link).exists()

        if linkExist:
            print(TermColors.white + '\t"' + link.name + '" exists')
        else:
            print(TermColors.green + '\tlinking "' + app.name + '" to /Applications')
            # make soft link
            source = str(app.parent / app.name)
            destination = str(Path(mainAppsPath) / app.name)
            system('ln -s "' + source + '" "' + destination + '"')
    print(TermColors.white + 'Done!')

else:
    print("No apps were found in the home directory.")

# remove dead soft links from /Applications
print('Checking main Applications directory for dead links...')
for app in listOfMainApps:
    linkPath = Path(mainAppsPath) / app.name
    if linkPath.is_symlink():
        linkSource = Path(linkPath).readlink()
        sourceExist = Path(linkSource).exists()
        if sourceExist:
            print(TermColors.white + '\t"' + str(linkSource) + '" is alive!')
        else:
            print(TermColors.red + '\t"' + str(linkSource) + '" is dead...deleting...')
            system('rm -f "' + str(Path(mainAppsPath) / app.name) + '"')
print(TermColors.white + 'Done!')
print('Exiting...')
