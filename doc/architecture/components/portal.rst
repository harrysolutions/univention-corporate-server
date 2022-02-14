.. _component-portal:

UCS portal
==========

The UCS portal is the entry point to UCS for domain users and administrators. It
simplifies the access to various services of the domain for users, because users
only have to remember or bookmark one link as starting point. Furthermore, it
allows users to log in to the UCS domain through single sign-on.

.. TODO Add reference to authentication section in the last sentence of the following paragraph.

With single sign-on, users provide their credentials—username and password—only
once per session and can use the supported [#f1]_ services without the need to
provide the credentials again. For information about single sign-on, see the
authentication section.

Every UCS system has a portal page, regardless of its system role. It shows the
login to the local system. The portal can show content that depends on login
status and user group to show a user specific portal.

For more information about how to configure and customize the UCS portal page,
see the `UCS manual in the UCS portal page section
<https://docs.software-univention.de/manual.html#central:portal>`_.

The portal depends on :ref:`component-udm` to operate properly.

For technical details about the UCS portal, see :ref:`service-ucs-portal`.

.. TODO Add reference to single sign-on details from the authentication section.

.. [#f1] To use single sign-on with a service, the service needs to support and
   integrate single sign-on in the UCS domain. UCS supports the standards SAML
   and OpenID Connect.
