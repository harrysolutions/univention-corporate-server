.. _windows-services-for-windows:

Services for Windows
********************

.. _windows-general:

Introduction
============

UCS can offer Active Directory (AD) services, be a member of an Active
Directory domain or synchronize objects between Active Directory domains
and a UCS domain.

For the purposes of Windows systems, UCS can assume the tasks of Windows
server systems:

-  Domain controller function / authentication services

-  File services

-  Print services

In UCS all these services are provided by Samba.

UCS supports the mostly automatic migration of an existing Active
Directory domain to UCS. All users, groups, computer objects and group
policies are migrated without the need to rejoin the Windows clients.
This is documented in :ref:`windows-adtakeover`.

Microsoft Active Directory domain controllers cannot join the Samba
domain. This functionality is planned at a later point in time.

Samba can not join an Active Directory Forest yet at this point.

Incoming trust relationships with other Active Directory domains are
configurable. In this setup the external Active Directory domain trusts
authentication decisions of the UCS domain (Windows trusts UCS) so that
UCS users can log on to systems and Active Directory backed services in
the Windows domain (see :ref:`windows-trust`).
Outgoing trusts with Active Directory domain (UCS trusts Windows) are
not supported currently.

.. _windows-addomain:

Operation of a Samba domain based on Active Directory
=====================================================

.. _windows-setup4:

Installation
------------

Samba as an AD domain controller can be installed on all UCS Directory
Nodes from the Univention App Center with the application
*Active Directory-compatible domain controller*.
Alternatively, the software package
:program:`univention-samba4` can be installed. On the system
roles |UCSPRIMARYDN| and |UCSBACKUPDN| the
:program:`univention-s4-connector` package must also be
installed (:command:`univention-run-join-scripts` command
must be run after installation). Additional information can be found in
:ref:`computers-softwaremanagement-installsoftware`.

A Samba member server can be installed on UCS Managed Nodes from the
Univention App Center with the application
:program:`Windows-compatible Fileserver`.
Alternatively, the software package
:program:`univention-samba` can be installed
(:command:`univention-run-join-scripts` command must be run
after installation). Additional information can be found in
:ref:`computers-softwaremanagement-installsoftware`.

Samba supports the operation as a *read-only domain controller*. The setup is
documented in `Extended Windows integration documentation
<https://docs.software-univention.de/windows-5.0.html>`_.

.. _windows-samba4-services:

Services of a Samba domain
--------------------------

.. _windows-samba4-services-auth:

Authentication services
^^^^^^^^^^^^^^^^^^^^^^^

User logins can only be performed on Microsoft Windows systems joined in
the Samba domain. Domain joins are documented in
:ref:`windows-domain-join`.

Users who log on to a Windows system are supplied with a Kerberos ticket
when they log on. The ticket is then used for the further
authentication. This ticket allows access to the domain's resources.

Common sources of error in failed logins are:

-  Synchronization of the system times between the Windows client and
   domain controller is essential for functioning Kerberos
   authentication. By default the system time is updated via NTP during
   system startup. This can also be done manually using the command
   :command:`w32tm /resync`.

-  DNS service records need to be resolved during login. For this
   reason, the Windows client should use the domain controller's IP
   address as its DNS name server.

.. _windows-samba4-fileservices:

File services
^^^^^^^^^^^^^

A file server provides files over the network and allows concentrating
the storage of user data on a central server.

The file services integrated in UCS support the provision of shares
using the CIFS protocol (see :ref:`shares-general`). Insofar as the
underlying file system supports Access Control Lists (ACLs) (can be used with
``ext4`` and ``XFS``), the ACLs can also be used by Windows clients.

Samba Active Directory domain controllers, i.e. UCS Directory Nodes, can
also provide file services. As a general rule, it is recommended to
separate domain controllers and file/print services in Samba
environments - following the Microsoft recommendations for Active
Directory - that means using UCS Directory Nodes for
logins/authentication and UCS Managed Nodes for file/print services.
This ensures that a high system load on a file server does not result in
disruptions to the authentication service. For smaller environments in
which it is not possible to run two servers, file and print services can
also be run on a UCS Directory Node.

Samba supports the *CIFS* protocol and the successor *SMB2* to provide file
services. Using a client which supports *SMB2* (as of :program:`Windows Vista`,
i.e., :program:`Windows 7/8` too) improves the performance and scalability.

The protocol can be configured using the |UCSUCR| variable
:envvar:`samba/max/protocol`. It must be set on all Samba
servers and then all Samba server(s) restarted.

-  ``NT1`` configures *CIFS* (supported by all Windows versions)

-  ``SMB2`` *SMB2* (supported as of :program:`Windows Vista` / :program:`Windows 7`)

-  ``SMB3`` configures *SMB3* (supported as of :program:`Windows 8`)

.. _windows-samba4-services-print:

Print services
^^^^^^^^^^^^^^

Samba offers the possibility of sharing printers set up under Linux as
network printers for Windows clients. The management of the printer
shares and the provision of the printer drivers is described in
:ref:`print-general`.

Samba AD domain controllers can also provide print services. In this
case, the restrictions described in :ref:`windows-samba4-fileservices` must be taken into
consideration.

.. _windows-s4connector:

Univention S4 connector
^^^^^^^^^^^^^^^^^^^^^^^

When using Samba as an Active Directory domain controller, Samba
provides a separate LDAP directory service. The synchronization between
the UCS LDAP and the Samba LDAP occurs via an internal system service,
the Univention S4 connector. The connector is enabled on the
|UCSPRIMARYDN| by default and typically requires no further configuration.

Further information on the status of the synchronization can be found in
the log file
:file:`/var/log/univention/connector-s4.log`. Additional
information on analyzing connector replication problems can be found in
:uv:kb:`Samba 4 Troubleshooting <32>`.

The :command:`univention-s4search` command can be used to
search in the Samba directory service. If it is run as the
``root`` user, the required
credentials of the machine account are used automatically:

::

   root@primary:~# univention-s4search sAMAccountName=Administrator
   # record 1
   dn: CN=Administrator,CN=Users,DC=example,DC=com
   objectClass: top
   objectClass: person
   objectClass: organizationalPerson
   objectClass: user
   cn: Administrator
   instanceType: 4
   (..)


.. _windows-multimaster:

Replication of directory data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Samba/AD domains use the Directory Replication System (DRS) to replicate
the directory data. DRS allows multi-master replication, i.e., the write
changes from multiple domain controllers are synchronized at protocol
level. Consequently, the use of snapshots in virtualization solutions
should be avoided when using Samba/AD and Samba/AD should be operated on
a server which is never switched off.

The complexity of the multi-master replication increases with each
additional Samba/AD domain controller. Consequently, it must be checked
whether additional Samba/AD domain controllers provided by UCS Directory
Nodes are necessary or if a UCS Managed Node would not be a better
choice for new servers.

Additional information on troubleshooting replication problems can be
found in :uv:kb:`Samba 4 Troubleshooting <32>`.

.. _windows-sysvolshare:

Synchronization of the SYSVOL share
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The SYSVOL share is a share which provides group policies and logon
scripts in Active Directory/Samba. It is synchronized among all domain
controllers and stored in the :file:`/var/lib/samba/sysvol/` directory.

