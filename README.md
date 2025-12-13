TODO: 
- different run configs:
  - test/debug
  - live monitoring: select a script. Should open with a combo box, pick one, and then those emit values that attach to the widgets. 
- Create a JSON serialization format to save different configs

Display types:
- circular gauge
- horizontal tachometer
- plain text

Data types:
- RPM
  - Units: rpm
  - Range: 0 - 30
  - Display: circular gauge default, supports all


When the application starts, the following needs to happen:
- set window stuff, i.e. geometry, title, central widget, QHLayout, menu items
- Look for a default config file
  - If no file is found or an empty file is found, the screen should be blank 
- So in `init`, all that has to happen & they should all be one line reference to another method
- If a file is found AUTOMATICALLY, it should make it to MainWindow as a layout object.
- so we do need load_json for the menu thing but not for the startup. 
- I also probably should move more specific non ui stuff to the back

^ That means I have to get rid of the older hardcoded qt objects
Also important, eventually all widgets need to be hooked up to an emitter of some sort



could have a class member called config or something that holds a layout or None