.. _central-general:

|UCSWEB|
========

.. highlight:: console

.. _central-management-umc-introduction:

Introduction
------------

.. _fig-ucs-portal:

.. figure:: /images/portal.*
   :alt: UCS portal page

   UCS portal page

The |UCSWEB| is the central tool for managing a UCS domain as well as for
accessing installed applications of the domain.

The |UCSWEB| is divided into several subpages which all have a similarly
designed header. Via the symbols in the top right, one may launch a search on
the current page (magnifier) or open the user menu (three bars) (login is
possible through the latter). The login at the web interface is done via a
central page once for all sub pages of UCS as well as for third party
applications as far as a web based *single sign-on* is supported
(:ref:`central-management-umc-login`).

Central starting point for users and administrators for all following
actions is the UCS portal page (cf. :numref:`fig-ucs-portal`). By
default, the portal page is available on all system roles and allows an
overview of all Apps and further services which are installed in the UCS
domain. All aspects of the portal page can be customized to match one's
needs (:ref:`central-portal`).

For environments with more than one server, an additional entry to a
server overview page is shown on the portal page. This sub page gives an
overview of all available UCS systems in the domain. It allows a fast
navigation to other systems in order to adjust local settings via UMC
modules.

UMC modules are the web based tool for the administration of the UCS
domain. There are various modules available for the administration of
the different aspects of a domain depending on the respective system
role. Installing additional software components may add new UMC modules
to the system. :ref:`central-user-interface` describes
their general operation.

The subsequent sections detail the usage of various aspects of the domain
management. :ref:`central-navigation` gives an overview of the LDAP directory
browser. The use of administrative settings via policies is discussed in
:ref:`central-policies`. How to extend the scope of function of the domain
administration is detailed in :ref:`central-extended-attrs`.
:ref:`central-cn-and-ous` details how containers and organizational units can be
used to structure the LDAP directory. :ref:`delegated-administration` explains
delegating administration rights to additional user groups.

In conclusion, the command line interface of the domain administration is
illustrated (:ref:`central-udm`), and the evaluation of domain data via the UCS
reporting function are explained (:ref:`central-reports`).

.. _central-access:

Access
~~~~~~

The |UCSWEB| can be opened on any UCS system via the URL
``https://servername/``. Alternatively, access is also possible via the server's
IP address. Under certain circumstances it may be necessary to access the
services over an insecure connection (e.g., if no SSL certificates have been
created for the system yet). In this case, ``http`` must be used instead of
``https`` in the URL. In this case, passwords are sent over the network in plain
text!

.. _central-browser-compatibility:

Browser compatibility
~~~~~~~~~~~~~~~~~~~~~

The |UCSWEB| uses numerous JavaScript and CSS functions. Cookies need to be
permitted in the browser. The following browsers are supported:

* :program:`Chrome` as of version 85

* :program:`Firefox` as of version 78

* :program:`Microsoft Edge` as of version 88

* :program:`Safari` and :program:`Safari Mobile` as of version 13

Users with older browsers may experience display problems or the site does not
work at all.

The |UCSWEB| is available in German and English (and French if it is chosen as
language during the installation from DVD); the language to be used can be
changed via the entry :guilabel:`Switch language` of the user menu in the upper
right corner.

.. _central-theming:

Switching between dark and light theme for |UCSWEB|\ s
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All |UCSWEB|\ s have a dark and a light theme that can be switched between with
the |UCSUCRV| :envvar:`ucs/web/theme`. The value of :envvar:`ucs/web/theme`
corresponds to a CSS file under :file:`/usr/share/univention-web/themes/` with
the same name (without file extension). For example, setting
:envvar:`ucs/web/theme` to ``light`` will use
:file:`/usr/share/univention-web/themes/light.css` as theme for all |UCSWEB|\ s.

.. _central-theming-custom:

Creating a custom theme/Adjusting the design of |UCSWEB|\ s
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a custom theme it is advised not to edit
:file:`/usr/share/univention-web/themes/dark.css` or
:file:`/usr/share/univention-web/themes/light.css` since
the changes may be overwritten when upgrading UCS. Instead copy one of
these files to e.g.
:file:`/usr/share/univention-web/themes/mytheme.css` and
set the |UCSUCRV| :envvar:`ucs/web/theme` to
``mytheme``.

The files :file:`/usr/share/univention-web/themes/dark.css` and
:file:`/usr/share/univention-web/themes/light.css` contain the same list of `CSS
variables
<https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties>`_.
These variables are used in other CSS files and are the supported layer of
configurability for |UCSWEB|\ s. The names and current use case for these
variables will not change between UCS upgrades but new ones may be added.

Some |UCSWEB|\ s import their own local :file:`custom.css` file which can be
used to further adjust the design of that page. These are
:file:`/usr/share/univention-management-console-login/css/custom.css`
(:ref:`domain-saml-ssologin`) and
:file:`/usr/share/univention-portal/custom.css` (:ref:`central-portal`). The
files are empty when installing UCS and are not modified when installing any UCS
update. Be aware though that a given `CSS selector
<https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors>`__
may break when installing any UCS update.

.. _central-management-umc-feedback:

Feedback on UCS
~~~~~~~~~~~~~~~

By choosing the :menuselection:`Help --> Feedback` option in the upper right
menu, you can provide feedback on UCS via a web form.

.. _central-management-umc-piwik:

Collection of usage statistics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Anonymous usage statistics on the use of the |UCSWEB| are collected when using
the *core edition* version of UCS (which is generally used for evaluating UCS).
Further information can be found in @@u:@@sdb>1318</u:sdb>.

.. _central-management-umc-login:

Login
-----

.. _umc-login:

.. figure:: /images/umc_login.*
   :alt: UCS login page

   UCS login page

UCS comes with a central login page. Logging in to the |UCSWEB| is done with the
credentials of the respective domain account. On the portal, the login process
can be started either via the user menu an then :guilabel:`Login` or by clicking
on the entry in the portal itself. If a site (e.g., a UMC module) requires a
login, it will redirect to the central login page. To log out, the entry
:guilabel:`Logout` in the user menu can be used.

By default a login does not use single sign-on. The login can be changed to use
single sign-on (SSO) via SAML (:ref:`domain-saml`). To configure this,
``ucs-sso.[Domain name]`` must be reachable and the |UCSUCRV|
:envvar:`portal/auth-mode` has to be set to ``saml``. For the change to take
effect the portal server needs to be restarted: :command:`systemctl restart
univention-portal-server.service`. The login using the user menu has now be
changed. Portal tiles have to be adapted manually. The default portal has a SSO
login tile preconfigured which can be activated using the portal edit mode.

