.. _computers-softwaremanagement:

*******************
Software deployment
*******************

.. _computers-introduction:

Introduction
============

The software deployment integrated in UCS offers extensive possibilities for the
rollout and updating of UCS installations. Security and version updates can be
installed via the UMC module :guilabel:`Software update`, a command line tool or
based on policies. This is described in the section :ref:`software-ucs-updates`.
The UCS software deployment does not support the updating of Microsoft Windows
systems. An additional Windows software distribution is required for this.

For larger installations, there is the possibility of establishing a local
repository server from which all further updates can be performed, see
:ref:`software-configrepo`.

The UCS software deployment is based on the underlying Debian package management
tools, which are expanded through UCS-specific tools. The different tools for
the installation of software are introduced in
:ref:`computers-softwaremanagement-installsoftware`. The installation of version
and errata updates can be automated via policies, see
:ref:`computers-softwaremanagement-maintenancepolicy`

The software monitor provides a tool with which all package installations
statuses can be centrally stored in a database, see
:ref:`computers-softwaremonitor`.

The initial installation of UCS systems is not covered in this chapter, but is
documented in :ref:`installation-chapter` instead.

.. _computers-differentiation-of-update-variants-ucs-versions:

Differentiation of update variants / UCS versions
=================================================

Four types of UCS updates are differentiated:

* *Major releases* appear approximately every three to four years. Major
  releases can differ significantly from previous major releases in terms of
  their scope of services, functioning and the software they contain.

* During the maintenance period of a major release, *minor releases* are
  released approximately every 10-12 months. These updates include corrections
  to recently identified errors and the expansion of the product with additional
  features. At the same time and as far as this is possible, the minor releases
  are compatible with the previous versions in terms of their functioning,
  interfaces and operation. Should a change in behavior prove practical or
  unavoidable, this will be noted in the release notes when the new version is
  published.

- Univention continuously releases *errata
  updates*. Errata updates provide fixes for security
  vulnerabilities and bugfixes/smaller enhancements to make them
  available to customer systems quickly. An overview of all errata
  updates can be found at https://errata.software-univention.de/.

- *Patchlevel releases* are released approximately every three months and
  combine all errata updates published until then.

Every released UCS version has an unambiguous version number; it is composed of
a figure (the major version), a full stop, a second figure (the minor version),
a hyphen and a third figure (the patch level version). The version UCS 4.2-1
thus refers to the first patch level update for the second minor update for the
major release UCS 4.

The *pre-update script* :file:`preup.sh` is run before every release update. It
checks for example whether any problems exist, in which case the update is
canceled in a controlled manner. The *post-update script* :file:`postup.sh` is
run at the end of the update to perform additional cleanups, if necessary.

Errata updates always refer to certain minor releases, e.g., for UCS 5.0. Errata
updates can generally be installed for all patch level versions of a minor
release.

If a new release or errata updates are available, a corresponding notification
is given when a user opens a UMC module. The availability of new updates is also
notified via e-mail; the corresponding newsletters - separated into release and
error updates - can be subscribed on the Univention website. A changelog
document is published for every release update listing the updated packages,
information on error corrections and new functions and references to the
Univention Bugzilla.

.. _software-appcenter:

Univention App Center
=====================

The Univention App Center allows simple integration of software components in a
UCS domain. The applications are provided both by third parties and by
Univention itself (e.g., UCS@school). The maintenance and support for the
applications are provided by the respective manufacturer.

.. _appcenter-overview:

.. figure:: /images/appcenter_overview.*
   :alt: Overview of applications available in the App Center

   Overview of applications available in the App Center

The Univention App Center can be opened via the UMC module :guilabel:`App
Center`. It shows by default all installed as well as available software
components. :guilabel:`Search Apps...` can be used to search for available
applications. Furthermore, the applications can also be filtered using the
:guilabel:`Category` panel. More filters like the :emphasis:`Badges` and the
:emphasis:`App License` can be used. For example, the view can be limited to
applications with the categories ``Education`` or ``Office``. To only show the
``Recommended Apps`` for theses categories, it is sufficient to activate the
appropriate filter.