In Microsoft Active Directory, the SYSVOL share is synchronized by the
File Replication Service (introduced with Windows 2000) or the
Distributed File System (as of :program:`Windows 2008 R2`). These replication methods are not yet fully
implemented in Samba/AD. The synchronization between the Samba/AD domain
controllers is performed in UCS via a Cron job (every five minutes as
standard - can be configured using the |UCSUCRV|
:envvar:`samba4/sysvol/sync/cron`).

.. _windows-samba4-desktopmanagement:

Configuration and management of Windows desktops
------------------------------------------------

.. _gruppenrichtlinien:

Group policies
^^^^^^^^^^^^^^

.. _gpo-intro:

Introduction
''''''''''''

Group policies are an Active Directory feature which allows the central
configuration of settings for computers and users. Group policies are
also supported by Samba/AD domains. The policies only apply to Windows
clients; Linux or Mac OS systems cannot evaluate the policies.

Group policies are often referred to as GPOs (*group policy
objects*). Put more precisely, a GPO can contain a series of
policies. Despite their name, group policy objects cannot be assigned
directly to certain user groups, but instead are linked with certain AD
administration units (domains, sites or organizational units) in the
Samba directory service (Samba AD/DS) and thus refer to subordinate
objects. A group-specific or user-specific evaluation is only indirectly
possible via the *Security Filtering* of a group
policy object, in which the *Apply group policy
Allow/Deny* privilege can be directly restricted to certain
groups, users or computers.

As a basic rule, a distinction must be made between *group
policies* (GPOs) and the similarly named *group
policy preferences (GPPs)*:

-  The settings made via *GPOs* are binding,
   whereas *GPPs* are merely used to enter
   preferences in the registry of Windows clients, which can still be
   overwritten on the client in certain circumstances.

-  The settings made via *GPOs* are also
   dynamically applied to the target objects, whereas, in contrast, the
   settings made via *GPPs* are entered statically
   in the registry of Windows clients (this is also referred to as
   *tattooing*).

For these reasons, *GPOs* are preferable to
*GPPs* in the majority of cases. This remainder of
this section deals exclusively with *GPOs*.

In contrast to UCS policies (see :ref:`central-policies`), group
policies are not configured via UMC modules, but instead are configured
in a separate editor, the *Group Policy
Management* editor, which is a component of the
*Remote Server Administration Tools (RSAT)*. The
installation is described in :ref:`gpo-install`.

There are two types of policies:

-  *User policies* configure a user's settings,
   e.g., the configuration of the desktop. It is also possible to
   configure applications via group policies (e.g., the start page of a
   browser or settings in LibreOffice).

-  *Computer policies* define a Windows client's
   settings.

Computer policies are evaluated for the first time the computer starts
up; user policies during login. The policies are also continually
evaluated for logged in users / running systems and updated (every
90-120 minutes by default. The period varies at random to avoid peak
loads.)

The command :command:`gpupdate /force` can also be run
specifically to start the evaluation of group policies.

Some policies - e.g., for the installation of software or for login
scripts - are only evaluated during login (user policies) or system
startup (computer policies).

The majority of group policies only set one value in the Windows
registry, which is then evaluated by Windows or an application. As
standard users cannot modify any settings in the corresponding section
of the Windows registry, it is also possible to configure restricted
user desktops in which, for example, users cannot open the Windows Task
Manager.

The group policies are stored in the SYSVOL share, see :ref:`windows-sysvolshare`. They are linked with user
and host accounts in the Samba directory service.

.. _gpo-install:

Installation of Group Policy Management
'''''''''''''''''''''''''''''''''''''''

Group Policy Management can be installed as a component of the
*Remote Server Administration Tools* on Windows
clients. They can be found at `Remote Server Administration Tools (RSAT)
for Windows
10 <https://www.microsoft.com/en-us/download/details.aspx?id=45520>`__
for Windows 10.

.. _windows-gpo-activate:

.. figure:: /images/gpo-activate.*

Following the installation, Group Policy Management must still be
enabled in the Windows Control Panel. This is done by enabling the
:guilabel:`Group Policy Management Tools` option under
:menuselection:`Start --> Control Panel --> Programs --> Turn Windows features
on or off --> Remote Server Administration Tools --> Feature
Administration Tools`.

Following the enabling, Group Policy Management can be run under
:menuselection:`Start --> Administrative Tools --> Group Policy Management`.

.. _gpo-config:

Configuration of policies with Group Policy Management
''''''''''''''''''''''''''''''''''''''''''''''''''''''

Group policies can only be configured by users who are members of the ``Domain
Admins`` group (e.g., the ``Administrator``). When logging in, attention must be
paid to logging in with the domain Administrator account and not the local
Administrator account. Group Policy Management can be run on any system in the
domain.

If more than one Samba domain controller is in use, consideration must
be given to the replication of the GPO data, see :ref:`gpo-gposync`.

There are two basic possibilities for creating GPOs:

-  They can be created in the :guilabel:`Group Policy Objects`
   folder and then linked to different positions in the LDAP. This is
   practical if a policy is to be linked to several positions in the
   LDAP.

-  The GPO can also be created at an LDAP position ad hoc and then
   directly linked to it. This is the simpler means for small and
   medium-sized domains. Domains created ad hoc are also shown in the
   :guilabel:`Group Policy Objects` folder.

A policy can have one of three statuses: enabled, disabled or unset. The
effect is always based on the formulation of the policy. For example, if
it says :guilabel:`Disable feature xy`, the policy must be
enabled to switch off the feature. Some policies have additional
options, for example the :guilabel:`Enable mail quota` policy
could include an additional option for managing the storage space.

.. _windows-gpo-edit:

.. figure:: /images/gpo-edit-policy.*

Two standard policy objects are predefined:

-  The *Default Domain Policy* object can be used
   to configure global policies for all users and computers within the
   same domain.

-  The *Default Domain Controllers Policy* object
   has no use in a Samba domain (in a Microsoft AD domain the policies
   for Microsoft domain controllers would be performed via this object).
   The configuration of the Samba domain controllers in UCS is largely
   performed via |UCSUCR|.

AD domains can be structured in sites. All the sites are listed in the
main menu of Global Policy Management. There is also a list of the
domains there. The current Samba versions do not support forest domains,
so there is only ever one domain displayed here.

One domain can be structured in different organizational units (OUs).
This can, for example, be used to store the employees from accounting
and the users in the administration department in different LDAP
positions.

Group policies can mutually overlap. In this case, the inheritance principle
applies, e.g., the superordinate policies overwrite the subordinate ones. The
applicable policies for a user can be displayed on the Windows client either
with the modeling wizard in Group Policy Management or by entering the command
:command:`gpresult /user USERNAME /v`  in the Windows command line.

.. _windows-gpo-user:

.. figure:: /images/gpo-gpresult.*

The policies are evaluated in the following order:

-  By default *Default Domain Policy* settings
   apply for all the users and computers within the domain.

-  Policies linked to an OU overwrite policies from the default domain
   policy. If the OUs are nested further, in the case of conflict, the
   "most subordinate" policies in each case, in other words the one most
   closely linked to the target object, apply. The following evaluation
   order applies:

   -  Assignment of a policy to an Active Directory site

   -  Settings of the default domain policy

   -  Assignment of a policy to an organizational unit (OU) (in turn,
      each subordinate OU overrules policies from superordinate OUs).

Example: A company blocks access to the Windows Task Manager in general.
This is done by enabling the :guilabel:`Remove Task Manager`
policy in the *Default Domain Policy* object.
However, the Task Manager should still be available to some staff with
the requisite technical expertise. These users are saved in the
*IT staff* OU. An additional group policy object
is now created in which the :guilabel:`Remove Task Manager`
policy is set to *disabled*. The new GPO is linked
with the *IT staff* OU.

.. _gpo-gposync:

Configuration of group policies in environments with more than one Samba domain controller
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

A group policy is technically composed of two parts: On the one hand
there is a directory in the domain controllers' file system which
contains the actual policy files which are to be implemented on the
Window system (saved in the SYSVOL share (see :ref:`windows-sysvolshare`)). On the other hand there is an
object with the same name in the LDAP tree of the Samba directory
service (Samba AD/DS), which is usually saved below an LDAP container
named *Group Policy Objects*.

Although the LDAP replication between the domain controllers is
performed in just a few seconds, the files in the SYSVOL share are only
replicated every five minutes in the default setting. It must be noted
that the application of newly configured group policies in this period
may fail if a client happens to consult a domain controller which has
not yet replicated the current files.

.. _gpo-adm:

Administrative templates (ADMX/ADM)
'''''''''''''''''''''''''''''''''''

