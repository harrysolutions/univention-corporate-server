.. _computers-general:

Computer management
*******************

.. _computers-hostaccounts:

Management of computer accounts via |UCSUMC| module
===================================================

All UCS, Linux and Windows systems within a UCS domain each have a
computer domain account (also referred to as the host account) with
which the systems can authenticate themselves among each other and with
which they can access the LDAP directory.

The computer account is generally created automatically when the system
joins the UCS domain (see :ref:`domain-join`); however, the
computer account can also be added prior to the domain join.

The password for the computer account is generated automatically during
the domain join and saved in the
:file:`/etc/machine.secret` file. By default the
password consists of 20 characters (can be configured via the |UCSUCRV|
:envvar:`machine/password/length`). The password is regenerated
automatically at fixed intervals (default setting: 21 days; can be
configured using the |UCSUCRV|
:envvar:`server/password/interval`). Password rotation can also
be disabled using the variable :envvar:`server/password/change`.

There is an different computer object type for every system role.
Further information on the individual system roles can be found in
:ref:`system-roles`.

Computer accounts are managed in the UMC module
:guilabel:`Computers`.

By default a simplified wizard for creating a computer is shown, which
only requests the most important settings. All attributes can be shown
by clicking on :guilabel:`Advanced`. If there is a DNS forward
zone and/or a DNS reverse zone (see :ref:`networks-dns`) assigned to
the selected network object (see :ref:`networks-introduction`), a
host record and/or pointer record is automatically created for the host.
If there is a DHCP service configured for the network object and a MAC
address is configured, a DHCP host entry is created (see
:ref:`module-dhcp-dhcp`).

The simplified wizard can be disabled for all system roles by setting
the |UCSUCRV|
:envvar:`directory/manager/web/modules/computers/computer/wizard/disabled`
to ``true``.

.. _computers-create:

.. figure:: /images/computers_computer.*
   :alt: Creating a computer in the UMC module

   Creating a computer in the UMC module

.. _computers-create-advanced:

.. figure:: /images/computers_computer_advanced.*
   :alt: Advanced computer settings

   Advanced computer settings

.. _computers-management-table-general:

Computer management module - General tab
----------------------------------------

.. _computers-management-table-general-tab:

.. list-table:: *General* tab
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Name
     - The name for the host should be entered in this input field.

       To guarantee compatibility with different operating systems and services,
       computer names should only contain the lowercase letters *a* to *z*,
       numbers, hyphens and underscores. Umlauts and special characters are not
       permitted. The full stop is used as a separating mark between the
       individual components of a fully qualified domain name and must therefore
       not appear as part of the computer name. Computer names must begin with a
       letter.

       Microsoft Windows accepts computer names with a maximum of 13 characters,
       so as a rule computer names should be limited to 13 characters if there
       is any chance that Microsoft Windows will be used.

       After creation, the computer name can only be changed for the system
       roles *Windows Workstation/Server*, *macOS Client* and *IP client*.

   * - Description
     - Any description can be entered for the host in this input field.

   * - Inventory number
     - Inventory numbers for hosts can be stored here.

   * - Network
     - The host can be assigned to an existing network object. Information on the
       IP configuration can be found in :ref:`networks-introduction`.

   * - MAC address
     - The MAC address of the computer can be entered here, for example
       ``2e:44:56:3f:12:32``. If the computer is to receive a DHCP entry, the
       entry of the MAC address is essential.

   * - IP address
     - Fixed IP addresses for the host can be given here. Further information on
       the IP configuration can be found in :ref:`networks-introduction`.

       If a network was selected on the *General* tab, the IP address assigned
       to the host from the network will be shown here automatically.

       An IP address entered here (i.e. in the LDAP directory) can only be
       transferred to the host via DHCP. If no DHCP is being used, the IP
       address must be configured locally, see
       :ref:`hardware-network-configuration`.

       If the IP addresses entered for a host are changed without the DNS zones
       being changed, they are automatically changed in the computer object and
       - where they exist - in the DNS entries of the forward and reverse lookup
       zones. If the IP address of the host was entered at other places as
       well, these entries must be changed manually! For example, if the IP
       address was given in a DHCP boot policy instead of the name of the boot
       server, this IP address will need to be changed manually by editing the
       policy.

   * - Forward zone for DNS entry
     - The DNS forward zone in which the computer is entered. The zone is used
       for the resolution of the computer name in the assigned IP address.
       Further information on the IP configuration can be found in
       :ref:`networks-introduction`.

   * - Reverse zone for DNS entry
     - The DNS reverse zone in which the computer is entered. The zone is used
       to resolve the computer's IP address in a computer name.  Further
       information on the IP configuration can be found in
       :ref:`networks-introduction`.

   * - DHCP service
     - If a computer is supposed to procure its IP address via DHCP, a DHCP
       service must be assigned here. Information on the IP configuration can be
       found in :ref:`networks-introduction`.

       During assignment, it must be ensured that the DHCP servers of the DHCP
       service object are responsible for the physical network.

       If a network is selected on the *General* tab an appropriate entry for
       the network will be added automatically. It can be adapted subsequently.

.. _computers-management-table-account:

Computer management module - Account tab
----------------------------------------

.. _computers-management-table-account-tab:

.. list-table:: *Account* tab (advanced settings)
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Password
     - The password for the computer account is usually automatically created
       and rotated.  For special cases such as the integration of external
       systems it can also be explicitly configured in this field.

       The same password must then also be entered locally on the computer in
       the :file:`/etc/machine.secret` file.

   * - Primary group
     - The primary group of the host can be selected in this selection field.
       This is only necessary when they deviate from the automatically created
       default values. The default value for a |UCSPRIMARYDN| or |UCSBACKUPDN|
       is ``DC Backup Hosts``, for a |UCSREPLICADN| ``DC Slave Hosts`` and for
       |UCSMANAGEDNODE|\ s ``Computers``.

.. _computers-management-table-unix-account:

Computer management module - Unix account tab
---------------------------------------------

.. _computers-management-table-unix-account-tab:

.. list-table:: *Unix account* tab (advanced settings)
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Unix home directory (*)
     - A different input field for the host account can be entered here. The
       automatically created default value for the home directory is
       :file:`/dev/null`.

   * - Login shell
     - If a different login shell from the default value is to be used for the
       computer account, the login shell can be adapted manually in this input
       field. The automatically set default value assumes a login shell of
       :file:`/bin/sh`.

.. _computers-management-table-services:

Computer management module - Services tab
---------------------------------------------

.. _computers-management-table-services-tab:

.. list-table:: *Services* tab (advanced settings)
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Service
     - By means of a service object, applications or services can determine
       whether a service is available on a computer or generally in the domain.

.. note::

   The tab *Services* is only displayed on UCS server system roles.

.. _computers-management-deployment-services:

