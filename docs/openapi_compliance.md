# OpenAPI Schema Compliance Issues

This document tracks the warnings and errors reported during OpenAPI schema generation with drf-spectacular and provides actionable steps to resolve each issue.

## Schema Generation Summary
- **Warnings:** 22 (9 unique)
- **Errors:** 36 (8 unique)

---

## Model Field Issues

### 1. Deprecated JSONField Usage
**Issue:** Multiple models use deprecated `django.contrib.postgres.fields.JSONField` with mutable defaults.

**Affected Models:**
- `myFinance.AdditionalInfo.value`
- `myFinance.Credential.additional_info`
- `myFinance.ErrorLog.message`

**Error Messages:**
```
(fields.E010) JSONField default should be a callable instead of an instance so that it's not shared between all field instances.
HINT: Use a callable instead, e.g., use `dict` instead of `{}`.

(fields.W904) django.contrib.postgres.fields.JSONField is deprecated. Support for it (except in historical migrations) will be removed in Django 4.0.
HINT: Use django.db.models.JSONField instead.
```

**Checklist to Fix:**
- [ ] Replace `from django.contrib.postgres.fields import JSONField` with `from django.db import models`
- [ ] Change `JSONField(default={})` to `models.JSONField(default=dict)`
- [ ] Update imports in affected model files:
  - [ ] `myFinance/models.py` - AdditionalInfo model
  - [ ] `myFinance/models.py` - Credential model  
  - [ ] `myFinance/models.py` - ErrorLog model
- [ ] Run migrations: `python manage.py makemigrations && python manage.py migrate`

### 2. Auto-Created Primary Key Warnings
**Issue:** Models using auto-created primary keys without explicit configuration.

**Affected Models:**
- `myFinance.AdditionalInfo`
- `myFinance.Credential`
- `myFinance.DateInput`
- `myFinance.DiscountCredential`
- `myFinance.ErrorLog`
- `myFinance.Plan`
- `myFinance.RecurringTransaction`
- `myFinance.Tag`
- `myFinance.TagGoal`
- `myFinance.Transaction`
- `myFinance.TransactionNameTag`

**Error Message:**
```
(models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
HINT: Configure the DEFAULT_AUTO_FIELD setting or the MyfinanceConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
```

**Checklist to Fix:**
- [ ] Add to `finance/settings.py`: `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'`
- [ ] OR add to `myFinance/apps.py` in `MyfinanceConfig` class: `default_auto_field = 'django.db.models.BigAutoField'`
- [ ] Run migrations: `python manage.py makemigrations && python manage.py migrate`

---

## API View Serializer Issues

### 3. APIViews Missing Serializers
**Issue:** Multiple APIViews cannot have their serializers guessed by drf-spectacular.

**Affected Views (in `app/views.py`):**
- `MonthTrackingView` (line 84)
- `CredentialTypes` (line 247)
- `UserView` (line 258)
- `BankInfo` (line 138)
- `MonthCategoryView` (line 92)
- `SummeryWidgetsView` (line 44)
- `TotalMonthExpensesView` (line 293)
- `UserTransactionsNames` (line 184)

**Error Message:**
```
Error [ViewName]: unable to guess serializer. This is graceful fallback handling for APIViews. Consider using GenericAPIView as view base class, if view is under your control. Either way you may want to add a serializer_class (or method). Ignoring view for now.
```

**Checklist to Fix:**
For each affected view, choose ONE of these approaches:

**Option A: Add explicit serializer_class**
- [ ] `MonthTrackingView`: Create and add `serializer_class = MonthTrackingSerializer`
- [ ] `CredentialTypes`: Create and add `serializer_class = CredentialTypesSerializer`
- [ ] `UserView`: Create and add `serializer_class = UserSerializer`
- [ ] `BankInfo`: Create and add `serializer_class = BankInfoSerializer`
- [ ] `MonthCategoryView`: Create and add `serializer_class = MonthCategorySerializer`
- [ ] `SummeryWidgetsView`: Create and add `serializer_class = SummeryWidgetsSerializer`
- [ ] `TotalMonthExpensesView`: Create and add `serializer_class = TotalMonthExpensesSerializer`
- [ ] `UserTransactionsNames`: Create and add `serializer_class = UserTransactionsNamesSerializer`

**Option B: Use @extend_schema decorator**
- [ ] Add `from drf_spectacular.utils import extend_schema` to `app/views.py`
- [ ] Decorate each view's methods with `@extend_schema(responses={200: YourSerializer})`