The policies displayed in Group Policy Management can be expanded with
so-called *administrative templates*. This type of
template defines the name under which the policy should appear in Group
Policy Management and which value should be set in the Windows registry.
Administrative templates are saved in so-called *ADMX
files* (previously *ADM files*), see `Group Policy ADMX Syntax Reference Guide <https://technet.microsoft.com/en-us/library/1db6fd85-d682-4d7d-9223-6b8dfafddc1c>`_. Among other things, ADMX files
offer the advantage that they can be provided centrally across several
domain controllers so that Group Policy Management on all Windows clients
displays the same configuration possibilities, see `How to Implement the Central
Store for Group Policy Admin Templates, Completely (Hint: Remove Those .ADM
files!)
<https://blogs.technet.microsoft.com/askpfeplat/2011/12/12/how-to-implement-the-central-store-for-group-policy-admin-templates-completely-hint-remove-those-adm-files/>`_.

The following example of an ADM file defines a computer policy in which a
registry key is configured for the (fictitious) Univention RDP client. ADM
files can also be converted to the newer ADMX format using third-party tools.
Further information on the format of ADM files can be found under `Writing
Custom ADM Files for System Policy Editor
<https://support.microsoft.com/en-us/kb/225087>`_ and `How to create custom ADM
templates <http://www.frickelsoft.net/blog/downloads/howto_admTemplates.pdf>`_.
The administrative template must have the file suffix :file:`.adm`:

.. code-block:: console

   CLASS MACHINE
   CATEGORY "Univention"
   POLICY "RDP client"
   KEYNAME "Univention\RDP\StorageRedirect"
   EXPLAIN "If this option it activated, sound output is enabled in the RDP client"
   VALUENAME "Sound redirection"
   VALUEON "Activated"
   VALUEOFF "Deactivated"
   END POLICY
   END CATEGORY


.. _windows-gpo-admin:

.. figure:: /images/gpo-adm-template.*

The ADM file can then be converted to the ADMX format or imported
directly via Group Policy Management. This is done by running the
:guilabel:`Add/Remove Templates` option in the
:guilabel:`Administrative templates` context menu.
:guilabel:`Add` can be used to import an ADM file. The
administrative templates are also saved in the SYSVOL share and
replicated, which allows Group Policy Management to access them from the
Windows clients.

.. _gpo-wmifilter:

Application of policies based on computer properties (WMI filters)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

It is also possible to configure policies based on system properties.
These properties are provided via the Windows Management Instrumentation
interface. The mechanism which builds on this is known as
*WMI filtering*. This makes it possible, for
example, to apply a policy only to PCS with a 64-bit processor
architecture or with at least 8 GB of RAM. If a system property changes
(e.g., if more memory is installed), the respective filter is
automatically re-evaluated by the client.

The WMI filters are displayed in the domain structure in the :guilabel:`WMI
Filters</guimenu> container. @@guimenu@@>New` can be used to define an
additional filter. The filter rules are defined under :guilabel:`Queries`. The
rules are defined in a syntax similar to SQL. Examples rules can be found in
`WMI filtering using GPMC
<https://www.microsoft.com/en-US/download/details.aspx?id=53314>`_  and `Filtern
von Gruppenrichtlinien anhand von Benutzergruppen, WMI und
Zielgruppenadressierung
<http://www.gruppenrichtlinien.de/artikel/filtern-von-gruppenrichtlinien-anhand-von-benutzergruppen-wmi-und-zielgruppenadressierung/>`_.

.. _netlogon-freigabe-samba4:

Logon scripts / NETLOGON share
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The NETLOGON share serves the purpose of providing logon scripts in
Windows domains. The logon scripts are executed following after the user
login and allow the adaptation of the user's working environment.
Scripts have to be saved in a format which can be executed by Windows,
such as :file:`bat`.

The logon scripts are stored in :file:`/var/lib/samba/sysvol/@@replaceable@@>Domainname</replaceable>/scripts/`
and provided under the share name *NETLOGON*. The
file name of the script must be given relative to that directory.

The NETLOGON share is replicated within the scope of the SYSVOL
replication.

The logon script can be assigned for each user, see
:ref:`users-management`.

.. _windows-serverhome-samba4:

Configuration of the file server for the home directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The home directory can be defined user-specifically in the UMC module
:guilabel:`Users`, see :ref:`users-management`. This is
performed with the setting :guilabel:`Windows home path`,
e.g., :file:`\\ucs-file-server\smith`.

The multi edit mode of UMC modules can be used to assign the home
directory to multiple users at one time, see
:ref:`central-user-interface-edit`.

.. _windows-roamingprofiles-samba4:

Roaming profiles
^^^^^^^^^^^^^^^^

Samba supports roaming profiles, i.e., user settings are saved on a
central server. This directory is also used for storing the files which
the user saves in the *My Documents* folder.
Initially, these files are stored locally on the Windows computer and
then synchronized onto the Samba server when the user logs off.

No roaming profiles are used by default in Samba/AD.

Roaming profiles can be configured via a group policy found under
:menuselection:`Computer configuration --> Policies --> Administrative templates
--> System --> User profiles --> Set roaming profile path for all users logging
onto this computer`. If this is set to the UNC path
:file:`%LOGONSERVER%\%USERNAME%\windows-profiles\default` the profile data will
get written to the directories :samp:`windows-profiles\default.V{?}` in the home
directory of the user located on the currently chosen logon server.

Alternatively the profile path can be defined for individual user accounts. This
is possible in the UMC module :guilabel:`Users` under the :guilabel:`Account`
tab by filling the field *Windows profile directory*. The corresponding UDM
property is called ``profilepath``. In the OpenLDAP backend this is stored in
the LDAP attribute ``sambaProfilePath``.

If the profile path is changed, then a new profile directory will be
created. The data in the old profile directory will be kept. These data
can be manually copied or moved to the new profile directory. Finally,
the old profile directory can be deleted.

.. note::

   As standard, the Administrator accesses shares with root rights. If
   as a result the profile directory is created with the root user, it
   should be manually assigned to the Administrator with the command
   :command:`chown`.

.. _ad-connector-general:

Active Directory Connection
===========================

.. _ad-connector-einfuehrung:

Introduction
------------