If you click on one of the displayed applications, further details on it are
shown (e.g., description, manufacturer, contact information and screenshots or
videos). The *Notification* field displays whether the manufacturer of the
software component is notified when it is installed/uninstalled. A rough
classification of the licensing can be found under the *License* section. Some
applications provide a :guilabel:`Buy` button with a link to detailed licensing
information. For all other applications, it is recommended to contact the
manufacturer of the application about detailed licensing information using the
e-mail address shown under *Contact*.

.. _appcenter-details:

.. figure:: /images/appcenter_details.*
   :alt: Details for an application in the App Center

   Details for an application in the App Center

With *Vote Apps* there is a special form of Apps in the App Center that do not
install anything on the UCS system. Voting helps Univention and the potential
app provider to determine the interest in this app. Vote apps are usually only
displayed for a limited voting period. That Vote Apps are available, can be
recognized by the shown *Vote Apps* filter option in the App Center overview.

.. _appcenter-vote-apps:

.. figure:: /images/vote_apps.*
   :alt: Example Vote Apps in App Center overview and detail view

   Example Vote Apps in App Center overview and detail view

Some applications may not be compatible with other software packages from UCS.
For instance, most groupware packages require the UCS mail stack to be
uninstalled. Every application checks whether incompatible versions are
installed and then prompts which *Conflicts* exist and how they can be
resolved. The installation of these packages is then prevented until the
conflicts have been resolved.

Some components integrate packages that need to be installed on the
|UCSPRIMARYDN| (usually LDAP schema extensions or new modules for the UCS
management system). These packages are automatically installed on the
|UCSPRIMARYDN|. If this is not possible, the installation is aborted. In
addition, the packages are set up on all accessible |UCSBACKUPDN| systems.  If
several UCS systems are available in the domain, it can be selected on which
system the application is to be installed.

Some applications use the container technology :program:`Docker`. In these
cases, the application (and its direct environment) is encapsulated from the
rest and both security as well as the compatibility with other applications are
increased.

From a technical perspective, the app is started as Docker container and joined
into the UCS domain as |UCSMANAGEDNODE|. A corresponding computer object is
created for the |UCSMANAGEDNODE| in the LDAP directory.

On the network side, the container can only be reached from the computer on
which the app is installed. The app can, however, open certain ports, which can
be forwarded from the actual computer to the container. UCS' firewall is
correspondingly configured automatically to allow access to these ports.

If a command line is required in the app's environment, the first step is to
switch to the container. This can be done by running the following command
(using the fictitious app :program:`demo-docker-app` as an example in this
case):

.. code-block:: console

   $ univention-app shell demo-docker-app


Docker apps can be further configured via the UMC module. The app can be started
and stopped and the *autostart* option be set:

Started automatically
   ensures that the app is started automatically when the server is started up.

Started manually
   prevents the app from starting automatically, but it can be started via the
   UMC module.

Starting is prevented
   prevents the app from starting at any time; it cannot even be started via the
   UMC module.

In addition, apps can also be adjusted using additional parameters. The menu for
doing so can be opened using the :guilabel:`App Settings` button of an installed
app.

.. _appcenter-configure:

.. figure:: /images/appcenter_configure.*
   :alt: Setting of an application in the App Center

   Setting of an application in the App Center

After its installation, one or several new options are shown when
clicking on the icon of an application:

:guilabel:`Uninstall`
   removes an application.

:guilabel:`Open`
   refers you to a website or a UMC module with which you can further configure
   or use the installed application. This option is not displayed for
   applications which do not have a web interface or a UMC module.

Updates for applications are published independently of the |UCSUCS| release
cycles. If a new version of an application is available, the :guilabel:`Upgrade`
menu item is shown, which starts the installation of the new version. If updates
are available, a corresponding message is also shown in the UMC module
:guilabel:`Software update`.

Installations and the removal of packages are documented in the
:file:`/var/log/univention/management-console-module-appcenter.log` log file.

.. _software-ucs-updates:

Updates of UCS systems
======================

There are two ways to update UCS systems; either on individual systems (via UMC
module :guilabel:`Software update` or command line) or via a computer policy for
larger groups of UCS systems.