After successful login, a session is valid for all UCS systems of the domain as
well as for third party Apps if these support web based SSO.  It is possible to
enforce a login on the local system by clicking on the link :guilabel:`Login
without Single Sign On`.

In the login mask, enter the :guilabel:`Username` and :guilabel:`Password` of
the corresponding domain account:

* When logging in with the ``Administrator`` account on a |UCSPRIMARYDN| or
  |UCSBACKUPDN|, UMC modules for the administration and configuration of the
  local system as well as UMC modules for the administration of data in the LDAP
  directory are displayed. The initial password of this account has been
  specified in the setup wizard during the installation. It corresponds to the
  initial password of the local ``root`` account.  ``Administrator`` is also the
  account which should be used for the initial login at a newly installed
  |UCSPRIMARYDN|\ system.

* In some cases, it might be necessary to log on with the system's local
  ``root`` account (see :ref:`computers-rootaccount`). This account enables
  access only to the UMC modules for the administration and configuration of the
  local system.

* When logging on with another user account, the UMC modules approved
  for the user are shown. Additional information on allowing further
  modules can be found in :ref:`delegated-administration`.

The duration of a browser session is 8 hours for the SSO login. After these, the
login process must be carried out again. For the login at the local UCS system,
the browser session will be automatically closed after an inactivity of 8 hours.

By installing a third-party application, such as :program:`privacyIDEA`, it is
possible to extend the |UCSWEB| authentication with a two-factor authentication
(2FA). These extensions can be installed from the Univention App Center.

.. _central-portal:

UCS portal page
---------------

Portal pages offer a central view of all available services in a UCS domain.
Requirements strongly differ from small to large environments in organizations,
public authorities, or even schools. Therefore, UCS implemented a very flexible
and individually customizable concept for portal pages.

As illustrated in :numref:`portal-schema`, portal entries (i.e., links
to applications/Apps/services; UDM object type ``portals/entry``) can be
assigned to none, one or multiple portal categories. A portal category
(UDM object type ``portals/category``) can be assigned to none, one or
multiple portals. A portal itself (UDM object type ``portals/portal``)
renders all portal categories which are assigned to it.

The portal *domain*, shipped with every installation, is configured on each
server by default. In addition to all installed applications of the domain,
links to |UCSUMC| as well as the server overview are shown on this portal page.

Custom portals and portal entries can be defined and managed either via the UMC
module :guilabel:`Portal` or directly on the portal site.

After logging in to the portal on the |UCSPRIMARYDN| or |UCSBACKUPDN|, members
of the ``Domain Admins`` group can edit the portal after clicking on the
corresponding entry in the user menu. They now can create new entries on the
portal, modify existing entries, modify the order or the design.

Advanced settings, such as adding new portals or setting which group members can
see which portal entries can be made using the UMC portal settings module.

By default, all portal entries are displayed for everyone. In the UMC module
:guilabel:`Portal` in the category :guilabel:`Login`, it can be configured
whether anonymous visitors have to log in before they can see entries. It is
also possible to limit certain entries for certain groups. This requires the
LDAP attribute ``memberOf``. Nested group memberships (i.e., groups in groups)
are evaluated.

Further design adjustments can be made in the file
:file:`/usr/share/univention-portal/css/custom.css`.  This file will not be
overwritten during an update.

.. _portal-schema:

.. figure:: /images/portal-schema.*
   :alt: Schema of the portal concept in UCS

   Schema of the portal concept in UCS: Portals can be independently defined and
   assigned to UCS systems as start site; a link entry can be displayed on
   multiple portals.

.. _central-management-umc-assignment-of-portal-settings-module:

Assign rights for portal settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following describes how to make the UMC module :guilabel:`Portal` accessible
to selected groups or users.  This example assumes that a group
:guilabel:`Portal Admins` has been created and members of this group are
supposed to be given access to the portal settings.

On a |UCSPRIMARYDN| an ACL file has to be created first, for example
:file:`/opt/62my-portal-acl.acl`.  This file has to have the following content
to allow the necessary ACL changes:

.. code-block::

   access to dn="cn=portal,cn=univention,@%@ldap/base@%@" attrs=children
     by group/univentionGroup/uniqueMember="cn=Portal Admins,cn=groups,@%@ldap/base@%@" write
     by * +0 break

   access to dn.children="cn=portal,cn=univention,@%@ldap/base@%@" attrs=entry,@univentionObject,@univentionPortalEntry,
   @univentionPortal,@univentionPortalCategory,children
     by group/univentionGroup/uniqueMember="cn=Portal Admins,cn=groups,@%@ldap/base@%@" write
     by * +0 break


Then execute the following command to create an LDAP object for the LDAP ACLs:

.. code-block:: console

   $ udm settings/ldapacl create \
   > --position "cn=ldapacl,cn=univention,$(ucr get ldap/base)" \
   > --set name=62my-portal-acl \
   > --set filename=62my-portal-acl \
   > --set data="$(bzip2 -c /opt/62my-portal-acl.acl | base64)" \
   > --set package="62my-portal-acl" \
   > --set packageversion=1


If the ACL is to be deleted again, the following command can be used:

.. code-block::

   udm settings/ldapacl remove \
     --dn "cn=62my-portal-acl,cn=ldapacl,cn=univention,$(ucr get ldap/base)"
           

An appropriate UMC policy can now be created via UMC. The following
*UMC operations* must be allowed within the policy:

* *udm-portal*
* *udm-syntax*,
* *udm-validate*
* *udm-license*

How to create a policy is described in
:ref:`central-management-umc-create-policy`. Now the newly created policy only
needs to be assigned to the desired object, in this case the group ``Portal
Admins``. This can also be done directly within the UMC. For this example,
navigate to the group module and edit the desired group there. In the group
settings, existing policies for the group object can be selected under
:guilabel:`Policies`. More detailed information about policy assignment is
described under :ref:`central-policies-assign`.

.. _central-user-interface:

|UCSUMC| modules
----------------

.. _central-management-umc:

Introduction
~~~~~~~~~~~~

|UCSUMC| (UMC) modules are the web-based tool for administration of the UCS
domain. They are shown on the portal page (:ref:`central-portal`) for logged in
administrators. Depending on the system role, different UMC modules are
available. Additionally installed software components may bring their own new
UMC modules.

UMC modules for the administration of all the data included in the LDAP
directory (such as users, groups and computer accounts) are only provided on
|UCSPRIMARYDN|\ s and |UCSBACKUPDN| s. Changes made in these modules are applied
to the whole domain.

UMC modules for the configuration and administration of the local system are
provided on all system roles. These modules can for example be used to install
additional applications and updates, adapt the local configuration via |UCSUCR|
or start/stop services.