|UCSUCS| can be operated together with an existing Active Directory domain
(AD domain) in two different ways. Both modes can be set up using the
*Active Directory Connection* application from the
Univention App Center (see
:ref:`computers-softwaremanagement-installsoftware`). This is
available on a |UCSPRIMARYDN| and |UCSBACKUPDN|.

The two modes are:

-  UCS as a part (domain member) of an AD domain (see :ref:`ad-connector-ad-member-einrichtung`)

-  Synchronization of account data between an AD domain and a UCS domain
   (see :ref:`ad-connector-ad-connector-einrichtung`).

In both modes, the Active Directory Connection service is used in UCS
(UCS AD Connector for short), which can synchronize the directory
service objects between a Windows 2012/2016/2019 server with Active
Directory (AD) and the OpenLDAP directory of |UCSUCS|.

In the first case, the configuration of a UCS server system as a member
of an AD domain, the AD functions as the primary directory service and
the respective UCS system joins the trust context of the AD domain. The
domain membership gives the UCS system restricted access to the account
data of the Active Directory domain. The set-up of this operating mode
is described in detail in :ref:`ad-connector-ad-member-einrichtung`.

The second mode, which can be configured via the *Active
Directory Connection* app, is used to run the UCS domain
parallel to an existing AD domain. In this mode, each domain user is
assigned a user account with the same name in both the UCS and the AD
domain. Thanks to the use of the name identity and the synchronization
of the encrypted password data, this mode allows transparent access
between the two domains. In this mode, the authentication of a user in
the UCS domain occurs directly within the UCS domain and as such is not
directly dependent on the AD domain. The set-up of this operating mode
is described in detail in :ref:`ad-connector-ad-connector-einrichtung`.

.. _ad-connector-ad-member-einrichtung:

UCS as a member of an Active Directory domain
---------------------------------------------

In the configuration of a UCS server system as a member of an AD domain
(*AD member* mode), the AD functions as the
primary directory service and the respective UCS system joins the trust
context of the AD domain. The UCS system is not able to operate as an
Active Directory domain controller itself. The domain membership gives
the UCS system restricted access to the account data of the Active
Directory domain, which it exports from the AD by means of the UCS AD
Connector and writes locally in its own OpenLDAP-based directory
service. In this configuration, the UCS AD Connector does not write any
changes in the AD.

The *AD member* mode is ideal for expanding an AD
domain with applications that are available on the UCS platform. Apps
installed on the UCS platform can then be used by the users of the AD
domain. The authentication is still performed against native Microsoft
AD domain controllers.

The set-up wizard can be started directly from the UCS installation by
selecting *Join into an existing Active Directory
domain*. Subsequently, the set-up wizard can be installed with
the app *Active Directory Connection* from the
Univention App Center. Alternatively, the software package
:program:`univention-ad-connector` can be installed. Further
information can be found in
:ref:`computers-softwaremanagement-installsoftware`.

.. note::

   -  The *AD member* mode can only be configured
      on a |UCSPRIMARYDN|.

   -  The name of the DNS domain of the UCS systems must match that of
      the AD domain. The host name must of course be different.

   -  All the AD and UCS servers in a connector environment must use the
      same time zone.

.. _windows-gpo-mode:

.. figure:: /images/admember_1.*

In the first dialogue window of the set-up wizard, the point
*Configure UCS as part of an AD domain* is
preselected and can be confirmed with
:guilabel:`Next`.

The next dialogue window requests the address of an AD domain controller as well
as the name of the standard administrator account of the AD domain and its
password. The standard AD administrator account should be used here. The
specified AD domain controller should also provide DNS services for the domain.
Pressing the :guilabel:`Join AD domain` button starts the domain join.

.. _windows-ad-join:

.. figure:: /images/admember_2.*

If the system time of the UCS system is more than 5 minutes ahead of the
system time of the AD domain controller, manual adjustment of the system
times is required. This is necessary because the AD Kerberos
infrastructure is used for the authentication. System times should not,
however, be turned back, in order to avoid inconsistencies.

The domain join is performed automatically. The subsequent dialogue window
should be confirmed with :guilabel:`Finish`.  Then the UMC server should be
restarted by clicking :guilabel:`Restart`.

.. note::

   Once the *AD member* mode has been set up, the authentication is performed
   against the AD domain controller.  *Consequently, the password from the AD
   domain now applies for the administrator.* If an AD domain with a non-English
   language convention has been joined, the ``administrator`` account from UCS
   is automatically changed to the spelling of the AD during the domain join.
   The same applies for all user and group objects with *Well Known SID* (e.g.,
   ``Domain Admins``).

.. warning::

   If additional UCS systems were already part of the UCS domain in
   addition to the |UCSPRIMARYDN|, they must also join the domain anew. At
   the same time they recognize that the |UCSPRIMARYDN| is in
   *AD member* mode and also join the
   authentication structure of the AD domain and can then also provide
   Samba file shares, for example.

.. note::

   As the AD Kerberos infrastructure is used for the authentication of
   users in this mode, it is essential that the system times of UCS and
   the AD domain controller are synchronized (with a tolerance of 5
   minutes). For this purpose, the AD domain controller is configured as
   the NTP time server in UCS. In the case of authentication problems,
   the system time should always be the first thing to be checked.

Following this set-up, the UMC module :guilabel:`Active Directory
Connection` can be used for further administration, e.g., for
checking whether the service is running and to restart it if necessary
(see :ref:`ad-connector-neustart`).

To use an encrypted connection between Active Directory and the
|UCSPRIMARYDN| not only for the authentication, but also for data exchange
itself, the root certificate of the certification authority can be
exported from the AD domain controller and uploaded via the UMC module.
Further information on this topic is available in :ref:`ad-connector-ad-zertifikat`.

By default the Active Directory connection set up in this way does not
transfer any password data from AD to the UCS directory service. Some
apps from the Univention App Center require encrypted password data. If
an app needs it, a note is shown in the App Center.

In *AD member* mode the UCS AD Connector exports object data from the AD with
the authorizations of the |UCSPRIMARYDN|'s machine account by default. These
authorizations are not sufficient for exporting encrypted password data. In this
case, the LDAP DN of a privileged replication user can be adjusted manually in
the |UCSUCRV| :envvar:`connector/ad/ldap/binddn`. This must be a member of the
``Domain Admins`` group in the AD. The corresponding password must be saved in a
file on the |UCSPRIMARYDN| and the file name entered in the |UCSUCRV|
:envvar:`connector/ad/ldap/bindpw`. If the access password is changed at a later
point in time, the new password must be entered in this file. The access rights
for the file should be restricted so that only the ``root`` owner has access.

The following commands demonstrate the steps in an example:

.. code-block:: console

   ucr set connector/ad/ldap/binddn=Administrator
   ucr set connector/ad/ldap/bindpw=/etc/univention/connector/password
   touch /etc/univention/connector/password
   chmod 600 /etc/univention/connector/password
   echo -n "Administrator password" > /etc/univention/connector/password
   ucr set connector/ad/mapping/user/password/kinit=false


If desired, the AD domain controller can also be replaced by the
|UCSPRIMARYDN| at a later point in time. This is possible via the
*Active Directory Takeover* application (see
:ref:`windows-adtakeover`).

.. _ad-connector-ad-connector-einrichtung:

Setup of the UCS AD connector
-----------------------------

As an alternative to membership in an AD domain, as described in the
previous section, the Active Directory Connection can be used to
synchronize user and group objects between a UCS domain and an AD
domain. In addition to unidirectional synchronization, this operating
mode also allows bidirectional synchronization. In this operating mode,
both domains exist in parallel and their authentication systems function
independently. The prerequisite for this is the synchronization of the
encrypted password data.

