# Serializer 

---

## N+1 Query Prevention

Every serializer that traverses relationships assumes the queryset has been prefetched by the view. `SerializerMethodField`s use `.all()` to hit the prefetch cache rather than issuing new queries. Using `.count()` instead of `len()` on a prefetched queryset defeats the cache and fires an extra `COUNT`.

- Always use `len(obj.related.all())` on prefetched data, never `.count()`. Confirm the view's `get_queryset()` sets up the required `prefetch_related()` before adding a new `SerializerMethodField`.

## GCS Access List vs. Detail

List serializers never read from Google Cloud Storage. GCS lookups are deferred exclusively to detail serializers. This prevents timeout cascades when many rows load at once, and avoids logging 404s for builds still in progress. The `output_bucket` field on list serializers is derived only from `_cached_seqera_output_bucket` it returns `null` when the cache is cold.

- Never add a GCS call to a list serializer. If a field requires live GCS data, it belongs on the detail serializer only.

## Dual-Write for Rename Stability

Saved searches and dataset subscriptions store both a human-readable `key` name and a stable FK-based `key_id`. The runtime evaluator prefers `key_id` so that renaming a `Key` does not silently break persisted rules. This dual-write is idempotent and tolerates unresolvable names gracefully.

- **Note:** When adding new filter-condition fields that reference `Key` names, follow the same dual-write pattern: persist `key_id` alongside `key` so future renames do not break the stored rule.

## Role-Scoped Output in SerializerMethodFields

Several serializers filter their output based on the requesting user's role. Platform admin checks (`is_platform_admin`) issue a `user.groups` lookup  expensive when the same serializer instance handles many rows. The pattern is to memoize the result on `self.context` so the check runs once per request, not once per row.

- For any permission check inside a `SerializerMethodField` on a list serializer, cache the result on `self.context`. Do not call `is_platform_admin()` or equivalent per-row without caching.