.. _central-license:

Activation of UCS license / license overview
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The UCS license of a domain can be managed on the |UCSPRIMARYDN| via the
UMC module :guilabel:`Welcome!`.

The current license status can be shown by clicking the :guilabel:`License info`
button.

.. _umc-license:

.. figure:: /images/umc_coreedition.*
   :alt: Displaying the UCS license

   Displaying the UCS license

The button :guilabel:`Import a license` opens a dialogue in which a new license
key can be activated (otherwise the core edition license is used as default
license). A license file can be selected and imported via the button
:guilabel:`Import from file...`.  Alternatively, the license key can also be
copied into the input field below and activated with :guilabel:`Import from text
field`.

Installation of most of the applications in the Univention App Center requires a
personalized license key. UCS core edition licenses can be converted by clicking
:guilabel:`Request a new license`. The current license key is sent to Univention
and the updated key returned to a specified e-mail address within a few minutes.
The new key can be imported directly. The conversion does not affect the scope
of the license.

If the number of licensed user or computer objects is exceeded, it is not
possible to create any additional objects in UMC modules or edit any existing
ones unless an extended license is imported or no longer required users or
computers are deleted. A corresponding message is displayed when opening a UMC
module if the license is exceeded.

.. _central-management-umc-operating-instructions-for-domain-modules:

Operating instructions for modules to administrate LDAP directory data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All UMC modules for managing LDAP directory objects such as user, group
and computer accounts or configurations for printers, shares, mail and
policies are controlled identically from a structural perspective. The
following examples are presented using the user management but apply
equally for all modules. The operation of the DNS and DHCP modules is
slightly different. Further information can be found in
:ref:`ip-config-dns-umc` and :ref:`networks-dhcp-general`.

.. _umc-modules:

.. figure:: /images/umc-favorites-tab.*
   :alt: Module overview

   Module overview

The configuration properties/possibilities of the modules are described in the
following chapters:

-  Users - :ref:`users-general`

-  Groups - :ref:`groups`

-  Computers - :ref:`computers-general`

-  Networks - :ref:`networks-introduction`

-  DNS - :ref:`networks-dns`

-  DHCP - :ref:`module-dhcp-dhcp`

-  Shares - :ref:`shares-general`

-  Printers - :ref:`print-general`

-  E-mail - :ref:`mail-general`

-  Nagios - :ref:`nagios-general`

The use of policies (:ref:`central-policies`) and the LDAP navigation
(:ref:`central-navigation`) are described separately.

.. _umc-usage-search:

Searching for objects
^^^^^^^^^^^^^^^^^^^^^

The module overview lists all the objects managed by this module.  *Search*
performs a search for a selection of important attributes (e.g., for user
objects by first and last name, primary e-mail address, description, employee
number and user name). A wildcard search is also possible, e.g.,
``m*``.

Clicking on the :guilabel:`Advanced options` button (the filter icon) next to
the input field displays additional search options:

* The :guilabel:`Search in` field can be used to select whether the complete
  LDAP directory or only individual LDAP containers/OUs are searched. Further
  information on the structure of the LDAP directory service can be found in
  :ref:`central-cn-and-ous`.

* The :guilabel:`Property` field can be used to search for a certain attribute
  directly.

* The majority of the modules administrate a range of types of LDAP objects; the
  computer management for example administrates different objects for the
  individual system roles. The search can be limited to one type of LDAP object.

* Some of the internally used user groups and groups (e.g., for domain joins)
  are not shown by default. If the :guilabel:`Include hidden objects` option is
  enabled, these objects are also shown.

.. _umc-search:

.. figure:: /images/umc_user.*
   :alt: Searching for users

   Searching for users

.. _central-management-umc-create:

Creating objects
^^^^^^^^^^^^^^^^

At the top of the table that shows the objects is a toolbar which can be used to
create a new object using :guilabel:`Add`.

There are simplified wizards for some UMC modules (users, hosts), in which only
the most important settings are requested. All attributes can be shown by
clicking on :guilabel:`Advanced`.

.. _central-user-interface-edit:

Editing objects
^^^^^^^^^^^^^^^

Right-clicking on an LDAP object and selecting :guilabel:`Edit` allows to edit
the object. The individual attributes are described in the individual
documentation chapters. By clicking on :guilabel:`Save` at the top of the
module, all changes are written into the LDAP directory. The :guilabel:`Back`
button cancels the editing and returns to the previous search view.

In front of every item in the result list is a checkbox with which individual
objects can be selected. The selection status is also displayed in toolbar at
the top of the table, e.g., *2 users of 102 selected*. If more than one object
is selected, clicking on the :guilabel:`Edit` button in the toolbar activates
the multi edit mode. The same attributes are now shown as when editing an
individual object, but the changes are only accepted for the objects where the
:guilabel:`Overwrite` checkbox is activated. Only objects of the same type can
be edited at the same time.

.. _central-user-interface-remove:

Deleting objects
^^^^^^^^^^^^^^^^

Right-clicking on an LDAP object and selecting :guilabel:`Delete` allows to
delete the object. The prompt must be confirmed. Some objects use internal
references (e.g., a DNS or DHCP object can be associated with computer objects).
These can also be deleted by selecting the :guilabel:`Delete referring objects`
option.

Similar to editing multiple objects at once, multiple objects can be deleted at
once via the :guilabel:`Delete` button in the toolbar.

.. _central-user-interface-move:

Moving objects
^^^^^^^^^^^^^^

Right-clicking on an LDAP object and selecting :guilabel:`Move to...` allows to
to select an LDAP position to which the object should be moved.

Similar to editing multiple objects at once, multiple objects can be moved at
once by selecting :menuselection:`More --> Move to...` in the toolbar.

.. _central-management-umc-notifications:

Display of system notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UMC modules can deploy system notifications to alert the user to potential
errors like join scripts which have not been run or necessary actions such as
available updates. These notifications are shown in the top right corner of the
screen and can be viewed again in the Notifications menu, which can be opened by
clicking the bell icon in the top right corner of the screen.

.. _central-navigation:

LDAP directory browser
----------------------

The UMC module :guilabel:`LDAP directory` can be used to navigate through the
LDAP directory. When doing so, new objects can be created, modified or deleted
in the LDAP directory.

.. _umc-navigation:

.. figure:: /images/umc_navigation.*
   :alt: Navigating the LDAP directory

   Navigating the LDAP directory

The left half of the screen shows the LDAP directory as a tree structure whose
elements can be shown and hidden using the arrow icons.