.. _computers-update-strategy-in-environments-with-more-than-one-ucs-system:

Update strategy in environments with more than one UCS system
-------------------------------------------------------------

In environments with more than one UCS system, the update order of the
UCS systems must be borne in mind.

The authoritative version of the LDAP directory service is maintained on the
|UCSPRIMARYDN| and replicated on all the remaining LDAP servers of the UCS
domain. As changes to the LDAP schemes (see :ref:`domain-ldap-schema`) can occur
during release updates, the |UCSPRIMARYDN| **must always be the first system**
to be updated during a release update.

It is generally advisable to update all UCS systems in one maintenance
window whenever possible. If this is not possible, all not-updated UCS
systems should only be one release version older compared with the
|UCSPRIMARYDN|.

.. _computers-updating-individual-systems-via-the-umc:

Updating individual systems via |UCSUMC| module
-----------------------------------------------

The UMC module :guilabel:`Software update` allows the installation of release
updates and errata updates.

:numref:`software-umcupdate` shows the overview page of the module. The
currently installed version is displayed under :guilabel:`Release updates`.

.. _software-umcupdate:

.. figure:: /images/software_onlineupdate.*
   :alt: Updating a UCS system via UMC module 'Software update'

   Updating a UCS system via UMC module *Software update*


If a newer UCS version is available, a selection list is displayed.
After clicking on :guilabel:`Install release updates` and
confirmation all updates up to the respective version are installed.
Before the installation process is started, a message will be displayed
informing the user of possible restrictions of the server's services
during the update. Any intermediate versions are also installed
automatically.

Clicking on :guilabel:`Install available errata updates`
installs all the available errata updates for the current release and
all installed components.

:guilabel:`Check for package updates` activates an update of
the package sources currently entered. This can be used, for example, if
an updated version is provided for a component.

The messages created during the update are written to the file
:file:`/var/log/univention/updater.log`

.. _computers-updating-individual-systems-via-the-command-line:

Updating individual systems via the command line
------------------------------------------------

The following steps must be performed with ``root`` user rights.

An individual UCS system can be updated using the :command:`univention-upgrade`
command in the command line. A check is performed to establish whether new
release or application updates are available and these are then installed if a
prompt is confirmed. In addition, package updates are also performed (e.g., in
the scope of an errata update).

Remote updating over SSH is not advisable as this may result in the update
procedure being aborted. If updates should occur over a network connection
nevertheless, it must be verified that the update continues despite
disconnection from the network. This can be done, for example, using the tools
:program:`screen` and :program:`at`, which are installed on all system roles.

The messages created during the update are written to the file
:file:`/var/log/univention/updater.log`

.. _computers-softwaremanagement-releasepolicy:

Updating systems via a policy
-----------------------------

An update for more than one computer can be configured with an
:guilabel:`Automatic updates` policy in the UMC modules :guilabel:`Computers`
and :guilabel:`LDAP directory` (see :ref:`central-policies`).

.. _software-policyupdate:

.. figure:: /images/software_policy.*
   :alt: Updating UCS systems using an update policy

   Updating UCS systems using an update policy

A release update is only run when the *Activate release updates* selection field
is activated.

The *Update to this UCS version* input field includes the version number up to
which the system should be updated, for example ``5.0-0``. If no entry is made,
the system continues updating to the highest available version number.

The point at which the update should be performed is configured via a
:guilabel:`Maintenance` policy (see
:ref:`computers-softwaremanagement-maintenancepolicy`).

The messages created during the update are written to the file
:file:`/var/log/univention/updater.log`.

.. _computers-postprocessing-of-release-updates:

Postprocessing of release updates
---------------------------------

Once a release update has been performed successfully, a check should be
made for whether new or updated join scripts need to be run.

Either the UMC module :guilabel:`Domain join` or the command
line program :command:`univention-run-join-scripts` is used
for checking and starting the join scripts (see
:ref:`linux-domain-join`).

.. _computers-troubleshooting:

Troubleshooting in case of update problems
------------------------------------------

The messages generated during updates are written to the
:file:`/var/log/univention/updater.log` file, which can
be used for more in-depth error analysis.

