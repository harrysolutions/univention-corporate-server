.. _users-general:

User management
***************

.. highlight:: console

UCS integrates central identity management. All user information are managed
centrally in UCS via the |UCSUMC| module :guilabel:`Users` and stored in the
LDAP directory service.

All the services integrated in the domain access the central account
information, i.e., the same username and password are used for the user login to
a Windows client as for the login on the IMAP server.

The domain-wide management of user data reduces the administrative efforts as
changes do not need to be subsequently configured on different individual
systems. Moreover, this also avoids subsequent errors arising from
inconsistencies between the individual datasets.

There are three different types of users in UCS:

1. **Normal user accounts** have all available properties. These users can log
   in to UCS or Windows systems and, depending on the configuration, also to the
   installed Apps. The users can be administered via the UMC module
   :guilabel:`Users` (see :ref:`users-management`).

2. **Address book entries** can be used to maintain internal or external contact
   information. These contacts can not log in to UCS or Windows systems.
   Address book entries can be managed via the UMC module :guilabel:`Contacts`.

3. **Simple authentication account**: With a simple authentication account, a
   user object is created, which has only a user name and a password. With this
   account, only authentication against the LDAP directory service is possible,
   but no login to UCS or Windows systems. Simple authentication accounts can be
   accessed via the UMC module :guilabel:`LDAP directory` (see
   :ref:`central-navigation`).

One very important and required attribute for user accounts is the *username*. To
avoid conflicts with the different tools handling user accounts in UCS, adhere
to the following recommendations for the definition of usernames:

* Only use lower case letters (``a-z``), digits (``0-9``) and the hyphen (``-``)
  from the ASCII character set for usernames.

* The username starts with a lower case letter from the ASCII character set. The
  hyphen is not allowed as last character.

* In UCS the username has at least a length of 4 characters and at most 20
  characters.

The recommendation results in the following regular expression:
``^[a-z][a-z0-9-]{2,18}[a-z0-9]$``.

Besides the recommendation, usernames also contain underscores (``_``) and upper
case ASCII letters in practice.  Consider the recommendation as a guideline and
not a rule and keep potential side-effects in mind when defining usernames
outside the recommendation.

.. _users-management:

User management via |UCSUMC| module
===================================

Users are managed in the UMC module *Users* (see
:ref:`central-user-interface`).

.. _user-create:

.. figure:: /images/users_user.*
   :alt: Creating a user in the UMC module 'Users'

   Creating a user in the UMC module *Users*

With :guilabel:`Next` on :numref:`user-create` the second page
:numref:`user-password` is shown, where the initial password can be set.

.. _user-password:

.. figure:: /images/users_password.*
   :alt: Password setting for a new user

   Password setting for a new user

As an alternative the user may set the initial password himself if the
:program:`Self Service` app is installed. For this to work an external e-mail
address must be given, which is registered at the contact e-mail address. The
user will then receive an e-mail to that address containing a web address and a
token, which can be used to set the password and unlock the account. For this
also see :ref:`user-management-password-changes-by-users-self-service`.

.. _user-password-new:

.. figure:: /images/users_self-service.*
   :alt: Initial user password

   Initial user password

By default a simplified wizard for creating a user is shown, which only requests
the most important settings. All attributes can be shown by clicking on
:guilabel:`Advanced`. The simplified wizard can be deactivated by setting the
|UCSUCRV| :envvar:`directory/manager/web/modules/users/user/wizard/disabled` to
``true``.

.. _user-create-advanced:

.. figure:: /images/users_user_advanced.*
   :alt: Advanced user settings

   Advanced user settings


.. _users-management-table-general:

User management module - General tab
------------------------------------

.. _users-management-table-general-tab:

.. list-table:: *General* tab
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Title
     - The title of the user is to be entered here.

   * - First name
     - The first name of the user is to be entered here.

   * - Last name
     - The last name of the user is to be entered here.

   * - User name
     - This is the name, by which the user logs into the system. The name has to
       begin with a letter which has to be followed by: letters a-z in lower
       case, numerals 0-9, dots, hyphens, or underlines. User names may not
       contain blank spaces.

       In order to ensure compatibility to non-UCS systems the creation of users
       which are only distinguished from each other by upper and lower case
       letters is prevented. Thus, if the user name ``smith`` already exists,
       then the user name ``Smith`` cannot be created.

       By default it is not possible to create a user with the same name as an
       existing group. If the |UCSUCRV|
       :envvar:`directory/manager/user_group/uniqueness` is set to ``false``,
       this check is removed.

   * - Description
     - Arbitrary descriptions for the user can be entered here.

   * - Password
     - The user's password has to be entered here.

   * - Password (retype)
     - In order to avoid spelling errors, the user's password has to be entered
       for a second time.

   * - Override password history
     - By checking this box, the password history is overridden for this user
       and for this password change. This means, with this change the user can
       be assigned a password which is already in use.

       Further details on user password management can be found in
       :ref:`users-passwords`.

   * - Override password check
     - By checking this box, the requirements for the length of the password and
       for password quality checks are overridden for this user and for this
       password change. This means, the user can e.g. be assigned a shorter
       password than would be possible according to the defined minimum length.

       Further details on the password policies for users can be found in
       :ref:`users-passwords`.

   * - Primary e-mail address (mailbox)
     - The e-mail address of the user is declared here, see
       :ref:`mail-management-users`.

   * - Display name
     - The display name is automatically composed of the first and surnames. It
       generally does not need to be changed. The screen name is used for the
       synchronization with Active Directory and Samba/AD among other things.

   * - Birthday
     - This field is used to save a user's birthday.

   * - Organization
     - The organization is to be entered here.

   * - Employee number
     - Numbers for staff members can be entered in this field.

   * - Employee type
     - The category of the staff member can be entered here.

   * - Superior
     - The superior of the user can be selected here.

   * - Picture of the user (JPEG format)
     - This mask can be used to save a picture of the user in LDAP in JPEG
       format. In the default settings the file size is limited to 512
       kilobytes.