Computer management module - Deployment tab
-------------------------------------------

This *Deployment* tab is used for the Univention Net Installer, see `Extended
installation documentation
<https://docs.software-univention.de/installation-5.0.html>`_.

.. _computers-management-table-dns-alias:

Computer management module - DNS alias tab
------------------------------------------

.. _computers-management-table-dns-alias-tab:

.. list-table:: *DNS alias* tab (advanced settings)
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Zone for DNS Alias
     - If a zone entry for forward mapping has been set up for the host in the
       *Forward zone for DNS entry* field, the additional alias entries via
       which the host can be reached can be configured here.

.. _computers-management-table-groups:

Computer management module - Groups tab
---------------------------------------

The computer can be added into different groups in *Groups* tab.

.. _computers-management-table-options:

Computer management module - Options alias tab
----------------------------------------------

The *Options* tab allows to disable LDAP object classes for host objects. The
entry fields for attributes of disabled object classes are no longer shown. Not
all object classes can be modified subsequently.

.. _computers-management-table-options-tab:

.. list-table:: *(Options)* tab
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Kerberos principal
     - If this checkbox is not selected the host does not receive the
       ``krb5Principal`` and ``krb5KDCEntry`` object classes.

   * - POSIX account
     - If this checkbox is not selected the host does not receive the
       ``posixAccount`` object class.

   * - Samba account
     - If this checkbox is not selected the host does not receive the
       ``sambaSamAccount`` object class.

.. _computers-ubuntu:

Integration of Ubuntu clients
-----------------------------

Ubuntu clients can be managed in the UMC module
:guilabel:`Computers` with their own system role. The network
properties for DNS/DHCP can also be managed there.

The use of policies is not supported.

Some configuration adjustments need to be performed on Ubuntu systems; these are
documented in the `Extended domain services documentation
<https://docs.software-univention.de/domain-5.0.html>`_.

.. _computers-configuration-of-hardware-and-drivers:

Configuration of hardware and drivers
=====================================

.. _computers-available-kernel-variants:

Available kernel variants
-------------------------

The standard kernel in UCS 5.0 is based on the Linux kernel 4.19. In principle,
there are three different types of kernel packages:

* A *kernel image package* provides an executable kernel which can be installed
  and started.

* A *kernel source package* provides the source code for a kernel. From this
  source, a tailor-made kernel can be created, and functions can be activated or
  deactivated.

* A *kernel header package* provides interface information which is required by
  external packages if these have to access kernel functions. This information
  is usually necessary for compiling external kernel drivers.

Normally, the operation of a UCS system only requires the installation of one
kernel image package.

Several kernel versions can be installed in parallel. This makes sure that there
is always an older version available to which can be reverted in case of an
error. So-called meta packages are available which always refer to the kernel
version currently recommended for UCS. In case of an update, the new kernel
version will be installed, making it possible to keep the system up to date at
any time.

.. _computers-hardware-drivers-kernel-modules:

Hardware drivers / kernel modules
---------------------------------

The boot process occurs in two steps using an initial RAM disk (*initrd* for
short). This is composed of an archive with further drivers and programs.

The GRUB boot manager (see :ref:`grub`) loads the kernel and the *initrd* into
the system memory, where the *initrd* archive is extracted and mounted as a
temporary root file system. The real root file system is then mounted from this,
before the temporary archive is removed and the system start implemented.

The drivers to be used are recognized automatically during system start and
loaded via the :program:`udev` device manager. At this point, the necessary
device links are also created under :file:`/dev/`. If drivers are not recognized
(which can occur if no respective hardware IDs are registered or hardware is
employed which cannot be recognized automatically, e.g., ISA boards), kernel
modules to be loaded can be added via |UCSUCRV| :envvar:`kernel/modules`. If
more than one kernel module is to be loaded, these must be separated by a
semicolon. The |UCSUCRV| :envvar:`kernel/blacklist` can be used to configure a
list of one or more kernel modules for which automatic loading should be
prevented. Multiple entries must also be separated by a semicolon.

Unlike other operating systems, the Linux kernel (with very few exceptions)
provides all drivers for hardware components from one source. For this reason,
it is not normally necessary to install drivers from external sources
subsequently.

However, if external drivers or kernel modules are required, they can be
integrated via the DKMS framework (Dynamic Kernel Module Support). This provides
a standardized interface for kernel sources, which are then built automatically
for every installed kernel (insofar as the source package is compatible with the
respective kernel). For this to happen, the kernel header package
:program:`linux-headers-amd64` must be installed in addition to the
:program:`dkms` package.  Please note that not all the external kernel modules
are compatible with all kernels.

.. _grub:

GRUB boot manager
-----------------

In |UCSUCS| GNU GRUB 2 is used as the boot manager. GRUB provides a menu which
allows the selection of a Linux kernel or another operating system to be booted.
GRUB can also access file systems directly and can thus, for example, load
another kernel in case of an error.

.. _grub-selection:

.. figure:: /images/computers_grub.*
   :alt: GRUB menu

   GRUB menu

GRUB gets loaded in a two-step procedure; in the Master Boot Record of the hard
drive, the Stage 1 loader is written which refers to the data of Stage 2, which
in turn manages the rest of the boot procedure.

The selection of kernels to be started in the boot menu is stored in the file
:file:`/boot/grub/grub.cfg`. This file is generated automatically; all installed
kernel packages are available for selection. The memory test program
:command:`Memtest86+` can be started by selecting the option :guilabel:`Memory
test` and performs a consistency check for the main memory.

There is a five second waiting period during which the kernel to be booted can
be selected. This delay can be changed via the |UCSUCRV| :envvar:`grub/timeout`.

By default a screen size of ``800x600`` pixels and 16 Bit color depth is preset.
A different value can be set via the |UCSUCRV| :envvar:`grub/gfxmode`. Only
resolutions are supported which can be set via VESA BIOS extensions. A list of
available modes can be found in `VESA BIOS Extensions
<https://en.wikipedia.org/wiki/VESA_BIOS_Extensions>`_. The input must be
specified in the format :samp:`{HORIZONTAL}x{VERTICAL}@{COLOURDEPTHBIT}`, so for
example ``1024x768@16``.

Kernel options for the started Linux kernel can be passed with the |UCSUCRV|
:envvar:`grub/append`. |UCSUCRV| :envvar:`grub/xenhopt` can be used to pass
options to the Xen hypervisor.

The graphic representation of the boot procedure - the so-called splash screen -
can be deactivated by setting |UCSUCRV| :envvar:`grub/bootsplash` to
``nosplash``.

.. _hardware-network-configuration:

Network configuration
---------------------

The configuration of network interfaces can be adjusted with the UMC module
:guilabel:`Network settings`.

The configuration is saved in |UCSUCR| variables, which can also be set
directly. These variables are listed in the individual sections.

