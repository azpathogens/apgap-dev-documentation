# Permissions

## Role Hierarchy

The system has four primary roles, roughly ordered by access level:

| Role | Key Characteristic |
|------|-------------------|
| **Platform Admin** | Full access |
| **Lab Director** (`is_lab_admin=True`) | Admin within their lab, and can approve/reject requests |
| **Lab Collaborator** | Read/write within their lab. Cannot approve requests |
| **Bioinformatics User** | Project-scoped access only |

Role checks can be found in `utils/permission_helpers.py` 

- `is_platform_admin(user)` checks superuser status, boolean field, and group membership
- `is_lab_director(user, lab=None)` pass a lab to scope the check, or `None` to check any lab
- `is_lab_collaborator(user, lab=None)`  same pattern as above. Lab Reader maps to Lab Collaborator
- `is_bioinformatics_user(user, project=None)`  same pattern, scoped to project
- `is_data_analyst(user)`
- `has_lab_access(user, lab)` / `has_project_access(user, project)`  
- `get_user_labs(user)` / `get_user_projects(user, lab=None)`  

---