The status of the |UCSUCR| variables before the release update is saved in
the :file:`/var/univention-backup/update-to-TARGETRELEASEVERSION/`
directory. This can then be used to check whether and which variables
have been changed during the update.

.. _software-configrepo:

Configuration of the repository server for updates and package installations
============================================================================

Package installations and updates can either be performed from the Univention
update server or from a locally maintained repository. A local repository is
practical if there are a lot of UCS systems to update as the updates only need
to be downloaded once in this case. As repositories can also be updated offline,
a local repository also allows the updating of UCS environments without Internet
access.

A local repository can require a lot of disk space.

Using the registered settings, APT package sources are automatically generated
in the :file:`/etc/apt/sources.list.d/` directory for release and errata updates
as well as addon components. If further repositories are required on a system,
these can be entered in the :file:`/etc/apt/sources.list` file.

By default the Univention repository ``updates.software-univention.de`` is used
for a new installation.

The Univention repository contains all packages provided by Univention and
Debian. A distinction is made between maintained and unmaintained packages.

* All packages in the standard package scope are in *maintained* status.
  Security updates are provided in a timely manner only for *maintained*
  packages. The list of *maintained* packages can be viewed on a UCS system in
  :file:`univention-errata-level/maintained-packages.txt`.

* *unmaintained* packages are not covered by security updates or other
  maintenance. To check if *unmaintained* packages are installed, the command
  :command:`univention-list-installed-unmaintained-packages` can be executed.

For additional repositories the installation of *unmaintained* packages is not
possible by default. To enable installation, the |UCSUCRV|
:envvar:`repository/online/component/.*/unmaintained` must be set to ``yes``.

.. _computers-configuration-via-the-univention-management-console:

Configuration via |UCSUMC| module
---------------------------------

The :guilabel:`Repository server` can be specified in the UMC
module :guilabel:`Repository Settings`.

.. _computers-configuration-via-univention-configuration-registry:

Configuration via Univention Configuration Registry
---------------------------------------------------

The repository server to be used can be entered in the |UCSUCRV|
:envvar:`repository/online/server` and is preset to
``updates.software-univention.de`` for a new installation.

.. _computers-policy-based-configuration-of-the-repository-server:

Policy-based configuration of the repository server
---------------------------------------------------

The repository server to be used can also be specified using the *Repository
server* policy in the |UCSUMC| module :guilabel:`Computers`. Only UCS server
systems for which a DNS entry has been configured are shown in the selection
field (see :ref:`central-policies`).

.. _software-createrepo:

Creating and updating a local repository
----------------------------------------

Package installations and updates can either be performed from the Univention
update server or from a locally maintained repository. A local repository is
practical if there are a lot of UCS systems to update as the updates only need
to be downloaded once in this case. As repositories can also be updated offline,
a local repository also allows the updating of UCS environments without Internet
access.

The local repository can be activated/deactivated using the |UCSUCRV|
:envvar:`local/repository`.

There is also the possibility of synchronizing local repositories, which means,
for example, a main repository is maintained at the company headquarters and
then synchronized to local repositories at the individual locations.

To set up a repository, the :command:`univention-repository-create` command must
be run as the ``root`` user.

The packages in the repository can be updated using the
:command:`univention-repository-update` tool. With
:command:`univention-repository-update net` the repository is synchronized with
another specified repository server. This is defined in the |UCSUCRV|
:envvar:`repository/mirror/server` and typically points to
``updates.software-univention.de``.

An overview of the possible options is displayed with the following command:

.. code-block:: console

   $ univention-repository-update -h


The repository is stored in the :file:`/var/lib/univention-repository/mirror/`
directory.

.. _computers-softwaremanagement-installsoftware:

Installation of further software
================================

The initial selection of the software components of a UCS system is performed
within the scope of the installation. The software components are selected
relative to the functions, whereby e.g. the *Proxy server* component is
selected, which then procures the actual software packages via a meta package.
The administrator does not need to know the actual package names. However,
individual packages can also be specifically installed and removed for further
tasks. When installing a package, it is sometimes necessary to install
additional packages, which are required for the proper functioning of the
package. These are called package dependencies. All software components are
loaded from a repository (see :ref:`software-configrepo`).