.. _users-management-table-groups:

User management module - Groups tab
-----------------------------------

.. _users-management-table-groups-tab:

.. list-table:: *Groups* tab
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Primary group
     - This selection list can be used for specifying the user's primary group.
       All the groups registered in the domain are open for selection. By
       default, the group ``Domain Users`` is preset.

   * - Groups
     - Here it is possible to set further group memberships for the user in
       addition to the primary group.

.. _users-management-table-account:

User management module - Account tab
------------------------------------

.. _users-management-table-account-tab:

.. list-table:: *Account* tab
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Account is deactivated
     - The *Account is deactivated* checkbox can be used to deactivate the user
       account. If this is activated, the user cannot log into the system. This
       affects all authentication methods. This is typically used when a user
       leaves the company. In a heterogeneous environment, an account
       deactivation might also be caused by external tools.

   * - Account expiry date
     - A date is specified in this input field on which the account will
       automatically be locked. This is practical for user accounts that only
       need to be active for a certain period of time, e.g., for interns.

       If the date is deleted or replaced by a different, future date, the user
       will regain the right to log in.

   * - User has to change password on next login
     - If this checkbox is ticked, then the user has to change his password
       during the next login procedure.

   * - Password expiry date
     - If the password is subject to an expiry date, then this date is displayed
       in this entry field. This entry field cannot be edited directly, see
       :ref:`users-passwords`.

       If a password expiry interval is defined, the password expiry date is
       automatically adjusted when passwords are changed.

       If no *Expiry interval* is declared, the old expiry date will be deleted
       and no new date will be set.

   * - Unlock lockout
     - If the account has automatically been locked temporarily for security
       reasons, usually because the user has entered the password incorrectly
       too often, this checkbox can be used to unlock the account again manually
       before the lockout is lifted automatically when the lockout duration has
       passed. This temporary account lockout can happen if a corresponding
       domain wide policy setting has been defined by an administrator. There
       are three different mechanisms that may trigger lockout if configured
       properly:

       * Failed PAM authentication attempts to an UCS server (see
         :ref:`users-faillog`).

       * Failed LDAP authentication attempts (if the :program:`ppolicy` overlay
         has been activated and configured).

       * Failed Samba/AD authentication attempts (if the Samba domain
         ``passwordsettings`` have been configured).

   * - Lockout till
     - If the account has automatically been locked temporarily for security
       reasons, usually because the user has entered the password incorrectly
       too often, this field shows the time when the account automatically gets
       unlocked.

   * - Activation date
     - If a user account shall only become usable at a later date, this can be
       set here. A cron job periodically checks if accounts need to be
       activated. It runs every 15 minutes by default. When saving the changes,
       the account is automatically marked as deactivated in case a date in the
       future has been specified.

   * - Windows home drive
     - If the Windows home directory for this user is to show up on a different
       Windows drive than that specified by the Samba configuration, then the
       corresponding drive letter can be entered here, e.g. :file:`M:`.

   * - Windows home path
     - The path of the directory which is to be the user's Windows home
       directory, is to be entered here, e.g. :file:`\\ucs-file-server\smith`.

   * - Windows logon script
     - The user-specific logon script relative to the NETLOGON share is entered
       here, e.g.  :file:`user.bat`.

   * - Windows profile directory
     - The profile directory for the user can be entered here, e.g.
       :file:`\\ucs-file-server\user\profile`.

   * - Relative ID
     - The relative ID (RID) is the local part of the SID. If a user is to be
       assigned a certain RID, the ID in question can be entered in this field.
       If no RID is assigned, the next available RID will automatically be used.
       The RID cannot be subsequently changed.  Integers from 1000 upwards are
       permitted.  RIDs below 1000 are reserved to standard groups and other
       special objects.

   * - Samba privilege(s)
     - This selection mask can be used to assign a user selected Windows systems
       rights, for example the permission to join a system to the domain.

   * - Permitted times for Windows logins
     - This input field contains time periods for which this user can log in to
       Windows computers.

       If no entry is made in this field, the user can log in at any time of
       day.

   * - Allow the authentication only on these Microsoft Windows host(s)
     - This setting specifies the clients where the user may log in. If no
       settings are made, the user can log in to any client.

   * - UNIX home directory
     - The path of the user's home directory.

   * - Login shell
     - The user's login shell is to be entered in this field. This program is
       started if the user performs a text-based login. By default,
       :file:`/bin/bash` is preset.

   * - User ID
     - If the user is to be assigned a certain user ID, the ID in question can
       be entered in this field. If no value is specified, a free user ID is
       assigned automatically.

       The user ID can only be declared when adding the user. When the user data
       are subsequently edited, the user ID will be represented in gray and
       barred from change.

   * - Group ID of the primary group
     - The group ID of the user's primary group is shown here. The primary group
       can be changed in the *General* tab.

   * - Home share
     - If a share is selected here, the home directory is stored on the
       specified server. If no selection is made, the user data are saved on
       the respective login system.

   * - Home share path
     - The path of the home directory relative to the *Home share* is declared
       here. The username is already preset as a default value when creating a
       user.