By default containers, organizational units, users, groups and computers
are synchronized.

Information on the attributes configured in the basic setting and
particularities to take into account can be found in :ref:`ad-connector-details-zur-vorkonfigurierten-synchronization`.

The identical user settings in both domains allow users to access
services in both environments transparently. After logging on to a UCS
domain, subsequent connection to a file share or to an Exchange server
with Active Directory is possible without a renewed password request.
Users and administrators will find users and groups of the same name on
the resources of the other domain and can thus work with their familiar
permission structures.

The initialization is performed after the first start of the connector.
All the entries are read out of the UCS, converted to AD objects
according to the mapping set and added (or modified if already present)
on the AD side. All the objects are then exported from the AD and
converted to UCS objects and added/modified accordingly on the UCS side.
As long as there are changes, the directory service servers continue to
be requested. The UCS AD connector can also be operated in a
unidirectional mode.

Following the initial sync, additional changes are requested at a set
interval. This value is set to five seconds and can be adjusted manually
using the |UCSUCR| variable :envvar:`connector/ad/poll/sleep`.

If an object cannot be synchronized, it is firstly reset (“rejected”).
Following a configurable number of cycles – the interval can be adjusted
using the |UCSUCR| variable :envvar:`connector/ad/retryrejected` –
another attempt is made to import the changes. The standard value is ten
cycles. In addition, when the UCS AD Connector is restarted, an attempt
is also made to synchronize the previously rejected changes again.

The UCS AD connector can only be installed on a |UCSPRIMARYDN| or
|UCSBACKUPDN| system.

.. _ad-connector-basicsetup:

Basic configuration of the UCS AD Connector
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The UCS AD Connector is configured using a wizard in the UMC module
:guilabel:`Active Directory Connection`.

The module can be installed from the Univention App Center with the
application *Active Directory Connection*.
Alternatively, the software package
:program:`univention-ad-connector` can be installed.
Additional information can be found in
:ref:`computers-softwaremanagement-installsoftware`.

.. note::

   All AD and UCS servers in a connector environment must use the same
   time zone.

.. warning::

   Despite intensive tests it is not possible to rule out that the
   results of the synchronization may affect the operation of a
   productive domain. The connector should therefore be tested for the
   respective requirements in a separate environment in advance.

It is convenient to perform the following steps with a web browser from
the AD domain controller, as the files need to be downloaded from the AD
domain controller and uploaded to the wizard.

In the first dialog window of the set-up wizard, the point
*Synchronization of content data between an AD and this UCS
domain* must be selected and confirmed with
:guilabel:`Next`.

.. _windows-ad-connector:

.. figure:: /images/adconnector_1.*

The address of an AD domain controller is requested in the next dialogue
window. Here you can specify the IP address of a fully qualified DNS
name. If the UCS system is not be able to resolve the computer name of
the AD system, the AD DNS server can either be configured as the DNS
forwarder under UCS or a DNS host record can be created for the AD
system in the UMC module :guilabel:`DNS` (see
:ref:`networks-dns-hostrecord`).

Alternatively, a static entry can also be adopted in
:file:`/etc/hosts` via |UCSUCR|, e.g.

.. code-block:: console

   ucr set hosts/static/192.0.2.100=w2k8-32.ad.example.com

In the :guilabel:`Active Directory account` field, the user is configured which
is used for the access on the AD. The setting is saved in the |UCSUCRV|
:envvar:`connector/ad/ldap/binddn`. The replication user must be a member of the
``Domain Admins`` group in the AD.

The password used for the access must be entered in the
:guilabel:`Active Directory password` field. On the UCS system
it is only saved locally in a file which only the ``root`` user can read.

:ref:`ad-connector-ad-passwort`
describes the steps required if these access data need to be adjusted at
a later point in time.

Clicking on :guilabel:`Next` prompts the set-up wizard
to check the connection to the AD domain controller. If it is not
possible to create an SSL/TLS-encrypted connection, a warning is emitted
in which you are advised to install a certification authority on the AD
domain controller. It is recommended to follow this advice. UCS 5.0
requires TLS 1.2, which needs to be activated manually for Windows
Server Releases prior to 2012R2. UCS 5.0 doesn't support the hash
algorithm SHA-1 any longer. If this has been used in the creation of the
AD root certificate or for the certificate of the Windows server then
they should be replaced. Following this step, the set-up can be
continued by clicking :guilabel:`Next` again. If it is
still not possible to create an SSL/TLS-encrypted connection, a security
query appears asking whether to set up the synchronization without SSL
encryption. If this is desired, the set-up can be continued by clicking
:guilabel:`Continue without encryption`. In this case,
the synchronization of the directory data is performed unencrypted.

If the AD domain controller supports SSL/TLS-encrypted connections, the
set-up wizard offers :guilabel:`Upload AD root certificate` in
the next step. This certificate must be exported from the AD
certification authority in advance (see :ref:`ad-connector-ad-zertifikat`). In contrast,
if this step is skipped, the certificate can also be uploaded via the
UMC module at a later point in time and the SSL/TLS encryption enabled
(until that point all directory data will, however, be synchronized
unencrypted).

The connector can be operated in different modes, which can be selected
in the next dialogue window :guilabel:`Configuration of Active
Directory domain synchronization`. In addition to bidirectional
synchronization, replication can also be performed in one direction from
AD to UCS or from UCS to AD. Once the mode has been selected,
:guilabel:`Next` needs to be clicked.

Once :guilabel:`Next` is clicked, the configuration is
taken over and the UCS AD Connector started. The subsequent dialogue
window needs to be closed by clicking on
:guilabel:`Finish`.

Following this set-up, the UMC module :guilabel:`Active Directory
Connection` can be used for further administration of the
Active Directory Connection, e.g., for checking whether the service is
running and restart it if necessary (see :ref:`ad-connector-neustart`).

.. note::

   The connector can also synchronize several AD domains within one UCS domain;
   this is documented in `Extended Windows integration documentation
   <https://docs.software-univention.de/windows-5.0.html>`_.

.. _windows-ad-dialog:

.. figure:: /images/adconnector_2.*

.. _ad-connector-ad-zertifikat:

Importing the SSL certificate of the Active Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An SSL certificate must be created on the Active Directory system and
the root certificate exported to allow encrypted communication. The
certificate is created by the Active Directory's certificate service.
The necessary steps depend on the Windows versions used. Three versions
are shown below as examples.

The encrypted communication between the UCS system and Active Directory
can also be deactivated by setting the |UCSUCRV|
:envvar:`connector/ad/ldap/ssl` to ``no``.
This setting does not affect the replication of encrypted password data.

.. _windows-adconn-win2012:

Exporting the certificate on Windows 2012 / 2016 / 2019
'''''''''''''''''''''''''''''''''''''''''''''''''''''''

If the certificate service is not installed, it must be installed before
proceeding.

The server manager must be opened. There, select the :guilabel:`Active
Directory Certificate Services` role in the :guilabel:`Manage
AR Add Roles and Features` menu. When selecting the role
services, it is sufficient simply to select :guilabel:`Certification
Authority`. A yellow warning triangle is then shown in the top
bar in the server manager. Here, the :guilabel:`Configure Active
Directory Certificate Services on the server` option must be
selected. :guilabel:`Certification Authority` is selected as
the role service to be configured. The type of installation is
:guilabel:`Enterprise CA AR Root CA` Now, click on
:guilabel:`Create a new private key` and confirm the suggested
encryption settings and the suggested name of the certification
authority. Any period of validity can be set. The standard paths can be
used for the database location.