Software which is not available in the Debian package format should be installed
into the :file:`/opt/` or :file:`/usr/local/` directories. These directories are
not used for installing UCS packages, thus a clean separation between UCS
packages and other software is ensured.

There are several possibilities for installing further packages subsequently on
an installed system, as the following sections describe.

.. _computers-softwareselection:

Installation/uninstallation of UCS components in the Univention App Center
--------------------------------------------------------------------------

All software components offered in the Univention Installer can also be
installed and removed at a later point in time via the Univention App Center.
This is done by selecting the *UCS components* package category. Further
information on the Univention App Center can be found in
:ref:`software-appcenter`.

.. _appcenter-ucscomponents:

.. figure:: /images/appcenter-ucs.*
   :alt: Selection of UCS components in the App Center

   Selection of UCS components in the App Center

.. _computers-installation-removal-of-individual-packages-in-the-univention-management-console:

Installation/removal of individual packages via |UCSUMC| module
---------------------------------------------------------------

The UMC module :guilabel:`Package Management` can be used to
install and uninstall individual software packages.

.. _software-umcinstall:

.. figure:: /images/software_install.*
   :alt: Installing the package univention-squid via |UCSUMC| module 'Package management'

   Installing the package :program:`univention-squid` via |UCSUMC| module
   'Package management'

A search mask is displayed on the start page in which the user can
select the package category or a search filter (name or description).
The results are displayed in a table with the following columns:

-  Package name

-  Package description

-  Installation status

Clicking an entry in the result list opens a detailed information page
with a comprehensive description of the package.

In addition, one or more buttons will be displayed. They have the following
meanings:

Install
   is displayed if the software package is not installed yet.

Uninstall
   is displayed if the software package is installed.

Upgrade
   is displayed if the software package is installed but not updated.

Close
   can be used for returning to the previous search request.

.. _computers-installation-removal-of-individual-packages-in-the-command-line:

Installation/removal of individual packages in the command line
---------------------------------------------------------------

The following steps must be performed with ``root`` user rights.

Individual packages are installed using the command:

.. code-block:: console

   $ univention-install PACKAGENAME


Packages can be removed with the following command:

.. code-block:: console

   $ univention-remove PACKAGENAME

If the name of a package is unknown, the command :command:`apt-cache search` can
be used to search for the package. Parts of the name or words which appear in
the description of the package are listed, for example:

.. code-block:: console

   $ apt-cache search fax


.. _computers-installation-and-remove-hooks:

Hook scripts for administrators
-------------------------------

Custom scripts can be called after each app installation, -upgrade or -removal.
Such scripts can be used to automate repeating administrative tasks.

To use this feature custom scripts can be placed in one of the directories
listed below. If such a directory does not yet exist, it can be manually
created:

* :file:`/var/lib/univention-appcenter/apps/{{appid}}/local/hooks/post-install.d/`
* :file:`/var/lib/univention-appcenter/apps/{{appid}}/local/hooks/post-upgrade.d/`
* :file:`/var/lib/univention-appcenter/apps/{{appid}}/local/hooks/post-remove.d/`

Where ``{appid}`` is the name of the app for which the scripts should be
executed.

Script file names are only allowed to consist of lower case letters and numbers
(``^[a-z0-9]+$``). Additionally scripts have to be marked as executable
(:command:`chmod +x [filename]`), because they are internally called by
:program:`run-parts`. As a consequence :command:`run-parts --test [directory]`
can be used to verify if and which files would be executed. Further information
can be found in the manual with :command:`man run-parts`.

The :file:`/var/log/univention/appcenter.log` contains
possible scripting error messages and further hints.

.. _computers-softwaremanagement-packagelists:

Policy-based installation/uninstallation of individual packages via package lists
---------------------------------------------------------------------------------

Package lists can be used to install and remove software using policies.  This
allows central software deployment for a large number of computer systems.

Each system role has its own package policy type.

Package policies are managed in the UMC module :guilabel:`Policies` with the
*Policy: Packages + system role*.

.. list-table:: 'General' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - Name
     - An unambiguous name for this package list, e.g., *mail server*.

   * - Package installation list
     - A list of packages to be installed.

   * - Package removal list
     - A list of packages to be removed.