.. _users-management-table-contact:

User management module - Contact tab
------------------------------------

.. _users-management-table-contact-tab:

.. list-table:: *Contact* tab
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - E-mail address(es)
     - Additional e-mail addresses can be saved here. These are not evaluated by
       the mail server.

       The values of this attribute are stored in the LDAP attribute ``mail``.
       Most address book applications using an LDAP search function will search
       for an e-mail address by this attribute.

   * - Telephone number(s)
     - This field contains the user's business phone number.

   * - Room number(s)
     - The room number of the user.

   * - Department number(s)
     - The department number of the user can be entered here.

   * - Street
     - The street and house number of the user's business address can be entered
       here.

   * - Postal code
     - This field contains the postal code of the user's business address.

   * - City
     - This field contains the city of the user's business address.

   * - Private telephone number(s)
     - The private fixed network phone number can be entered here.

   * - Mobile telephone number(s)
     - The user's mobile numbers can be entered here.

   * - Pager telephone number(s)
     - Pager numbers can be entered here.

   * - Private postal address(es)
     - One or more of the user's private postal addresses can be entered in this
       field.

.. _users-management-table-mail:

User management module - Mail tab
---------------------------------

This tab is displayed in the advanced settings.

The settings are described in :ref:`mail-management-users`.

.. _users-management-table-options:

User management module - Options tab
------------------------------------

.. _users-management-table-options-tab:

.. list-table:: *(Options)* tab
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Public key infrastructure account
     - If this checkbox is not ticked, the user will not be assigned the object
       class ``pkiUser``.

.. _users-app-activation:

User activation for apps
========================

Many apps from the App Center are compatible with the central identity
management in UCS. This allows system administrators to activate the
users for apps. In some cases, app specific settings for the user can be
made. This depends on the app and how it uses the identity management.

.. _user-app-activation:

.. figure:: /images/user_activation.*
   :alt: User activation for installed apps

   User activation for installed apps

Once an app with user activation is installed in the UCS environment, it will
appear with the logo in the :guilabel:`Apps` tab of the user in the UMC module
*Users*. With a tick in the checkbox the user is activated for the app. If the
app offers specific settings another tab with the name of the app will appear to
set these parameters. The app activation and the parameters are stored at the
user object in the LDAP directory service.

To withdraw a user activation for an app, it is sufficient to deselect
the checkbox.

When the app is uninstalled, the checkbox of the user activation for the
app is removed from the :guilabel:`Apps` tab of the user in
the UMC module.

.. _users-passwords:

User password management
========================

Passwords which are difficult to guess and regular password changes are
an essential element of the system security of a UCS domain. The
following properties can be configured for users using a
*password policy*.

If Samba is used, the settings of the Samba domain object (see
:ref:`users-password-samba`) apply for logins to Window clients. The settings of
the Samba domain object and the policy should be set identically, otherwise
different password requirements will apply for logins to Windows and UCS
systems.

The password is saved in different attributes for every user saved in
the management system:

* The ``krb5Key`` attribute stores the Kerberos password.

* The ``userPassword`` attribute stores the Unix password (in other Linux
  distributions present in :file:`/etc/shadow`).

* The ``sambaNTPassword`` attribute stores the NT password hash used by Samba.

Password changes are always initiated via Kerberos, either in the UCS PAM
configuration or via Samba.

.. _password-policy:

.. figure:: /images/users_policy_password.*
   :alt: Configuring a password policy

   Configuring a password policy

History length
   The *history length* saves the last password hashes. These passwords can then
   not be used by the user as a new password when setting a new password. With a
   password history length of five, for example, five new passwords must be set
   before a password can be reused. If no password history check should be
   performed, the value must be set to ``0``.

   The passwords are not stored retroactively. Example: If ten passwords were
   stored, and the value is reduced to three, the oldest seven passwords will be
   deleted during the next password change. If then the value is increased
   again, the number of stored passwords initially remains at three, and is only
   increased by each password change.

Password length
   The *password length* is the minimum length in characters that a user
   password must comply with. If no value is entered here, the minimum size is
   eight characters. The default value of eight characters for password length
   is fixed, so it always applies if no policy is set and the *Override password
   check* checkbox is not ticked. This means it even applies if the
   *default-settings* password policy has been deleted.

   If no password length check should be performed, the value must be set to ``0``.

   A per server default can be configured via |UCSUCRV|
   :envvar:`password/quality/length/min`, which applies to users that are not
   subject to a *UDM password policy*. See the |UCSUCRV| description for
   details.

