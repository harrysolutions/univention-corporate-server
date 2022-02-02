.. _classification:

******************************
Classification in the IT world
******************************

To comprehend the architecture of Univention Corporate Server (UCS) it is
important to understand the origin and where it is located in the world of
information technology.

Origin
======

UCS is a Linux distribution derived from `Debian GNU/Linux <w-debian_>`_. Among
others, it benefits from the strong package manager, the high quality
maintenance and the long-term stability as operating system for servers. Over
the years, Debian has been and is a solid basis for UCS.

UCS is part of the open source family and has strong relations to important
projects like for example `Samba <w-samba_>`_ and `OpenLDAP <w-openldap_>`_.

History
-------

Univention started UCS in 2002 as a collection of scripts that turn a Debian
system into a Linux server that offers Windows domain functionality. The goal
was to offer companies and organizations a standardized Linux server as
alternative to Microsoft Windows Server that implements Microsoft's domain
concept. Over the time it developed to an enterprise Linux distribution with
maintenance cycles that better suited organizations.

Packages
--------

Packages on UCS use the deb file format, which is a standard Unix *ar archive*
including two *tar archives*. One holds control information and the other the
data for installation. For more information on the deb file format, see `dev (file
format) at Wikipedia <w-deb-file-format_>`_ and `Basics of the Debian package
management system in the Debian FAQ <debian-faq-pkg-basics_>`_.

UCS like Debian uses a package manager, which is a collection of software tools
to automate the process of installation, upgrade, configuration and removal of
computer programs. In UCS the package manager is the advanced package tool
(APT). For more information about APT, see the `Debian package management
chapter in the Debian reference <debian-ref-package-mngmt_>`_.

Univention distributes most packages from Debian GNU/Linux for the *amd64*
architecture without changes for UCS. This includes the GNU/Linux kernel offered
by Debian and about xx% of the packages.

.. TODO Ask SME: For some rough statistics
   TODO Ask SME: How many packages do we copy from Debian? How many of them are changed by Univention? Do we copy all packages?
   TODO Ask SME: How many packages are added by Univention?

In the following circumstances, Univention builds and maintains derived
packages:

* A later software version of a package is needed for UCS than Debian offers.
* Bug fixes or backports of a specific software are needed for a package.

Additionally, Univention develops software responsible for UCS functionality
that is distributed as Debian package.

Identity management
===================

The most important functional pillar of UCS is identity management.

Simplified, an IT environment consists of services and actors. Services offer
functionality. Actors use functionality. Services can also behave as actors
when they use the functionality of another service. Actors identify themselves
against services to proof that they are eligible to use the functionality.

The identification is done with *user accounts* the represent actors. User
accounts typically have unique properties like for example username,
password and email address. User accounts that digitally represent a person
additionally have for example first name and last name.

Imagine a small IT environment with 20 persons and five systems. Without a
central identity management, an administrator would have to maintain the
20 user accounts of the persons on each of the five systems that sums up to 100
items to manage. The number of the items to manage is a linear function and
increases with the number of systems that need to know user accounts.

With a central identity management, there is one service that holds the
information about the user accounts. All other services have access to that
information. An administrator only has to maintain the user accounts on that
system. The maintenance effort for the user accounts does not anymore multiply
with the number of systems that need to know the user accounts. The slope of
this linear function is less steep.

Central identity management reduces the maintenance effort of user accounts for
administrators.

UCS is a product for central identity management for user accounts and the
collection of user accounts in groups.
