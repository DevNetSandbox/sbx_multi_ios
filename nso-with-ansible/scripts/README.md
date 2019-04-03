# plug and play scripting


Plug in play scripting allows you to quickly add functionality/workflow to NSO

This repo contains a couple samples of how to use them

* command scripts - are used to add commands into NSO.
* post-commit scripts - scripts that execute after every commit

These can be any executable script (**chmod +x scriptname**) which contains the correct convention

* command scripts must respond to the --command argument with the appropriate command metadata
e.g my-new-command.py --command
```
begin command
    modes: oper
    styles: c i j
    cmdpath: my-new-command
    help: do something interesting to a device
end
begin param
  name: device
  presence: mandatory
  flag: -d
  help: Device to generate
end
```
* post-commit scripts must respond to the --post-commit argument with the following
e.g `my-post-commit-hook.sh --post-commit`
```
begin post-commit
end
```

# Credits

Thanks Dan Sullivan for his awesome blog.

https://community.cisco.com/t5/nso-developer-hub-blogs/operationalizing-nso-using-plug-and-play-scripting/ba-p/3662854