Password expiry interval
   A *password expiry interval* demands regular password changes. A password
   change is demanded during login to |UCSWEB|\ s, to Kerberos, on Windows
   clients and on UCS systems following expiry of the period in days. The
   remaining validity of the password is displayed in the user management under
   *Password expiry date* in the *Account* tab. If this input field is left
   blank, no password expiry interval is applied.

Password quality check
   If the option *Password quality check* is activated, additional checks -
   including dictionary checks - are performed for password changes in Samba,
   |UCSWEB|\ s and Kerberos.

   The configuration is done via |UCSUCR| and should occur on all login servers.
   The following checks can be enforced:

   * Minimum number of digits in the new password
     (:envvar:`password/quality/credit/digits`).

   * Minimum number of uppercase letters in the new password
     (:envvar:`password/quality/credit/upper`).

   * Minimum number of lowercase letters in the new password
     (:envvar:`password/quality/credit/lower`).

   * Minimum number of characters in the new password which are neither letters
     nor digits (:envvar:`password/quality/credit/other`).

   * Individual characters/digits can be excluded
     (:envvar:`password/quality/forbidden/chars`).

   * Individual characters/figures can be made compulsory
     (:envvar:`password/quality/required/chars`).

   * Standard Microsoft password complexity criteria can be applied
     (:envvar:`password/quality/mspolicy`). This can be done in addition to the
     :program:`python-cracklib` checks (value ``yes``) or instead of them
     (``sufficient``). See |UCSUCRV| description for details.

.. _users-password-samba:

Password settings for Windows clients when using Samba
======================================================

With the Samba domain object, one can set the password requirements for
logins to Windows clients in a Samba domain.

The Samba domain object is managed via the UMC module *LDAP
directory*. It can be found in the ``samba``
container below the LDAP base and carries the domain's NetBIOS name.

The settings of the Samba domain object and the policy (see :ref:`users-passwords`) should be set identically,
otherwise different password requirements will apply for logins to
Windows and UCS systems.

.. list-table:: 'General' tab
   :header-rows: 1
   :widths: 30 70

   * - Attribute
     - Description

   * - Password length
     - The minimum number of characters for a user password.

   * - Password history
     - The latest password changes are saved in the form of hashes. These
       passwords can then not be used by the user as a new password when setting
       a new password. With a password history of five, for example, five new
       passwords must be set before a password can be reused.

   * - Minimum password age
     - The period of time set for this must have at least expired since the last
       password change before a user can reset his password again.

   * - Maximum password age
     - Once the saved period of time has elapsed, the password must be changed
       again by the user the next time he logs in. If the value is left blank,
       the password is infinitely valid.

.. _user-management-password-changes-by-users:

User self services
==================

.. _user-management-password-changes-by-users-via-umc:

Password change by user via UCS portal page
-------------------------------------------

Every logged in user can change his own password by opening the menu via the
hamburger icon in the top right corner and selecting :menuselection:`User settings -->
Change password`. The change is performed directly via the PAM stack (see
:ref:`computers-Authentication-PAM`) and is then available centrally for all
services.

.. _user-management-password-changes-by-users-self-service:

Password management via Self Service app
----------------------------------------

By installing the UCS components :program:`Self Service Backend` and
:program:`Self Service` in the domain via the :guilabel:`App Center`, users are
enabled to take care of their password management without administrator
interaction.

The :program:`Self Service` app creates its own portal, accessible at the web
URI ``/univention/selfservice/``, which bundles all its functionality. The
original portal has the same entries registered at its user menu. They allow
users to update their password given their old password as well as to reset
their lost password by requesting a token to be sent to a previously registered
contact e-mail address. The token has to be entered on the dedicated password
reset web page.

The following |UCSUCRV|\ s can be used to activate or deactivate individual
features of the password management.

.. envvar:: umc/self-service/passwordreset/backend/enabled

   Activates or deactivates the backend of the *Password forgotten* page. This
   |UCSUCRV| has to be set on the systems that is defined as :program:`Self
   Service backend` via the |UCSUCRV| :envvar:`self-service/backend-server`,
   since requests regarding these variables are forwarded to the :program:`Self
   Service backend`.

.. envvar:: umc/self-service/protect-account/backend/enabled

   Activates or deactivates the backend of the *Protect account* page. This
   |UCSUCRV| has to be set on the systems that is defined as :program:`Self
   Service backend` via the |UCSUCRV| :envvar:`self-service/backend-server`,
   since requests regarding these variables are forwarded to the :program:`Self
   Service backend`.

.. envvar:: umc/self-service/service-specific-passwords/backend/enabled

   Activates or deactivates the backend for service specific passwords.
   Currently, only the service RADIUS is supported. Find more information in
   :ref:`ip-config-radius-configuration-service-specific-password`.

Those variables also activate or deactivate the corresponding entries in the
portal. However, you can also adjust them manually, they are in fact just normal
portal entries.

.. _user-management-password-changes-by-users-contact-data:

Contact information
-------------------

