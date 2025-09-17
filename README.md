# op-schema



## Customer lifecycle management

The system provides two different ways to “remove” a customer:

### 🔹 Deactivate (soft delete)
- **Endpoint**: `PUT /customers/{id}/deactivate`
- Sets the field `is_active = False`.
- The customer record remains in the database.
- All schedules, history, and relationships are preserved.
- **Use cases**:
  - The customer is no longer active (e.g., moved away, deceased, or no longer receiving services).
  - You want to retain historical and statistical data.

### 🔹 Delete (hard delete)
- **Endpoint**: `DELETE /customers/{id}`
- Permanently removes the customer from the database.
- **Should only be used when**:
  - The customer record was created by mistake (duplicate entry, incorrect details).
- ⚠️ **Warning**: This also removes related data such as schedules and visits associated with the customer.

### Best practices
- **Default action**: use `deactivate`.
- **Exception**: use `delete` only when the data is invalid and must be permanently removed.
- Frontend should always request explicit confirmation before invoking `delete`.  
  Example: *“Are you sure you want to permanently delete this customer?”*