Clicking on an element of the tree structure switches to this LDAP position and
displays the objects at this LDAP position in the in the right side of the
screen. The *Type* selection list can be used to limit the display to
selected attributes.

The :guilabel:`Add` button can be used to add new objects here too. Similar to
the control elements described in :ref:`central-user-interface`, existing
objects can also be edited, deleted or moved here.

.. _umc-container-edit:

.. figure:: /images/umc_navigation_edit.*
   :alt: Editing LDAP container settings

   Editing LDAP container settings

Right-clicking on an element in the tree structure allows editing the properties
of the container or the LDAP base with :guilabel:`Edit`.

.. _central-policies:

Policies
--------

*Policies* describe administrative settings which can practically be used on
more than one object. They facilitate the administration as they can be
connected to containers and then apply to all the objects in the container in
question and the objects in sub containers. The values are applied according to
the inheritance principle. For every object, the applied value is always that
which lies closest to the object in question.

If, for example, the same password expiry interval is to be defined for all
users of a location, then a special container can be created for these users.
After moving the user objects into the container, a password policy can be
linked to the container. This policy is valid for all user objects within the
container.

An exception to this rule is a value which was defined in a policy in the form
of *fixed attributes*. Such values cannot be overwritten by subordinate
policies.

The command line program :command:`univention-policy-result` can be used to show
in detail which policy applies to which directory service object.

Every policy applies to a certain type of UMC domain object, e.g., for users or
DHCP subnets.

.. _central-management-umc-create-policy:

Creating a policy
~~~~~~~~~~~~~~~~~

Policies can be managed via the UMC module :guilabel:`Policies`. The operation
is the same as for the functions described in :ref:`central-user-interface`.

The attributes and properties of the policies are described in the corresponding
chapters, e.g. the DHCP policies in the network chapter.

The names of policies must not contain any umlauts.

:guilabel:`Referencing objects` provides a list of all containers or LDAP
objects for which this policy currently applies.

The expanded settings host some general policy options which are generally only
required in special cases.

LDAP filter
   A LDAP filter expression can be specified here, which an object must match
   for this policy to get applied.

Required object classes
   Here you can specify LDAP object classes that an object must possess for the
   policy to apply to this object. If, for example, a user policy is only
   relevant for Windows environments, the ``sambaSamAccount`` object class could
   be demanded here.

Excluded object classes
   Similar to the configuration of the required object classes, you can also
   list object classes here which should be excluded.

Fixed attributes
   Attributes can be selected here, the values of which may not be changed by
   subordinate policies.

Empty attributes
   Attributes can be selected here, which are to be set to empty in the policy,
   meaning they will be stored without containing a value. This can be useful
   for removing values inherited by an object from a superordinate policy. In
   subordinate policies, new values can be assigned to the attributes in
   question.

.. _central-policies-assign:

Applying policies
~~~~~~~~~~~~~~~~~

Policies can be assigned in two ways:

* A policy can be assigned to the LDAP base or a container/OU. To do so, the
  :guilabel:`Policies` tab in the properties of the LDAP object must be opened
  in the navigation (see :ref:`central-navigation`).

* A *Policies* tab is shown in the UMC modules of LDAP directory
  objects for which there are policies available (e.g., for users). A particular
  policy for a user can be specified at this place.

The :guilabel:`Policies` configuration dialogue is functionally identical;
however, all policy types are offered when assigning policies to a LDAP
container, whilst only the policy types applicable for the object type in
question are offered when assigning policies to an LDAP object.

A policy can be assigned to the LDAP object or container under *Policies*. The
values resulting from this policy are displayed directly. The
:guilabel:`Inherited` setting means that the settings are adopted from a
superordinate policy again - when one exists.

If an object is linked to a policy, or inherits policy settings which cannot be
applied to the object, the settings remain without effect for the object. This
makes it possible, for example, to assign a policy to the base entry of the LDAP
directory, which is then valid for all the objects of the domain which can apply
this policy. Objects which cannot apply to this policy are not affected.

.. _central-management-umc-edit-policy:

Editing a policy
~~~~~~~~~~~~~~~~

Policies can be edited and deleted in the UMC module :guilabel:`Policies`. The
interface is described in :ref:`central-user-interface`.

.. caution::

   When editing a policy, the settings for all the objects linked to this policy
   are changed! The values from the changed policy apply to objects already
   registered in the system and linked to the policy, in the same way as to
   objects added in the future.

The policy tab of the individual LDAP objects also includes the :guilabel:`edit`
option, which can be used to edit the policy currently applicable for this
object.

.. _central-extended-attrs:

Expansion of UMC modules with extended attributes
-------------------------------------------------

The domain management UMC modules allow the comprehensive management of the data
in a domain. *Extended attributes* offer the possibility of integrating new
attributes in the domain management which are not covered by the UCS standard
scope. Extended attributes are also employed by third party vendors for the
integration of solutions in UCS.

Extended attributes are managed in the UMC module :guilabel:`LDAP directory`.
There one needs to switch to the ``univention`` container and then to the
``custom attributes`` subcontainer. Existing attributes can be edited here or a
new :guilabel:`Settings: extended attribute` object created here with
:guilabel:`Add`.

.. _umc-extended-attrs-figure:

.. figure:: /images/umc_extended_attribute.*
   :alt: Extended attribute for managing a car license

Extended attributes can be internationalized. In this case, the name and
description should be compiled in English as this is the standard language for
UMC modules.

.. list-table:: 'General' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - Unique name
     - The name of the LDAP object which will be used to store the extended
       attribute. Within a container, the name has to be unique.

   * - UDM CLI name
     - The specified attribute name should be used when employing the command
       line interface |UCSUDM|. When the extended attribute is saved, the
       *Unique name* of the *General* tab is automatically adopted and can be
       subsequently modified.

   * - Short description
     - Used as title of the input field in UMC modules or as the attribute
       description in the command line interface.

   * - Translations of short description
     - Translated short descriptions can be saved in several languages so that
       the title of extended attributes is also output with other language
       settings in the respective national language. This can be done by
       assigning the respective short description to a language code (e.g.,
       ``de_DE`` or ``fr_FR``) in this input field.

   * - Long description
     - This long description is shown as a tool tip in the input fields in UMC
       modules.

   * - Translations of long description
     - Additional information displayed in the tool tip for an extended
       attribute can also be saved for several languages. This can be done by
       assigning the respective long description to a language code (e.g.,
       ``de_DE`` or ``fr_FR``) in this input field.

