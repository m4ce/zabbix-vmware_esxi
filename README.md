# Zabbix VMware ESXi CIM monitoring with low-level discovery

This external check plugin allows to monitor a standalone VMware ESXi through the built-in CIM interface. There are a few other plugins out there that let you accomplish the same, mostly for Nagios or similars.

<u><b>What is unique about this plugin is that it massively leverages the powerful low-level discovery features available in Zabbix</b></u>.

## Installation
For this setup to work, you would first need to create a user with CIM interaction permissions on your ESXi(s).

In order to accomplish that, execute the following snippet on your ESXi server(s). If you deploy your ESXi server(s) using kickstart, you can optionally add the snippet to your template so that every newly-deployed box will get it.

<b>Note</b>: the user must be part of the root group, else it won't be able to access the CIM interface even though it has the permissions to do so.

```
/usr/lib/vmware/auth/bin/adduser -s /sbin/nologin -D -H zabbix -G root
echo "secure_zabbix_password" | /usr/lib/vmware/auth/bin/passwd --stdin zabbix
vim-cmd vimsvc/auth/role_add CIM_ReadOnly Host.Cim.CimInteraction System.Anonymous
vim-cmd vimsvc/auth/entity_permission_add vim.Folder:ha-folder-root 'zabbix' false CIM_ReadOnly true
```

Before importing the XML template through the web interface, you can optionally add the following value mappings into Zabbix (this is really for cosmetic reasons, mainly to make latest data look prettier and errors a bit more human friendly).

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

The template relies on two main macros: {#VMWARE_USER} and {#VMWARE_PASSWORD}. Given that, you need to make sure they are defined either at the global level, template level or host level.

## Screenshots

Dashboard example:

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-dashboard.png)

Latest data hardware monitoring (discovered via LLD):

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data1.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data2.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data3.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data4.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data5.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data6.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data7.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data8.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data9.png)

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data10.png)

Hypervisor monitoring using Zabbix built-in simple checks:

![ScreenShot](https://raw.github.com/m4ce/zabbix-vmware_esxi/master/screenshots/zabbix-vmware-latest_data11.png)

## Contact
Matteo Cerutti - matteo.cerutti@hotmail.co.uk
