bstat
=====

Outliner format and viewer for status info of build systems and maybe related
systems.

Below are specs that need to be tested.

See also ReadMe.rst for generic outliner info.

Spec
----

Status
  Status is numerical value. Primary states:

  0. OK
  1. Error
  2. Failure

  Only 0-9 (10) core states are available.
  And only 3 handled by default view.

  First level sub states use 2-digit, etc.
  Extension states 3-9 are for new semantics?

  Error
    Unspecified unrecoverable.
  Failure
    Specific failure, proper parametrization may relieve/skip failed component.

Component
  Something that has a direct or indirect status through sub components.
  And has Id+view attributes: label, description.

Updates
  Status is retrieved simply using shell env call.
  One call can update multiple components at once.



Example::

  - component:
      id:
      label:
      description:
      status:
      update: $/my-update
      sub:

      - component:

  - my-update