.. list-table:: 'Module' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - Modules to be extended
     - The |UCSUDM| module which is to be expanded with the extended attribute.
       An extended attribute can apply for multiple modules.
   * - Required  options/object classes
     - Some extended attributes can only be used practically if certain object
       classes are activated on the :guilabel:`Options` tab. One or more options
       can optionally be saved in this input field so that this extended
       attribute is displayed or editable.
   * - Hook class
     - The functions of the hook class specified here are used during saving,
       modifying and deleting the objects with extended attributes. Additional
       information can be found in `Univention Developer Reference
       <https://docs.software-univention.de/developer-reference-5.0.html>`_.

.. list-table:: 'LDAP mapping' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - LDAP object class
     - Object class to which the attribute entered under *LDAP
       attribute* belongs.

       Predefined LDAP schema extensions for extended attributes are provided
       with the object class ``univentionFreeAttributes``. Further information
       can be found in :ref:`domain-ldap-extensions`.

       Each LDAP object which should be extended with an attribute is
       automatically extended with the LDAP object class specified here if a
       value for the extended attribute has been entered by the user.

   * - LDAP attribute
     - The name of the LDAP attribute where the values of the LDAP object are to
       be stored. The LDAP attribute must be included in the specified object
       class.

   * - Remove object class if the attribute is removed
     - If the value of an extended attribute in a UMC module is deleted, the
       attribute is removed from the LDAP object. If no further attributes of
       the registered object class are used in this LDAP object, the *LDAP
       object class* will also be removed from the LDAP object if this option is
       activated.

.. list-table:: 'UMC' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - Do not show this extended attribute in UMC modules
     - This option can be activated if an attribute should only be administrated
       internally instead of by the administrator, e.g., indirectly by scripts.
       The attribute can then only be set via the command line interface
       |UCSUDM| and is not displayed in UMC modules.

   * - Exclude from from of UMC module
     - If it should not be possible to search for an extended attribute in the
       search window of a wizard, this option can be activated to remove the
       extended attribute from the list of possible search criteria.

       This is only needed in exceptional cases.

   * - Ordering number
     - If several extended attributes are to be managed on one tab, the order of
       the individual attributes on the tab can be influenced here. They are
       added to the end of the tab or the group in question in ascending order
       of their numbers.

       Assigning consecutive position numbers results in the attributes being
       ordered on the left and right alternately in two columns. Otherwise, the
       positioning starts in the left column. If additional attributes have the
       same position number, their order is random.

   * - Overwrite existing widget
     - In some cases it is useful to overwrite predefined input fields with
       extended attributes. If the internal UDM name of an attribute is
       configured here, its input field is overwritten by this extended
       attribute. The UDM attribute name can be identified with the command
       :command:`univention-directory-manager` (see :ref:`central-udm`). This
       option may cause problems if it is applied to a mandatory attribute.

   * - Span both columns
     - As standard all input fields are grouped into two columns. This option
       can be used for overlong input fields, which need the full width of the
       tab.

   * - Tab name
     - The name of the tab in UMC modules on which the extended attribute should
       be displayed.  New tabs can also be added here.

       If no tab name is entered, *user-defined* will be used.

   * - Translations of tab name
     - Translated tab names can be assigned to the corresponding language code
       (e.g.  ``de_DE`` or ``fr_FR``) in this input field.

   * - Overwrite existing tab
     - If this option is activated, the tab in question is overwritten before
       the extended attributes are positioned on it. This option can be used to
       hide existing input fields on a predefined tab. It must be noted that
       this option can cause problems with compulsory fields. If the tab to be
       overwritten uses translations, the overwriting tab must also include
       identical translations.

   * - Tab with advanced settings
     - Settings possibilities which are rarely used can be placed in the
       extended settings tab

   * - Group name
     - Groups allow the structuring of a tab. A group is separated by a gray
       horizontal bar and can be shown and hidden.

       If no group name is specified for an extended attribute, the attribute is
       placed above the first group entry.

   * - Translations of group name
     - To translate the name of the group, translated group names for the
       corresponding language code can be saved in this input field (e.g.,
       ``de_DE`` or ``fr_FR``).

   * - Group ordering number
     - If multiple groups are managed in one tab, this position number can be
       used to specify the order of the groups. They are shown in the ascending
       order of their position numbers.

.. list-table:: 'Data type' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - Syntax class
     - When values are entered in UMC modules, a syntax check is performed.

       Apart from standard syntax definitions (``string``) and (``integer``),
       there are three possibilities for expressing a binary condition. The
       syntax ``TrueFalse`` is represented at LDAP level using the strings
       ``true`` and ``false``, the syntax ``TrueFalseUpper`` corresponds to the
       OpenLDAP boolean values ``TRUE`` and ``FALSE`` and the syntax ``boolean``
       does not save any value or the string *1*.

       The syntax ``string`` is the default. An overview of the additionally
       available syntax definitions and instructions on integrating your own
       syntaxes can be found in `Univention Developer Reference
       <https://docs.software-univention.de/developer-reference-5.0.html>`_.

   * - Default value
     - If a preset value is defined here, new objects to be created will be
       initialized with this value. The value can still be edited manually
       during creation. Existing objects remain unchanged.

   * - Multi value
     - This option establishes whether a single value or multiple values can be
       entered in the input mask. The scheme definition of the LDAP attribute
       specifies whether one or several instances of the attribute may be used
       in one LDAP object.

   * - Value required
     - If this option is active, a valid value must be entered for the extended
       attribute in order to create or save the object in question.

   * - Editable after creation
     - This option establishes whether the object saved in the extended
       attribute can only be modified when saving the object, or whether it can
       also be modified subsequently.

   * - Value is only managed internally
     - If this option is activated, the attribute cannot be modified manually,
       neither at creation time, nor later. This is useful for internal state
       information configured through a hook function or internally inside a
       module.

   * - Copyable
     - Values of this extended attribute are automatically filled into the form
       when copying a object.

.. _central-cn-and-ous:

Structuring of the domain with user-defined LDAP structures
-----------------------------------------------------------

Containers and organizational units (OU) are used to structure the data in the
LDAP directory. There is no technical difference between the two types, just in
their application:

* Organizational units usually represent real, existing units such as a
  department in a company or an institution

* Containers are usually used for fictitious units such as all the computers
  within a company

Containers and organizational units are managed in the UMC module
:guilabel:`LDAP directory` and are created with :guilabel:`Add` and the object
types *Container: Container* and *Container: Organisational unit*.

Containers and OUs can in principle be added at any position in the LDAP;
however, OUs cannot be created below containers.

.. rubric:: General tab

.. list-table:: 'General' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - Name
     - A random name for the container / organizational unit.

   * - Description
     - A random description for the container / organizational unit.

.. rubric:: Advanced settings tab

