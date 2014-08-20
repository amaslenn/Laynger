Laynger
=======

Laynger is a plugin for Sublime Text 2/3 which allows user to change central border in 2-columns layout using keyboard.  

![alt tag](https://raw.githubusercontent.com/amaslenn/Laynger/master/laynger.gif)

## Settings
Default settings

    {
        // save and restore borders
        "keep_layout": true,

        // save and restore files in groups
       "keep_groups": true
    }

## Usage
`Alt + Shift + Left/Right`: move central border to the left/right  
`Alt + Shift + d`: revert central border to default position (center)

Since plugin keeps groups and positions of the files, it is useful to overwrite default key bindings (_you can copy them from Default Key Bindings of the Laynger to User's one and uncomment_)

    { "keys": ["alt+shift+1"], "command": "laynger", "args" : { "opt": "1_column"} },
    { "keys": ["alt+shift+2"], "command": "laynger", "args" : { "opt": "2_columns"} }