The AD server must then be restarted.

This certificate must now be exported and copied onto the UCS system:
:menuselection:`Server Manager --> Active Directory Certificate
Services` Then right click on the server and select
:guilabel:`Certification Authority`. There, right click on the
name of the generated certificate and :menuselection:`Open --> Copy to File
--> DER encoded binary X.509 (.CER) --> Select an arbitrary filename -->
Finish`.

A computer list is shown there and the elements :guilabel:`Revoked
Certificates</guimenu>, @@guimenu@@>Issued Certificates`,
:guilabel:`Pending Requests`, :guilabel:`Failed
Requests</guimenu> and @@guimenu@@>Certificate Templates`
displayed under every system. Here, one must right click on the computer
name - not on one of the elements - and then select
:guilabel:`Properties`. The root certificate is usually called
``Certificate #0``. Then select
:guilabel:`Open --> Copy to File --> DER encoded binary X.509 (.CER) -->
Select an arbitrary filename --> Finish`.

.. _windows-copying-the-active-directory-certificate-to-the-ucs-system:

Copying the Active Directory certificate to the UCS system
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

The SSL AD certificate should now be imported into the UCS system using
the UMC module.

This is done by clicking on :guilabel:`Upload` in the sub menu :guilabel:`Active
Directory connection SSL configuration`.

This opens a window in which a file can be selected, which is being
uploaded and integrated into the UCS AD Connector.

.. _ad-connector-neustart:

Starting/Stopping the Active Directory Connection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The connector can be started using *Start Active Directory connection service*
and stopped using *Stop Active Directory connection service*.  Alternatively,
the starting/stopping can also be performed with the
:file:`/etc/init.d/univention-ad-connector` init-script.

.. _windows-functional-test-of-basic-settings:

Functional test of basic settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The correct basic configuration of the connector can be checked by
searching in Active Directory from the UCS system. Here one can search
e.g. for the administrator account in Active Directory with
:command:`univention-adsearch cn=Administrator`.

As :command:`univention-adsearch` accesses the configuration
saved in |UCSUCR|, this allows you to check the reachability/configuration
of the Active Directory access.

.. _ad-connector-ad-passwort:

Changing the AD access password
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The access data required by the UCS AD Connector for Active Directory are
configured via the |UCSUCRV| :envvar:`connector/ad/ldap/binddn` and
:envvar:`connector/ad/ldap/bindpw`. If the password has changed or you wish to
use another user account, these variables must be adapted manually. The
|UCSUCRV| :envvar:`connector/ad/ldap/binddn` is used to configure the LDAP DN of
a privileged replication user. This must be a member of the ``Domain Admins``
group in the AD. The corresponding password must be saved locally in a file on
the UCS system, the name of which must be entered in the |UCSUCRV|
:envvar:`connector/ad/ldap/bindpw`. The access rights for the file should be
restricted so that only the ``root`` owner has access. The following commands
show this as an example:

.. code-block:: console

   eval "$(ucr shell)"
   echo "Updating ${connector_ad_ldap_bindpw?}"
   echo "for AD sync user ${connector_ad_ldap_binddn?}"
   touch "${connector_ad_ldap_bindpw?}"
   chmod 600 "${connector_ad_ldap_bindpw?}"
   echo -n "Current AD Syncuser password" > "${connector_ad_ldap_bindpw?}"


.. _ad-connector-tools:

Additional tools / Debugging connector problems
-----------------------------------------------

The UCS AD Connector provides the following tools and log files for
diagnosis:

.. _ad-connector-univention-adsearch:

:command:`univention-adsearch`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool facilitates a simple LDAP search in Active Directory. Objects
deleted in AD are always shown (they are still kept in an LDAP subtree
in AD). As the first parameter the script awaits an LDAP filter; the
second parameter can be a list of LDAP attributes to be displayed.

Example:

.. code-block:: console

   univention-adsearch cn=administrator cn givenName

.. _ad-connector-univention-adconnector-list-rejected:

:command:`univention-adconnector-list-rejected`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This tool lists the DNs of non-synchronized objects. In addition, in so
far as temporarily stored, the corresponding DN in the respective other
LDAP directory will be displayed. In conclusion
``lastUSN`` shows the ID of the last change
synchronized by AD.

This script may display an error message or an incomplete output if the
AD connector is in operation.

.. _windows-logfiles:

Logfiles
^^^^^^^^

For troubleshooting when experiencing synchronization problems,
corresponding messages can be found in the following files on the UCS
system:

::

   /var/log/univention/connector-ad.log
   /var/log/univention/connector-status.log

.. _ad-connector-details-zur-vorkonfigurierten-synchronization:

Details on preconfigured synchronization
----------------------------------------

All containers which are ignored due to corresponding filters are
exempted from synchronization as standard. This can be found in the
:file:`/etc/univention/connector/ad/mapping`
configuration file under the
*global_ignore_subtree* setting. To except users
from synchronization their user name can be added to the |UCSUCRV|
:envvar:`connector/ad/mapping/user/ignorelist`. For more
flexibility a filter can be set in the |UCSUCRV|
:envvar:`connector/ad/mapping/user/ignorefilter`. However this
filter does not support the full LDAP filter syntax. It is always case
sensitive and the placeholder "*" can only be used as a single value
without any other characters.

.. _ad-connector-container-und-organisationseinheiten:

Containers and organizational units
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Containers and organizational units are synchronized together with their
description. In addition, the ``cn=mail`` and
``cn=kerberos`` containers are ignored on both sides. Some
particularities must be noted for containers on the AD side. In the
:guilabel:`User manager` Active Directory offers no
possibility to create containers, but displays them only in the advanced
mode (:guilabel:`View AR Advanced settings`).

.. _windows-ad-connector-particularities:

Particularities
'''''''''''''''

-  Containers or organizational units deleted in AD are deleted
   recursively in UCS, which means that any non-synchronized subordinate
   objects, which are not visible in AD, are also deleted.

.. _ad-connector-gruppen:

Groups
^^^^^^

Groups are synchronized using the group name, whereby a user's primary
group is taken into account (which is only stored for the user in LDAP
in AD).

Group members with no opposite in the other system, e.g., due to ignore
filters, are ignored (thus remain members of the group).

The description of the group is also synchronized.

.. _windows-groups-particularities:

Particularities
'''''''''''''''

-  The *pre Windows 2000 name* (LDAP attribute
   ``samAccountName``) is used in AD, which means
   that a group in Active Directory can appear under a different name
   from in UCS.

-  The connector ignores groups, which have been configured as a
   *Well-Known Group* under :guilabel:`Samba
   group type` in |UCSUDM|. There is no synchronization of the
   SID or the RID.

-  Groups which were configured as *Local Group*
   under :guilabel:`Samba group type` in |UCSUDM| are
   synchronized as a *global group* in the Active
   Directory by the connector.

-  Newly created or moved groups are always saved in the same
   subcontainer on the opposite side. If several groups with the same
   name are present in different containers during initialization, the
   members are synchronized, but not the position in LDAP. If one of
   these groups is migrated on one side, the target container on the
   other side is identical, so that the DNs of the groups can no longer
   be differentiated from this point onward.