.. list-table:: 'Advanced settings' tab
   :header-rows: 1

   * - Attribute
     - Description

   * - Add to standard ``[object type]`` containers
     - If this option is activated, the container or organizational unit will be
       regarded as a standard container for a certain object type.  If the
       current container is declared the standard user container, for example,
       this container will also be displayed in users search and create masks.

.. rubric:: Policies tag

The *Policies* tab is described in :ref:`central-policies-assign`.

.. _delegated-administration:

Delegated administration for UMC modules
----------------------------------------

By default only the members of the ``Domain Admins`` group can access all UMC
modules. Policies can be used to configure the access to UMC modules for groups
or individual users. For example, this can be used to assign a helpdesk team the
authority to manage printers without giving them complete access to the
administration of the domain.

UMC modules are assigned via a *UMC* policy which can be assigned to user and
group objects. The evaluation is performed additively, i.e., general access
rights can be assigned via ACLs assigned to groups and these rights can be
extended via ACLs bound to user (see :ref:`central-policies`).

In addition to the assignment of UMC policies, LDAP access rights need to be
taken into account, as well, for modules that manage data in the LDAP directory.
All LDAP modifications are applied to the whole UCS domain. Therefore by default
only members of the ``Domain Admins`` group and some internally used accounts
have full access to the UCS LDAP. If a module is granted via a UMC policy, the
LDAP access must also be allowed for the user/group in the LDAP ACLs. Further
information on LDAP ACLs can be found in :ref:`domain-ldap-acls`.

.. list-table:: Policy 'UMC'
   :header-rows: 1

   * - Attribute
     - Description

   * - List of allowed UCS operation sets
     - All the UMC modules defined here are displayed to the user or group to
       which this ACL is applied. The names of the domain modules begin with
       'UDM'.

.. caution::

   For access to UMC modules, only policies are considered that are assigned to
   groups or directly to user and computer accounts. Nested group memberships
   (i.e., groups in groups) are not evaluated.

.. _central-udm:

Command line interface of domain management (|UCSUDM|)
------------------------------------------------------

The |UCSUDM| is the command line interface alternative to the web-based
interface of the domain management UMC modules. It functions as a powerful tool
for the automation of administrative procedures in scripts and for the
integration in other programs.

|UCSUDM| can be started with the :command:`univention-directory-manager` command
(short form :command:`udm`) as the ``root`` user on the |UCSPRIMARYDN|.

UMC modules and |UCSUDM| use the same domain management modules, i.e., all
functions of the web interface are also available in the command line interface.

.. _central-udm-parms:

