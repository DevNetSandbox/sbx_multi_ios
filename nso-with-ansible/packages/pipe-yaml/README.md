# pipe-yaml

This is a quick "package" that shows how the NSO CLI can be customized to
support custom `| xxx` commands

# Installation

`ncsc -c yaml-c.cli -o <ncs_run dir>/packages`

# Usage

You can add `| yaml` to the output of any command already (with `| display json`)
and it will convert to yaml
 
```
admin@ncs# show running-config devices authgroups | display json | yaml
data:
  tailf-ncs:devices:
    authgroups:
      group:
      - name: default
        umap:
        - local-user: admin
          remote-name: admin
          remote-password: $8$ZTkLBltuYpuUyauRJ8JMk5MwkWY4ZJ7fJ2DW/Y8frZU=
        - local-user: oper
          remote-name: oper
          remote-password: $8$9CYGEGQpijTJJ5Q0aHXhbqrECEtwc22nqXV7+LH/+pM=
      snmp-group:
      - default-map:
          community-name: public
        name: default
        umap:
        - local-user: admin
          usm:
            auth:
              md5:
                remote-password: $8$0cshgJEA821dYXq379lGjavo+iE/0E4iL8HC9Bu3D6Q=
            priv:
              des:
                remote-password: $8$I3WdUeYzupKXgO32Eg7B5KY+mdv7FRqBwmQ1AOx58QY=
            remote-name: admin
            security-level: auth-priv
```