* Certain group names are converted using a mapping table so that, for example
  in a German language setup, the UCS group ``Domain Users`` is synchronized
  with the AD group *Domänen-Benutzer*. When used in anglophone AD domains, this
  mapping can result in *germanophone* groups' being created and should thus be
  deactivated in this case. This can be done using the |UCSUCRV|
  :envvar:`connector/ad/mapping/group/language`

  The complete table is:

  .. list-table::
     :header-rows: 1

     * - *UCS group*
       - *AD group*

     * - ``Domain Users``
       - ``Domänen-Benutzer``

     * - ``Domain Admins``
       - ``Domänen-Admins``

     * - ``Windows Hosts``
       - ``Domänencomputer``

-  Nested groups are represented differently in AD and UCS. In UCS, if
   groups are members of groups, these objects can not always be
   synchronized on the AD side and appear in the list of rejected
   objects. Due to the existing limitations in Active Directory, nested
   groups should only be assigned there.

* If a global group :samp:`{A}` is accepted as a member of another global group
  :samp:`{B}` in |UCSUDM|, this membership does not appear in Active Directory
  because of the internal AD limitations in :program:`Windows 2000/2003`. If
  group :samp:`{A}`'s name is then changed, the group membership to group
  :samp:`{B}` will be lost. Since :program:`Windows 2008` this limitation no
  longer exists and thus global groups can also be nested in Active Directory.

.. _windows-groups-custommappings:

Custom Mappings
'''''''''''''''

It is also possible to modify and append custom mappings. For that to
work a file has to be created named
:file:`/etc/univention/connector/ad/localmapping.py`.
Within that file the following function should be implemented:

::

   def mapping_hook(ad_mapping):
       return ad_mapping

The contents of the :command:`ad_mapping` variable can be
modified to influence the mapping. The resulting mapping gets written to
:file:`/var/log/univention/connector-ad-mapping.log`
when the UCSADC is restarted.

.. _ad-connector-benutzer:

Users
^^^^^

Users are synchronized like groups using the user name or using the AD
pre Windows 2000 name. The *First name*,
*Last name</emphasis>, @@emphasis@@>Primary group*
(in so far as present on the other side),
*Organization*,
*Description</emphasis>, *Street*,
*City*, @@emphasis@@>Postal code*,
*Windows home path*, *Windows login
script</emphasis>, @@emphasis@@>Disabled* and
*Account expiry date* attributes are transferred.
Indirectly *Password*, *Password
expiry date* and *Change password on next
login* are also synchronized. *Primary e-mail
address</emphasis> and @@emphasis@@>Telephone number* are
prepared but commented out due to differing syntax in the mapping
configuration.

The ``root`` and ``Administrator`` users are exempted.

.. _windows-user-particularities:

Particularities
'''''''''''''''

-  Users are also identified using the name, so that for users created
   before the first synchronization on both sides, the same process
   applies as for groups as regards the position in LDAP.

-  In some cases, a user to be created under AD, for which the password
   has been rejected, is deleted from AD immediately after creation. The
   reasoning behind this is that AD created this user firstly and then
   deletes it immediately once the password is rejected. If these
   operations are transmitted to UCS, they are transmitted back to AD.
   If the user is re-entered on the AD side before the operation is
   transmitted back, it is deleted after the transmission. The
   occurrence of this process is dependent on the polling interval set
   for the connector.

-  AD and UCS create new users in a specific primary group (usually
   ``Domain Users`` or ``Domänen-Benutzer``) depending on the presetting.
   During the first synchronization from UCS to AD the users are
   therefore always a member in this group.

.. _windows-adtakeover:

Migrating an Active Directory domain to UCS using Univention AD Takeover
========================================================================

.. _windows-adtakeover-intro:

Introduction
------------

UCS supports the takeover of user, group and computer objects as well as
Group Policy Objects (GPOs) from a Microsoft Active Directory (AD)
domain. Windows clients do not need to rejoin the domain. The takeover
is an interactive process consisting of three distinct phases:

-  Copying all objects from Active Directory to UCS

-  Copying of the group policy files from the AD server to UCS

-  Deactivation of the AD server and assignment of all FSMO roles to the
   UCS DC

The following requirements must be met for the takeover:

-  The UCS Directory Node (|UCSPRIMARYDN|) needs to be installed with a
   unique hostname, not used in the AD domain.

-  The UCS Directory Node needs to be installed with the same DNS domain
   name, NetBIOS (pre Windows 2000) domain name and Kerberos realm as
   the AD domain. It is also recommended to configure the same LDAP base
   DN.

-  The UCS Directory Node needs to be installed with a unique IPv4
   address in the same IP subnet as the Active Directory domain
   controller that is used for the takeover.

.. caution::

   If the system is already a member of an Active Directory Domain,
   installing the *Active Directory Takeover*
   application removes this membership. Therefore, the installation of
   the *Takeover* application has to take place
   only shortly before the actual takeover of the AD domain.

The *Active Directory Takeover* application must
be installed from the Univention App Center for the migration. It must
be installed on the system where the Univention S4 Connector is running
(see :ref:`windows-s4connector`, usually the
|UCSPRIMARYDN|).

.. _windows-adtakeover-preparations:

Preparation
-----------

The following steps are strongly recommended before attempting the
takeover:

-  A backup of the AD server(s) should be performed.

-  If user logins to the AD server are possible (e.g. through domain
   logins or terminal server sessions) it is recommended to deactivate
   them and to stop any services in the AD domain, which deliver data,
   e.g. mail servers. This ensures that no data is lost in case of a
   rollback to the original snapshot/backup.

-  It is recommended to set the same password for the ``Administrator`` account on the AD server
   as the corresponding account in the UCS domain. In case different
   passwords are used, the password that was set last, will be the one
   that is finally valid after the takeover process (timestamps are
   compared for this).

-  In a default installation the ``Administrator`` account of the AD server
   is deactivated. It should be activated in the local user management
   module.

The activation of the ``Administrator`` account on the AD server is
recommended because this account has all the required privileges to copy
the GPO SYSVOL files. The activation can be achieved by means of the
:guilabel:`Active Directory Users and Computers` module or by
running the following two commands:

.. code-block:: console

   net user administrator /active:yes
   net user administrator PASSWORD


.. _windows-adtakeover-migrate:

Domain migration
----------------

The takeover must be initiated on the UCS Directory Node that runs the
Univention S4 Connector (by default the |UCSPRIMARYDN|). During the
takeover process Samba must only run on this UCS system. If other UCS
Samba/AD Nodes are present in the UCS domain, Samba needs to be stopped
on those systems. This is important to avoid data corruption by mixing
directory data taken over from Active Directory with Samba/AD directory
data replicated from other UCS Samba/AD Nodes.

Other UCS Samba/AD systems can be stopped by logging into each of the
other UCS Directory Nodes as the ``root`` user and running

.. code-block:: console

   /etc/init.d/samba4 stop


After ensuring that only the Univention S4 Connector host runs Samba/AD,
the takeover process can be started. If the UCS domain was installed
initially with a UCS version before UCS 3.2, the following |UCSUCRV| needs
to be set first:

.. code-block:: console

   ucr set connector/s4/mapping/group/grouptype=false


The takeover is performed with the UMC module :guilabel:`Active
Directory Takeover`. The IP address of the AD system must be
specified under :guilabel:`Name or address of the Domain
Controller`. An account from the AD domain must be specified
under :guilabel:`Active Directory Administrator account` which
is a member of the AD group ``Domain Admins`` (e.g., the ``Administrator``) and the corresponding
password entered under :guilabel:`Active Directory Administrator
password`.

