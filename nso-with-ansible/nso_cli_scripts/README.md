# nso_cli_scripts

These scripts are designed to show how you can automate using the

# Usage

### From within NSO CLI

```
admin@ncs(config)# load merge nso_cli_scripts/apply_ntp_template.cli
Loading.
apply-template-result {
    device nx
    result no-namespace
    info No matching namespaces found for device: nx.
}
apply-template-result {
    device xe
    result ok
}
apply-template-result {
    device xr
    result ok
}
```

**NOTE:** you can also use the `rload` command for a relative load, so that your
script files do not need to start from the top of the tree