.. _network-settings:

.. figure:: /images/computers_network.*
   :alt: Configuring the network settings

   Configuring the network settings

All the network cards available in the system are listed under *IPv4 network
devices* and *IPv6 network devices* (only network interfaces in the
:samp:`eth{X}` scheme are shown).

Network interfaces can be configured for IPv4 and/or IPv6. IPv4 addresses have a
32-bit length and are generally written in four blocks in decimal form (e.g.,
``192.0.2.10``), whereas IPv6 addresses are four times as long and typically
written in hexadecimal form (e.g., ``2001:0DB8:FE29:DE27:0000:0000:0000:0000``).

.. _computers-ipv4:

Configuration of IPv4 addresses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the *Dynamic (DHCP)* option was not chosen, the IP address to be bound to the
network card must be entered. In addition to the *IPv4 address* the *net mask*
must also be entered.  *DHCP query* is used to request an address from a DHCP
server. Unless the *Dynamic (DHCP)* option is activated, the values received
from the DHCP request are configured statically.

Server systems can also be configured via DHCP. This is necessary for some cloud
providers, for example. If the assignment of an IP address for a server fails, a
random link local address (:samp:`169.254.{x}.{y}`) is configured as a
replacement.

For UCS server systems the address received via DHCP is also written to the LDAP
directory.

.. note::

   Not all services (e.g., DNS servers) are suitable for use on a DHCP-based
   server.

UCR variables:

* :envvar:`interfaces/ethX/address`
* :envvar:`interfaces/ethX/netmask`
* :envvar:`interfaces/ethX/type`

Besides the physical interfaces, additional virtual interfaces can also be
defined in the form :envvar:`interfaces/ethX_Y/setting`.

.. _computers-ipv6:

Configuration of IPv6 addresses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The IPv6 address can be configured in two ways: Stateless address
autoconfiguration (SLAAC) is employed in the :guilabel:`Autoconfiguration
(SLAAC)` configuration. In this, the IP address is assigned from the routers of
the local network segment. Alternatively, the address can also be configured
statically by entering the *IPv6 address* and *IPv6 prefix*.

In contrast to DHCP, in SLAAC there is no assignment of additional data such as
the DNS server to be used. There is an additional protocol for this (DHCPv6),
which, however, is not employed in the dynamic assignment. One network card can
be used for different IPv6 addresses. The *Identifier* is a unique name for
individual addresses. The main address always uses the identifier ``default``;
functional identifiers such as ``Interface mail server`` can be assigned for all
other addresses.

UCR variables:

* :envvar:`interfaces/ethX/ipv6/address`
* :envvar:`interfaces/ethX/ipv6/prefix`,
* :envvar:`interfaces/ethX/ipv6/acceptRA` activates SLAAC

Further network settings can be performed under :guilabel:`Global network
settings`.

The IP addresses for the standard gateways in the subnetwork can be entered
under *Gateway (IPv4)* and *Gateway (IPv6)*. It is not obligatory to enter a
gateway for IPv6, but recommended. A gateway configured here has preference over
router advertisements, which might otherwise be able to change the route.

(UCR variables:

* :envvar:`gateway`
* :envvar:`ipv6/gateway`

)

.. _computers-configuring-the-name-servers:

Configuring the name servers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are two types of DNS servers:

External DNS Server
   An *External DNS Server* is employed for the resolution of host names and
   addresses outside of the UCS domain, e.g., ``univention.de``. This is
   typically a name server operated by the Internet provider.

Domain DNS Server
   A *Domain DNS Server* is a local name server in the UCS domain. This name
   server usually administrates host names and IP addresses belonging to the UCS
   domain. If an address is not found in the local inventory, an external DNS
   server is automatically requested. The DNS data are saved in the LDAP
   directory service, i.e., all domain DNS servers deliver identical data.

A local DNS server is set up on the |UCSPRIMARYDN|, |UCSBACKUPDN| and
|UCSREPLICADN| system roles. Here, you can configure which server should be
primarily used for the name resolution by entering the *Domain DNS
Server*.

UCR variables:

* :envvar:`nameserver1` to :envvar:`nameserver3`
* :envvar:`dns/forwarder1` to :envvar:`dns/forwarder3`,

.. _computers-network-complex:

Bridges, bonding, VLANs
^^^^^^^^^^^^^^^^^^^^^^^

UCS supports advanced network configurations using bridging, bonding and virtual
networks (VLAN):

* Bridging is often used with virtualization to connect multiple virtual
  machines running on a host through one shared physical network interface.

* Bondings allows failover redundancy for hosts with multiple physical network
  interfaces to the same network.

* VLANs can be used to separate network traffic logically while using only one
  (or more) physical network interface.

.. _computers-network-complex-bridge:

Configure bridging
^^^^^^^^^^^^^^^^^^

.. index::
   single: network; bridge
   single: network; switch
   pair: bridge; network

The most common application scenario for *bridging* is the shared use of a
physical network card by one or more virtual machines. Instead of one network
card for each virtual machine and the virtualization server itself, all systems
are connected via a shared uplink. A bridge can be compared with a switch
implemented in software which is used to connect the individual hosts together.
The hardware network adapter used is called a *bridge port*.

In order to configure a bridge, ``Bridge`` must be selected as the *Interface
type* under :guilabel:`Add`. The *Name of new bridge interface* can be selected
at will. Then click on :guilabel:`Next`.

The physical network card intended to act as the uplink can be selected under
*Bridge ports*. In the typical scenario of connecting virtual machines
via just one network card, there is no risk of a network loop. If the bridge is
used to connect two Ethernet networks, the spanning tree protocol (STP) is
employed to avoid network loops. The Linux kernel only implements STP, not the
Rapid STP or Multiple STP versions.

The *Forwarding delay* setting configures the waiting time in seconds during
which information is collected about the network topology when a connection is
being made via STP. If the bridge is used for connecting virtual machines to one
physical network card, STP should be disabled by setting the value to ``0``.
Otherwise problems may occur when using DHCP, as the packets sent during the
waiting time are not forwarded.

The *Additional bridge options* input field can be used to configure arbitrary
bridge parameters. This is only necessary in exceptional cases; an overview of
the possible settings can be found on the manual page
:manpage:`bridge-utils-interfaces(5)`.

Clicking on :guilabel:`Next` offers the possibility of optionally assigning the
bridge an IP address. This interface can then also be used as a network
interface for the virtualization host. The options are the same as described in
:ref:`computers-ipv4` and :ref:`computers-ipv6`.

.. _computers-network-complex-bonding:

Configure bonding
^^^^^^^^^^^^^^^^^

.. index::
   single: network; bonding
   single: network; link aggregation
   pair: bonding; network
   single: network; etherchannel
   single: network; teaming
   single: network; trunking