Parameters of the command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A complete list of available modules is displayed if the :command:`udm`` is run
with the ``modules`` parameter:

.. code-block:: console

   $ univention-directory-manager modules
   Available Modules are:
     computers/computer
     computers/domaincontroller_backup
     computers/domaincontroller_master
     computers/domaincontroller_slave
     [...]

There are up to five operations for every module:

list
   lists all existing objects of this type.

create
   creates a new object.

modify
   or the *editing* of existing objects.

remove
   deletes an object.

move
   is used to move an object to another position in the LDAP directory.

The possible options of a UDM module and the operations which can be used on it
can be output by specifying the operation name, e.g.,

.. code-block:: console

   $ univention-directory-manager users/user move
   [...]
   general options:
     --binddn                         bind DN
     --bindpwd                        bind password
     --bindpwdfile                    file containing bind password
   [...]
   create options:
     --position                       Set position in tree
     --set                            Set variable to value, e.g. foo=bar
   [...]
   modify options:
     --dn                             Edit object with DN
     --set                            Set variable to value, e.g. foo=bar
   [...]
   remove options:
     --dn                             Remove object with DN
     --superordinate                  Use superordinate module
   [...]
   list options:
     --filter                         Lookup filter
     --position                       Search underneath of position in tree
   [...]
   move options:
     --dn                             Move object with DN
     --position                       Move to position in tree
   [...]


The following command outputs further information, the operations and the
options for every module. This also displays all attributes of the module:

.. code-block::

   univention-directory-manager [category/modulename]


With the ``create`` operation, the attributes marked with ``*`` must be
specified when creating a new object.

Some attributes can be assigned more than one value (e.g., mail addresses to
user objects). These multi-value fields are marked with ``[]`` behind the
attribute name. Some attributes can only be set if certain options are set for
the object. This is performed for the individual attributes by entering the
option name:

.. code-block::

   users/user variables:
     General:
       username (*)                             Username
   [...]
     Contact:
       e-mail (person,[])                       E-Mail Address


Here, ``username (*)`` signifies that this attribute must always be set when
creating user objects. If the *person* option is set for the user account (this
is the standard case), one or more e-mail addresses can be added to the contact
information.

A range of standard parameters are defined for every module:

.. highlight:: console

.. option:: --dn

   The parameter is used to specify the LDAP
   position of the object during modifications or deletion. The complete
   DN must be entered, e.g.,

   .. code-block::

      $ univention-directory-manager users/user remove \
      > --dn "uid=ldapadmin,cn=users,dc=company,dc=example"

.. option:: --position

   The parameter is used to specify at which LDAP position an object should be
   created. If no ``--position`` is entered, the object is created below the
   LDAP base! In the ``move`` operation, this parameter specifies to which
   position an object should be moved, e.g:

   .. code-block::

      $ univention-directory-manager computers/ipmanagedclient move \
      > --dn "cn=desk01,cn=management,cn=computers,dc=company,dc=com" \
      > --position "cn=finance,cn=computers,dc=company,dc=example"

.. option:: --set

   The parameter specifies that the given value should be assigned to the
   following attribute. The parameter must be used per attribute value pair,
   e.g:

   .. code-block::

      $ univention-directory-manager users/user create \
      > --position "cn=users,dc=compaby,dc=example" \
      > --set username="jsmith" \
      > --set firstname="John" \
      > --set lastname="Smith" \
      > --set password="12345678"

.. option:: --option

   The parameter defines the LDAP object classes of an object. If, for example,
   only ``pki`` is provided as options for a user object, it is not possible to
   specify a ``mailPrimaryAddress`` for this user as this attribute is part of
   the ``mail`` option:

.. option:: --superordinate

   ``--superordinate`` is used to specify dependent, superordinate modules. A
   DHCP object, for example, requires a DHCP service object under which it can
   be stored. This is transferred with the ``--superordinate`` option.

.. option:: --policy-reference

   The ``--policy-reference`` parameter allows the assignment of policies to
   objects (and similarly their deletion with ``--policy-dereference``). If a
   policy is linked to an object, the settings from the policy are used for the
   object, e.g.:

   .. code-block:: console

      $ univention-directory-manager [category | modulename] [Operation] \
      > --policy-reference "cn=sales,cn=pwhistory," \
      > "cn=users,cn=policies,dc=company,dc=example"

.. option:: --ignore-exists

   The ``--ignore_exists`` parameters skips existing objects. If it is not
   possible to create an object, as it already exists, the error code ``0`` (no
   error) is still returned.

.. option:: --append

   ``--append`` and ``--remove`` are used to add/remove a value from a
   multi-value field, e.g.:

   .. code-block:: console

      $ univention-directory-manager groups/group modify \
      > --dn "cn=staff,cn=groups,dc=company,dc=example" \
      > --append users="uid=smith,cn=users,dc=company,dc=example" \
      > --remove users="uid=miller,cn=users,dc=company,dc=example"

.. option:: --remove

   See :option:`--append`.


.. _central-udm-example:

Example invocations of the command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following examples for the command line front end of |UCSUDM| can be used as
templates for your own scripts.

.. _central-udm-example-users:

Users
^^^^^

Creating a user in the standard user container:

.. code-block::

   $ univention-directory-manager users/user create \
   > --position "cn=users,dc=example,dc=com" \
   > --set username="user01" \
   > --set firstname="Random" \
   > --set lastname="User" \
   > --set organisation="Example company LLC" \
   > --set mailPrimaryAddress="mail@example.com" \
   > --set password="secretpassword"

Subsequent addition of the postal address for an existing user:

.. code-block::

   $ univention-directory-manager users/user modify \
   > --dn "uid=user01,cn=users,dc=example,dc=com" \
   > --set street="Exemplary Road 42" \
   > --set postcode="28239" \
   > --set city="Bremen"

This command can be used to display all the users whose user name begins with
*user*:

.. code-block::

   $ univention-directory-manager users/user list \
   > --filter uid=user*

Searching for objects with the ``--filter`` can also be limited to a position in
the LDAP directory; in this case, to all users in the container
``cn=bremen,cn=users,dc=example,dc=com``:

.. code-block::

   $ univention-directory-manager users/user list \
   > --filter uid="user*" \
   > --position "cn=bremen,cn=users,dc=example,dc=com"

This call removes the user ``user04``:

.. code-block::

   $ univention-directory-manager users/user remove \
   > --dn "uid=user04,cn=users,dc=example,dc=com"

A company has two sites with containers created for each. The following command
can be used to transfer a user from the container for the site "Hamburg" to the
container for the site "Bremen":

.. code-block::

   $ univention-directory-manager users/user move \
   > --dn "uid=user03,cn=hamburg,cn=users,dc=example,dc=com" \
   > --position "cn=bremen,cn=users,dc=example,dc=com"

.. _central-udm-example-groups:

Groups
^^^^^^

Creating a group ``Example Users`` and adding the user ``user01`` to this group:

.. code-block::

   $ univention-directory-manager groups/group create \
   > --position "cn=groups,dc=example,dc=com" \
   > --set name="Example Users" \
   > --set users="uid=user01,cn=users,dc=example,dc=com"

Subsequent addition of the user ``user02`` to the existing group:

.. code-block::

   $ univention-directory-manager groups/group modify \
   > --dn "cn=Example Users,cn=groups,dc=example,dc=com" \
   > --append users="uid=user02,cn=users,dc=example,dc=com"

.. caution::

   A ``--set`` on the attribute ``users`` overwrites the list of group members
   in contrast to ``--append``.

Subsequent removal of the user ``user01`` from the group:

.. code-block::

   $ univention-directory-manager groups/group modify \
   > --dn "cn=Example Users,cn=groups,dc=example,dc=com" \
   > --remove users="uid=user01,cn=users,dc=example,dc=com"

.. _central-udm-example-cn-policies:

Container / Policies
^^^^^^^^^^^^^^^^^^^^

This call creates a container ``cn=Bremen`` beneath the standard container
``cn=computers`` for the computers at the "Bremen" site. The additional option
``computerPath`` also registers this container directly as the standard
container for computer objects (see :ref:`central-cn-and-ous`):

.. code-block::

   $ univention-directory-manager container/cn create \
   > --position "cn=computers,dc=example,dc=com" \
   > --set name="bremen" \
   > --set computerPath=1

This command creates a disk quota policy with soft and hard limits and the name
*Default quota*:

.. code-block::

   $ univention-directory-manager policies/share_userquota create \
   > --position "cn=policies,dc=example,dc=com" \
   > --set name="Default quota" \
   > --set softLimitSpace=5GB \
   > --set hardLimitSpace=10GB

This policy is now linked to the user container ``cn=users``:

.. code-block::

   $ univention-directory-manager container/cn modify \
   > --dn "cn=users,dc=example,dc=com" \
   > --policy-reference "cn=Default quota,cn=policies,dc=example,dc=com"

Creating a |UCSUCR| policy with which the storage time for log files can be set
to one year. One space is used to separate the name and value of the variable:

.. code-block::

   $ univention-directory-manager policies/registry create \
   > --position "cn=config-registry,cn=policies,dc=example,dc=com" \
   > --set name="default UCR settings" \
   > --set registry="logrotate/rotate/count 52"

This command can be used to attach an additional value to the created policy:

.. code-block::

   $ univention-directory-manager policies/registry modify \
   > --dn "cn=default UCR settings,cn=config-registry,cn=policies,dc=example,dc=com" \
   > --append registry='"logrotate/compress" "no"'

.. _central-udm-example-cn-computers:

Computers
^^^^^^^^^

In the following example, a Windows client is created. If this client joins the
Samba domain at a later point in time (see :ref:`windows-domain-join`), this
computer account is then automatically used:

.. code-block::

   $ univention-directory-manager computers/windows create \
   > --position "cn=computers,dc=example,dc=com" \
   > --set name=WinClient01 \
   > --set mac=aa:bb:cc:aa:bb:cc \
   > --set ip=192.0.2.10

.. _central-udm-example-shares:

Shares
^^^^^^

The following command creates a share *Documentation* on the server
*fileserver.example.com*. As long as :file:`/var/shares/documentation/` does not
yet exist on the server, it is also created automatically:

.. code-block::

   $ univention-directory-manager shares/share create \
   > --position "cn=shares,dc=example,dc=com" \
   > --set name="Documentation" \
   > --set host="fileserver.example.com" \
   > --set path="/var/shares/documentation"

.. _central-udm-example-printer:

Printers
^^^^^^^^

Creating a printer share *LaserPrinter01* on the print server
*printserver.example.com*. The properties of the printer are specified in the
PPD file, the name of which is given relative to the directory
:file:`/usr/share/ppd/`. The connected printer is network-compatible and is
connected via the IPP protocol.

.. code-block::

   $ univention-directory-manager shares/printer create \
   > --position "cn=printers,dc=example,dc=com" \
   > --set name="LaserPrinter01"  \
   > --set spoolHost="printserver.example.com" \
   > --set uri="ipp:// 192.0.2.100" \
   > --set model="foomatic-rip/HP-Color_LaserJet_9500-Postscript.ppd" \
   > --set location="Head office" \
   > --set producer="producer: cn=HP,cn=cups,cn=univention,dc=example,dc=com"

.. note::

   There must be a blank space between the print protocol and the URL target
   path in the parameter ``uri``. A list of the print protocols can be found in
   :ref:`print-shares`.

Printers can be grouped in a printer group for simpler administration. Further
information on printer groups can be found in :ref:`printer-groups`.

.. code-block::

   $ univention-directory-manager shares/printergroup create \
   > --set name=LaserPrinters \
   > --set spoolHost="printserver.example.com" \
   > --append groupMember=LaserPrinter01 \
   > --append groupMember=LaserPrinter02

.. _central-udm-example-dnsdhcp:

DNS/DHCP
^^^^^^^^

To configure an IP assignment via DHCP, a DHCP computer entry must be registered
for the MAC address. Further information on DHCP can be found in
:ref:`module-dhcp-dhcp`.

.. code-block::

   $ univention-directory-manager dhcp/host create \
   > --superordinate "cn=example.com,cn=dhcp,dc=example,dc=com" \
   > --set host="Client222" \
   > --set fixedaddress="192.0.2.110" \
   > --set hwaddress="ethernet 00:11:22:33:44:55"

If it should be possible for a computer name to be resolved via DNS, the
following commands can be used to configure a forward (host record) and reverse
resolution (PTR record).

.. code-block::

   $ univention-directory-manager dns/host_record create \
   > --superordinate "zoneName=example.com,cn=dns,dc=example,dc=com" \
   > --set name="Client222" \
   > --set a="192.0.2.110"

   $ univention-directory-manager dns/ptr_record create \
   > --superordinate "zoneName=0.168.192.in-addr.arpa,cn=dns,dc=example,dc=com" \
   > --set address="110" \
   > --set ptr_record="Client222.example.com."

Further information on DNS can be found in :ref:`networks-dns`.

.. _central-udm-example-extended-attr:

Extended attributes
^^^^^^^^^^^^^^^^^^^

Extended attributes can be used to expand the functional scope of UMC modules,
see :ref:`central-extended-attrs`. In the following example, a new attribute is
added, where the car license number of the company car can be saved for each
user. The values are managed in the object class ``univentionFreeAttributes``
created specially for this purpose:

.. code-block::

   $ univention-directory-manager settings/extended_attribute create \
   > --position "cn=custom attributes,cn=univention,dc=example,dc=com" \
   > --set name="CarLicense" \
   > --set module="users/user" \
   > --set ldapMapping="univentionFreeAttribute1" \
   > --set objectClass="univentionFreeAttributes" \
   > --set longDescription="License plate number of the company car" \
   > --set tabName="Company car" \
   > --set multivalue=0 \
   > --set syntax="string" \
   > --set shortDescription="Car license"

.. _central-udm_rest_api:

HTTP API of domain management
-----------------------------

UCS provides an HTTP API for UDM which can be used to inspect, modify, create
and delete UDM objects via HTTP requests.

For more information on the API please refer to :ref:`developer-reference`.

.. _central-reports:

Evaluation of data from the LDAP directory with Univention Directory Reports
----------------------------------------------------------------------------

Univention Directory Reports offers the possibility of creating predefined
reports for any objects to be managed in the directory service.

The structure of the reports is defined using templates. The specification
language developed for this purpose allows the use of wildcards, which can be
replaced with values from the LDAP directory.  Any number of report templates
can be created. This allows users to select very detailed reports or just create
simple address lists, for example.

The creation of the reports is directly integrated in the UMC modules
:guilabel:`Users`, :guilabel:`Groups` and :guilabel:`Computers`. Alternatively,
the command line program :command:`univention-directory-reports` can be used.

Six report templates are already provided with the delivered Univention
Directory Reports, which can be used for users, groups and computers.  Three
templates create PDF documents and three CSV files, which can be used as an
import source for other programs. Further templates can be created and
registered.

.. _central-reports-create:

Creating reports via |UCSUMC| modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To create a report, you need to open the UMC module :guilabel:`Users`,
:guilabel:`Groups` or :guilabel:`Computers`. Then all the objects which should
be covered by the report must be selected (you can select all objects by
clicking the checkbox the left of *Name*). Clicking on :guilabel:`More AR Create
report` allows to choose between the *Standard Report* in PDF format and the
*Standard CSV Report* in CSV format.

.. _umc-report:

.. figure:: /images/umc_report.*
   :alt: Creating a report

   Creating a report

The reports created via a UMC module are stored for 12 hours and then deleted by
a cron job. The settings for when the cron job should run and how long the
reports should be stored for can be defined via two |UCSUCR| variables:

.. envvar:: directory/reports/cleanup/cron

   Defines when the cron job should be run.

.. envvar:: directory/reports/cleanup/age

   Defines the maximum age of a report document in seconds before it is deleted.

.. _central-management-umc-create-reports-cli:

Creating reports on the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Reports can also be created via the command line with the
:command:`univention-directory-reports` program. Information on the use of the
program can be viewed using the ``--help`` option.

The following command can be used to list the report templates available to
users, for example:

.. code-block::

   $ univention-directory-reports -m users/user -l


.. _central-management-umc-adjustment-expansion-of-directory-reports:

Adjustment/expansion of Univention Directory Reports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Existing reports can be created directly with the presettings. Some presettings
can be adapted using |UCSUCR|. For example, it is possible to replace the logo
that appears in the header of each page of a PDF report. To do so, the value of
the |UCSUCRV| :envvar:`directory/reports/logo` can include the name of an image
file. The usual image formats such as JPEG, PNG and GIF can be used. The image
is automatically adapted to a fixed width of 5.0 cm.

In addition to the logo, the contents of the report can also be adapted by
defining new report templates.

.. _central-management-umc-lets-encrypt:

Let's Encrypt
-------------

Let's Encrypt is a non-profit certificate authority that provides X.509
certificates for TLS encryption at no charge. It is the world's largest
certificate authority with the goal of all websites being secure and using
HTTPS.

The Let's Encrypt app in Univention App Center offers a largely automated
integration of the acme-tiny Let's Encrypt client in UCS. The supported services
in UCS are the Apache Webserver, the Postfix SMTP mailserver and the Dovecot
IMAP mailserver.