.. _windows-ad-takeover1:

.. figure:: /images/takeover1.*

The module checks whether the AD domain controller can be accessed and
displays the domain data to be migrated.

.. _windows-ad-takeover2:

.. figure:: /images/takeover2.*

When :guilabel:`Next` is clicked, the following steps are
performed automatically. Additional information is logged to
:file:`/var/log/univention/ad-takeover.log` as well as
to
:file:`/var/log/univention/management-console-module-adtakeover.log`.

-  Adjust the system time of the UCS system to the system time of the
   Active Directory domain controller in case the UCS time is behind by
   more than three minutes.

-  Join the UCS Directory Node into the Active Directory domain

-  Start Samba and the Univention S4 connector to replicate the Active
   Directory objects into the UCS OpenLDAP directory

-  When "*Well Known*" account and group objects
   (identified by their special RIDs) are synchronized into the UCS
   OpenLDAP, a listener module running on each UCS system sets a |UCSUCR|
   variable to locally to map the English name to the non-English AD
   name. These variables are used to translate the English names used in
   the UCS configuration files to the specific names used in Active
   Directory. To give an example, if ``Domain Admins`` has a different name in
   the AD, then the |UCSUCR| variable
   :envvar:`groups/default/domainadmins` is set to that specific
   name (likewise for uses, e.g.
   :envvar:`users/default/administrator`).

The UCS Directory Node now contains all users, groups and computers of
the Active Directory domain. In the next step, the SYSVOL share is
copied, in which among other things the group policies are stored.

This phase requires to log onto the Active Directory domain controller
as the ``Administrator`` (or
the equivalent non-English name). There a command needs to be started to
copy the group policy files from the Active Directory SYSVOL share to
the UCS SYSVOL share.

The command to be run in shown in the UMC module. If it has been
successfully run, it must be confirmed with :guilabel:`Next`.


.. _windows-ad-sysvol:

.. figure:: /images/takeover3.*

It may be necessary to install the required :command:`robocopy` tool, which is
part of the Windows Server 2003 Resource Kit Tools. Starting with Windows 2008
the tool is already installed.

Note: The ``/mir`` option of :command:`robocopy` mirrors the
specified source directory to the destination directory. Please be aware
that if you delete data in the source directory and execute this command
a second time, this data will also be deleted in the destination
directory.

After successful completion of this step, it is now necessary to
shutdown all domain controllers of the Active Directory domain. Then
:guilabel:`Next` must be clicked in the UMC module.

.. _windows-ad-shutdown:

.. figure:: /images/takeover4.*

The following steps are now automatically performed:

-  Claiming all FSMO roles for the UCS Directory Node. These describe
   different tasks that a server can take on in an AD domain.

-  Register the name of the Active Directory domain controller as a DNS
   alias (see :ref:`ip-config-CNAME-Record-Alias-Records`) for the
   UCS DNS server.

-  Configure the IP address of the Active Directory domain controller as
   a virtual Ethernet interface

-  Perform some cleanup, e.g. removal of the AD domain controller
   account and related objects in the Samba SAM account database.

-  Finally restart Samba and the DNS server

.. _windows-adtakeover-finalsteps:

Final steps of the takeover
---------------------------

Finally the following steps are required:

-  The domain function level of the migrated Active Directory domain
   needs to be checked by running the following command:

   .. code-block:: console

      samba-tool domain level show


   In case this command returns the message ``ATTENTION: You
   run SAMBA 4 on a forest function level lower than Windows 2000
   (Native).`` the following commands should be run to fix this:

   .. code-block:: console

      samba-tool domain level raise --forest-level=2003 --domain-level=2003
      samba-tool dbcheck --fix --yes


-  In case there has been more than one Active Directory domain
   controller in the original Active Directory domain, all the host
   accounts of the other domain controllers must be removed in the
   computers management UMC modules. In addition their accounts must be
   removed from the Samba SAM database. This may be done by logging on
   to a migrated Windows client as member of the group ``Domain Admins`` and running the tool
   :guilabel:`Active Directory Users and Computers`.

-  If more than one UCS Directory Node with Samba/AD has been installed,
   these servers need to be re-joined.

-  All Windows clients need to be rebooted.

.. _windows-adtakeover-tests:

Tests
-----

It is recommended to perform thorough tests with Windows client systems,
e.g.

-  Login to a migrated client as a migrated user

-  Login to a migrated client as the Administrator

-  Testing group policies

-  Join of a new Windows client

-  Creation of a new UCS user and login to a Windows client

.. _windows-trust:

Trust relationships
===================

Trust relationships between domains make it possible for users from one
domain to log on to computers from another domain.

In general, Windows trust relations can be unidirectional or
bidirectional. Technically a bidirectional trust is simply realized as
two unidirectional trusts, one in each direction.

The terminology of unidirectional trusts depends on the perspective of
either the trusting or trusted domain: From the perspective of the
trusting domain, the trust is called *outgoing*.
From the perspective of the trusted domain, the trust is called
*incoming*.

In UCS, outgoing trust (UCS trusts Windows) is not supported currently.
As a consequence, bidirectional trust is not supported either.

When setting up and using the trust relationship the domain controllers
of both domains must be able to reach each other over the network and
identify each other via DNS. At least the fully qualified DNS names of
the domain controllers of the respective remote domain must be
resolvable to allow communication between both domains to work. This can
be achieved by configuring conditional DNS forwarding in both domains.

The following example assumes, that the UCS Samba/AD DC |UCSPRIMARYDN|
``primary.ucsdom.example``
has the IP address ``192.0.2.10`` and that the Active Directory
domain controller ``dc1.addom.example`` of the remote domain
has the IP address ``192.0.2.20``.

On the UCS side the conditional forwarding of DNS queries can be set up
as ``root`` with the following
commands:

.. code-block:: console

   cat >>/etc/bind/local.conf.samba4 <<__CONF__
   zone "addom.example" {
     type forward;
     forwarders { 192.0.2.20; };
   };
   __CONF__
   systemctl restart bind9



The success can be checked by running :command:`host
dc1.addom.example`.

In addition, it may be useful to create a static entry for the domain
controller of the remote Active Directory domain in the file
:file:`/etc/hosts`:

.. code-block:: console

   ucr set hosts/static/192.0.2.20=dc1.addom.example


On a Windows AD DC, a so-called *conditional
forwarding* can be set up for the UCS domain via the DNS
server console.

After this preliminary work, the trust itself can be established
directly from the command line of the UCS Samba/AD DC.

Trust relationships can only be configured on domain controllers but
they affect the whole domain.

In Samba/AD domain the trust relationship can be configured easily on
the command line using the tool :command:`samba-tool`:

.. code-block:: console

   samba-tool domain trust create addom.example \
              -k no -UADDOM\\Administrator%ADAdminPassword \
              --type=external --direction=incoming


The trust can be checked using the following commands:

.. code-block:: console

   samba-tool domain trust list
   wbinfo --ping-dc –domain=addom.example
   wbinfo --check-secret –domain=addom.example


After the setup, a UCS user should be able to log on to systems of the
remote Active Directory domain. Users must either use the format
``UCSDOM\username`` as login
name or their Kerberos principal in the notation ``username@ucsdom.example``.

