# Configuration

The config for JujuSpell continues list of controllers where each controller have fallowing attributes:

* `name` controller name (both on the client side and in the controller)
* `customer` customer name for better identification
* `owner` owner name
* `description` [optional] controller description
* `tags` [optional] list of tags used for filtering
* `risk` [optional] risk level [1-5] used for filtering, where 5 is default value and the most risky
* `endpoint` controller api endpoint (currently we are not supporting multiple api endpoints)
* `ca_cert` certificate for controller
* `username` username
* `password` password
* `model_mapping` {lma, default} map model category to real name of the model
* `connection` [optional] definition for remote clouds (sshuttle and port-forwarding)
  * `destination` remote destination accessible with ssh
  * `subnets` [optional] list of subnets, this option will be used with sshuttle enabled
  * `jumps` [optional] ssh jumps are sorted according to the order in which they are performed


Example:
```yaml
controllers:
  - name: example_controller
    customer: example_customer
    owner: Gandalf
    description: some nice notes about controllers and models  # optional
    tags: ["test"]  # optional
    risk: 5  # optional [5]
    endpoint: 10.1.1.46:17070
    ca_cert: |
        -----BEGIN CERTIFICATE-----
        -----END CERTIFICATE-----
    username: admin
    password: pass1234
    model_mapping:
      lma: monitoring
      default: production
    connection:  # optional
      destination: ubuntu@10.1.1.99  # infra node
      subnets:  # optional (sshuttle)
        - 10.1.1.0/24
        - 20.1.1.0/24
      jumps:  # optional
        - bastion
```


## Loading configuration

Currently we have three environment variables can change the way how we load config files.

* `JUJUSPELL_DATA`: A fodler default at `~/.local/share/juju-spell/`
* * `JUJUSPELL_CONFIG`: Default is `{JUJUSPELL_DATA}/config.yaml`
* * `JUJUSPELL_PERSONAL_CONFIG`: Default is `{JUJUSPELL_DATA}/config.person.yaml`

* When loading the config files, we will first load `JUJUSPELL_CONFIG` and then update it with `JUJUSPELL_PERSONAL_CONFIG` based on the unique key `uuid`, which is the controller's uuid.
* We also provide `--config` argument. Once user give this input, we will not using the `JUJUSPELL_CONFIG` and `JUJUSPELL_PERSONAL_CONFIG` to load config but use `--config`, which should be a config file path, as the only input to load config.