Additional personal data can be stored in LDAP with the users account.
This may include a picture, the users private address and other contact
information. By default only administrators can modify them. As an
alternative selected attributes may be unlocked for the user to change
himself. The user then can do this using the :program:`Self Service` app.

.. _user-self-service:

.. figure:: /images/users_self-service_profile.*
   :alt: User profile self-service

   User profile self-service

For this the following |UCSUCRV|\ s must be configured:



.. envvar:: self-service/ldap_attributes

   This variable configures the *LDAP* attributes a user can modify at its own
   user account. The names of the attributes must be separated by comma. This
   variable must be set on |UCSPRIMARYDN| (and |UCSBACKUPDN|\ s).

.. envvar:: self-service/udm_attributes

   This variable configures the *UDM* attributes a user can modify. The names of
   the attributes must be separated by comma. This variable must be set on all
   hosts, where the :program:`Self Service`  app is installed (incl. |UCSPRIMARYDN|).

.. envvar:: umc/self-service/profiledata/enabled

   This variable must be set to ``true`` on all involved server systems to
   enable the mechanism.

.. envvar:: umc/self-service/allow-authenticated-use

   This variable defines whether the specification of user name and password is
   necessary when opening and modifying your own user profile if you are already
   logged in to Univention Portal.

   As of UCS 4.4-7, this |UCSUCRV| is automatically set to ``true`` when the
   :program:`Self Service` is installed for the first time. The ``true`` value
   activates the use of an existing Univention Portal session. The fields
   *Username* and *Password* are then automatically filled in or no longer
   displayed.

   Systems upgraded to UCS 4.4-7 will retain the old behavior by automatically
   setting the value to ``false``. Note that this variable must be set to the
   same value on all participating systems where the :program:`Self Service` app
   is installed (incl. |UCSPRIMARYDN|).


Both ``*attributes`` variables must match each other. The names of the
attributes and their mapping can be fetched from the following command:

.. code-block::

   $ python3 -c 'from univention.admin.handlers.users.user import mapping;\
   > print("\n".join( \
   > map("{0[0]:>30s} {0[1][0]:<30s}".format, sorted(mapping._map.items()))) \
   > )'

.. _user-management-password-changes-by-users-selfregistration:

Self registration
-----------------

The Self Service allows for users to register themselves, which will create a
user account that has to be verified via email.

User accounts that are created via the Self Service will have the
``RegisteredThroughSelfService`` attribute of the user set to ``TRUE`` and the
``PasswordRecoveryEmailVerified`` attribute set to FALSE. After the user has
verified his account via the verification email the
``PasswordRecoveryEmailVerified`` attribute will be set to ``TRUE``.

.. _user-management-password-changes-by-users-selfregistration-account-creation:

Account creation
^^^^^^^^^^^^^^^^

.. _user-registration:

.. figure:: /images/users_self-service_registration.*
   :alt: Account registration

   Account registration

Aspects about the *Create an account* page and the account creation
itself can be configured with the following |UCSUCRV|\ s. These |UCSUCRV|\ s
have to be set on the systems that is defined as :program:`Self Service Backend`
via the |UCSUCRV| :envvar:`self-service/backend-server`, since
requests regarding these variables are forwarded to the Self Service
backend.

.. envvar:: umc/self-service/account-registration/backend/enabled

   With this variable the account registration can be disabled/enabled.

.. envvar:: umc/self-service/account-registration/usertemplate

   With this variable a user template (:ref:`users-templates`) can be specified
   that will be used for the creation of self registered accounts.

.. envvar:: umc/self-service/account-registration/usercontainer

   With this variable a container can be specified under which the self
   registered users are created.

.. envvar:: umc/self-service/account-registration/udm_attributes

   This variable configures which UDM attributes of a user account are shown on
   the *Create an account* page of the Self Service. The names of the UDM
   attributes must be provided as a comma separated list.

.. envvar:: umc/self-service/account-registration/udm_attributes/required

   This variable configures which of the UDM attributes set via the |UCSUCRV|
   :envvar:`umc/self-service/account-registration/udm_attributes` are required
   for the user to provide. The names of the UDM attributes must be provided as
   a comma separated list.

.. _user-management-password-changes-by-users-selfregistration-verification-email:

Verification email
^^^^^^^^^^^^^^^^^^

After a user has clicked on :guilabel:`Create account`, they
will see a message that an email for the account verification has been
sent.

.. _user-verification-email:

.. figure:: /images/users_self-service_verification_email.*
   :alt: Sending the verification email

   Sending the verification email

Aspects about the verification email and the verification token can be
configured with the following |UCSUCRV|\ s. These |UCSUCRV|\ s have to be set on
the :program:`Self Service Backend` that is defined via the |UCSUCRV|
:envvar:`self-service/backend-server`, since requests regarding these variables
are forwarded to the :program:`Self Service Backend`.

.. envvar:: umc/self-service/account-verification/email/webserver_address

   Defines the ``host`` part to use in the verification link URL. The default is
   to use the FQDN of the :program:`Self Service Backend` defined via the
   |UCSUCRV| :envvar:`self-service/backend-server` since this |UCSUCRV| is
   evaluated there.

