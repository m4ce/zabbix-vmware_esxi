# Zabbix VMware ESXi CIM monitoring with low-level discovery

This external check plugin allows to monitor a standalone VMware ESXi through the built-in CIM interface. There are a few other plugins out there that let you accomplish the same, mostly for Nagios or similars.

What is unique about this plugin is that it massively leverages low-level discovery features in Zabbix.

For this setup, you would need to add a user that has CIM interaction permissions on your ESXi before you can actually make use of the template and the respective plugin.

In order to accomplish that, execute the following snippet on your ESXi server. If you deploy your ESXi servers using kickstart, you can optionally add it to your template so that every newly-deployed box will get it (Note: the user needs to be part of the root group, else it won't be able to access the CIM interface even though it has the permissions set over the role).

```
/usr/lib/vmware/auth/bin/adduser -s /sbin/nologin -D -H zabbix -G root
echo "secure_zabbix_password" | /usr/lib/vmware/auth/bin/passwd --stdin zabbix
vim-cmd vimsvc/auth/role_add CIM_ReadOnly Host.Cim.CimInteraction System.Anonymous
vim-cmd vimsvc/auth/entity_permission_add vim.Folder:ha-folder-root 'zabbix' false CIM_ReadOnly true
```

Before importing the XML template, you can optionally add the following value mappings into Zabbix (this is really for cosmetic reasons):

```
mysql> SELECT name, value, newvalue FROM valuemaps INNER JOIN mappings ON valuemaps.valuemapid = mappings.valuemapid WHERE name LIKE 'VMware%';
+-------------------------------------------+-------+----------------------------+
| name                                      | value | newvalue                   |
+-------------------------------------------+-------+----------------------------+
| VMware - Ethernet port enabled states     | 0     | Unknown                    |
| VMware - Ethernet port enabled states     | 1     | Other                      |
| VMware - Ethernet port enabled states     | 2     | Enabled                    |
| VMware - Ethernet port enabled states     | 3     | Disabled                   |
| VMware - Ethernet port enabled states     | 4     | Shutting down              |
| VMware - Ethernet port enabled states     | 5     | Not applicable             |
| VMware - Ethernet port enabled states     | 6     | Enabled but offline        |
| VMware - Ethernet port enabled states     | 7     | In test                    |
| VMware - Ethernet port enabled states     | 8     | Deferred                   |
| VMware - Ethernet port enabled states     | 9     | Quiesce                    |
| VMware - Ethernet port enabled states     | 10    | Starting                   |
| VMware - Ethernet port enabled states     | 11    | DMTF reserved              |
| VMware - Ethernet port enabled states     | 32768 | Vendor Reserved            |
| VMware - Ethernet port full duplex status | 0     | Disabled                   |
| VMware - Ethernet port full duplex status | 1     | Enabled                    |
| VMware - Hypervisor status                | 0     | Unknown (grey)             |
| VMware - Hypervisor status                | 1     | OK (green)                 |
| VMware - Hypervisor status                | 2     | Degraded (yellow)          |
| VMware - Hypervisor status                | 3     | Failed (red)               |
| VMware - Virtual machine power state      | 0     | Powered off                |
| VMware - Virtual machine power state      | 1     | Powered on                 |
| VMware - Virtual machine power state      | 2     | Suspended                  |
| VMware CIM - Health Status                | -1    | Unsupported                |
| VMware CIM - Health Status                | 0     | Unknown                    |
| VMware CIM - Health Status                | 5     | OK                         |
| VMware CIM - Health Status                | 10    | Degraded                   |
| VMware CIM - Health Status                | 15    | Minor                      |
| VMware CIM - Health Status                | 20    | Major                      |
| VMware CIM - Health Status                | 25    | Critical                   |
| VMware CIM - Health Status                | 30    | Non-recoverable error      |
| VMware CIM - Operational Status           | -1    | Unsupported                |
| VMware CIM - Operational Status           | 0     | Unknown                    |
| VMware CIM - Operational Status           | 1     | Other                      |
| VMware CIM - Operational Status           | 2     | OK                         |
| VMware CIM - Operational Status           | 3     | Degraded                   |
| VMware CIM - Operational Status           | 4     | Stressed                   |
| VMware CIM - Operational Status           | 5     | Predictive failure         |
| VMware CIM - Operational Status           | 6     | Error                      |
| VMware CIM - Operational Status           | 7     | Non-recoverable error      |
| VMware CIM - Operational Status           | 8     | Starting                   |
| VMware CIM - Operational Status           | 9     | Stopping                   |
| VMware CIM - Operational Status           | 10    | Stopped                    |
| VMware CIM - Operational Status           | 11    | In service                 |
| VMware CIM - Operational Status           | 12    | No contact                 |
| VMware CIM - Operational Status           | 13    | Lost communication         |
| VMware CIM - Operational Status           | 14    | Aborted                    |
| VMware CIM - Operational Status           | 15    | Dormant                    |
| VMware CIM - Operational Status           | 16    | Supporting entity in error |
| VMware CIM - Operational Status           | 17    | Completed                  |
| VMware CIM - Operational Status           | 18    | Power mode                 |
| VMware CIM - Operational Status           | 19    | DMTF reserved              |
| VMware CIM - Operational Status           | 20    | Vendor reserved            |
+-------------------------------------------+-------+----------------------------+
```

The template is configured to use two main macros, which are {#VMWARE_USER} and {#VMWARE_PASSWORD} respectively. Therefore, you would need to define them either at the global level or, template level or host level.

Some screenshots will follow soon.
