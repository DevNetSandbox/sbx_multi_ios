# GitLab

Quickly spin up a GitLab stack in your sandbox.

# Quickstart

While VPN'd into the sandbox. Run the following commands from the devbox `ssh developer@10.10.20.50`
```
git clone https://github.com/DevNetSandbox/sbx_multi_ios.git
cd sbx_multi_ios/gitlab
./setup.sh
```

Once the process is complete, GitLab should be accessible at http://10.10.20.50 The
default credentials are `developer/C1sco12345`

# Troubleshooting / Verification

Should you need to tinker with the admin settings you can use the `root` account with
password `C1sco12345`

You can verify the runner registered successfully at http://10.10.20.50/admin/runners