The software packages defined in a package list are installed/uninstalled at the
time defined in the :guilabel:`Maintenance` policy (for the configuration see
:ref:`computers-softwaremanagement-maintenancepolicy`).

The software assignable in the package policies are also registered in the LDAP.

.. _computers-softwaremanagement-maintenancepolicy:

Specification of an update point using the package maintenance policy
=====================================================================

A *Maintenance* policy (see :ref:`central-policies`) in the UMC modules for
computer and domain management can be used to specify a point at which the
following steps should be performed:

-  Check for available release updates to be installed (see :ref:`computers-softwaremanagement-releasepolicy`) and, if
   applicable, installation.

-  Installation/uninstallation of package lists (see :ref:`computers-softwaremanagement-packagelists`)

-  Installation of available errata updates

Alternatively, the updates can also be performed when the system is
booting or shut down.

.. list-table:: 'General' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - Perform maintenance after system startup
     - If this option is activated, the update steps are performed when the
       computer is started up.

   * - Perform maintenance before system shutdown
     - If this option is activated, the update steps are performed when the
       computer is shut down.

   * - Use Cron settings
     - If this flag is activated, the fields *Month*, *Day of week*, *Day*,
       *Hour* and *Minute* can be used to specify an exact time when the update
       steps should be performed.

   * - Reboot after maintenance
     - This option allows you to perform an automatic system restart after
       release updates either directly or after a specified time period of
       hours.

.. _computers-softwaremonitor:

Central monitoring of software installation statuses with the software monitor
==============================================================================

.. index:: DNS record; _pkgdb._tcp

The software monitor is a database in which information is stored concerning the
software packages installed across all UCS systems. This database offers an
administrator an overview of which release and package versions are installed in
the domain and offers information for the step-by-step updating of a UCS domain
and for use in identifying problems.

The software monitor can be installed from the Univention App Center with the
application :program:`Software installation monitor`. Alternatively, the
software package :program:`univention-pkgdb` can be installed. Additional
information can be found in :ref:`computers-softwaremanagement-installsoftware`.

UCS systems update their entries automatically when software is installed,
uninstalled or updated. The system on which the software monitor is operated is
located by the DNS service record ``_pkgdb._tcp``.

The software monitor brings its own UMC module :guilabel:`Software monitor`. The
following functions are available:

Systems
   allows to search for the version numbers of installed systems. It is possible
   to search for system names, UCS versions and system roles.

Packages
   allows to search in the installation data tracked by the package status
   database. Besides searching for a *Package name* there are various search
   possibilities available for the installation status of packages:

   Selection state
      The *selection state* influences the action taken when updating a package.
      ``Install`` is used to select a package for installation. If a package is
      configured to ``Hold`` it will be excluded from further updates.  There are
      two possibilities for uninstalling a package: A package removed with
      ``DeInstall`` keeps locally created configuration data, whilst a package
      removed with ``Purge`` is completely deleted.

   Installation state
      The *installation state* describes the status of an installed package in
      relation to upcoming updates. The normal status is ``Ok``, which leads to a
      package being updated when a newer version exists. If a package is configured
      to ``Hold`` it will be excluded from the update.

   Package state
      The *package state* describes the status of a set-up package. The normal status
      here is ``Installed`` for installed packages and ``ConfigFiles`` for removed
      packages. All other statuses appear when the package's installation was
      canceled in different phases.

.. _software-monitor:

.. figure:: /images/software_softwaremonitor.*
   :alt: Searching for packages in the software monitor

   Searching for packages in the software monitor

If you do not wish UCS systems to store installation processes in the software
monitor (e.g., when there is no network connection to the database), this can be
arranged by setting the |UCSUCRV| :envvar:`pkgdb/scan` to ``no``.

Should storing be reactivated at a later date, the command
:command:`univention-pkgdb-scan` must be executed to ensure that package
versions installed in the meanwhile are also adopted in the database.

The following command can be used to remove a system's program inventory from
the database again:

.. code-block:: console

   $ univention-pkgdb-scan --remove-system [HOSTNAME]

