# Changelog

## v0.1.0-beta (2020-07-06)

#### New Features

* Add readme and license information, closes [#15](https://github.com/twanh/FileSearcher/issues/15)
* Create buildpipeline, closes: [#14](https://github.com/twanh/FileSearcher/issues/14)
* Add the ability to run the app in prod (default) and dev (commandline arg)
* Create trayicon and improve the background cycle. Quiting the app only from the trayicon! - closes: [#8](https://github.com/twanh/FileSearcher/issues/8)
* Custom icon - closes: [#12](https://github.com/twanh/FileSearcher/issues/12)
* When the application shows the input is automaticly focussed - closes: [#7](https://github.com/twanh/FileSearcher/issues/7)
* Application now automaticly centers it self on startup - closes: [#11](https://github.com/twanh/FileSearcher/issues/11)
* Add saving of functionality
* The searcher automaticly reindexes the root_folder with on a set interval - closes [#9](https://github.com/twanh/FileSearcher/issues/9)
* Better closing with sys.exit
* Better closing with sys.exit
* Create the functionality to run in the background and respond to a hotkey - closes [#8](https://github.com/twanh/FileSearcher/issues/8)
#### Fixes

* Change the icon image path to update the path when the application is build
* Close the application with taskkill, but this is only temporary and only works on windows and in dev - workon: [#10](https://github.com/twanh/FileSearcher/issues/10)
* [#1](https://github.com/twanh/FileSearcher/issues/1), search requests are now only sent when the query is longer then 4 or enter is pressed
#### Refactorings

* update requirements.txt, update eel
* Remove all unused interface links - closes: [#13](https://github.com/twanh/FileSearcher/issues/13)
* Add docstrings and minor improvements'