*Bonding* can be used to bundle two (or more) physical network cards in order to
increase the performance or improve redundancy in failover scenarios.

In order to configure a bonding, ``Bonding`` must be selected as the *Interface
type* under :guilabel:`Add`. The *Name of the bonding interface* can be selected
at will. Then click on :guilabel:`Next`.

The network cards which form part of the bonding interface are selected under
*Bond slaves*. The network cards which should be given preference in failover
scenarios (see below) can be selected via *Bond primary*.

The *Mode* configures the distribution of the network cards within the bonding:

* ``balance-rr (0)`` distributes the packets equally over the available network
  interfaces within the bonding one after the other. This increases performance
  and improves redundancy. In order to use this mode, the network switches used
  must support *link aggregation*.

* When ``active-backup (1)`` is used, only one network card is active for each
  bonding interface (by default this is the network interface configured in
  *Bond primary*). If the primary network card fails, this is detected by the
  Linux kernel, which switches to another card in the bonding. This version
  increases redundancy. It can be used with every network switch.

In addition, there are also a number of other bonding methods. These are
generally only relevant for special cases and are described under
:ref:`bonding`.

The Media Independent Interface (MII) of the network cards is used to detect
failed network adapters. The *MII link monitoring frequency* setting
specifies the testing interval in milliseconds.

All other bonding parameters can be configured under *Additional bonding
options*. This is only necessary in exceptional cases; an overview of the
possible settings can be found under :ref:`bonding`.

Clicking on :guilabel:`Next` allows to optionally assign the bonding interface
an IP address. If one of the existing network cards which form part of the
bonding interface has already been assigned an IP address, this configuration
will be removed. The options are the same as described in :ref:`computers-ipv4`
and :ref:`computers-ipv6`.

.. _computers-network-complex-vlan:

Configure VLAN
^^^^^^^^^^^^^^

.. index::
   pair: network; vlan
   single: network; 802.1q

VLANs can be used to separate the network traffic in a physical network
logically over one or more virtual subnetworks. Each of these virtual networks
is an independent broadcast domain. This makes it e.g. possible to differentiate
between a network for the employees and a guest network for visitors in a
company network although they use the same physical cables. The individual end
devices can be assigned to the VLANs via the configuration of the switches. The
network switches must support 802.1q VLANs.

A distinction is made between two types of connections between network cards:

* A connection only transports packets from a specific VLAN. In this case,
  untagged data packets are transmitted.

  This is typically the case if only one individual end device is connected via
  this network connection.

* A connection transports packets from several VLANs. This is also referred to
  as a trunk link. In this case, each packet is assigned to a VLAN using a VLAN
  ID. During transmission between trunk links and specific VLANs, the network
  switch takes over the task of filtering the packets by means of the VLAN IDs
  as well as adding and removing the VLAN IDs.

  This type of connection is primarily used between switches/servers.

  Some switches also allow the sending of packets with and without VLAN tags
  over a shared connection, but this is not described in more detail here.

When configuring a VLAN in the UMC module :guilabel:`Network settings` it is
possible to configure for a computer which VLANs it wants to participate in. An
example here would be an internal company web server, which should be available
both to the employees and any users of the guest network.

In order to configure a VLAN, ``Virtual LAN`` must be selected as the *Interface
type* under :guilabel:`Add`. The network interface for which the VLAN is
specified with *Parent interface*. The *VLAN ID* is the unique identifier of the
VLAN. Valid values are from 1 to 4095. Then :guilabel:`Next` must be clicked.

Clicking on :guilabel:`Next` allows to optionally assign the VLAN interface an
IP address. The options are the same as described in :ref:`computers-ipv4` and
:ref:`computers-ipv6`. When assigning an IP address, ensure that the address
matches the assigned VLAN address range.

.. _computers-configuring-proxy-access:

Proxy access configuration
--------------------------

The majority of the command line tools which access web servers (e.g.,
:command:`wget`, :command:`elinks` or :command:`curl`) check whether the
environment variable ``http_proxy`` is set. If this is the case, the proxy
server set in this variable is used automatically.

The |UCSUCRV| :envvar:`proxy/http` can also be used to activate the setting of
this environment variable via an entry in :file:`/etc/profile`.