.. envvar:: umc/self-service/account-verification/email/sender_address`

   Defines the sender address of the verification email. Default is ``Account
   Verification Service <noreply@FQDN>``.

.. envvar:: umc/self-service/account-verification/email/server

   Server name or IP address of the mail server to use.

.. envvar:: umc/self-service/account-verification/email/text_file

   A path to a text file whose content will be used for the body of the
   verification email. The text can contain the following strings which will be
   substituted accordingly: ``{link}``, ``{token}``, ``{tokenlink}`` and
   ``{username}``. As default the file
   :file:`/usr/share/univention-self-service/email_bodies/verification_email_body.txt`
   is used.

.. envvar:: umc/self-service/account-verification/email/token_length

   Defines the number of characters that is used for the verification token.
   Defaults to ``64``.

.. _user-management-password-changes-by-users-selfregistration-account-verification:

Account verification
^^^^^^^^^^^^^^^^^^^^

Following the verification link from the email, the user will land on
the *Account verification* page of the :program:`Self Service`.

.. _user-verification:

.. figure:: /images/users_self-service_verification.*
   :alt: Account verification

   Account verification

The account verification and request of new verification tokens can be
disabled/enabled with the |UCSUCRV|
:envvar:`umc/self-service/account-verification/backend/enabled`. This |UCSUCRV|
has to be set on the systems that is defined as :program:`Self Service Backend`
via the |UCSUCRV| :envvar:`self-service/backend-server`.

.. _user-verification-message:


.. figure:: /images/users_self-service_verification_message.*
   :alt: Account verification message

   Account verification message

The SSO login can be configured to deny login from unverified, self
registered accounts. This is configured through the |UCSUCRV|
:envvar:`saml/idp/selfservice/check_email_verification`. This
needs to be set on the |UCSPRIMARYDN| and all |UCSBACKUPDN|\ s. The setting
has no effect on accounts created by an administrator.

The message on the SSO login page for unverified, self registered
accounts, can be set with the |UCSUCRV|\ s
:envvar:`saml/idp/selfservice/account-verification/error-title`
and
:envvar:`saml/idp/selfservice/account-verification/error-descr`.
A localized message can be configured by adding a local to the variable, for
example ``saml/idp/selfservice/account-verification/error-title/en``.

.. _user-management-password-changes-by-users-selfderegistration:

Self deregistration
-----------------------------------------------

The :program:`Self Service` allows for users to request the deletion of their
own account. This feature can be activated with the |UCSUCRV|
:envvar:`umc/self-service/account-deregistration/enabled`, which will show a
:guilabel:`Delete my account` Button on the *Your profile* page of the Self
Service (:ref:`users-templates`).

If a user has requested to delete his account, it will not be deleted directly
but deactivated. In addition the ``DeregisteredThroughSelfService`` attribute of
the user will be set to ``TRUE`` and the ``DeregistrationTimestamp`` attribute
of the user will be set to the current time in the `GeneralizedTime LDAP syntax
<https://ldapwiki.com/wiki/GeneralizedTime>`__. If the user has a
``PasswordRecoveryEmail`` set they will receive a notification email which can
be configured with the following |UCSUCRV|\ s.

.. envvar:: umc/self-service/account-deregistration/email/sender_address

   Defines the sender address of the email. Default is ``Password Reset Service
   <noreply@FQDN>``.

.. envvar:: umc/self-service/account-deregistration/email/server

   Server name or IP address of the mail server to use.

.. envvar:: umc/self-service/account-deregistration/email/text_file

   A path to a text file whose content will be used for the body of the email.
   The text can contain the following strings which will be substituted
   accordingly: ``{username}``. As default the file
   :file:`/usr/share/univention-self-service/email_bodies/deregistration_notification_email_body.txt`
   is used.

The Self Service provides a script under
:file:`/usr/share/univention-self-service/delete_deregistered_accounts.py` that
can be used to delete all users/user objects which have
``DeregisteredThroughSelfService`` set to ``TRUE`` and whose
``DeregistrationTimestamp`` is older than a specified time.

The following command would delete users whose ``DeregistrationTimestamp`` is
older than 5 days and 2 hours:

.. code-block::

   $ /usr/share/univention-self-service/delete_deregistered_accounts.py \
   > --timedelta-days 5 \
   > --timedelta-hours 2

For all possible arguments to the script see:

.. code-block::

   $ /usr/share/univention-self-service/delete_deregistered_accounts.py --help


The script can be run regularly by creating a cron job via |UCSUCR|.

.. code-block::

   $ ucr set cron/delete_deregistered_accounts/command=\
   > /usr/share/univention-self-service/delete_deregistered_accounts.py\
   > ' --timedelta-days 30' \
   > cron/delete_deregistered_accounts/time='00 06 * * *'  # daily at 06:00


More information on how to set cron jobs via |UCSUCR| can be found in
:ref:`computers-Defining-cron-jobs-in-Univention-Configuration-Registry`.

.. _users-faillog:

Automatic lockout of users after failed login attempts
======================================================

By default, a user can enter their password incorrectly any number of
times. To hinder brute force attacks on passwords, an automatic lockout
for user accounts can be activated after a configured number of failed
login attempts.

UCS unifies various methods for user authentication and authorization.
Depending on the installed software components, there may be different
mechanisms for configuring and counting failed login attempts.

