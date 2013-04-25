
*********************
Coq Tactics Reference
*********************

remember
--------

remember &expr as &name
  - this adds a hypothesis ``&name = &expr``
  - this tactic is essential for situations where you are doing inductive
    logic on an expression that you need to keep track of later.
  - when you have ``destruct`` or ``induction`` etc.

  For example:

  .. code:: coq

    ev S
    -----
    remember (ev S) as evs.
    destruct evs.


rewrite
-------

rewrite *<-* &theorem *in &hypothesis*
    - `theorem` needs to be proven (or admitted), or in your hypotheses to
      rewrite with it.
    - It needs to be in the form of ``a = b``, and it will take any instances of
      `a` it sees and replaces it with ``b`` 
    - `unfold`-ing can be important so that rewrite will 'find' the
      instances.
    - if you want to replace ``b`` with ``a``, use ``rewrite <- ...``.
    - ``in hypothesis`` does the replacement in the named hypothesis



