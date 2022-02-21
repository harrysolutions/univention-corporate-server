.. _component-portal:

UCS portal
==========

The UCS portal is the entry point to UCS for domain users and administrators. It
is a web application and simplifies the access to various services and
applications of the domain for users and external links, because users only have
to remember or bookmark one link as starting point.

The portal is user-centric. It is a kind of a home page for the work place. Once
users are logged in, they see their personal portal. Organizations can
customize the portal individually specific to users and groups.

The portal offers a single sign-on login to users. With single sign-on, users
provide their credentials—username and password—only once per session and can
use services and apps without the need to provide the credentials again. To use
single sign-on with a service, the service needs to support and integrate single
sign-on in the UCS domain. UCS supports the standards :ref:`SAML
<services-authentication-saml>` and :ref:`OpenID Connect
<services-authentication-openid-connect>`. For information about single
sign-on, see the :ref:`authentication part <services-authentication>`.

Every UCS system can have a portal page, regardless of its system role. A domain
can have multiple portal configurations with different content. The
portal configuration controls the following aspects:

* Which portal shows up on which UCS system in the domain?
* Who sees which portal on which UCS system?

The portal depends on :ref:`component-domain-management` to operate properly.
For technical details about the UCS portal, see :ref:`services-ucs-portal`.

For instructions about how to configure and customize the UCS portal page, see
the `UCS manual in the UCS portal page section
<ucs-manual-portal_>`_.
