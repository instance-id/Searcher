<!-- Open me in a markdown capable browser, or go to https://github.com/instance-id/searcher_addon -->

## Searcher

![](https://i.imgur.com/2JCkraG.png)

### Currently only *fully* working on Windows and Linux. If there is interest in a working Mac version, let me know.

#### [Installation](#install) | [Compatability Details](#notes)
---
Thanks for checking out Searcher. Below are the instructions to get you up and running. 

## Help Docs
https://help.instance.id/searcher/

## Note for Houdini 18.5+  
SideFX has only included SQLite v 3.31.0 with H18.5 and their support has told me they have no plans to upgrade it to 3.33.0 (which has FTS5 enabled (Full-Text Search), which is needed by Searcher). Because of this, an extra step is required to install/use Searcher with Houdini 18.5+ until/unless they decide to include SQLite 3.33.0 instead of 3.31.0.

Download:  
Windows x64: [SQLite v3.33.0](https://www.sqlite.org/2020/sqlite-dll-win64-x64-3330000.zip)   
- Extract the downloaded sqlite-dll-win64-x64-3330000.zip file, then in another window browse to your Houdini installation directory: aka `$HFS/bin`.  
  By default this is located at: `C:\Program Files\SideFX\Houdini19.0.xxx\bin`
- In the Houdini $HFS/bin folder, locate the `sqlite3.dll` file and either make a backup copy to save elsewhere (just in case), or simply rename it to `sqlite3.dll.bak`
- From the extracted sqlite-dll-win64-x64-3330000.zip, locate the new `sqlite3.dll` then copy and paste it into the `$HFS/bin` folder.

From my testing, that was all that needed to be done, as Searcher worked for me at that point, but Houdini support mentioned that the sqlite3.dll located in the `$HFS/python27/dlls` or `$HFS/python37/dlls` folder should be replaced as well. Just make sure to back it up/rename it as well. Always better to be safe than sorry!

The process is the same for Unix OS's, you just have to go to the `$HFS/bin` folder that cooresponds to your particular OS and instead of looking for sqlite3.dll, the file will just be `sqlite3`. I would love to test it, but Houdini 18.5 on Linux crashes when I try to open it on both my laptop and VM on my desktop.  

Linux: [SQLite v3.33.0](https://www.sqlite.org/2020/sqlite-tools-linux-x86-3330000.zip)   
MacOS: [SQLite v3.33.0](https://www.sqlite.org/2020/sqlite-tools-osx-x86-3330000.zip)   

---
#### Install

1. Extract/unzip 'Searcher_\<version>.zip'. (ex. Searcher_{#version}.zip) Inside will be a packages and Searcher folder as well as a README.md and a url link to this page.
    ```
    Searcher_{#version}.zip /
            Searcher_{#version}/__ /packages/
                            |_ /Searcher/
                            |__ README.md
                            |__ Searcher_install_instructions.url
   ```

2. Move the Searcher folder somewhere permanent. It can be placed where ever you would like. Make note of the folder path, as it will be needed in a later step. Examples below:  
   
    | OS                                           | Path  (replace \<user> with your actual username) |
    | -------------------------------------------- | ------------------------------------------------- |
    | <i class="fa fa-windows fa-1x"></i> Windows: | C:\Users\\\<user>\houdini_addons\Searcher         |
    | <i class="fa fa-linux fa-1x"></i> Linux:     | /home/\<user>/houdini_addons/Searcher             |
    | <i class="fa fa-apple fa-1x"></i> MacOS:     | /Users/\<user>/Library/h_addons/Searcher          |

3. Move the 'packages' folder into your Houdini $HOME directory. The locations are seen below:
    | OS                                           | Path  (replace \<user> with your actual username)                      |
    | -------------------------------------------- | ---------------------------------------------------------------------- |
    | <i class="fa fa-windows fa-1x"></i> Windows: | C:\Users\\\<user>\Documents\houdini18.0\packages\Searcher.json         |
    | <i class="fa fa-linux fa-1x"></i> Linux:     | /home/\<user>/houdini18.0/packages/Searcher.json                       |
    | <i class="fa fa-apple fa-1x"></i> MacOS:     | /Users/\<user>/Library/Preferences/houdini/18.0/packages/Searcher.json |

4. Within the 'packages' folder is the Searcher.json file. Open this file in your editor of choice and edit line #27. Within the second set of quotation marks input the path to the Searcher folder from step #2. On Windows, replace the backslashes (\\) in the path with a forwardslashs (/)
Ex. If using Windows and following the example listed above, line 27 would look like this:
    ```
			"SEARCHERLOCATION": "C:/Users/<user>/houdini_addons/Searcher",
    ```
5. Save the file and start Houdini. On the main shelf toolbar add the Searcher shelf by clicking on the plus(+) button, then the Shelves tab, followed by selecting "Searcher Shelf" seen in the images below:
    ![](https://i.imgur.com/GzdyUYt.png)  
    ![](https://i.imgur.com/F4C5MOx.png)

6. You should now be able to hit the hotkey below to open the Searcher window:  
    Open Searcher Window: <kbd>Ctrl</kbd>+<kbd>`</kbd>

### Notes

##### Compatability:

| Houdini                                       | Versions Tested          |
| --------------------------------------------- | ------------------------ |
| ![](https://i.imgur.com/h9Nefqz.png) Houdini: | Version: 18.0.348 and up |

##### Tested versions
| OS         | Versions Tested                        |
| ---------- | -------------------------------------- |
| ⊞ Windows: | Windows 10 Pro v10.0.19041.264 (v2004) |
| 🐧 Linux:   | Pop_OS! (Ubuntu) 19.04/19.10/20.04     |
| 🍎 MacOS:   | Possibly coming soon, if requested     |



<i class="fa fa-firefox fa-1x"></i> [website](https://instance.id/) | <i class="fa fa-twitter fa-1x"></i> [twitter](https://twitter.com/instance_id) | <i class="fa fa-github fa-1x"> </i> [github](https://github.com/instance-id) | <i class="fa fa-bug fa-1x"></i> [issues](https://github.com/instance-id/searcher_addon/issues?q=) | <i class="fa fa-at fa-1x"></i> [email](https://github.com/instance-id/searcher_addon/issues?q=)  