**Option C: Convert to GenericAPIView**
- [ ] Change base class from `APIView` to `GenericAPIView` for each affected view
- [ ] Add appropriate `serializer_class` and `queryset` attributes

---

## ViewSet Configuration Issues

### 4. ViewSet Queryset Failures
**Issue:** ViewSets fail to obtain model through queryset due to authentication issues.

**Affected ViewSets:**
- `CredentialViewSet` (line 203)
- `RecurringTransactionsViewSet` (line 235)
- `UserTagViewSet` (line 263)
- `TransactionViewSet` (line 190)

**Error Messages:**
```
Warning [ViewSetName]: Failed to obtain model through view's queryset due to raised exception. Prevent this either by setting "queryset = Model.objects.none()" on the view, checking for "getattr(self, "swagger_fake_view", False)" in get_queryset() or by simply using @extend_schema.
```

**Checklist to Fix:**
For each affected ViewSet:
- [ ] `CredentialViewSet`: Add `queryset = Credential.objects.none()` or modify `get_queryset()` method
- [ ] `RecurringTransactionsViewSet`: Add `queryset = RecurringTransaction.objects.none()` or modify `get_queryset()`
- [ ] `UserTagViewSet`: Add `queryset = Tag.objects.none()` or modify `get_queryset()`
- [ ] `TransactionViewSet`: Add `queryset = Transaction.objects.none()` or modify `get_queryset()`

**Pattern to implement in `get_queryset()` methods:**
```python
def get_queryset(self):
    if getattr(self, 'swagger_fake_view', False):
        return YourModel.objects.none()
    # Your existing queryset logic
    return YourModel.objects.filter(user=self.request.user)
```

### 5. Path Parameter Type Issues
**Issue:** Unable to derive types for path parameters in ViewSets.

**Affected ViewSets:**
- `CredentialViewSet` - parameter "id"
- `RecurringTransactionsViewSet` - parameter "id"  
- `UserTagViewSet` - parameter "id"
- `TransactionViewSet` - parameter "id"

**Error Message:**
```
Warning [ViewSetName]: could not derive type of path parameter "id" because it is untyped and obtaining queryset from the viewset failed. Consider adding a type to the path (e.g. <int:id>) or annotating the parameter type with @extend_schema.
```

**Checklist to Fix:**
- [ ] Update URL patterns in `app/urls.py` to use typed path parameters:
  - Change `<id>` to `<int:id>` for all affected endpoints
- [ ] OR use `@extend_schema` decorator with explicit parameter typing

### 6. Serializer Method Field Type Hints
**Issue:** Unable to resolve type hint for serializer method.

**Affected Serializer:**
- `CredentialSerializer.balance` method (line 69 in `myFinance/serialisers.py`)

**Error Message:**
```
Warning [CredentialViewSet > CredentialSerializer]: unable to resolve type hint for function "balance". Consider using a type hint or @extend_schema_field. Defaulting to string.
```

**Checklist to Fix:**
- [ ] Add type hint to the `balance` method in `CredentialSerializer`:
  ```python
  def balance(self, obj) -> float:
      # existing implementation
  ```
- [ ] OR use `@extend_schema_field` decorator:
  ```python
  from drf_spectacular.utils import extend_schema_field
  
  @extend_schema_field(serializers.FloatField)
  def balance(self, obj):
      # existing implementation
  ```

---

## Verification Steps

After implementing fixes:

- [ ] Run schema generation again: `python manage.py spectacular --file api/openapi.yaml`
- [ ] Verify reduced warning/error count
- [ ] Check that previously missing endpoints now appear in the schema
- [ ] Test API documentation interface (if using Swagger UI/ReDoc)
- [ ] Update and commit the new schema: `git add api/openapi.yaml && git commit -m "Update OpenAPI schema after compliance fixes"`

---

## Priority Order

**High Priority (Schema Completeness):**
1. Fix APIView serializer issues (#3) - these views are missing from the schema
2. Fix ViewSet queryset issues (#4) - affects parameter typing and endpoint accuracy

**Medium Priority (Future Django Compatibility):**
3. Fix deprecated JSONField usage (#1) - will break in Django 4.0+
4. Fix auto-created primary key warnings (#2) - best practice compliance

**Low Priority (Schema Quality):**
5. Fix serializer method type hints (#6) - improves schema accuracy
6. Fix path parameter typing (#5) - improves schema accuracy 