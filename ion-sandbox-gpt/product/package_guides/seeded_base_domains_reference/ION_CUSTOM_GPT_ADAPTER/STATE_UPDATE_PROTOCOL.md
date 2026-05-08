# State Update Protocol

A state update must include:

1. the file or object being changed;
2. the reason the change is allowed;
3. the prior state considered;
4. the proposed delta;
5. the receipt appended;
6. the export package name.

Do not update `ION_ENGINE/` from a user data package. Engine evolution
belongs to the live ION source repo and product packager.