The three different methods are described in the next sections.

.. _users-faillog-samba:

Samba Active Directory Service
------------------------------

In Samba Active Directory environments, various services are provided by
Samba, such as Kerberos. To lockout users after too many failed login
attempts, the tool :command:`samba-tool` can be used.


* To show the currently configured values:

  .. code-block::

     $ samba-tool domain passwordsettings show

* To specify how often a user can attempt to log in with an incorrect password
  before the account is locked:

  .. code-block::

     $ samba-tool domain passwordsettings set --account-lockout-threshold=5

* To specify the number of minutes an account will be locked after too many
  incorrect passwords have been entered:

  .. code-block::

     $ samba-tool domain passwordsettings set --account-lockout-duration=3

* To define the number of minutes after which the counter is reset:

  .. code-block::

     samba-tool domain passwordsettings set --reset-account-lockout-after=5

  If an account gets automatically unlocked after the lockout duration, the
  counter is not reset immediately, to keep the account under strict monitoring
  for some time. During the time window between the end of the lockout duration
  and the point when the counter gets reset, a single attempt to log in with an
  incorrect password will lock the account immediately again.


The manual unlocking of a user is done in the user administration on the tab
:guilabel:`Account` by activating the checkbox *Unlock account*.

.. _users-faillog-pam:

PAM-Stack
---------

The automatic locking of users after failed logins in the PAM stack can be
enabled by setting the |UCSUCRV| :envvar:`auth/faillog` to ``yes``. The upper
limit of failed login attempts at which an account lockout is configured in the
|UCSUCRV| :envvar:`auth/faillog/limit`. The counter is reset each time the
password is entered correctly.

The lockout is activated locally per system by default. In other words, if a
user enters their password incorrectly too many times on one system, they can still
login on another system. Setting the |UCSUCRV|
:envvar:`auth/faillog/lock_global` will make the lock effective globally and
register it in the LDAP directory. The global lock can only be set on
|UCSPRIMARYDN|/Backup systems as other system roles do not have the necessary
permissions in the LDAP directory. On all systems with any of these system
roles, the lockout gets automatically activated locally or deactivated again via
the listener module, depending on the current lock state in the LDAP directory.

As standard, the lockout is not subject to time limitations and must be reset by
the administrator. However, it can also be reset automatically after a certain
time interval has elapsed. This is done by specifying a time period in seconds
in the |UCSUCRV| :envvar:`auth/faillog/unlock_time`. If the value is set to 0,
the lock is reset immediately.

By default, the ``root`` user is excluded from the password lock, but can also
be subjected to it by setting the |UCSUCRV| :envvar:`auth/faillog/root` to
``yes``.

If accounts are only locked locally, the administrator can unlock a user account
by entering the command:

.. code-block::

   $ faillog -r -u USERNAME

If the lock occurs globally in the LDAP directory, the user can be reset in the
|UCSUMC| module :guilabel:`Users` on the tab *Account* via the checkbox *Unlock
account*.

.. _users-faillog-openldap:

OpenLDAP
--------

On UCS Directory Nodes, automatic account locking can be enabled for too many
failed LDAP server login attempts. The MDB LDAP backend must be used. This is
the default backend since UCS 4, previous systems must be migrated to the MDB
LDAP backend, see `UCS performance guide
<https://docs.software-univention.de/performance-guide-5.0.html>`_.

Automatic account locking must be enabled for each UCS Directory Node.
To do this, the |UCSUCRV|\ s :envvar:`ldap/ppolicy` and
:envvar:`ldap/ppolicy/enabled` must be set to
``yes`` and the OpenLDAP server must be restarted:

.. code-block:: console

   $ ucr set ldap/ppolicy=yes ldap/ppolicy/enabled=yes
   $ systemctl restart slapd


The default policy is designed so that five repeated failed LDAP server logon
attempts within five minutes cause the lockout. A locked account can only be
unlocked by a domain administrator through the UMC module :guilabel:`Users` via
the checkbox *Unlock account* on the *Account* tab.

The number of repeated failed LDAP server logon attempts can be adjusted
in the configuration object with the *objectClass* ``pwdPolicy``:

.. code-block:: console

   $ univention-ldapsearch objectclass=pwdPolicy


``pwdMaxFailure``
   attribute determines the number of LDAP authentication errors before locking.

``pwdMaxFailureCountInterval``
   attribute determines the time interval in seconds that is considered. Failed
   logon attempts outside this interval are ignored in the count.

The following command can be used to block the account after 10
attempts:

.. code-block:: console

   $ LB="$(ucr get ldap/base)"
   $ ldapmodify -x -D "cn=admin,$LB" -y /etc/ldap.secret <<__EOT__
   > dn: cn=default,cn=ppolicy,cn=univention,$LB
   > changetype: modify
   > replace: pwdMaxFailure
   > pwdMaxFailure: 10
   > __EOT__


The manual unlocking of a user is done in the user administration on the tab
*Account* by activating the checkbox *Unlock account*.

.. _users-templates:

User templates
==============

A user template can be used to preset settings when creating a user. If at least
one user template is defined, it can be selected when creating a user.