The proxy URL must be specified for this, e.g., ``http://192.0.2.100``. The
proxy port can be specified in the proxy URL using a colon, e.g.,
``http://192.0.2.100:3128``. If the proxy requires authentication for the
accessing user, this can be provided in the form
:samp:`http://{username}:{password}@192.0.2.100``.

The environment variable is not adopted for sessions currently opened. A relogin
is required for the change to be activated.

The Univention tools for software updates also support operation via a proxy and
query the |UCSUCR| variable.

Individual domains can be excluded from use by the proxy by including them
separated by commas in the |UCSUCRV| :envvar:`proxy/no_proxy`. Subdomains are
taken into account; e.g. an exception for ``software-univention.de`` also
applies for ``updates.software-univention.de``.

.. _computers-mounting-nfs-shares:

Mounting NFS shares
-------------------

The *NFS mounts* policy of the UMC computer management can be used to
configure NFS shares, which are mounted on the system. There is a *NFS
share* for selection, which is mounted in the file path specified under
*Mount point*.

.. _nfs-mount:

.. figure:: /images/computers_policy_nfsshare.*
   :alt: Mounting a NFS share

   Mounting a NFS share

.. _computers-hardware-sysinfo:

Collection of list of supported hardware
----------------------------------------

Univention collects information about hardware which is compatible with UCS and
in use by customers. The information processed for this is gathered by the UMC
module :guilabel:`Hardware information`.

All files are forwarded to Univention anonymously and only transferred once
permission has been received from the user.

The start dialogue contains the entry fields *Manufacturer* and *Model*, which
must be completed with the values determined from the DMI information of the
hardware. The fields can also be adapted and an additional
*Descriptive comment* added.

If the hardware information is transferred as part of a support request, the
:guilabel:`This is related to a support case` option should be activated. A
ticket number can be entered in the next field; this facilitates assignment and
allows quicker processing.

Clicking on :guilabel:`Next` offers an overview of the transferred hardware
information. In addition, a compressed TAR archive is created, which contains a
list of the hardware components used in the system and can be downloaded via
:guilabel:`Archive with system information`.

Clicking on :guilabel:`Next` again allows you to select the way the data are
transferred to Univention. :guilabel:`Upload` transmits the data via HTTPS,
:guilabel:`Send mail)` opens a dialogue, which lists the needed steps to send
the archive via e-mail.

.. _computers-administration-of-local-system-configuration-with-univention-configuration-registry:

Administration of local system configuration with Univention Configuration Registry
===================================================================================

|UCSUCR| is the central tool for managing the local system configuration of a
UCS-based system. Direct editing of the configuration files is usually not
necessary.

Settings are specified in a consistent format in a registry mechanism, the
so-called *Univention Configuration Registry variables*. These variables are
used to generate the configuration files used effectively by the
services/programs from the configuration templates (the so-called *Univention
Configuration Registry templates*).

This procedure offers a range of advantages:

* It is not usually necessary to edit any configuration files manually.  This
  avoids errors arising from invalid syntax of configuration settings or
  similar.

* There is a uniform interface for editing the settings and the different
  syntax formats of the configuration files are hidden from the administrator.

* Settings are decoupled from the actual configuration file, i.e., if a
  software uses a different configuration format in a new version, a new
  template in a new format is simply delivered instead of performing
  time-consuming and error-prone conversion of the file.

* The variables used in a configuration file administrated with |UCSUCR| are
  registered internally. This ensures that when a UCR variable is changed, all
  the configuration files containing the changed variable are recreated.

|UCSUCR| variables can be configured in the command line using the
:command:`univention-config-registry` command (short form: :command:`ucr`) or via
the UMC module :guilabel:`Univention Configuration Registry`.

As the majority of packages perform their configuration via |UCSUCR| and the
corresponding basic settings need to be set up during the installation, hundreds
of |UCSUCR| variables are already set after the installation of a UCS system.

UCR variables can also be used efficiently in shell scripts for accessing
current system settings.

The variables are named according to a tree structure with a forward slash being
used to separate components of the name. For example, |UCSUCR| variables
beginning with ``ldap`` are settings which apply to the local directory service.

A description is given for the majority of variables explaining their use.

If a configuration file is administrated by a UCR template and the required
setting has not already been covered by an existing variable, the UCR template
should be edited instead of the configuration file. If the configuration were
directly adapted, the next time the file is regenerated - e.g., when a
registered UCR variable is set - the local modification will be overwritten
again. Adaptation of UCR templates is described in :ref:`ucr-templates-extend`.

Part of the settings configured in |UCSUCR| are system-specific (e.g., the
computer name); many settings can, however, be used on more then one computer.
The |UCSUCR| policy in the domain administration UMC modules can be used to
compile variables and apply them on more than one computer.

The evaluation of the |UCSUCR| variables on a UCS system comprises four stages:

* First the local |UCSUCR| variables are evaluated.

* The local variables are overruled by policy variables which are usually
  sourced from the directory service

* The :option:`--schedule` option is used to set local variables which are only
  intended to apply for a certain period of time. This level of the |UCSUCR| is
  reserved for local settings which are automated by time-controlled mechanisms
  in |UCSUCS|.

* When the :option:`--force` option is used in setting a local variable,
  settings adopted from the directory service and variables from the schedule
  level are overruled and the given value for the local system fixed instead. An
  example:

  .. code-block:: console

     $ univention-config-registry set --force mail/messagesizelimit=1000000


If a variable is set which is overwritten by a superordinate policy, a warning
message is given.

The use of the |UCSUCR| policy is documented in the :ref:`ucr-templates-policy`.

.. _computers-using-the-univention-management-console-web-interface:

Using the |UCSUMC| module
-------------------------

The UMC module :guilabel:`Univention Configuration Registry` can be used to
display and adjust the variables of a system. There is also the possibility of
setting new variables using :guilabel:`Add new variable`.

A search mask is displayed on the start page. All variables are classified using
a *Category*, for example all LDAP-specific settings.

The *Search attribute* can be entered as a filter in the search mask, which can
refer to the variable name, value or description.

Following a successful search, the variables found are displayed in a table with
the variable name and the value. A detailed description of the variable is
displayed when moving the mouse cursor over the variable name.

A variable can be edited by clicking on its name. A variable can be deleted by
right-clicking and selecting :guilabel:`Delete`.

.. _computers-using-the-command-line-front-end:

Using the command line front end
--------------------------------

The command line interface of |UCSUCR| is run using the
:command:`univention-config-registry` command. Alternatively, the short form
:command:`ucr` can be used.

.. _computers-querying-a-ucr-variable:

Querying a UCR variable
^^^^^^^^^^^^^^^^^^^^^^^

A single |UCSUCR| variable can be queried with the parameter
:option:`get`:

.. code-block:: console

   $ univention-config-registry get ldap/server/ip


The parameter :option:`dump` can also be used to display all currently set
variables:

.. code-block:: console

   $ univention-config-registry dump


.. _computers-setting-ucr-variables:

Setting UCR variables
^^^^^^^^^^^^^^^^^^^^^

The parameter :option:`set` is used to set a variable. The variable can be given
any name consisting exclusively of letters, full stops, figures, hyphens and
forward slashes.

.. code-block:: console

   $ univention-config-registry set VARIABLENAME=VALUE


If the variable already exists, the content is updated; otherwise, a new entry
is created.

The syntax is not checked when a |UCSUCR| variable is set. The change to a
variable results in all configuration files for which the variable is registered
being rewritten immediately. The files in question are output on the console.

In doing so it must be noted that although the configuration of a service is
updated, the service in question is not restarted automatically! The restart
must be performed manually.

It is also possible to perform simultaneous changes to several variables in one
command line. If these refer to the same configuration file, the file is only
rewritten once.

.. code-block:: console

   $ univention-config-registry set \
   > dns/forwarder1=192.0.2.2 \
   > sshd/xforwarding="no" \
   > sshd/port=2222

A conditional setting is also possible. For example, if a value should only be
saved in a |UCSUCR| variable when the variable does not yet exist, this can be
done by entering a question mark (``?``) instead of the equals sign ( ``=``)
when assigning values.

.. code-block:: console

   $ univention-config-registry set dns/forwarder1?192.0.2.2


.. _computers-searching-for-variables-and-set-values:

Searching for variables and set values
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The parameter :option:`search` can be used to search for a variable. This
command searches for variable names which contain ``nscd`` and displays these
with their current assignments:

.. code-block:: console

   $ univention-config-registry search nscd


Alternatively, searches can also be performed for set variable values. This
request searches for all variables set to ``primary.example.com``:

.. code-block:: console

   $ univention-config-registry search --value primary.example.com


Search templates in the form of regular expressions can also be used in
the search. The complete format is documented at
https://docs.python.org/2/library/re.html.

.. _computers-deleting-ucr-variables:

Deleting UCR variables
^^^^^^^^^^^^^^^^^^^^^^

The parameter :option:`unset` is used to delete a variable. The following
example deletes the variable :envvar:`dns/forwarder2`. It is also possible here
to specify several variables to be deleted:

.. code-block:: console

   $ univention-config-registry unset dns/forwarder2


.. _computers-regeneration-of-configuration-files-from-their-template:

Regeneration of configuration files from their template
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The parameter :option:`commit` is used to regenerate a configuration file from
its template. The name of the configuration file is entered as a parameter,
e.g.:

.. code-block:: console

   $ univention-config-registry commit /etc/samba/smb.conf


As UCR templates are generally regenerated automatically when UCR variables are
edited, this is primarily used for tests.

If no file name is given when running :command:`ucr commit`, all of the files
managed by |UCSUCR| will be regenerated from the templates. It is, however, not
generally necessary to regenerate all the configuration files.

.. _computers-sourcing-variables-in-shell-scripts:

Sourcing variables in shell scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The parameter :option:`shell` is used to display |UCSUCR| variables and their
current assignments in a format that can be used in shell scripts.

.. code-block:: console

   $ univention-config-registry shell ldap/server/name


Different conversions are involved in this: forward slashes in variable names
are replaced with underscores and characters in the values which have a
particular significance in shell scripts are included in quotation marks to
ensure they are not altered.

The |UCSUCR| output must be executed via the command :command:`eval` for
|UCSUCR| variables to be able to be read in a shell script as environment
variables:

.. code-block:: console

   # eval "$(univention-config-registry shell ldap/server/name)"
   # echo "$ldap_server_name"
   primary.firma.de


.. _ucr-templates-policy:

Policy-based configuration of UCR variables
-------------------------------------------

Part of the settings configured in |UCSUCR| are system-specific (e.g., the
computer name); many settings can, however, be used on more then one computer.
The *Univention Configuration Registry* policy managed in the UMC module
:guilabel:`Policies` can be used to compile variables and apply them on more
than one computer.

.. _policy-apache-settings:

.. figure:: /images/computers_policy_apache_settings.*
   :alt: Policy-based configuration of the Apache start page and forced HTTPS

   Policy-based configuration of the Apache start page and forced HTTPS

Firstly, a *Name* must be set for the policy which is to be created, under which
the variables will later be assigned to the individual computer objects.

In addition, at least one *Variable* must be configured and a *Value* assigned.

This policy can then be assigned to a computer object or a container or OU
(see :ref:`central-policies-assign`). Note that the evaluation of
configured values differs from other policies: The values are not
forwarded directly to the computer, but rather written on the assigned
computer by Univention Directory Policy. The time interval used for this
is configured by the |UCSUCRV| :envvar:`ldap/policy/cron` and is
set to hourly as standard.

.. _ucr-templates-extend:

Modifying UCR templates
-----------------------

In the simplest case, a |UCSUCR| template is a copy of the original
configuration file in which the points at which the value of a variable
are to be used contain a reference to the variable name.

Inline Python code can also be integrated for more complicated
scenarios, which then also allows more complicated constructions such as
conditional assignments.

.. note::

   |UCSUCR| templates are included in the corresponding software packages
   as configuration files. When packages are updated, a check is
   performed for whether any changes have been made to the configuration
   files.

   If configuration files are no longer there in the form in which they were
   delivered, they will not be overwritten. Instead a new version will be
   created in the same directory with the ending :file:`.debian.dpkg-new`.

   If changes are to be made on the |UCSUCR| templates, these templates are also
   not overwritten during the update and are instead re-saved in the same
   directory with the ending :file:`.dpkg-new` or :file:`.dpkg-dist`.
   Corresponding notes are written in the
   :file:`/var/log/univention/actualise.log` log file. This only occurs if UCR
   templates have been locally modified.

The UCR templates are stored in the :file:`/etc/univention/templates/files/`
directory.  The path to the templates is the absolute path to the configuration
file with the prefixed path to the template directory. For example, the template
for the :file:`/etc/issue` configuration file can be found under
:file:`/etc/univention/templates/files/etc/issue`.

For the configuration files to be processed correctly by |UCSUCR| they must be
in UNIX format. If configuration files are edited in DOS or Windows, for
example, control characters are inserted to indicate line breaks, which can
disrupt the way |UCSUCR| uses the file.

.. _ucr-templates-extend-simple:

Referencing of UCR variables in templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the simplest case, a UCR variable can be directly referenced in the template.
The variable name framed by the string ``@%@`` represents the wildcard. As an
example the option for the activation of X11 forwarding in the configuration
file :file:`/etc/ssh/sshd_config` of the OpenSSH server:

.. code-block::

   X11Forwarding @%@sshd/xforwarding@%@

Newly added references to UCR variables are automatically evaluated by
templates; additional registration is only required with the use of inline
Python code (see :ref:`ucr-templates-extend-python`).

.. _ucr-templates-extend-python:

Integration of inline Python code in templates
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Any type of Python code can be embedded in UCR templates by entering a code
block framed by the string ``@!@``. For example, these blocks can be used to
realize conditional requests so that when a parameter is changed via a variable,
further dependent settings are automatically adopted in the configuration file.
The following code sequence configures for example network settings using the
|UCSUCR| settings:

.. code-block::

   @!@
   if configRegistry.get('apache2/ssl/certificate'):
       print('SSLCertificateFile %s' %
           configRegistry['apache2/ssl/certificate'])
   @!@


All the data output with the print function are written in the generated
configuration file. The data saved in |UCSUCR| can be requested via the
``ConfigRegistry`` object, e.g.:

.. code-block::

   @!@
   if configRegistry.get('version/version') and \
           configRegistry.get('version/patchlevel'):
       print('UCS %(version/version)s-%(version/patchlevel)s' %
           configRegistry)
   @!@


In contrast to directly referenced UCR variables (see
:ref:`ucr-templates-extend-simple`), variables accessed in inline Python code
must be explicitly registered.

The |UCSUCR| variables used in the configuration files are registered in *info*
files in the :file:`/etc/univention/templates/info/` directory which are usually
named after the package name with the file ending :file:`.info`. If new Python
code is entered into the templates or the existing code changed in such a way
that it requires additional or different variables, one of the existing
:file:`.info` files will need to be modified or a new one added.

Following the changing of :file:`.info` files, the :command:`ucr update` command
must be run.

.. _computers-basic-system-services:

Basic system services
=====================

This chapter describes basic system services of a UCS Installation such
as the configuration of the PAM authentication framework, system logs
and the NSCD.

.. _computers-rootaccount:

Administrative access with the root account
-------------------------------------------

There is a ``root`` account on every UCS system for complete administrative
access. The password is set during installation of the system. The root user
**is not** stored in the LDAP directory, but instead in the local user accounts.

The password for the root user can be changed via the command line by using the
:command:`passwd` command. It must be pointed out that this process does not
include any checks regarding either the length of the password or the passwords
used in the past.

.. _computers-configuration-of-language-and-keyboard-settings:

Configuration of language and keyboard settings
-----------------------------------------------

In Linux, localization properties for software are defined in so-called
*locales*. Configuration includes, among other things, settings for date and
currency format, the set of characters in use and the language used for
internationalized programs. The installed locales can be changed in the UMC
module :guilabel:`Language settings` under :menuselection:`Language settings -->
Installed system locales`. The standard locale is set under *Default system
locale*.

.. _language-settings:

.. figure:: /images/computers_timezone.*
   :alt: Configuring the language settings

   Configuring the language settings

The *Keyboard layout* in the menu entry *Time zone and keyboard settings* is
applied during local logins to the system.

.. _computers-systemservices:

Starting/stopping system services / configuration of automatic startup
----------------------------------------------------------------------

The UMC module :guilabel:`System services` can be used to check the current
status of a system service and to start or stop it as required.

.. _umc-services:

.. figure:: /images/umc-systemservices.*
   :alt: Overview of system services

   Overview of system services

In this list of all the services installed on the system, the current running
runtime status and a *Description* are displayed under *Status*. The service can
be started, stopped or restarted under :guilabel:`more`.

By default every service is started automatically when the system is started. In
some situations, it can be useful not to have the service start directly, but
instead only after further configuration. The action *Start manually* is used so
that the service is not started automatically when the system is started, but
can still be started subsequently. The action *Start never* also prevents
subsequent service starts.

.. _computers-authentication-pam:

Authentication / PAM
--------------------

Authentication services in Univention Corporate Server are realized via
*Pluggable Authentication Modules* (PAM). To this
end different login procedures are displayed on a common interface so
that a new login method does not require adaptation for existing
applications.

.. _computers-limiting-authentication-to-selected-users:

Limiting authentication to selected users
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default only the ``root`` user and members of the ``Domain Admins`` group can
login remotely via SSH and locally on a ``tty``.

This restriction can be configured with the |UCSUCRV|
:samp:`auth/{SERVICE}/restrict`. Access to this service can be authorized by
setting the variables :samp:`auth/{SERVICE}/user/{USERNAME}` and
:samp:`auth/{SERVICE}/group/{GROUPNAME}` to ``yes``.

Login restrictions are supported for *SSH* (``sshd``), login on a *tty*
(``login``), *rlogin* (``rlogin``), *PPP* (``ppp``) and other services
(``other``). An example for *SSH*:

.. code-block::

   auth/sshd/group/Administrators: yes
   auth/sshd/group/Computers: yes
   auth/sshd/group/DC Backup Hosts: yes
   auth/sshd/group/DC Slave Hosts: yes
   auth/sshd/group/Domain Admins: yes
   auth/sshd/restrict: yes


.. _computers-configure-ldap-server:

Configuration of the LDAP server in use
---------------------------------------

Several LDAP servers can be operated in a UCS domain. The primary one used is
specified with the |UCSUCRV| :envvar:`ldap/server/name`, further servers can be
specified via the |UCSUCRV| :envvar:`ldap/server/addition`.

Alternatively, the LDAP servers can also be specified via a *LDAP server*
policy. The order of the servers determines the order of the computer's requests
to the server if a LDAP server cannot be reached.

By default only :envvar:`ldap/server/name` is set following the installation or
the domain join. If there is more than one LDAP server available, it is
advisable to assign at least two LDAP servers using the *LDAP server* policy in
order to improve redundancy. In cases of an environment distributed over
several locations, preference should be given to LDAP servers from the local
network.

.. _computers-configureprintserver:

Configuration of the print server in use
----------------------------------------

The print server to be used can be specified with the |UCSUCRV|
:envvar:`cups/server`.

Alternatively, the server can also be specified via the *Print server* policy in
the UMC module :guilabel:`Computers`.

.. _computers-logging-retrieval-of-system-messages-and-system-status:

Logging/retrieval of system messages and system status
------------------------------------------------------

.. _computers-log-files:

Log files
^^^^^^^^^

All UCS-specific log files (e.g., for the listener/notifier replication) are
stored in the :file:`/var/log/univention/` directory. Services log in their own
standard log files: for example, Apache to the file
:file:`/var/log/apache2/error.log`.

The log files are managed by :program:`logrotate`. It ensures that log files are
named in series in intervals (can be configured in weeks using the |UCSUCRV|
:envvar:`log/rotate/weeks`, with the default setting being 12) and older log
files are then deleted. For example, the current log file for the |UCSUDL| is
found in the :file:`listener.log` file; the one for the previous week in
:file:`listener.log.1`, etc.

Alternatively, log files can also be rotated only once they have reached a
certain size. For example, if they are only to be rotated once they reach a size
of 50 MB, the |UCSUCRV| :envvar:`logrotate/rotates` can be set to ``size 50M``.

The |UCSUCRV| :envvar:`logrotate/compress` is used to configure whether the
older log files are additionally zipped with :command:`gzip`.

.. _computers-logging-the-system-status:

Logging the system status
^^^^^^^^^^^^^^^^^^^^^^^^^

:command:`univention-system-stats` can be used to document the current system
status in the :file:`/var/log/univention/system-stats.log` file. The following
values are logged:

* The free disk space on the system partitions (:command:`df
  -lhT`)

* The current process list (:command:`ps auxf`)

* Two :command:`top` lists of the current processes and
  system load (:command:`top -b -n2`)

* The current free system memory (:command:`free`)

* The time elapsed since the system was started
  (:command:`uptime`)

* Temperature, fan and voltage indexes from
  :program:`lm-sensors`
  (:command:`sensors`)

* A list of the current Samba connections
  (:command:`smbstatus`)

The runtimes in which the system status should be logged can be defined in Cron
syntax via the |UCSUCRV| :envvar:`system/stats/cron`, e.g., ``0,30 \* \* \* \*``
for logging every half and full hour. The logging is activated by setting the
|UCSUCRV| :envvar:`system/stats` to ``yes``. This is the default since UCS 3.0.

.. _computers-modules-top:

Process overview via |UCSUMC| module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The UMC module :guilabel:`Process overview` displays a table of the current
processes on the system. The processes can be sorted based on the following
properties by clicking on the corresponding table header:

* CPU utilization in percent

* The user name under which the process is running

* Memory consumption in percent

* The process ID

The menu item *more* can be used to terminate processes. Two different types of
termination are possible:

Terminate
   The action :guilabel:`Terminate` sends the process a ``SIGTERM`` signal; this
   is the standard method for the controlled termination of programs.

Force terminate
   Sometimes, it may be the case that a program - e.g., after crashing - can no
   longer be terminated with this procedure. In this case, the action
   :guilabel:`Force terminate` can be used to send the signal ``SIGKILL`` and
   force the process to terminate.

As a general rule, terminating the program with ``SIGTERM`` is preferable as
many programs then stop the program in a controlled manner and, for example,
save open files.

.. _computers-modules-diagnostic:

System diagnostic via |UCSUMC| module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The UMC module :guilabel:`System diagnostic` offers a corresponding user
interface to analyze a UCS system for a range of known problems.

The module evaluates a range of problem scenarios known to it and suggests
solutions if it is able to resolve the identified solutions automatically. This
function is displayed via ancillary buttons. In addition, links are shown to
further articles and corresponding UMC modules.

.. _computers-executing-recurring-actions-with-cron:

Executing recurring actions with Cron
-------------------------------------

Regularly recurring actions (e.g., the processing of log files) can be
started at a defined time with the Cron service. Such an action is known
as a cron job.

.. _computers-hourly-daily-weekly-monthly-execution-of-scripts:

Hourly/daily/weekly/monthly execution of scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Four directories are predefined on every UCS system, :file:`/etc/cron.hourly/`,
:file:`/etc/cron.daily/`, :file:`/etc/cron.weekly/` and
:file:`/etc/cron.monthly/`. Shell scripts which are placed in these directories
and marked as executable are run automatically every hour, day, week or month.

.. _cron-local:

Defining local cron jobs in :file:`/etc/cron.d/`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. index:: cron; syntax
   :name: cron-syntax

A cron job is defined in a line, which is composed of a total of seven columns:

* Minute (0-59)

* Hour (0-23)

* Day (1-31)

* Month (1-12)

* Weekday (0-7) (0 and 7 both stand for Sunday)

* Name of user executing the job (e.g., root)

* The command to be run

The time specifications can be set in different ways. One can specify a specific
minute/hour/etc. or run an action every minute/hour/etc. with a ``*``. Intervals
can also be defined, for example ``*/2`` as a minute specification runs an
action every two minutes.

Example:

.. code-block::

   30 * * * * root /usr/sbin/jitter 600 /usr/share/univention-samba/slave-sync


.. _computers-defining-cron-jobs-in-univention-configuration-registry:

Defining cron jobs in Univention Configuration Registry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cron jobs can also be defined in |UCSUCR|. This is particularly useful if
they are set via a |UCSUDM| policy and are thus used on more than one
computer.

Each cron job is composed of at least two |UCSUCR| variables.
:samp:`{JOBNAME}` is a general description.

* :samp:`cron/{JOBNAME}/command` specifies the command to be run (required)

* :samp:`cron/{JOBNAME}/time` specifies the execution time (see
  :ref:`cron-local`) (required)

* As standard, the cron job is run as a user ``root``.
  :samp:`cron/{JOBNAME}/user` can be used to specify a different user.

* If an e-mail address is specified under :samp:`cron/{JOBNAME}/mailto`, the
  output of the cron job is sent there per e-mail.

* :samp:`cron/{JOBNAME}/description` can be used to provide a description.

.. _computers-nscd:

Name service cache daemon
-------------------------

Data of the NSS service is cached by the *Name Server Cache Daemon* (NSCD) in
order to speed up frequently recurring requests for unchanged data. Thus, if a
repeated request occurs, instead of a complete LDAP request to be processed, the
data are simply drawn directly from the cache.

Since UCS 3.1, the groups are no longer cached via the NSCD for performance and
stability reasons; instead they are now cached by a local group cache, see
:ref:`groups-cache`.

The central configuration file of the (:file:`/etc/nscd.conf`) is managed by
|UCSUCR|.

The access to the cache is handled via a hash table. The size of the hash table
can be specified in |UCSUCR|, and should be higher than the number of
simultaneously used users/hosts. For technical reasons, a prime number should be
used for the size of the table. The following table shows the standard values of
the variables:

.. list-table:: Default size of the hash table
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Default size of the hash table

   * - ``nscd /hosts/size``
     -  ``6007``

   * - ``nscd/passwd/size``
     - ``6007``

With very big caches it may be necessary to increase the size of the cache
database in the system memory. This can be configured through the |UCSUCR|
variables :envvar:`nscd/hosts/maxdbsize`, :envvar:`nscd/group/maxdbsize` and
:envvar:`nscd/passwd/maxdbsize`.

As standard, five threads are started by NSCD. In environments with many
accesses it may prove necessary to increase the number via the |UCSUCRV|
:envvar:`nscd/threads`.

In the basic setting, a resolved group or host name is kept in cache for one
hour, a user name for ten minutes. With the |UCSUCR| variables
:envvar:`nscd/group/positive_time_to_live` and
:envvar:`nscd/passwd/positive_time_to_live` these periods can be extended or
diminished (in seconds).

From time to time it might be necessary to manually invalidate the cache of the
NSCD. This can be done individually for each cache table with the following
commands:

.. code-block:: console

   $ nscd -i passwd
   $ nscd -i hosts


The verbosity of the log messages can be configured through the |UCSUCRV|
:envvar:`nscd/debug/level`.

.. _computers-ssh-login-to-systems:

SSH login to systems
--------------------

When installing a UCS system, an SSH server is also installed per preselection.
SSH is used for realizing encrypted connections to other hosts, wherein the
identity of a host can be assured via a check sum.  Essential aspects of the SSH
server's configuration can be adjusted in |UCSUCR|.

By default the login of the privileged ``root`` user is permitted by SSH (e.g.
for configuring a newly installed system where no users have been created yet,
from a remote location).

* If the |UCSUCRV| :envvar:`sshd/permitroot` is set to ``without-password``,
  then no interactive password request will be performed for the ``root`` user,
  but only a login based on a public key. By this means brute force attacks to
  passwords can be avoided.

* To prohibit SSH login completely, this can be deactivated by setting the
  |UCSUCRV| :envvar:`auth/sshd/user/root` to ``no``.

The |UCSUCRV| :envvar:`sshd/xforwarding` can be used to configure
whether an X11 output should be passed on via SSH. This is necessary,
for example, for allowing a user to start a program with graphic output
on a remote computer by logging in with :command:`ssh -X
TARGETHOST`. Valid settings are ``yes`` and
``no``.

The standard port for SSH connections is port 22 via TCP. If a different
port is to be used, this can be arranged via the |UCSUCRV|
:envvar:`sshd/port`.

.. _basicservices-ntp:

Configuring the time zone / time synchronization
------------------------------------------------

The time zone in which a system is located can be changed in the UMC module
:guilabel:`Language settings` under :menuselection:`Time zone and keyboard
settings --> Time zone`.

Asynchronous system times between individual hosts of a domain can be the source
of a large number of errors, for example:

* The reliability of log files is impaired.

* Kerberos operation is disrupted.

* The correct evaluation of the validity periods of passwords can be disturbed

Usually the |UCSPRIMARYDN| functions as the time server of a domain. With the
|UCSUCR| variables :envvar:`timeserver`, :envvar:`timeserver2` and
:envvar:`timeserver3` external NTP servers can be included as time sources.

Manual time synchronization can be started by the command :command:`ntpdate`.

Windows clients joined in a Samba/AD domain only accept signed NTP time
requests. If the |UCSUCRV| :envvar:`ntp/signed` is set to ``yes``, the NTP
replies are signed by Samba/AD.