.. _user-create-template:

.. figure:: /images/users_usertemplate.*
   :alt: Selecting a user template

   Selecting a user template

User templates are administrated in the UMC module :guilabel:`LDAP directory`.
There one needs to switch to the ``univention`` container and then to the
``templates`` subcontainer. A new user template can be created here via the
:guilabel:`Add` with the object type ``Settings: User template``.

In a user template, either a fixed value can be specified (e.g., for the
address) or an attribute of the user management referenced. Attributes are then
referenced in chevrons.

A list of possible attributes can be displayed with the following command in the
section *users/user variables* of the output:

.. code-block:: console

   $ univention-director-manager users/user

If a user template is used for adding a user, this template will overwrite all
the fields with the preset values of the template. In doing so, an empty field
is set to ``""``.

It is also possible to only use partial values of attributes or convert values
in uppercase/lowercase.

For example, the UNIX home directory can be stored under
:file:`/home/<title>.<lastname>` or the primary e-mail address can be predefined
with ``<firstname>.<lastname>@company.com``.  Substitutions are generally
possibly for any value, but there is no syntax or semantics check. So, if no
first name is specified when creating a user, the above e-mail address would
begin with a dot and would thus be invalid according to the e-mail standard.
Similar sources of error can also occur when handling file paths etc.
Non-resolvable attributes (for instance due to typing errors in the template)
are deleted.

If only a single character of an attribute is required instead of the complete
attribute value, the index of the required character can be entered in the user
template in square parentheses after the name of the attribute. The count of
characters of the attribute begins with ``0``, so that index ``1`` corresponds
to the second character of the attribute value.  Accordingly,
``<firstname>[0].<lastname>@company.com`` means an e-mail address will consist
of the first letter of the first name plus the last name.

A substring of the attribute value can be defined by entering a range in square
parentheses. In doing so, the index of the first required character and the
index of the last required character plus one are to be entered. For example,
the input ``<firstname>[2:5]`` returns the third to fifth character of the first
name.

Adding ``:lower`` or ``:upper`` to the attribute name converts the attribute
value to lowercase or uppercase, e.g., ``<firstname:lower>``. If a modifier like
``:lower`` is appended to the entire field, the complete value is transformed,
e.g.  ``<lastname>@company.com<:lower>``.

The option ``:umlauts`` can be used to convert special characters such as *è*,
*ä* or *ß* into the corresponding ASCII characters.

The option ``:alphanum`` can be used to remove all non alphanumeric characters
such as ````` (backtick) or ``#`` (hash). A whitelist of characters that are
ignored by this option can be defined in the UCR variable
:envvar:`directory/manager/templates/alphanum/whitelist`. If this option is
applied to an entire field, even manually placed symbols like the ``@`` in an
email address are removed. To avoid that, this option should be applied to
specific attributes only or desired symbols should be entered into the
whitelist.

The options ``:strip`` or ``:trim`` remove all white space characters from the
start and end of the string.

It is also possible to combine options, e.g: ``:umlauts,upper``.

.. _users-lastbind-overlay-module:

Overlay module for recording an account's last successful LDAP bind
===================================================================

.. caution::

   Before using this feature please read :uv:kb:`support article about
   activating the OpenLDAP lastbind overlay module <14404>`.

The optional `lastbind overlay module
<http://manpages.ubuntu.com/manpages/xenial/man5/slapo-lastbind.5.html>`_ for
OpenLDAP allows recording the timestamp of the last successful LDAP bind in the
``authTimestamp`` attribute and can for example be used to detect unused
accounts.

The ``lastbind`` overlay module can be activated by setting the |UCSUCRV|
:envvar:`ldap/overlay/lastbind` to ``yes`` and restarting the OpenLDAP server.
When the module is activated on an UCS server, a timestamp is written to the
account's ``authTimestamp`` attribute when that account logs into the LDAP
server. The |UCSUCRV| :envvar:`ldap/overlay/lastbind/precision` can be used to
configure the time in seconds that has to pass before the ``authTimestamp``
attribute is updated. This prevents a large number of write operations that can
impair performance.

The ``authTimestamp`` attribute can only be queried on the LDAP server where the
``lastbind`` overlay module is activated. It is not replicated to other LDAP
servers. For that reason the
:file:`/usr/share/univention-ldap/univention_lastbind.py` script can be executed
to collect the youngest ``authTimestamp`` value from all reachable LDAP servers
in the UCS domain and save it into the ``lastbind`` extended UDM attribute of a
user. The script can be invoked to update the ``lastbind`` extended attribute of
one or all users. The ``lastbind`` extended attribute maps to the
``univentionAuthTimestamp`` LDAP attribute.

One way to keep the ``lastbind`` extended attribute
up-to-date is by creating a cron job via UCR:

.. code-block:: console

   $ ucr set cron/update_lastbind_attribute/command='\
   > /usr/share/univention-ldap/univention_lastbind.py \
   > --allusers' \
   > cron/update_lastbind_attribute/time='00 06 * * *'  # daily at 06:00 a.m.


More information on how to set cron jobs via UCR can be found in
:ref:`computers-Defining-cron-jobs-in-Univention-Configuration-Registry`.
